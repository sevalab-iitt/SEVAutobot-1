# Autonomous Navigation System Investigation

## 1. Objective

The goal of this work is to make the complete autonomous navigation pipeline of the JetAutoPro robot functional.

The robot already contains vendor-provided ROS packages for SLAM and autonomous navigation. Instead of rebuilding the navigation system from scratch, the existing implementation will first be inspected, tested, and repaired.

The final navigation pipeline should provide:

```text
Sensors
   │
   ├── RPLIDAR A1
   ├── Wheel/robot odometry
   └── Camera (where required)
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
Navigation Stack
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

## 2. Robot ROS Environment

The robot currently uses:

* Jetson Nano
* Ubuntu 18.04
* ROS Melodic
* ROS1
* JetAutoPro platform

The main ROS workspace is:

```text
/home/jetauto/jetauto_ws
```

The source directory is:

```text
/home/jetauto/jetauto_ws/src
```

---

## 3. Existing ROS Packages

The following packages were found inside the workspace:

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

The two most important packages for this investigation are:

```text
jetauto_navigation
jetauto_slam
```

### Navigation package

Location:

```text
/home/jetauto/jetauto_ws/src/jetauto_navigation
```

### SLAM package

Location:

```text
/home/jetauto/jetauto_ws/src/jetauto_slam
```

---

## 4. Initial Package Search

### Command

```bash
cd ~/jetauto_ws/src
ls
```

### Result

```text
jetauto_app
jetauto_interfaces
jetauto_slam
jetauto_bringup
jetauto_multi
lidar_cloud
jetauto_calibration
jetauto_navigation
scan_drivers.py
jetauto_driver
jetauto_peripherals
jetauto_example
jetauto_simulations
xf_mic_asr_offline
third_party
```

This confirms that the vendor's navigation and SLAM source packages are available locally.

---

## 5. Navigation and SLAM Directory Search

### Command

```bash
find ~/jetauto_ws/src -type d \( -name "*navigation*" -o -name "*slam*" \) | sort
```

### Result

```text
/home/jetauto/jetauto_ws/src/jetauto_example/launch/orb_slam_demo
/home/jetauto/jetauto_ws/src/jetauto_example/scripts/navigation_transport
/home/jetauto/jetauto_ws/src/jetauto_multi/launch/multi_navigation
/home/jetauto/jetauto_multi/launch/multi_slam
/home/jetauto/jetauto_ws/src/jetauto_navigation
/home/jetauto/jetauto_ws/src/jetauto_slam
```

### Observation

There are multiple navigation/SLAM-related components.

The primary packages appear to be:

```text
jetauto_navigation
jetauto_slam
```

There are also additional examples and multi-robot implementations:

```text
jetauto_example/launch/orb_slam_demo
jetauto_example/scripts/navigation_transport
jetauto_multi/launch/multi_navigation
jetauto_multi/launch/multi_slam
```

These should not be modified unless they are later found to be part of the actual JetAuto desktop navigation workflow.

---

## 6. Existing User Files and Robot Data

The home directory also contains several files and directories related to previous mapping and navigation experiments.

Examples include:

```text
my_map.pgm
my_map.yaml
my_map1.pgm
my_map1.yaml

trtabmap.pgm
trtabmap.yaml
trtabmap1.pgm
trtabmap1.yaml
trtabmap2.pgm
trtabmap2.yaml

rtabmap_maps/
.rtabmap/
.ros/
```

There are also ROS and robot logs:

```text
robot_bringup.log
jetauto_ros_topics.txt
jetauto_session_20260625_102652.log
rosgraph_active.dot
terminal_log.txt
```

These may be useful when debugging the existing system.

---

## 7. Current Investigation Strategy

The existing navigation implementation will be investigated before making changes.

The investigation follows this order:

```text
Desktop Navigation Shortcut
          │
          ▼
Startup Script
          │
          ▼
ROS Launch File
          │
          ▼
ROS Nodes
          │
          ├── Drivers
          ├── LiDAR
          ├── Odometry
          ├── TF
          ├── Localization
          ├── move_base
          ├── Costmaps
          └── Planners
          │
          ▼
       /cmd_vel
          │
          ▼
JetAuto Motor Controller
```

The objective is to determine which component fails when the vendor navigation system is launched.

---

## 8. Next Investigation Commands

The following commands will identify all navigation-related launch files.

```bash
find ~/jetauto_ws/src -type f \
  \( -name "*.launch" -o -name "*.launch.xml" \) \
  | grep -Ei "nav|slam|rviz|move"
```

Then inspect the ROS package registry:

```bash
source /opt/ros/melodic/setup.bash
source ~/jetauto_ws/devel/setup.bash

rospack list | grep -Ei "jetauto|hiwonder|navigation|slam|move"
```

The exact output should be recorded here after execution.

---

## 9. Important Principle

RViz is not the navigation system itself.

RViz provides visualization and interfaces such as:

```text
2D Pose Estimate
2D Nav Goal
Map visualization
LaserScan visualization
TF visualization
Costmap visualization
```

The actual autonomous navigation is performed by ROS navigation nodes.

A typical ROS1 navigation chain is:

```text
RViz
 │
 │ navigation goal
 ▼
move_base
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
JetAuto Driver
 │
 ▼
Robot Motion
```

Therefore, opening RViz successfully does not prove that autonomous navigation is working.

---

## 10. Known Working Components

Previous project work established that the robot can perform:

* GMapping-based mapping
* RTAB-Map mapping/localization
* RPLIDAR A1 operation
* Robot odometry/TF investigation
* JetAuto motor/control operation

Therefore, the existing components should be reused where possible.

The current objective is primarily to complete and repair:

```text
Localization
       ↓
TF
       ↓
Navigation Costmaps
       ↓
Global Planner
       ↓
Local Planner
       ↓
/cmd_vel
       ↓
Robot Motion
```

---

## 11. Changes Policy

Before modifying vendor files:

1. Identify the original launch file.
2. Record the original configuration.
3. Identify the failing node.
4. Record the error.
5. Determine the cause.
6. Make the smallest required change.
7. Test again.
8. Document the change.
9. Commit the change to Git.

Vendor source files should not be modified blindly.

---

The next step is to identify the exact launch files and startup scripts used by the vendor's Navigation and SLAM applications.
