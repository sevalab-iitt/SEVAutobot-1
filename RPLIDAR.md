# RPLIDAR  
 
---

## Table of Contents

1. [How RPLIDAR Data Acquisition Works](#1-how-rplidar-data-acquisition-works)
2. [ROS Data Format (`sensor_msgs/LaserScan`)](#2-ros-data-format-sensor_msgslaserscan)
3. [From LaserScan to Point Clouds](#3-from-laserscan-to-point-clouds)
4. [Complete Data Flow](#4-complete-data-flow)
5. [Setup Fix: The Buffer Overflow Crash](#5-setup-fix-the-buffer-overflow-crash)
6. [Setup Fix: Autostart on Boot](#6-setup-fix-autostart-on-boot)
7. [Common Issue: Duplicate Process Conflict](#7-common-issue-duplicate-process-conflict)
8. [How to Actually Get the LiDAR Data — Step by Step](#8-how-to-actually-get-the-lidar-data--step-by-step)
9. [Quick Reference](#9-quick-reference)
10. [Troubleshooting Checklist](#10-troubleshooting-checklist)

---

## 1. How RPLIDAR Data Acquisition Works

There are **two different layers** involved in how RPLIDAR data is handled:

1. **The hardware layer** — how the RPLIDAR measures distances and streams raw data.
2. **The ROS layer** — how the `rplidar_ros` driver converts that raw stream into standard ROS messages.

### Operating Principle

The RPLIDAR A1M8 uses **laser triangulation** rather than time-of-flight (ToF):

- A laser diode emits a beam while the optical assembly continuously rotates.
- Reflected light is captured by an internal CMOS sensor.
- The displacement of the reflected laser spot is used to calculate distance through **triangulation**.
- The sensor performs this process continuously while rotating to produce a complete 360° scan.
- This is a process of sampling physical quantities — like temperature, pressure, or voltage — and converting them into digital numeric values for a computer to process.

### Rotation Speed

Typical operating speed: **5.5–10 Hz** (approximately 5.5–10 full revolutions per second). Each revolution represents one complete laser scan.

### Sampling Rate

Depending on the selected scan mode (e.g. **Boost**, **Sensitivity**, or **Stability**), the lidar generates several thousand measurements every second. Example: **Sensitivity mode** produces ~8000 samples/second, distributed across each 360° revolution.

### No Onboard Scan Storage

Unlike cameras that capture entire frames before transmitting them, the RPLIDAR **does not store complete scans internally**:

- Each measurement is transmitted immediately.
- Only a very small hardware FIFO buffer exists.
- The sensor functions as a **real-time streaming device**, not a logging device.

### Raw Serial Data Format

Measurements are transmitted over the USB/serial interface using **Slamtec's proprietary binary protocol**. Each measurement packet contains:

| Field | Description |
|--------|-------------|
| Start flag | Indicates the beginning of a new revolution |
| Quality | Signal strength/confidence (6 bits) |
| Angle | Raw angular measurement |
| Distance | Raw distance measurement |

These packets stream continuously over:
```
/dev/serial/by-id/usb-...
```

### Role of `rplidar_ros`

The `rplidar_ros` driver performs the following tasks:

1. Reads raw binary packets from the serial interface.
2. Decodes them using the Slamtec SDK.
3. Groups measurements belonging to one complete 360° revolution.
4. Publishes the assembled scan as a ROS message.

---

## 2. ROS Data Format (`sensor_msgs/LaserScan`)

After a complete revolution is assembled, `rplidar_ros` publishes the scan on the `/scan` topic, using the standard ROS message type `sensor_msgs/LaserScan`:

```cpp
Header header
float32 angle_min
float32 angle_max
float32 angle_increment
float32 time_increment
float32 scan_time
float32 range_min
float32 range_max
float32[] ranges
float32[] intensities
```

| Field | Description |
|--------|-------------|
| `header` | Timestamp and coordinate frame (typically `"laser"`) |
| `angle_min` | Starting scan angle (radians) |
| `angle_max` | Ending scan angle (radians) |
| `angle_increment` | Angular spacing between measurements |
| `time_increment` | Time between consecutive measurements |
| `scan_time` | Time required for one full revolution |
| `range_min` | Minimum valid measurement distance (meters) |
| `range_max` | Maximum valid measurement distance (meters) |
| `ranges[]` | Distance measurements (meters) |
| `intensities[]` | Signal strength for each point (often zero on RPLIDAR A1) |

### The `ranges[]` Array

The most important field is `ranges[]` — it contains one distance measurement for each angular step. Unlike the raw sensor packets, **the angle is not stored for every point**. Instead, the angle is computed using:

```
angle = angle_min + i × angle_increment
```
where `i` is the index in the `ranges[]` array.

### Invalid Measurements

Measurements with no valid laser return are represented as `0.0`, `inf`, or `nan`. These values should typically be filtered before further processing:

```python
import math
for r in scan.ranges:
    if math.isfinite(r):
        # Valid measurement
        process(r)
```

---

## 3. From LaserScan to Point Clouds

`LaserScan` is a compact **polar-coordinate representation** — each measurement consists of `(angle, distance)`. Using the ROS package `laser_geometry`, these polar coordinates can be converted into Cartesian coordinates:

```
x = r cos(θ)
y = r sin(θ)
z = 0
```

The resulting data is published as `sensor_msgs/PointCloud2`, or saved to formats such as `.pcd` for mapping, visualization, or SLAM applications.

---

## 4. Complete Data Flow

```
                RPLIDAR Hardware
                        │
      Laser triangulation measurements
                        │
                        ▼
     Proprietary binary packets (serial/USB)
                        │
                        ▼
          Slamtec SDK + rplidar_ros
                        │
      Decode + assemble one full revolution
                        │
                        ▼
      sensor_msgs/LaserScan (/scan topic)
                        │
                        ▼
        Navigation / RViz / SLAM / ROS Nodes
                        │
                        ▼
    Optional conversion to PointCloud2 / .pcd
```

**Summary:** the RPLIDAR hardware does not store complete scans internally. Instead, it continuously streams binary angle–distance measurement packets over a serial interface using Slamtec's proprietary protocol. The `rplidar_ros` driver reads this binary stream, decodes the packets, reconstructs a complete 360° revolution, and publishes it as a standard `sensor_msgs/LaserScan` message on the `/scan` topic. This standardized ROS representation enables downstream applications — RViz visualization, obstacle detection, SLAM, navigation, and conversion to `PointCloud2` — to process lidar data independently of the underlying hardware protocol.

---

## 5. Setup Fix: The Buffer Overflow Crash

### Symptom
```bash
roslaunch rplidar_ros rplidar.launch
```
caused an infinite crash-restart loop:
 
 <img width="959" height="246" alt="image" src="https://github.com/user-attachments/assets/855e7ed2-7cc7-45a8-8519-18b711b3aad9" />
 
Crashed immediately after printing `SDK Version:2.0.0`, before publishing any `/scan` data. `respawn="true"` in the launch file caused endless restarts.

### Root Cause

`*** buffer overflow detected ***` is glibc's stack-protector (`fortify_source`) catching a stack-smashing bug in the compiled `rplidarNode` binary, triggered specifically by `angle_compensate`:

- Lidar auto-selected a **high-sample-rate scan mode** ("Sensitivity", 8 kHz).
- `angle_compensate` in `rplidar_ros` uses a **fixed-size stack buffer** to build the angle-compensated scan.
- At 8 kHz sample rate, more samples per revolution are produced than that buffer was sized for → stack overflow → glibc aborts the process (`SIGABRT`, exit code `-6`).

Confirmed by running the node directly via `rosrun rplidar_ros rplidarNode` (bypassing the launch file's `angle_compensate=true` param) — it started cleanly, no crash.

### The Fix

**File:** `~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch`

Changed:
```xml
<param name="angle_compensate" type="bool" value="true"/>
```
to:
```xml
<param name="angle_compensate" type="bool" value="false"/>
```

> **Note:** `angle_compensate` is hardcoded via `<param>` with no `<arg>` wrapper, so passing `angle_compensate:=false` on the command line does **nothing**. The XML must be edited directly.

**Commands used:**
```bash
# Backup first
cp ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch \
   ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch.bak

# Edit just the one line
sed -i 's/name="angle_compensate" type="bool" value="true"/name="angle_compensate" type="bool" value="false"/' \
  ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch

# Confirm only that line changed
diff ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch.bak \
     ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch
```

### Final Working Launch File
 <img width="755" height="296" alt="image" src="https://github.com/user-attachments/assets/dca35eb6-f920-4f82-a401-6310290b57e0" />


**Verify:** relaunch and confirm the SUMMARY block prints `angle_compensate: False`, with no `*** buffer overflow detected ***`.

---

## 6. Setup Fix: Autostart on Boot

### Discovery

JetAuto already has an autostart mechanism:
```bash
systemctl list-units --type=service --all | grep -i ros
# roscore.service — always running

find ~/jetauto_ws -iname "*.service"
# jupyter.service, start_app_node.service, clear_log.service,
# fan_control.service, expand_rootfs.service, voltage_detect.service
```

`start_app_node.service` is JetAuto's official master autostart entry point:
```ini
[Unit]
Description=start node
After=NetworkManager.service time-sync.target
[Service]
Type=simple
User=jetauto
Restart=always
RestartSec=30
KillMode=mixed
ExecStart=/home/jetauto/jetauto_ws/src/jetauto_bringup/scripts/source_env.bash roslaunch jetauto_bringup bringup.launch
StandardOutput=null
StandardError=null
[Install]
WantedBy=multi-user.target
```

> **Note:** `StandardOutput=null` / `StandardError=null` means crashes are **silent** in `systemctl status` — use `journalctl -u start_app_node.service` to see real errors.

### Managing This Service
```bash
sudo systemctl status start_app_node.service      # check state
sudo systemctl is-enabled start_app_node.service  # confirm boot-persistence
sudo systemctl enable start_app_node.service       # enable permanently
sudo systemctl start start_app_node.service        # start now
sudo systemctl stop start_app_node.service         # stop now (temporary)
sudo systemctl disable start_app_node.service      # disable permanently
sudo systemctl restart start_app_node.service      # restart
journalctl -u start_app_node.service --no-pager | tail -100   # view real logs
```

### Problem Found: Lidar Was Missing from `bringup.launch`

`bringup.launch` (`~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch`) brings up the chassis controller, servos, cameras, app communication (`rosbridge`), and joystick — but had **no include for `rplidar_ros`**. This is why `/rplidarNode` never appeared in `rosnode list`, even though `/lidar_app` (a higher-level app-control node) was running and waiting for `/scan` data that never came.

### The Fix

Backup first:
```bash
cp ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch \
   ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch.bak
```

Edit `~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch` and add, near the chassis/servo includes:
```xml
<!--激光雷达驱动(lidar driver)-->
<include file="$(find rplidar_ros)/launch/rplidar.launch"/>
```

Restart the service to apply:
```bash
sudo systemctl restart start_app_node.service
sleep 8
rosnode list | grep -i rplidar
rostopic list | grep -i scan
```

Since this include points to the same `rplidar.launch` fixed in Section 5 (`angle_compensate=false`), the crash fix automatically carries over.

**Full reboot test (final proof):**
```bash
sudo reboot
# after reboot:
rosnode list | grep -i rplidar
```

---

## 7. Common Issue: Duplicate Process Conflict

### Symptom
<img width="347" height="131" alt="image" src="https://github.com/user-attachments/assets/674bb92e-c852-4f0d-94aa-46f8ef202c42" />

```
`/scan` topic exists (registered), but nothing is actually publishing to it. **This is the single most common lidar issue on this robot** and will likely recur.

### Root Cause

**Two `roslaunch rplidar_ros rplidar.launch` processes running simultaneously** — one from the systemd bringup service, and a leftover manual one from testing that was never fully killed. Both fight over the same `/dev/ttyUSB0` serial port. Symptoms in `ps aux`:
```
roslaunch rplidar_ros rplidar.launch     (older PID)
roslaunch rplidar_ros rplidar.launch     (newer PID)
[rplidarNode] <defunct>                   ← zombie process
rplidarNode-1.log  / rplidarNode-2.log    ← two competing node instances
```
This can also cause `start_app_node.service` to exit with `code=1/FAILURE`, due to "new node registered with same name" conflicts.

### The Fix
```bash
# 1. Stop the service so it stops respawning during cleanup
sudo systemctl stop start_app_node.service

# 2. Kill every lidar-related process, including zombie parents
pkill -9 -f rplidarNode
pkill -9 -f "roslaunch rplidar_ros"
ps aux | grep -i rplidar        # confirm clean (only the grep line itself)

# 3. Check no manual terminal is still running roslaunch (Ctrl+C any that are)

# 4. Restart the bringup service fresh
sudo systemctl start start_app_node.service
sleep 8

# 5. Confirm single clean process + real data
ps aux | grep -i rplidar        # should show exactly ONE rplidarNode
rosnode list | grep rplidar
rostopic hz /scan                # should show steady ~10 Hz
```

### One-Command Safety Net

Save this as a reusable script so this fix is always one command away:
```bash
nano ~/lidar_safe_start.sh
```
 <img width="625" height="242" alt="image" src="https://github.com/user-attachments/assets/404f4dc7-4e1a-431b-a191-3f4893c46b9d" />

```bash
chmod +x ~/lidar_safe_start.sh
```
From now on, run `~/lidar_safe_start.sh` any time `/scan` goes silent.

**Rule to prevent recurrence:** the lidar already auto-starts via `bringup.launch` + `start_app_node.service` on every boot. Never manually run `roslaunch rplidar_ros rplidar.launch` unless you're specifically testing — and if you do, always kill it afterward (`pkill -9 -f rplidarNode; pkill -9 -f roslaunch`) before assuming the managed instance is working correctly.

---

## 8. How to Actually Get the LiDAR Data — Step by Step

### Step 1 — Confirm the sensor is connected
```bash
ls -l /dev/serial/by-id/
 ```
 ## Expected: `<img width="641" height="41" alt="image" src="https://github.com/user-attachments/assets/43696fb6-ce29-4f7b-a4f3-e7276051fb5e" />
`. If empty, fix the physical connection first.

### Step 2 — Clean up anything already running
```bash
sudo systemctl stop start_app_node.service
pkill -9 -f rplidarNode
pkill -9 -f roslaunch
ps aux | grep -i rplidar
```
Should show nothing but the grep line itself. (Shortcut: `~/lidar_safe_start.sh` does this automatically.)

### Step 3 — Start the lidar the proper way
```bash
sudo systemctl start start_app_node.service
sleep 8
```
Always restart through the systemd service, not a manual `roslaunch` — this avoids the duplicate-process conflict in Section 7.
<img width="953" height="155" alt="image" src="https://github.com/user-attachments/assets/9325ede1-70de-48c3-b1f2-8bbca34474de" />

### Step 4 — Confirm it's working
```bash
rostopic hz /scan
```
Should show a steady rate near 10 Hz.

### Step 5 — Convert raw scans into point cloud format

Create the converter script once:
```bash
nano ~/scan_to_cloud.py
```
```python
#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan, PointCloud2
import laser_geometry.laser_geometry as lg

projector = lg.LaserProjection()
pub = rospy.Publisher('/cloud', PointCloud2, queue_size=1)

def callback(scan_msg):
    cloud = projector.projectLaser(scan_msg)
    pub.publish(cloud)

rospy.init_node('scan_to_cloud')
rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
```
```bash
chmod +x ~/scan_to_cloud.py
python ~/scan_to_cloud.py &
```
Confirm it's working:
```bash
rostopic hz /cloud
```

### Step 6 — (Optional) View it live in RViz
```bash
rosrun rviz rviz
```
- **Fixed Frame** → `laser`
- **Add** → **By topic** → `/cloud` → **PointCloud2** (or `/scan` → **LaserScan** for the raw 2D view)

RViz is purely for looking at data that's already flowing — not required for actually collecting it.

### Step 7 — Capture a proper, bounded dataset
```bash
mkdir -p ~/lidardata/dataset/pointclouds
cd ~/lidardata/dataset/pointclouds
timeout 10 rosrun pcl_ros pointcloud_to_pcd input:=/cloud _prefix:=scan_
```
Always use `timeout <seconds>` — this bounds the capture to a fixed, known duration instead of generating an unbounded stream of files.

### Step 8 — Merge the capture into a single file
```bash
pcl_concatenate_points_pcd scan_*.pcd
mv output.pcd merged_scan_$(date +%Y%m%d_%H%M%S).pcd
```
> If the lidar was stationary throughout capture, this only overlays near-identical scans — it does not build a bigger map. Real map-building requires the robot to move + odometry data (SLAM).

### Step 9 — Extract to CSV for analysis
```bash
FILE=$(ls merged_scan_*.pcd | tail -1)
DATA_START=$(grep -n "^DATA" "$FILE" | cut -d: -f1)
echo "x,y,z" > extracted_points.csv
tail -n +$((DATA_START+1)) "$FILE" | tr ' ' ',' >> extracted_points.csv
```
Loadable directly in Python/pandas or Excel.

### Step 10 — Package and download the dataset

On the robot:
```bash
cd ~/lidardata
tar -czvf lidar_dataset_$(date +%Y%m%d).tar.gz dataset/
```
On your laptop (not the robot):
```bash
scp jetauto@<robot_ip_address>:~/lidardata/lidar_dataset_*.tar.gz ./
```
(Find the robot's IP with `hostname -I` run on the robot.)

### Full Sequence, All Together
```bash
ls -l /dev/serial/by-id/
sudo systemctl stop start_app_node.service
pkill -9 -f rplidarNode; pkill -9 -f roslaunch
ps aux | grep -i rplidar
sudo systemctl start start_app_node.service
sleep 8
rostopic hz /scan

python ~/scan_to_cloud.py &

mkdir -p ~/lidardata/dataset/pointclouds
cd ~/lidardata/dataset/pointclouds
timeout 10 rosrun pcl_ros pointcloud_to_pcd input:=/cloud _prefix:=scan_

pcl_concatenate_points_pcd scan_*.pcd
mv output.pcd merged_scan_$(date +%Y%m%d_%H%M%S).pcd

FILE=$(ls merged_scan_*.pcd | tail -1)
DATA_START=$(grep -n "^DATA" "$FILE" | cut -d: -f1)
echo "x,y,z" > extracted_points.csv
tail -n +$((DATA_START+1)) "$FILE" | tr ' ' ',' >> extracted_points.csv

cd ~/lidardata
tar -czvf lidar_dataset_$(date +%Y%m%d).tar.gz dataset/
# then on your laptop: scp jetauto@<robot_ip>:~/lidardata/lidar_dataset_*.tar.gz ./
```

---

## 9. Quick Reference

```bash
# === CHECK STATUS ===
ls -l /dev/serial/by-id/          # hardware connected?
ps aux | grep -i rplidar           # exactly ONE process, no zombies?
rosnode list | grep rplidar        # node registered?
rostopic hz /scan                  # data flowing at ~10Hz?

# === FIX "NO NEW MESSAGES" ===
~/lidar_safe_start.sh

# === VIEW THE LIVE FEED ===
rostopic echo /scan -n 1           # one snapshot
rostopic echo /scan                # continuous stream
rosrun rviz rviz                   # visual

# === COLLECT DATA ===
python ~/scan_to_cloud.py &
timeout 10 rosrun pcl_ros pointcloud_to_pcd input:=/cloud _prefix:=scan_
pcl_concatenate_points_pcd scan_*.pcd

# === VIEW A SAVED FILE ===
pcl_viewer <file>.pcd

# === REAL ERROR LOGS (systemd hides them by default) ===
journalctl -u start_app_node.service --no-pager | tail -100
```

---

## 10. Troubleshooting Checklist

| Symptom | Likely Cause | Fix |
|---|---|---|
| `*** buffer overflow detected ***`, node dies repeatedly | `angle_compensate=true` overflows a fixed buffer at high sample rates | Set `angle_compensate` to `false` in `rplidar.launch` (§5) |
| `/rplidarNode` missing from `rosnode list` | Not included in `bringup.launch` | Add the `rplidar_ros` include (§6) |
| `/scan` exists but "no new messages" | Duplicate `rplidarNode`/`roslaunch` processes | Run `~/lidar_safe_start.sh` (§7) |
| `systemctl status` shows nothing on crash | Service redirects stdout/stderr to `null` | Use `journalctl -u start_app_node.service --no-pager \| tail -100` |
| `/dev/ttyUSB0` / `/dev/serial/by-id/` missing entirely | Physical USB/connection dropout | Reseat cable, try different port/cable, check power |
| Point cloud in RViz looks sparse or object-shaped weird | Normal 2D-lidar behavior — flat scan plane, occluded backside, fixed angular resolution | Move object closer to sensor for more points on it |
| Hundreds of near-identical `.pcd` files generated | `pointcloud_to_pcd` left running without a stop condition | Always use `timeout <seconds>` |
| Merged point cloud looks like one dense blob | Lidar was stationary; concatenation just overlays repeated scans | Move the robot between captures + use odometry/SLAM for true map extension |
| `pcl_viewer` window doesn't open | No display attached / SSH without X forwarding | Use `ssh -X`, or inspect with `head -15 <file>.pcd` instead |
