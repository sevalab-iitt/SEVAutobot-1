# Autonomous Navigation Investigation

## 1. Objective

The goal of this work is to make the complete autonomous navigation pipeline of the JetAutoPro robot functional.

The robot already contains vendor-provided ROS packages for SLAM and autonomous navigation. Instead of rebuilding the navigation system from scratch, the existing implementation will first be inspected, tested, and repaired.

The final navigation pipeline should provide:

```text
Sensors
   │
   ├── RPLIDAR A1
   ├── Wheel / robot odometry
   └── Camera where required
   │
   ▼
ROS Drivers
   │
   ├── /scan
   ├── odometry
   └── TF
   │
   ▼
SLAM / Localization
   │
   ├── GMapping
   └── RTAB-Map
   │
   ▼
Map + Robot Pose
   │
   ▼
ROS1 Navigation Stack
   │
   ├── Global Costmap
   ├── Local Costmap
   ├── Global Planner
   └── Local Planner
   │
   ▼
/cmd_vel
   │
   ▼
JetAuto Controller
   │
   ▼
Motors
```

---

# 2. Robot Environment

The current robot environment is:

| Component        | Configuration              |
| ---------------- | -------------------------- |
| Robot            | JetAutoPro                 |
| Main computer    | NVIDIA Jetson Nano         |
| OS               | Ubuntu 18.04               |
| ROS              | ROS Melodic                |
| ROS architecture | ROS1                       |
| LiDAR            | RPLIDAR A1                 |
| Depth camera     | Orbbec Astra Pro Plus      |
| Workspace        | `/home/jetauto/jetauto_ws` |

The main ROS source directory is:

```text
/home/jetauto/jetauto_ws/src
```

---

# 3. Existing ROS Packages

The following packages were found:

```text
jetauto_app
jetauto_bringup
jetauto_calibration
jetauto_driver
jetauto_example
jetauto_interfaces
jetauto_multi
jetauto_navigation
jetauto_peripherals
jetauto_simulations
jetauto_slam
lidar_cloud
third_party
xf_mic_asr_offline
```

The primary packages for autonomous navigation are:

```text
jetauto_slam
jetauto_navigation
```

---

# 4. Navigation and SLAM Launch Files

The following launch files were found using:

```bash
find ~/jetauto_ws/src -type f \
\( -name "*.launch" -o -name "*.launch.xml" \) \
| grep -Ei "nav|slam|rviz|move"
```

## SLAM

```text
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/slam.launch

/home/jetauto/jetauto_ws/src/jetauto_slam/launch/rviz_slam.launch

/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/rtabmap.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/explore.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/depthimage_to_laserscan.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/karto.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/slam_base.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/hector.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/gmapping.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/cartographer.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/rrt_exploration.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/ekf.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/frontier.launch
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/jetauto_robot.launch
```

This shows that the vendor SLAM package supports multiple SLAM approaches, including:

* GMapping
* RTAB-Map
* Karto
* Hector
* Cartographer
* Frontier exploration
* RRT exploration
* EKF-related processing

---

# 5. Navigation Launch Files

The navigation package contains:

```text
/home/jetauto/jetauto_ws/src/jetauto_navigation/launch/navigation.launch

/home/jetauto/jetauto_ws/src/jetauto_navigation/launch/rviz_rtabmap_navigation.launch

/home/jetauto/jetauto_ws/src/jetauto_navigation/launch/publish_point.launch

/home/jetauto/jetauto_ws/src/jetauto_navigation/launch/include/navigation_base.launch

/home/jetauto/jetauto_ws/src/jetauto_navigation/launch/include/load_map.launch

/home/jetauto/jetauto_ws/src/jetauto_navigation/launch/include/move_base.launch

/home/jetauto/jetauto_navigation/launch/include/amcl.launch

/home/jetauto/jetauto_navigation/launch/rtabmap_navigation.launch

/home/jetauto/jetauto_navigation/launch/rviz_navigation.launch
```

The presence of `move_base.launch`, `amcl.launch`, costmap-related navigation files, and `navigation_base.launch` indicates that this is a ROS1 navigation stack rather than a ROS2/Nav2 stack.

---

# 6. ROS Package Verification

The command:

```bash
rospack list | grep -Ei "jetauto|hiwonder|navigation|slam|move"
```

confirmed that the navigation packages are registered in the ROS environment.

Important packages include:

```text
jetauto_bringup
jetauto_controller
jetauto_driver
jetauto_navigation
jetauto_slam
jetauto_sdk
jetauto_peripherals
move_base
move_base_msgs
openslam_gmapping
rplidar_ros
```

Relevant vendor packages:

```text
jetauto_bringup
/home/jetauto/jetauto_ws/src/jetauto_bringup

jetauto_controller
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller

jetauto_driver
/home/jetauto/jetauto_ws/src/jetauto_driver

jetauto_navigation
/home/jetauto/jetauto_ws/src/jetauto_navigation

jetauto_slam
/home/jetauto/jetauto_ws/src/jetauto_slam
```

This confirms that the standard ROS1 `move_base` package is installed and that the JetAuto-specific navigation package is available.

---

# 7. Desktop Application Entry Points

The desktop contains the following relevant application files:

```text
/home/jetauto/Desktop/slam.desktop

/home/jetauto/Desktop/navigation.desktop

/home/jetauto/Desktop/slam_automatic.desktop
```

The command:

```bash
grep -RniE "navigation|slam" ~/Desktop 2>/dev/null
```

returned the following important entries.

## SLAM

```text
/home/jetauto/Desktop/slam.desktop
Exec=bash /home/jetauto/jetauto_ws/src/jetauto_bringup/scripts/slam.sh
```

Therefore:

```text
Desktop SLAM icon
        │
        ▼
slam.sh
        │
        ▼
SLAM launch system
```

## Navigation

```text
/home/jetauto/Desktop/navigation.desktop
Exec=bash /home/jetauto/jetauto_ws/src/jetauto_bringup/scripts/navigation.sh
```

Therefore:

```text
Desktop Navigation icon
        │
        ▼
navigation.sh
        │
        ▼
Navigation launch system
```

## Autonomous SLAM

```text
/home/jetauto/Desktop/slam_automatic.desktop
Exec=bash /home/jetauto/jetauto_ws/src/jetauto_bringup/scripts/slam_automatic.sh
```

Therefore:

```text
Desktop SLAM Automatic icon
        │
        ▼
slam_automatic.sh
        │
        ▼
Autonomous mapping system
```

---

# 8. Important Discovery

The desktop icons do not directly execute RViz.

The current architecture is:

```text
                         ┌──────────────────────┐
                         │   Desktop Shortcut   │
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
             slam.sh          navigation.sh     slam_automatic.sh
                 │                  │                  │
                 ▼                  ▼                  ▼
            SLAM stack       Navigation stack    Auto mapping
                 │                  │
                 ▼                  ▼
              RViz             RViz
```

The next investigation must therefore inspect these shell scripts.

---

# 9. Next Step: Inspect Vendor Startup Scripts

The following commands will be used:

```bash
sed -n '1,240p' \
~/jetauto_ws/src/jetauto_bringup/scripts/navigation.sh
```

```bash
sed -n '1,240p' \
~/jetauto_ws/src/jetauto_bringup/scripts/slam.sh
```

```bash
sed -n '1,240p' \
~/jetauto_ws/src/jetauto_bringup/scripts/slam_automatic.sh
```

The scripts will be treated as the entry point for tracing the complete vendor pipeline.

---

# 10. Navigation Pipeline Investigation

After inspecting `navigation.sh`, the referenced launch files will be inspected.

Expected chain:

```text
navigation.sh
     │
     ▼
navigation.launch
     │
     ├── load_map.launch
     │
     ├── navigation_base.launch
     │
     ├── move_base.launch
     │
     ├── amcl.launch
     │
     └── RViz
```

The exact chain must be verified from the source files before making any assumptions.

---

# 11. Navigation Components to Verify

The following components will be checked individually:

### A. Robot drivers

```text
JetAuto driver
STM32 controller
wheel encoders
```

### B. LiDAR

```text
RPLIDAR A1
/scan
```

### C. Odometry

```text
/odom
```

### D. TF

Expected important transforms:

```text
map
 └── odom
      └── base_footprint / base_link
           └── laser
```

The exact frame names will be obtained from the running system.

### E. Localization

Possible implementation:

```text
AMCL
```

or:

```text
RTAB-Map localization
```

depending on the selected navigation mode.

### F. Navigation

```text
move_base
```

### G. Costmaps

```text
global_costmap
local_costmap
```

### H. Planners

The exact global and local planner plugins will be obtained from the configuration files.

### I. Robot command

```text
/cmd_vel
```

The final command must reach the JetAuto controller.

---

# 12. Vendor Documentation Reference

The Hiwonder documentation states that ROS1 autonomous navigation is intended for the Jetson Nano controller. It describes using the Navigation desktop icon, setting the initial pose with `2D Pose Estimate`, selecting destinations with `2D Nav Goal`, and starting navigation.

The documentation also states that the Navigation function reads the most recently created map.

The vendor documentation identifies the Jetson Nano environment as Ubuntu 18.04 with ROS Melodic, matching the current robot environment.

Reference:

https://wiki.hiwonder.com/projects/JetAuto/en/jetauto-orin-nano/docs/1.quick_start_guide.html#_1-10-autonomous-navigation

---

# 13. Current Status

```text
[✓] JetAuto workspace identified
[✓] ROS Melodic environment confirmed
[✓] jetauto_slam package identified
[✓] jetauto_navigation package identified
[✓] SLAM launch files identified
[✓] Navigation launch files identified
[✓] move_base package confirmed
[✓] Desktop SLAM shortcut identified
[✓] Desktop Navigation shortcut identified
[✓] Desktop SLAM Automatic shortcut identified

[ ] navigation.sh inspected
[ ] slam.sh inspected
[ ] slam_automatic.sh inspected
[ ] navigation.launch inspected
[ ] navigation_base.launch inspected
[ ] move_base.launch inspected
[ ] load_map.launch inspected
[ ] AMCL configuration inspected
[ ] Costmap configuration inspected
[ ] TF tree verified
[ ] Navigation nodes tested
[ ] Navigation error reproduced
[ ] Root cause identified
[ ] Navigation repaired
[ ] End-to-end navigation tested
[ ] Git commit created
