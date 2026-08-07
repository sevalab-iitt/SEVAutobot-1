# RTAB-Map SLAM Integration & Debugging Report
### JetAuto Pro — RGB-D Visual SLAM Implementation

**Project:** JetAuto Pro SLAM & RTAB-Map Integration
**Platform:** Hiwonder JetAuto Pro (NVIDIA Jetson Nano)
**ROS Distribution:** ROS Melodic
**Operating System:** Ubuntu 18.04 LTS
**Author:** Raj Majhi
**Document Type:** Internship Technical Report

---

## Table of Contents

1. [Objective](#1-objective)
2. [Hardware & Software Used](#2-hardware--software-used)
3. [Background: Why RTAB-Map?](#3-background-why-rtab-map)
4. [System Architecture](#4-system-architecture)
5. [Procedure](#5-procedure)
6. [Problems Encountered, Root Causes & Solutions](#6-problems-encountered-root-causes--solutions)
7. [Commands Used (Reference)](#7-commands-used-reference)
8. [Verification](#8-verification)
9. [Results](#9-results)
10. [GMapping vs RTAB-Map Comparison](#10-gmapping-vs-rtab-map-comparison)
11. [Lessons Learned](#11-lessons-learned)
12. [Future Work](#12-future-work)
13. [Conclusion](#13-conclusion)
14. [Appendix](#14-appendix)

---

## 1. Objective

The goal of this work was to migrate the JetAuto Pro robot from 2D LiDAR-only SLAM (GMapping) to 3D RGB-D Visual SLAM using **RTAB-Map** (Real-Time Appearance-Based Mapping), and to debug the complete sensor and SLAM pipeline, which was initially non-functional.

Specific objectives:

- Restore LiDAR communication (`/scan`).
- Restore odometry (`/odom`).
- Debug and correct the RTAB-Map pipeline.
- Verify RGB-D camera (Astra Pro Plus) operation.
- Generate both 2D occupancy maps and 3D point cloud maps.
- Save, inspect, and export the generated maps for offline visualization.

---

## 2. Hardware & Software Used

### 2.1 Hardware

| Component | Model |
|---|---|
| Robot Platform | JetAuto Pro |
| SBC | NVIDIA Jetson Nano |
| LiDAR | RPLIDAR A1 |
| RGB-D Camera | Orbbec Astra Pro Plus |
| Secondary Camera | Logitech USB Camera |
| IMU | MPU6050 |

### 2.2 Software

| Software | Version |
|---|---|
| Ubuntu | 18.04 LTS |
| ROS | Melodic |
| RTAB-Map | ROS package (`rtabmap_ros`) |
| GMapping | ROS package |
| RViz | Bundled with ROS |
| OpenCV | 3.2 |
| TF | ROS TF |

---

## 3. Background: Why RTAB-Map?

GMapping produces a 2D occupancy grid from LiDAR scan-matching only, with no visual memory and limited loop closure. RTAB-Map instead fuses RGB-D imagery, LiDAR, odometry, and IMU data to build a dense, colored 3D reconstruction with strong appearance-based loop closure.

| Aspect | GMapping | RTAB-Map |
|---|---|---|
| Primary Sensor | 2D LiDAR | RGB-D Camera (+ optional LiDAR) |
| Map Type | 2D Occupancy Grid | 3D Map |
| Localization | Laser-based | Visual + Depth-based |
| Image Memory | None | Full database of visual observations |
| Loop Closure | Limited | Strong, appearance-based |

An RGB-D camera outputs two synchronized image streams — a **color image** (pixel = color) and a **depth image** (pixel = distance). Combined with camera intrinsics, each pixel becomes a colored 3D point `(x, y, z, r, g, b)`, which is the fundamental unit RTAB-Map operates on.

### Key RGB-D / LiDAR / Odometry Topics (JetAuto Pro)

| Topic | Purpose |
|---|---|
| `/astra_cam/rgb/image_raw` | Color image |
| `/astra_cam/depth_registered/image_raw` | Depth image aligned to RGB pixels |
| `/astra_cam/rgb/camera_info` | Camera intrinsics (fx, fy, cx, cy) |
| `/astra_cam/depth_registered/points` | Combined RGB-D point cloud |
| `/jetauto_1/odom` | Fused (EKF) robot odometry |
| `/tf` | Coordinate transform tree |

> **Note:** RTAB-Map prefers `depth_registered` topics over raw depth, because registration guarantees every RGB pixel has a matching depth value.

---

## 4. System Architecture

### 4.1 Data Pipeline (Conceptual)

```
                Astra Pro Plus

              RGB Image
                  │
                  ▼
            /rgb/image_raw

              Depth Image
                  │
                  ▼
         /depth_registered/image_raw

                  │
                  ▼
        Registered RGB + Depth
                  │
                  ▼
             RTAB-Map
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
 Visual Odometry     Loop Closure
        │                 │
        └────────┬────────┘
                 ▼
        Pose Graph Optimizer
                 ▼
           RTAB Database
                 ▼
        3D Map + 2D Map
```

### 4.2 Full Sensor Fusion Pipeline (Final Working System)

```
                    Astra Pro Plus
                 RGB + Depth Images
                         │
                         ▼
                  Feature Extraction
                         │
Wheel Encoder ───────┐
                      │
IMU ──────────────────┤
                      ▼
              EKF Odometry
                      │
RPLIDAR A1 ───────────┘
                      │
                      ▼
                RTAB-Map Core
                      │
     ┌────────────────┼─────────────────┐
     ▼                ▼                 ▼
 Pose Graph      Point Cloud        Database
     │                │                 │
     ▼                ▼                 ▼
 Loop Closure       3D Map        rtabmap.db
                      │
                      ▼
           Database Viewer / Export
```

### 4.3 JetAuto Launch File Hierarchy

Only one SLAM algorithm is active at a time, selected via `slam_base.launch`:

```
                 slam_base.launch
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
 gmapping.launch   rtabmap.launch   cartographer.launch
        │               │                │
        └───────────────┼────────────────┘
                        │
                  SLAM Algorithm
                        │
                  Builds the Map

Additional Modules:
  ekf.launch                → Better odometry
  frontier.launch           → Detect unexplored regions
  explore.launch            → Autonomous exploration
  rrt_exploration.launch    → RRT-based exploration
  depthimage_to_laserscan   → RGB-D → LaserScan conversion
  jetauto_robot.launch      → Robot hardware and sensors
```

| Launch File | Purpose |
|---|---|
| `cartographer.launch` | Google Cartographer SLAM (LiDAR + IMU + odometry) |
| `depthimage_to_laserscan.launch` | Converts depth image to virtual 2D LaserScan |
| `ekf.launch` | Extended Kalman Filter sensor fusion (not SLAM) |
| `explore.launch` | Autonomous frontier-based exploration |
| `frontier.launch` | Frontier (unexplored boundary) detection |
| `gmapping.launch` | 2D Rao-Blackwellized Particle Filter SLAM |
| `hector.launch` | LiDAR-only SLAM, works without odometry |
| `jetauto_robot.launch` | Robot hardware bring-up |
| `karto.launch` | Graph-based 2D SLAM (OpenKarto) |
| `rrt_exploration.launch` | RRT-based large-area exploration |
| `rtabmap.launch` | RTAB-Map RGB-D visual SLAM |
| `slam_base.launch` | Master selector launch file |

---

## 5. Procedure

The debugging effort proceeded through the following chronological phases.

### 5.1 Chronological Workflow

```
System Inspection
       ↓
ROS Environment Check
       ↓
Workspace Verification
       ↓
Auto-start Investigation
       ↓
Duplicate LiDAR Detection
       ↓
Incorrect LiDAR Type Found (G4 → A1)
       ↓
Serial Device Investigation (/dev/lidar → /dev/ttyUSB0)
       ↓
Verified RPLIDAR
       ↓
Restored /scan
       ↓
Restored /odom
       ↓
Verified TF Tree
       ↓
Launched GMapping → Generated 2D Map → Saved Occupancy Grid
       ↓
Launched RTAB-Map → Verified RGB-D Camera
       ↓
Generated 3D Map → Generated rtabmap.db
       ↓
Verified Database Viewer
       ↓
Exported Point Cloud
```

### 5.2 Phase 1 — Initial System Inspection

The robot initially failed to produce any map. Symptoms observed:

- `/scan` topic unavailable.
- `/odom` topic missing.
- Navigation launch files failed.
- RTAB-Map could not initialize.
- Astra camera intermittently reported **Resource Busy**.
- USB camera repeatedly crashed.
- Multiple launch files attempted to start the LiDAR simultaneously.

The first diagnostic step was checking simulated-time configuration:

```bash
rosparam get /use_sim_time
```

```text
true
```

The robot was using simulated time despite running on real hardware — corrected with:

```bash
rosparam set /use_sim_time false
```

### 5.3 Phase 2 — Ruling Out XML Corruption

Running `rostopic echo /scan` produced:

```text
cElementTree.ParseError:
not well-formed (invalid token)
```

This suggested a corrupted `package.xml`. Every package in the workspace was validated using two independent methods:

```bash
find ~/jetauto_ws/src -name package.xml

find ~/jetauto_ws/src \
-name package.xml \
-exec xmllint --noout {} \;
```

```python
import os
import xml.etree.ElementTree as ET

for root, dirs, files in os.walk("~/jetauto_ws/src"):
    ...
```

**Result:** No malformed XML files were found. The error originated elsewhere in the ROS environment, not from package manifests.

### 5.4 Phase 3 — Workspace and Auto-Start Investigation

The `ROS_PACKAGE_PATH` was inspected and revealed multiple active workspaces:

```bash
echo $ROS_PACKAGE_PATH
```

This showed both `jetauto_ws` and `catkin_ws`, the latter containing `jetauto_pointcloud_mapping` and `lidar_tools` — determined not to be the cause of the SLAM failure.

Since JetAuto auto-launches its full software stack at boot, the responsible systemd service was inspected:

```bash
systemctl cat start_app_node.service
```

```text
ExecStart=
/home/jetauto/jetauto_ws/src/
jetauto_bringup/scripts/source_env.bash
roslaunch jetauto_bringup bringup.launch
```

This identified `jetauto_bringup/launch/bringup.launch` as the primary debugging target, responsible for initializing the chassis controller, LiDAR, servo controller, Astra RGB-D camera, USB camera, ROSBridge, app functions, joystick, and startup checks.

#### Before / After — LiDAR Include in `bringup.launch`

| State | Configuration |
|---|---|
| **Before** | `<include file="$(find rplidar_ros)/launch/rplidar.launch"/>` |
| **After** | `<include file="$(find jetauto_peripherals)/launch/lidar.launch"/>` |

The peripheral launcher was adopted because it supports multiple LiDAR models via the `LIDAR_TYPE` environment variable.

### 5.5 Phase 4 — Duplicate LiDAR Node Resolution

After modifying the launch structure, ROS reported:

```text
RLException:

multiple nodes named

ydlidar_lidar_g4_publisher
```

A recursive search confirmed only one node **definition** existed:

```bash
grep -R "ydlidar_lidar_g4_publisher" \
~/jetauto_ws/src -n
```

Tracing the launch chain revealed the LiDAR driver was being included **twice**, through two separate paths:

```
bringup.launch
        │
        ▼
start_app.launch
        │
        ▼
lidar_app.launch
        │
        ▼
jetauto_peripherals/lidar.launch
```

**Root cause:** the LiDAR driver launch file was reachable from two different points in the launch tree, causing ROS to attempt starting the same node name twice.

To isolate and test launch files without interference from the automatic boot process, the auto-start service was temporarily stopped and the environment sourced manually:

```bash
sudo systemctl stop start_app_node.service

source \
~/jetauto_ws/src/jetauto_bringup/scripts/source_env.bash
```

### 5.6 Phase 5 — LiDAR Type Misconfiguration

The system reported an active LiDAR type of `G4`, but the physically installed hardware was an **RPLIDAR A1**. This mismatch was traced to the environment configuration file `~/.typerc`.

#### Before / After — `~/.typerc`

| State | Value |
|---|---|
| **Before** | `export LIDAR_TYPE=G4` |
| **After** | `export LIDAR_TYPE=A1` |

```bash
source ~/.typerc
echo $LIDAR_TYPE
```

```text
A1
```

This was the first major breakthrough: correcting `LIDAR_TYPE` automatically switched all downstream launch files from the YDLIDAR driver to the correct RPLIDAR driver.

### 5.7 Phase 6 — Device Mapping Correction

With the correct driver selected, the RPLIDAR launch file still failed because it referenced a non-existent symlink:

```bash
cat ~/jetauto_ws/src/jetauto_peripherals/launch/include/rplidar.launch
```

```xml
<param name="serial_port" value="/dev/lidar"/>
```

```bash
ls -l /dev/lidar
```

```text
No such file or directory
```

The actual Linux device was identified via the `by-id` symlink:

```bash
ls -l /dev/serial/by-id/
```

```text
usb-1a86_USB_Serial-if00-port0
→ ../../ttyUSB0
```

**Root cause:** the JetAuto software assumes a custom udev rule that creates `/dev/lidar` as a persistent symlink to the LiDAR's USB-serial device. This udev rule was missing or not applied, so the expected device node never appeared.

```
Expected                      Actual
USB Device                    USB Device
    │                             │
    ▼                             ▼
/dev/lidar                  /dev/ttyUSB0
```

#### Before / After — RPLIDAR Serial Port Parameter

| State | Configuration |
|---|---|
| **Before** | `<param name="serial_port" value="/dev/lidar"/>` |
| **After** | `<param name="serial_port" value="/dev/ttyUSB0"/>` |

This was applied as a temporary debugging fix, not a permanent solution (a proper fix would involve restoring the udev rule).

### 5.8 Phase 7 — Verifying RPLIDAR Communication

The driver was launched independently to confirm hardware health:

```bash
roslaunch rplidar_ros rplidar.launch
```

```text
RPLIDAR running

Firmware Ver : 1.29

Hardware Rev : 7

Health Status : OK

Scan Frequency : 10 Hz
```

This confirmed successful USB communication, correct driver initialization, and healthy LiDAR hardware.

### 5.9 Phase 8 — Restoring and Understanding `/scan`

```bash
rostopic list | grep scan
```

```text
/jetauto_1/scan

/jetauto_1/scan_raw
```

```bash
rostopic hz /jetauto_1/scan
```

A stable publish rate confirmed correct operation.

**`scan_raw` vs `scan`:**

```
LiDAR
   │
   ▼
scan_raw
   │
Laser Filter
   │
   ▼
scan
```

| Topic | Description |
|---|---|
| `scan_raw` | Unfiltered laser data — contains sensor noise, invalid returns, outliers |
| `scan` | Filtered data used by GMapping, RTAB-Map, Navigation, and obstacle avoidance |

### 5.10 Phase 9 — Restoring and Understanding `/odom`

```bash
rostopic list | grep odom
```

```text
/jetauto_1/odom

/jetauto_1/odom_raw

/jetauto_1/set_odom
```

**`odom_raw` vs `odom`:**

```
Wheel Encoder
        +
       IMU
        │
        ▼
robot_localization EKF
        │
        ▼
       odom
```

| Topic | Description |
|---|---|
| `odom_raw` | Direct wheel-encoder odometry from the JetAuto controller |
| `odom` | EKF-fused odometry (encoder + IMU), used by RTAB-Map and Navigation |

Sample verification:

```bash
rostopic hz /jetauto_1/odom
```

```text
average rate: 29.984
        min: 0.026s max: 0.041s std dev: 0.00231s window: 29
```

```bash
rostopic hz /jetauto_1/odom_raw
```

```text
average rate: 50.119
        min: 0.018s max: 0.021s std dev: 0.00054s window: 47
```

### 5.11 Phase 10 — Namespace Clarification

All topics appeared under `/jetauto_1/...` rather than at the root (e.g. `/jetauto_1/scan` instead of `/scan`). This is intentional: JetAuto supports multi-robot operation, and each robot instance runs inside its own ROS namespace to avoid topic collisions:

```
Robot 1 → /jetauto_1/scan
Robot 2 → /jetauto_2/scan
Robot 3 → /jetauto_3/scan
```

### 5.12 Phase 11 — TF Tree Verification

```bash
rosrun tf view_frames
```

The generated `frames.pdf` confirmed connectivity across `base_footprint`, `lidar_frame`, camera frames, `odom`, and `map`.

Expected chain:

```
map
 ↓
odom
 ↓
base_footprint
 ↓
base_link
 ↓
lidar
 ↓
camera
```

> 📷 Screenshot: `frames.pdf` TF tree output showing full transform chain from `map` to `camera`.

### 5.13 Phase 12 — GMapping Execution (2D Baseline)

With LiDAR, TF, and odometry functioning, GMapping was launched to validate the base pipeline before moving to RTAB-Map:

```bash
roslaunch jetauto_slam slam.launch
```

This internally starts `robot_localization`, laser filters, `robot_state_publisher`, and `gmapping`.

```bash
roslaunch jetauto_slam rviz_slam.launch
```

> 📷 Screenshot: RViz displaying live laser scan, robot model, and expanding 2D occupancy grid.

**Mapping best practices applied:**

- Slow, deliberate movement.
- Smooth turns (avoiding rapid rotation).
- Deliberately revisiting previously mapped areas to aid loop closure.

**Saving the map:**

```bash
rosrun map_server map_saver -f my_map
```

Initial attempt stalled:

```text
Waiting for map...
```

**Root cause:** the LiDAR USB cable had temporarily disconnected, halting map publication. After reconnecting the cable, the save completed successfully, producing:

```
my_map.pgm
my_map.yaml
```

| File | Content |
|---|---|
| `my_map.pgm` | Occupancy image — white = free space, black = obstacle, gray = unknown |
| `my_map.yaml` | Metadata (image path, resolution, origin) used by ROS Navigation |

### 5.14 Phase 13 — RTAB-Map Execution (3D Visual SLAM)

With the 2D baseline validated, RTAB-Map was launched using the same JetAuto launch structure:

```bash
roslaunch jetauto_slam slam.launch
roslaunch jetauto_slam rviz_slam.launch
```

Available components after initialization: robot model, TF tree, RGB camera, depth camera, laser scan, point cloud, and occupancy grid — enabling live 3D reconstruction.

> 📷 Screenshot: RViz showing live colored 3D point cloud being built alongside the 2D occupancy grid.

**Astra camera conflict:**

```text
Device open failed

Resource busy
```

**Root cause:** the Astra RGB-D driver was being launched more than once, causing multiple nodes to compete for the same USB device (only one process can access the camera at a time).

**USB camera conflict:**

```text
Cannot identify /dev/usb_cam
OpenCV Exception
```

**Root cause:** the external USB monocular camera was physically disconnected while the launch file continued attempting to initialize it. Resolved once the camera was physically reconnected.

### 5.15 Phase 14 — RTAB-Map Database Inspection

RTAB-Map continuously writes to a session database:

```bash
rosparam get /rtabmap/database_path
```

```text
~/.ros/rtabmap.db
```

Unlike a simple map file, this database stores the complete mapping session:

```
rtabmap.db
│
├── RGB Images
├── Depth Images
├── Camera Calibration
├── Laser Scans
├── ORB Features
├── Robot Poses
├── Constraints
├── Loop Closures
├── Optimized Graph
└── Metadata
```

Opened via:

```bash
rtabmap-databaseViewer ~/.ros/rtabmap.db
```

> 📷 Screenshot: RTAB-Map Database Viewer main window — 3D point cloud viewer (top), RGB image and ORB feature panel (bottom-left/right), node information panel (bottom).

**Database Viewer layout:**

```
+---------------------------------------------------------+
|                  3D Point Cloud Viewer                  |
+---------------------------------------------------------+

+--------------------+-------------------------------+
| RGB Image          | Feature Detection             |
+--------------------+-------------------------------+

+----------------------------------------------------+
| Node Information                                   |
| Pose | Weight | Calibration | Links | Statistics   |
+----------------------------------------------------+
```

Each **node** represents one keyframe and stores:

```
Node
│
├── RGB Image
├── Depth Image
├── Features
├── Pose
├── Laser Scan
├── Timestamp
└── Links
```

- **RGB panel** — the color image at that keyframe, used for feature extraction, loop closure, and place recognition.
- **Feature panel** — yellow ORB feature points used to detect whether the robot has revisited a location (loop closure detection).
- **Pose graph** — nodes connected sequentially; when the robot revisits a location, an additional link is created and the graph is re-optimized to reduce accumulated odometry drift:

```
Node 1 — Node 2 — Node 3 — Node 4 — Node 5 — Node 6 — Node 7 — Node 8
   ╲_____________________________________________________╱
              (loop closure link on revisit)
```

**Extra nodes observed during loading:** normal behavior — RTAB-Map internally manages Working Memory (WM), Short-Term Memory (STM), and Long-Term Memory (LTM) to bound RAM usage in large environments.

**Fewer parameters than expected in the viewer:** expected — the Database Viewer only loads data stored inside the database; ROS runtime launch parameters are not persisted to `rtabmap.db`.

### 5.16 Phase 15 — Point Cloud Quality Assessment

The reconstructed point cloud successfully represented walls, tables, chairs, and the floor of the lab environment, but exhibited noise in some regions.

**Observed causes of noise:**

- Reflective surfaces
- Dynamic obstacles (people moving)
- Rapid robot motion
- Depth sensor inaccuracies (infrared projection errors at range or under changing light)

**Mitigations identified for future sessions:**

| Category | Practice |
|---|---|
| Robot Motion | Move slowly, avoid sudden turns, maintain constant speed |
| Camera Position | Maintain consistent height, avoid rapid tilting |
| Lighting | Ensure stable indoor lighting, avoid direct sunlight |
| Environment | Minimize moving people, avoid reflective glass, reduce dynamic obstacles |
| Loop Closure | Revisit mapped locations, create overlapping trajectories |

### 5.17 Phase 16 — Exporting and Backing Up the Map

Database backup (simple file copy, no special command required since RTAB-Map auto-saves):

```bash
mkdir -p ~/rtabmap_maps
cp ~/.ros/rtabmap.db ~/rtabmap_maps/lab_map.db
```

Export options available inside Database Viewer:

```
File
├── Export 3D Clouds
├── Export Mesh
├── Export Grid Map
└── Export Images
```

| Format | Purpose |
|---|---|
| PLY | Point cloud visualization |
| PCD | ROS point cloud processing |
| OBJ | Mesh reconstruction |
| PNG | Saved RGB/depth images |

Exported files can be opened in **CloudCompare**, **MeshLab**, **Open3D**, or RViz.

> 📷 Screenshot: Exported `lab_map.ply` opened in CloudCompare showing the reconstructed 3D lab environment.

---

## 6. Problems Encountered, Root Causes & Solutions

| # | Problem | Root Cause | Solution |
|---|---|---|---|
| 1 | `/use_sim_time` was `true` on real hardware | Leftover simulation configuration | `rosparam set /use_sim_time false` |
| 2 | XML parse error on `rostopic echo /scan` | Initially suspected, but **not** actually caused by malformed `package.xml` | Validated all manifests with `xmllint` and a Python XML parser; confirmed files were valid — error traced to environment/launch issues instead |
| 3 | Duplicate node `ydlidar_lidar_g4_publisher` | LiDAR driver reachable via two separate launch chains (`bringup → start_app → lidar_app → lidar.launch` and a second direct include) | Removed the duplicate include path |
| 4 | LiDAR type reported as G4 instead of A1 | Incorrect `LIDAR_TYPE` value in `~/.typerc` | Changed `LIDAR_TYPE=G4` → `LIDAR_TYPE=A1`, reloaded with `source ~/.typerc` |
| 5 | RPLIDAR launch failed to find `/dev/lidar` | Missing/unapplied udev rule that should symlink the LiDAR to `/dev/lidar` | Temporarily set `serial_port` to the actual device `/dev/ttyUSB0` |
| 6 | `/scan` and `/odom` unavailable | Cascading effect of items 3–5 preventing full bringup | Resolved after fixing LiDAR type and device path |
| 7 | `map_saver` stuck at "Waiting for map..." | LiDAR USB cable had disconnected during mapping | Reconnected the cable; map generation resumed |
| 8 | Astra camera: "Device open failed / Resource busy" | Astra driver launched more than once, multiple nodes competing for one USB device | Eliminated duplicate camera launch instances |
| 9 | USB camera: "Cannot identify /dev/usb_cam", OpenCV Exception | USB camera physically disconnected while launch file still attempted initialization | Physically reconnected the USB camera |

---

## 7. Commands Used (Reference)

```bash
# --- Environment ---
source ~/jetauto_ws/src/jetauto_bringup/scripts/source_env.bash
source ~/.typerc
echo $LIDAR_TYPE
echo $DEPTH_CAMERA_TYPE
echo $ROS_PACKAGE_PATH
rosparam get /use_sim_time
rosparam set /use_sim_time false

# --- Auto-start service control ---
systemctl cat start_app_node.service
sudo systemctl stop start_app_node.service

# --- Workspace / XML validation ---
find ~/jetauto_ws/src -name package.xml
find ~/jetauto_ws/src -name package.xml -exec xmllint --noout {} \;

# --- LiDAR ---
ls -l /dev/lidar
ls -l /dev/serial/by-id/
roslaunch rplidar_ros rplidar.launch
grep -R "ydlidar_lidar_g4_publisher" ~/jetauto_ws/src -n

# --- SLAM / RViz launch ---
roslaunch jetauto_slam slam.launch
roslaunch jetauto_slam rviz_slam.launch

# --- Topic / node inspection ---
rosnode list
rosnode list | grep rtabmap
rostopic list
rostopic list | grep scan
rostopic list | grep odom
rostopic list | grep image
rostopic list | grep depth
rostopic list | grep points
rostopic list | grep map
rostopic list | grep cloud
rostopic hz /jetauto_1/scan
rostopic hz /jetauto_1/odom
rostopic hz /jetauto_1/odom_raw
rostopic hz /jetauto_1/map
rostopic hz /jetauto_1/rtabmap/cloud_map
rostopic echo -n 1 /jetauto_1/odom
rostopic echo -n 1 /jetauto_1/rtabmap/info
rosrun tf tf_echo jetauto_1/odom jetauto_1/base_footprint

# --- TF ---
rosrun tf view_frames

# --- Map saving (GMapping) ---
rosrun map_server map_saver -f my_map

# --- RTAB-Map database ---
rosparam get /rtabmap/database_path
ls -lh ~/.ros/rtabmap.db
rtabmap-databaseViewer ~/.ros/rtabmap.db
mkdir -p ~/rtabmap_maps
cp ~/.ros/rtabmap.db ~/rtabmap_maps/lab1.db
```

---

## 8. Verification

| Subsystem | Verification Command | Expected Result |
|---|---|---|
| LiDAR type | `echo $LIDAR_TYPE` | `A1` |
| Camera type | `echo $DEPTH_CAMERA_TYPE` | `AstraProPlus` |
| LiDAR hardware | `roslaunch rplidar_ros rplidar.launch` | `Health Status : OK`, `Scan Frequency : 10 Hz` |
| Filtered scan topic | `rostopic list \| grep scan` | `/jetauto_1/scan`, `/jetauto_1/scan_raw` present |
| Scan rate | `rostopic hz /jetauto_1/scan` | ~10 Hz |
| Odometry topics | `rostopic list \| grep odom` | `/jetauto_1/odom`, `/jetauto_1/odom_raw`, `/jetauto_1/set_odom` |
| Odometry rate | `rostopic hz /jetauto_1/odom` | ~29–30 Hz (fused) |
| Raw odometry rate | `rostopic hz /jetauto_1/odom_raw` | ~50 Hz |
| TF completeness | `rosrun tf view_frames` | `map → odom → base_footprint → base_link → lidar → camera` fully connected |
| GMapping output | RViz occupancy grid | Grid expands as robot moves |
| Saved 2D map | `ls my_map.*` | `my_map.pgm`, `my_map.yaml` created |
| RTAB-Map node | `rosnode list \| grep rtabmap` | `/jetauto_1/rtabmap/rtabmap` running |
| RTAB-Map database | `rosparam get /rtabmap/database_path` then `ls -lh` | `~/.ros/rtabmap.db` exists and grows during mapping |
| Database contents | `rtabmap-databaseViewer` | RGB images, ORB features, pose graph, point cloud all visible |

---

## 9. Results

At the conclusion of this work, the following were fully functional:

- ✅ RPLIDAR A1 driver correctly selected and communicating over `/dev/ttyUSB0`
- ✅ Duplicate LiDAR node conflict resolved
- ✅ `/scan` and `/scan_raw` publishing at a stable ~10 Hz
- ✅ `/odom` (EKF-fused) and `/odom_raw` publishing correctly
- ✅ Complete TF tree from `map` to `camera`
- ✅ GMapping generating and saving a valid 2D occupancy grid (`my_map.pgm` / `.yaml`)
- ✅ Astra Pro Plus RGB-D camera operational without USB resource conflicts
- ✅ RTAB-Map generating a live, colored 3D point cloud
- ✅ RTAB-Map session persisted to `rtabmap.db`
- ✅ Database Viewer successfully inspecting nodes, RGB/feature panels, and pose graph
- ✅ Export pipeline verified (PLY/PCD/OBJ/PNG) for use in CloudCompare, MeshLab, Open3D

> 📷 Screenshot: Side-by-side comparison — GMapping 2D occupancy grid (left) vs. RTAB-Map 3D colored point cloud (right) of the same lab space.

---

## 10. GMapping vs RTAB-Map Comparison

| Feature | GMapping | RTAB-Map |
|---|---|---|
| Mapping dimensionality | 2D | 3D |
| Primary sensor(s) | LiDAR | RGB-D + LiDAR + IMU |
| Output | Occupancy grid | Point cloud + database |
| Loop closure | Limited | Strong, appearance-based |
| Image storage | No | Yes (RGB + depth per node) |
| Persistent database | No | Yes (`rtabmap.db`) |
| Offline analysis/export | No | Yes (Database Viewer, PLY/OBJ/PCD export) |
| Typical use case | Lightweight 2D navigation | Rich 3D environment reconstruction |

---

## 11. Lessons Learned

1. Hardware configuration is as critical as software configuration — a single incorrect environment variable (`LIDAR_TYPE`) prevented the entire SLAM stack from functioning.
2. Device mappings such as `/dev/lidar` should always be cross-checked against the actual Linux device (`/dev/serial/by-id/`, `/dev/ttyUSBx`) rather than assumed to exist.
3. ROS namespaces (e.g. `/jetauto_1`) must be understood before debugging topics, or missing-topic symptoms can be misdiagnosed.
4. Restoring `/scan` and `/odom` is the foundation for any SLAM algorithm — no higher-level pipeline (GMapping or RTAB-Map) can succeed without them.
5. RTAB-Map is significantly more complex than GMapping because it fuses multiple sensing modalities simultaneously.
6. The `rtabmap.db` database is the most valuable output of a mapping session, since it stores everything needed to reconstruct, re-analyze, and export the environment offline.
7. Visual (ORB) features are central to RTAB-Map's loop closure and graph optimization quality.
8. RGB-D reconstruction quality is highly sensitive to lighting stability and smooth robot motion.
9. USB-connected sensors (RGB-D camera, secondary USB camera) must be launched by only one process at a time to avoid "Resource Busy" conflicts.
10. A successful SLAM pipeline depends on the correct integration of *all* sensing modalities — LiDAR, odometry, IMU, and camera — not any single sensor in isolation.

---

## 12. Future Work

- Autonomous navigation using the generated maps.
- Integration with the ROS Navigation Stack.
- Real-time obstacle avoidance.
- 3D point cloud optimization / denoising.
- Loop closure parameter tuning.
- Dense mesh reconstruction.
- Object-aware semantic mapping.
- Exploration algorithms (Frontier Exploration and RRT Exploration).
- Comparative benchmarking of RTAB-Map, Cartographer, Hector SLAM, and Karto SLAM.

---

## 13. Conclusion

This work restored and validated the complete SLAM pipeline of the JetAuto Pro platform, beginning from a non-functional system affected by incorrect hardware configuration, missing device mappings, duplicate launch files, and unavailable sensor topics. Each issue — simulated-time mismatch, duplicate LiDAR node launches, incorrect `LIDAR_TYPE`, missing `/dev/lidar` symlink, and USB resource conflicts on the RGB-D and secondary cameras — was systematically diagnosed and resolved.

With LiDAR communication, odometry, and the TF tree restored, both GMapping and RTAB-Map were executed successfully. The robot generated accurate 2D occupancy maps and a colored 3D reconstruction of the environment using the Astra Pro Plus RGB-D camera. The mapping session was preserved in `rtabmap.db`, enabling offline visualization, node-level analysis, and export of the reconstructed environment in standard formats (PLY, PCD, OBJ, PNG).

The resulting workflow provides a stable, reproducible foundation for future work in autonomous navigation, 3D perception, and further SLAM research on the JetAuto Pro platform.

---

## 14. Appendix

### Appendix A — Complete Command Reference

```bash
source ~/jetauto_ws/src/jetauto_bringup/scripts/source_env.bash
roslaunch jetauto_slam slam.launch
roslaunch jetauto_slam rviz_slam.launch
roslaunch rplidar_ros rplidar.launch
rosrun tf view_frames
rosrun map_server map_saver -f my_map
rtabmap-databaseViewer ~/.ros/rtabmap.db
rostopic list
rostopic hz /jetauto_1/scan
rostopic hz /jetauto_1/odom
rosnode list
rosparam get /rtabmap/database_path
```

### Appendix B — Expected Boot / Environment Output

```text
LIDAR:   A1
CAMERA:  AstraProPlus
MACHINE: JetAutoPro
HOST:    jetauto_1
MASTER:  jetauto_1
```

### Appendix C — Expected Key Nodes After Full Bringup

```
jetauto_controller
ekf_localization
jetauto_odom_publisher
imu
imu_filter
robot_state_publisher
camera
usb_cam
jetauto_slam_gmapping
rtabmap (if RTAB enabled)
```

### Appendix D — Complete Reproducible Workflow

```
Power ON Robot
       ↓
Open Terminal
       ↓
source source_env.bash
       ↓
Verify Hardware (LIDAR_TYPE, DEPTH_CAMERA_TYPE)
       ↓
Launch RTAB-Map (roslaunch jetauto_slam slam.launch)
       ↓
Launch RViz (roslaunch jetauto_slam rviz_slam.launch)
       ↓
Verify Topics (scan, odom, image, depth, points, tf)
       ↓
Verify TF (rosrun tf view_frames)
       ↓
Verify Camera / LiDAR / Odometry Frequencies (rostopic hz)
       ↓
Move Robot (slow speed, smooth turns, revisit locations)
       ↓
Generate 3D Map
       ↓
Stop RTAB-Map (Ctrl+C) — database auto-saved
       ↓
Open Database Viewer (rtabmap-databaseViewer)
       ↓
Inspect Nodes (RGB, features, pose graph, point cloud)
       ↓
Export Point Cloud (File → Export 3D Clouds → PLY)
       ↓
Backup Database (cp ~/.ros/rtabmap.db ~/rtabmap_maps/)
       ↓
Open Exported Point Cloud (CloudCompare / MeshLab / Open3D)
```

---

**End of Document**
*RTAB-Map SLAM Integration & Debugging Report — JetAuto Pro*
