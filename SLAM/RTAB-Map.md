# RTAB-Map Learning Notes - Part 1
**Platform:** Hiwonder JetAuto Pro  
**ROS:** Melodic  
**OS:** Ubuntu 18.04  
**Depth Camera:** Orbbec Astra Pro Plus  
**LiDAR:** RPLIDAR A1

---

# Goal

Move from 2D LiDAR SLAM (GMapping) to 3D RGB-D Visual SLAM using RTAB-Map.

---

# Why RTAB-Map?

| GMapping | RTAB-Map |
|----------|----------|
| 2D LiDAR | RGB-D Camera (+ optional LiDAR) |
| 2D Occupancy Map | 3D Map |
| Laser-based localization | Visual + Depth localization |
| No image memory | Database of visual observations |
| Limited loop closure | Strong visual loop closure |

RTAB-Map allows the robot to reconstruct a complete 3D environment instead of only a 2D floor map.

---

# RGB-D Camera

An RGB-D camera outputs two synchronized images.

RGB Image

```
Pixel = Colour
```

Depth Image

```
Pixel = Distance
```

Example

RGB

```
Chair
Desk
Wall
```

Depth

```
2.1m
3.4m
5.2m
```

Combining both gives a coloured 3D point for every pixel.

```
(x, y, z, r, g, b)
```

This is the basis of RTAB-Map.

---

# Your Camera Topics

From your robot we can identify the important topics.

## RGB Camera

```
/astra_cam/rgb/*
```

Contains:

- RGB images
- Camera calibration

---

## Depth Camera

Important topics:

```
/astra_cam/depth/image_raw
```

Raw depth image.

```
/astra_cam/depth/image_rect
```

Rectified depth image.

```
/astra_cam/depth_registered/image_raw
```

Depth aligned with RGB image.

RTAB-Map usually prefers registered depth because every RGB pixel has matching depth.

---

## Camera Calibration

```
/astra_cam/rgb/camera_info
/astra_cam/depth/camera_info
```

Contains

- fx
- fy
- cx
- cy

These intrinsic parameters allow conversion from image pixels into 3D coordinates.

---

## Point Clouds

Most important topic

```
/astra_cam/depth/points
```

or

```
/astra_cam/depth_registered/points
```

Instead of pixels, these publish

```
x
y
z
r
g
b
```

for every visible point.

RTAB-Map uses these to generate dense 3D maps.

---

# Data Pipeline

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

---

# Topics That Matter

| Topic | Purpose |
|--------|----------|
| `/astra_cam/rgb/image_raw` | Colour image |
| `/astra_cam/depth_registered/image_raw` | Registered depth |
| `/astra_cam/rgb/camera_info` | Camera intrinsics |
| `/astra_cam/depth_registered/points` | Point cloud |
| `/jetauto_1/odom` | Robot odometry |
| `/tf` | Coordinate transforms |

Ignore compressed topics unless bandwidth is a concern.

---

# Key Takeaway

RTAB-Map does **not** work directly on images.

It combines:

- RGB images
- Depth images
- Camera calibration
- Odometry
- TF transforms

to estimate the robot pose, detect loop closures, and build a 3D map.


```
jetauto@jetauto-desktop:~$ rostopic list | grep camera
/astra_cam/depth/camera_info
/astra_cam/depth_registered/camera_info
/astra_cam/ir/camera_info
/astra_cam/projector/camera_info
/astra_cam/rgb/camera_info
/usb_cam/camera_info
jetauto@jetauto-desktop:~$ rostopic list | grep depth
/astra_cam/depth/camera_info
/astra_cam/depth/image
/astra_cam/depth/image/compressed
/astra_cam/depth/image/compressed/parameter_descriptions
/astra_cam/depth/image/compressed/parameter_updates
/astra_cam/depth/image/compressedDepth
/astra_cam/depth/image/compressedDepth/parameter_descriptions
/astra_cam/depth/image/compressedDepth/parameter_updates
/astra_cam/depth/image/theora
/astra_cam/depth/image/theora/parameter_descriptions
/astra_cam/depth/image/theora/parameter_updates
/astra_cam/depth/image_raw
/astra_cam/depth/image_raw/compressed
/astra_cam/depth/image_raw/compressed/parameter_descriptions
/astra_cam/depth/image_raw/compressed/parameter_updates
/astra_cam/depth/image_raw/compressedDepth
/astra_cam/depth/image_raw/compressedDepth/parameter_descriptions
/astra_cam/depth/image_raw/compressedDepth/parameter_updates
/astra_cam/depth/image_raw/theora
/astra_cam/depth/image_raw/theora/parameter_descriptions
/astra_cam/depth/image_raw/theora/parameter_updates
/astra_cam/depth/image_rect
/astra_cam/depth/image_rect/compressed
/astra_cam/depth/image_rect/compressed/parameter_descriptions
/astra_cam/depth/image_rect/compressed/parameter_updates
/astra_cam/depth/image_rect/compressedDepth
/astra_cam/depth/image_rect/compressedDepth/parameter_descriptions
/astra_cam/depth/image_rect/compressedDepth/parameter_updates
/astra_cam/depth/image_rect/theora
/astra_cam/depth/image_rect/theora/parameter_descriptions
/astra_cam/depth/image_rect/theora/parameter_updates
/astra_cam/depth/image_rect_raw
/astra_cam/depth/image_rect_raw/compressed
/astra_cam/depth/image_rect_raw/compressed/parameter_descriptions
/astra_cam/depth/image_rect_raw/compressed/parameter_updates
/astra_cam/depth/image_rect_raw/compressedDepth
/astra_cam/depth/image_rect_raw/compressedDepth/parameter_descriptions
/astra_cam/depth/image_rect_raw/compressedDepth/parameter_updates
/astra_cam/depth/image_rect_raw/theora
/astra_cam/depth/image_rect_raw/theora/parameter_descriptions
/astra_cam/depth/image_rect_raw/theora/parameter_updates
/astra_cam/depth/points
/astra_cam/depth_rectify_depth/parameter_descriptions
/astra_cam/depth_rectify_depth/parameter_updates
/astra_cam/depth_registered/camera_info
/astra_cam/depth_registered/hw_registered/image_rect
/astra_cam/depth_registered/hw_registered/image_rect/compressed
/astra_cam/depth_registered/hw_registered/image_rect/compressed/parameter_descriptions
/astra_cam/depth_registered/hw_registered/image_rect/compressed/parameter_updates
/astra_cam/depth_registered/hw_registered/image_rect/compressedDepth
/astra_cam/depth_registered/hw_registered/image_rect/compressedDepth/parameter_descriptions
/astra_cam/depth_registered/hw_registered/image_rect/compressedDepth/parameter_updates
/astra_cam/depth_registered/hw_registered/image_rect/theora
/astra_cam/depth_registered/hw_registered/image_rect/theora/parameter_descriptions
/astra_cam/depth_registered/hw_registered/image_rect/theora/parameter_updates
/astra_cam/depth_registered/hw_registered/image_rect_raw
/astra_cam/depth_registered/hw_registered/image_rect_raw/compressed
/astra_cam/depth_registered/hw_registered/image_rect_raw/compressed/parameter_descriptions
/astra_cam/depth_registered/hw_registered/image_rect_raw/compressed/parameter_updates
/astra_cam/depth_registered/hw_registered/image_rect_raw/compressedDepth
/astra_cam/depth_registered/hw_registered/image_rect_raw/compressedDepth/parameter_descriptions
/astra_cam/depth_registered/hw_registered/image_rect_raw/compressedDepth/parameter_updates
/astra_cam/depth_registered/hw_registered/image_rect_raw/theora
/astra_cam/depth_registered/hw_registered/image_rect_raw/theora/parameter_descriptions
/astra_cam/depth_registered/hw_registered/image_rect_raw/theora/parameter_updates
/astra_cam/depth_registered/image
/astra_cam/depth_registered/image/compressed
/astra_cam/depth_registered/image/compressed/parameter_descriptions
/astra_cam/depth_registered/image/compressed/parameter_updates
/astra_cam/depth_registered/image/compressedDepth
/astra_cam/depth_registered/image/compressedDepth/parameter_descriptions
/astra_cam/depth_registered/image/compressedDepth/parameter_updates
/astra_cam/depth_registered/image/theora
/astra_cam/depth_registered/image/theora/parameter_descriptions
/astra_cam/depth_registered/image/theora/parameter_updates
/astra_cam/depth_registered/image_raw
/astra_cam/depth_registered/image_raw/compressed
/astra_cam/depth_registered/image_raw/compressed/parameter_descriptions
/astra_cam/depth_registered/image_raw/compressed/parameter_updates
/astra_cam/depth_registered/image_raw/compressedDepth
/astra_cam/depth_registered/image_raw/compressedDepth/parameter_descriptions
/astra_cam/depth_registered/image_raw/compressedDepth/parameter_updates
/astra_cam/depth_registered/image_raw/theora
/astra_cam/depth_registered/image_raw/theora/parameter_descriptions
/astra_cam/depth_registered/image_raw/theora/parameter_updates
/astra_cam/depth_registered/points
/astra_cam/depth_registered_rectify_depth/parameter_descriptions
/astra_cam/depth_registered_rectify_depth/parameter_updates
```


<img width="1891" height="509" alt="image" src="https://github.com/user-attachments/assets/1657b005-9ffb-461a-8bb5-5f50c76a7f47" />


# JetAuto SLAM Launch Files Overview

This folder contains different SLAM algorithms and supporting modules. Only one SLAM method is typically launched at a time through `slam_base.launch`.

| Launch File | Purpose | When to Use |
|------------|---------|-------------|
| **cartographer.launch** | Launches Google's Cartographer SLAM. Uses LiDAR + IMU + odometry to build accurate 2D/3D maps with strong loop closure. More accurate than GMapping but computationally heavier. | Large environments requiring better accuracy. |
| **depthimage_to_laserscan.launch** | Converts a depth camera image into a virtual 2D LaserScan. Useful when no physical LiDAR is available. | RGB-D camera only systems. |
| **ekf.launch** | Runs an Extended Kalman Filter (robot_localization) to fuse multiple sensors like wheel odometry, IMU and GPS into a more accurate robot pose estimate. It does **not** perform SLAM. | Improving odometry before SLAM. |
| **explore.launch** | Automatically explores an unknown environment by continuously selecting new frontiers (unexplored areas) and navigating to them. Requires an existing SLAM system. | Autonomous exploration. |
| **frontier.launch** | Detects frontiers, i.e., boundaries between explored and unexplored space. It only finds candidate exploration targets and is usually used with `explore.launch`. | Frontier-based exploration. |
| **gmapping.launch** | Launches GMapping, a 2D Rao-Blackwellized Particle Filter SLAM algorithm using LiDAR and odometry. Produces a 2D occupancy grid map. | Small indoor environments with a 2D LiDAR. |
| **hector.launch** | Launches Hector SLAM, which mainly relies on high-frequency LiDAR scans and can work even without wheel odometry. Very useful when odometry is poor or unavailable. | UAVs or robots without reliable odometry. |
| **jetauto_robot.launch** | Starts the JetAuto hardware interface, sensors and robot description (URDF), making the robot available to other launch files. It prepares the robot but does not perform SLAM itself. | Base robot bring-up. |
| **karto.launch** | Runs OpenKarto SLAM, a graph-based 2D SLAM algorithm known for producing accurate maps with loop closure support. It generally performs better than GMapping in larger environments. | Medium to large indoor mapping. |
| **rrt_exploration.launch** | Uses the Rapidly-exploring Random Tree (RRT) algorithm to choose unexplored regions efficiently. Better suited for larger environments than simple frontier exploration. | Large-scale autonomous exploration. |
| **rtabmap.launch** | Launches RTAB-Map (Real-Time Appearance-Based Mapping). Uses RGB-D images, odometry and loop closure detection to create a 3D map while storing observations in a database. | RGB-D Visual SLAM and 3D reconstruction. |
| **slam_base.launch** | Master launch file that selects which SLAM algorithm to start based on the `slam_methods` argument. It also starts common components shared by all SLAM methods. | Main entry point for all SLAM modes. |

---

# Relationship Between the Files

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

Additional Modules

ekf.launch                → Better odometry
frontier.launch           → Detect unexplored regions
explore.launch            → Autonomous exploration
rrt_exploration.launch    → RRT-based exploration
depthimage_to_laserscan   → RGB-D → LaserScan conversion
jetauto_robot.launch      → Robot hardware and sensors
```

## Summary

- **SLAM algorithms:** `gmapping`, `cartographer`, `hector`, `karto`, `rtabmap`
- **Robot bring-up:** `jetauto_robot`
- **Sensor fusion:** `ekf`
- **Autonomous exploration:** `frontier`, `explore`, `rrt_exploration`
- **Sensor conversion:** `depthimage_to_laserscan`
- **Controller:** `slam_base` selects and launches the required SLAM pipeline.
