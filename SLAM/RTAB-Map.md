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

---

```
jetauto@jetauto-desktop:~$ rostopic list | grep odom
/jetauto_1/odom
/jetauto_1/odom_raw
/jetauto_1/set_odom
jetauto@jetauto-desktop:~$ rostopic hz /jetauto_1/odom
subscribed to [/jetauto_1/odom]
average rate: 29.984
        min: 0.026s max: 0.041s std dev: 0.00231s window: 29
average rate: 30.001
        min: 0.026s max: 0.041s std dev: 0.00199s window: 59
average rate: 29.991
        min: 0.026s max: 0.041s std dev: 0.00163s window: 90
average rate: 30.001
        min: 0.026s max: 0.041s std dev: 0.00147s window: 120
average rate: 30.001
        min: 0.026s max: 0.041s std dev: 0.00135s window: 150
average rate: 30.000
        min: 0.026s max: 0.041s std dev: 0.00128s window: 180
average rate: 29.916
        min: 0.000s max: 0.044s std dev: 0.00349s window: 209
average rate: 29.971
        min: 0.000s max: 0.048s std dev: 0.00695s window: 239
average rate: 29.999
        min: 0.000s max: 0.048s std dev: 0.00876s window: 269
^Caverage rate: 29.966
        min: 0.000s max: 0.048s std dev: 0.00877s window: 270
jetauto@jetauto-desktop:~$ rostopic hz /jetauto_1/odom_raw
subscribed to [/jetauto_1/odom_raw]
average rate: 50.119
        min: 0.018s max: 0.021s std dev: 0.00054s window: 47
average rate: 50.066
        min: 0.018s max: 0.021s std dev: 0.00049s window: 97
average rate: 50.037
        min: 0.015s max: 0.025s std dev: 0.00075s window: 147
average rate: 50.032
        min: 0.015s max: 0.027s std dev: 0.00092s window: 197
average rate: 49.917
        min: 0.000s max: 0.048s std dev: 0.00930s window: 247
average rate: 49.963
        min: 0.000s max: 0.048s std dev: 0.01189s window: 296
average rate: 49.882
        min: 0.000s max: 0.048s std dev: 0.01357s window: 345
average rate: 50.017
        min: 0.000s max: 0.048s std dev: 0.01462s window: 397
average rate: 50.010
        min: 0.000s max: 0.048s std dev: 0.01543s window: 446
average rate: 49.957
        min: 0.000s max: 0.048s std dev: 0.01606s window: 497
^Caverage rate: 49.961
        min: 0.000s max: 0.048s std dev: 0.01651s window: 544
jetauto@jetauto-desktop:~$ rosrun tf tf_echo jetauto_1/odom jetauto_1/base_footprint
At time 1785961587.370
- Translation: [0.000, 0.000, 0.000]
- Rotation: in Quaternion [0.000, 0.000, 0.532, 0.847]
            in RPY (radian) [0.000, -0.000, 1.123]
            in RPY (degree) [0.000, -0.000, 64.330]
At time 1785961588.104
- Translation: [0.000, 0.000, 0.000]
- Rotation: in Quaternion [0.000, 0.000, 0.536, 0.844]
            in RPY (radian) [0.000, -0.000, 1.131]
            in RPY (degree) [0.000, -0.000, 64.786]
At time 1785961589.070
- Translation: [0.000, 0.000, 0.000]
- Rotation: in Quaternion [0.000, 0.000, 0.540, 0.841]
            in RPY (radian) [0.000, -0.000, 1.142]
            in RPY (degree) [0.000, -0.000, 65.435]
^Cjetauto@jetauto-desktop:~$ rostopic echo -n 1 /jetauto_1/odom
header:
  seq: 4831
  stamp:
    secs: 1785961596
    nsecs: 969891787
  frame_id: "jetauto_1/odom"
child_frame_id: "jetauto_1/base_footprint"
pose:
  pose:
    position:
      x: 0.0
      y: 0.0
      z: 0.0
    orientation:
      x: 0.0
      y: 0.0
      z: 0.584247173872
      w: 0.811575775774
  covariance: [8.05315152779734, -0.00012122562714347087, -3.5998864867865324e-17, 0.0, 0.0, 0.0, -0.00012122562714346836, 8.053355931029863, 1.2190903611338472e-17, 0.0, 0.0, 0.0, 2.0217933925120353e-30, -6.851674269734901e-31, 0.0010488645071991677, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0005246819035485411, -6.633855816360837e-27, 0.0, 0.0, 0.0, 0.0, -6.62634396718649e-27, 0.0005246819035485411, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 9.807027009353446]
twist:
  twist:
    linear:
      x: 0.0
      y: 0.0
      z: 0.0
    angular:
      x: 0.0
      y: 0.0
      z: 0.0154020819442
  covariance: [0.0008185874104237142, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0008575168763310116, 3.236129170874014e-14, 0.0, 0.0, 0.0, 0.0, -3.7321208892278435e-28, 0.0006994094852672374, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.00017522574639950139, 9.183549615799121e-40, 0.0, 0.0, 0.0, 0.0, -2.381719296648268e-24, 0.00017522574639950139, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0003494558787590816]
---
jetauto@jetauto-desktop:~$ rosnode list | grep rtabmap
/jetauto_1/rtabmap/rtabmap
jetauto@jetauto-desktop:~$ rostopic list | grep map
/jetauto_1/map
/jetauto_1/rtabmap/cloud_ground
/jetauto_1/rtabmap/cloud_map
/jetauto_1/rtabmap/cloud_obstacles
/jetauto_1/rtabmap/global_path
/jetauto_1/rtabmap/global_path_nodes
/jetauto_1/rtabmap/global_pose
/jetauto_1/rtabmap/goal
/jetauto_1/rtabmap/goal_node
/jetauto_1/rtabmap/goal_out
/jetauto_1/rtabmap/goal_reached
/jetauto_1/rtabmap/gps/fix
/jetauto_1/rtabmap/grid_prob_map
/jetauto_1/rtabmap/imu
/jetauto_1/rtabmap/info
/jetauto_1/rtabmap/initialpose
/jetauto_1/rtabmap/labels
/jetauto_1/rtabmap/landmarks
/jetauto_1/rtabmap/local_grid_empty
/jetauto_1/rtabmap/local_grid_ground
/jetauto_1/rtabmap/local_grid_obstacle
/jetauto_1/rtabmap/local_path
/jetauto_1/rtabmap/local_path_nodes
/jetauto_1/rtabmap/localization_pose
/jetauto_1/rtabmap/mapData
/jetauto_1/rtabmap/mapGraph
/jetauto_1/rtabmap/mapOdomCache
/jetauto_1/rtabmap/mapPath
/jetauto_1/rtabmap/octomap_binary
/jetauto_1/rtabmap/octomap_empty_space
/jetauto_1/rtabmap/octomap_full
/jetauto_1/rtabmap/octomap_global_frontier_space
/jetauto_1/rtabmap/octomap_grid
/jetauto_1/rtabmap/octomap_ground
/jetauto_1/rtabmap/octomap_obstacles
/jetauto_1/rtabmap/octomap_occupied_space
/jetauto_1/rtabmap/proj_map
/jetauto_1/rtabmap/republish_node_data
/jetauto_1/rtabmap/scan_map
/jetauto_1/rtabmap/tag_detections
/jetauto_1/rtabmap/user_data_async
jetauto@jetauto-desktop:~$ rostopic hz /jetauto_1/map
subscribed to [/jetauto_1/map]
average rate: 4.763
        min: 0.207s max: 0.212s std dev: 0.00231s window: 4
average rate: 4.734
        min: 0.133s max: 0.293s std dev: 0.04008s window: 9
average rate: 4.714
        min: 0.133s max: 0.293s std dev: 0.03175s window: 14
average rate: 4.724
        min: 0.133s max: 0.293s std dev: 0.03664s window: 18
average rate: 4.704
        min: 0.133s max: 0.293s std dev: 0.03269s window: 23
average rate: 4.703
        min: 0.133s max: 0.293s std dev: 0.02954s window: 28
average rate: 4.710
        min: 0.129s max: 0.293s std dev: 0.03284s window: 33
average rate: 4.695
        min: 0.129s max: 0.293s std dev: 0.03119s window: 37
average rate: 4.700
        min: 0.129s max: 0.293s std dev: 0.02965s window: 42
^Caverage rate: 4.695
        min: 0.129s max: 0.293s std dev: 0.02909s window: 45
jetauto@jetauto-desktop:~$ rostopic echo -n 1 /jetauto_1/rtabmap/info
header:
  seq: 0
  stamp:
    secs: 1785961685
    nsecs: 751400069
  frame_id: "jetauto_1/map"
refId: 1157
loopClosureId: 0
proximityDetectionId: 0
landmarkId: 0
loopClosureTransform:
  translation:
    x: 0.0
    y: 0.0
    z: 0.0
  rotation:
    x: 0.0
    y: 0.0
    z: 0.0
    w: 0.0
wmState: [1018, 1036, 1053, 1071, 1089, 1106, 1122, 1138, 1154, 1, 144, 200, 241, 282, 313, 345, 372, 398, 424, 449, 473, 496, 516, 536, 558, 580, 602, 620, 642, 662, 681, 701, 719, 737, 756, 775, 794, 812, 829, 846, 863, 882, 900, 918, 936, 953, 969, 985, 1002]
posteriorKeys: []
posteriorValues: []
likelihoodKeys: []
likelihoodValues: []
rawLikelihoodKeys: []
rawLikelihoodValues: []
weightsKeys: []
weightsValues: []
labelsKeys: [1]
labelsValues: [map0]
statsKeys: [Keypoint/Current_frame/words, Keypoint/Dictionary_size/words, Keypoint/Index_memory_usage/KB,
  Keypoint/Indexed_words/words, Loop/Accepted_hypothesis_id/, Loop/Angular_variance/,
  Loop/Highest_hypothesis_id/, Loop/Highest_hypothesis_value/, Loop/Hypothesis_ratio/,
  Loop/Hypothesis_reactivated/, Loop/Id/, Loop/Landmark_detected/, Loop/Landmark_detected_node_ref/,
  Loop/Last_id/, Loop/Linear_variance/, Loop/MapToBase_pitch/deg, Loop/MapToBase_roll/deg,
  Loop/MapToBase_x/m, Loop/MapToBase_y/m, Loop/MapToBase_yaw/deg, Loop/MapToBase_z/m,
  Loop/Map_id/, Loop/Optimization_error/, Loop/Optimization_iterations/, Loop/Optimization_max_ang_error/deg,
  Loop/Optimization_max_ang_error_ratio/, Loop/Optimization_max_error/m, Loop/Optimization_max_error_ratio/,
  Loop/Reactivate_id/, Loop/RejectedHypothesis/, Loop/Suppressed_hypothesis_id/, Loop/Visual_inliers/,
  Loop/Visual_inliers_distribution/, Loop/Visual_inliers_mean_dist/m, Loop/Visual_inliers_ratio/,
  Loop/Visual_matches/, Loop/Vp_hypothesis/, Memory/Database_memory_used/MB, Memory/Distance_travelled/m,
  Memory/Fast_movement/, Memory/Immunized_globally/, Memory/Immunized_locally/, Memory/Immunized_locally_max/,
  Memory/Local_graph_size/, Memory/New_landmark/, Memory/Odom_cache_links/, Memory/Odom_cache_poses/,
  Memory/Odometry_variance_ang/, Memory/Odometry_variance_lin/, Memory/Rehearsal_id/,
  Memory/Rehearsal_merged/, Memory/Rehearsal_sim/, Memory/Short_time_memory_size/,
  Memory/Signatures_removed/, Memory/Signatures_retrieved/, Memory/Small_movement/,
  Memory/Working_memory_size/, Proximity/Space_detections_added_icp_global/, Proximity/Space_detections_added_icp_multi/,
  Proximity/Space_detections_added_visually/, Proximity/Space_last_detection_id/,
  Proximity/Space_paths/, Proximity/Space_scan_paths_checked/, Proximity/Space_visual_paths_checked/,
  Proximity/Time_detections/, RtabmapROS/HasSubscribers/, RtabmapROS/TimeMsgConversion/ms,
  RtabmapROS/TimePublishing/ms, RtabmapROS/TimeRtabmap/ms, RtabmapROS/TimeTotal/ms,
  RtabmapROS/TimeUpdatingMaps/ms, Timing/Add_loop_closure_link/ms, Timing/Cleaning_neighbors/ms,
  Timing/Emptying_trash/ms, Timing/Finalizing_statistics/ms, Timing/Forgetting/ms,
  Timing/Hypotheses_creation/ms, Timing/Hypotheses_validation/ms, Timing/Joining_trash/ms,
  Timing/Likelihood_computation/ms, Timing/Map_optimization/ms, Timing/Memory_cleanup/ms,
  Timing/Memory_update/ms, Timing/Neighbor_link_refining/ms, Timing/Posterior_computation/ms,
  Timing/Proximity_by_space/ms, Timing/Proximity_by_space_visual/ms, Timing/Proximity_by_time/ms,
  Timing/Reactivation/ms, Timing/Statistics_creation/ms, Timing/Total/ms, TimingMem/Add_new_words/ms,
  TimingMem/Compressing_data/ms, TimingMem/Descriptors_extraction/ms, TimingMem/Joining_dictionary_update/ms,
  TimingMem/Keypoints_3D/ms, TimingMem/Keypoints_detection/ms, TimingMem/Occupancy_grid/ms,
  TimingMem/Pre_update/ms, TimingMem/Rehearsal/ms, TimingMem/Scan_filtering/ms, TimingMem/Signature_creation/ms]
statsValues: [184.0, 2750.0, 992360.0, 2691.0, 0.0, 0.0, 969.0, 0.02876228094100952, 0.0, 1.0, 0.0, 0.0, 0.0, 1154.0, 0.0, -0.0, 0.0, 0.0016019509639590979, -0.0006535534048452973, 7.013830661773682, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 969.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 217.0, 0.0, 0.0, 19.0, 0.0, 0.0, 50.0, 0.0, 0.0, 0.0, 0.0010000000474974513, 0.0010000000474974513, 0.0, 0.0, 0.2248803824186325, 9.0, 1.0, 0.0, 1.0, 41.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.7588348388671875, 0.03600120544433594, 95.42393493652344, 100.43883514404297, 0.2200603485107422, 0.0, 0.0, 12.756109237670898, 2.135038375854492, 0.0059604644775390625, 0.0, 0.0, 0.006198883056640625, 0.0, 0.010013580322265625, 0.6351470947265625, 74.1729736328125, 0.0, 0.0, 0.0030994415283203125, 0.0, 0.03600120544433594, 0.6358623504638672, 0.17595291137695312, 75.67810821533203, 14.655828475952148, 22.323131561279297, 6.239175796508789, 0.006198883056640625, 0.14781951904296875, 28.306007385253906, 1.8758773803710938, 0.0019073486328125, 0.19598007202148438, 0.2460479736328125, 73.933837890625]
localPath: []
currentGoalId: 0
odom_cache:
  header:
    seq: 0
    stamp:
      secs: 0
      nsecs:         0
    frame_id: ''
  mapToOdom:
    translation:
      x: 0.00160195096396
      y: -0.000653553404845
      z: 0.0
    rotation:
      x: -0.0
      y: -0.0
      z: -0.927028349242
      w: 0.374991252832
  posesId: []
  poses: []
  links: []
---
jetauto@jetauto-desktop:~$ rostopic list | grep cloud
/jetauto_1/rtabmap/cloud_ground
/jetauto_1/rtabmap/cloud_map
/jetauto_1/rtabmap/cloud_obstacles
jetauto@jetauto-desktop:~$ sed -n '1,200p' ~/jetauto_ws/src/jetauto_slam/launch/rviz_slam.launch
<?xml version="1.0"?>
<launch>
    <!--是否使用仿真-->
    <arg name="sim"         default="false"/>
    <arg name="robot_name"  default="$(env HOST)"/>

    <!--建图方法选择-->
    <arg name="slam_methods" default="gmapping" doc="slam type
    [gmapping, cartographer, hector, karto, frontier, explore, rrt_exploration, rtabmap]"/>

    <arg name="gmapping"        default="gmapping"/>
    <arg name="cartographer"    default="cartographer"/>
    <arg name="hector"          default="hector"/>
    <arg name="karto"           default="karto"/>
    <arg name="frontier"        default="frontier"/>
    <arg name="explore"         default="explore"/>
    <arg name="rrt_exploration" default="rrt_exploration"/>
    <arg name="rtabmap"         default="rtabmap"/>

    <group if="$(eval robot_name != '/')">
        <node     if="$(arg sim)" pkg="rviz" type="rviz" name="rviz" required="true" args="-d $(find jetauto_slam)/rviz/$(arg slam_methods)_sim.rviz"/>
        <node unless="$(arg sim)" pkg="rviz" type="rviz" name="rviz" required="true" args="-d $(find jetauto_slam)/rviz/$(arg slam_methods).rviz"/>
    </group>
    <group if="$(eval robot_name == '/')">
        <node     if="$(arg sim)" pkg="rviz" type="rviz" name="rviz" required="true" args="-d $(find jetauto_slam)/rviz/without_namesapce/$(arg slam_methods)_sim.rviz"/>
        <node unless="$(arg sim)" pkg="rviz" type="rviz" name="rviz" required="true" args="-d $(find jetauto_slam)/rviz/without_namespace/$(arg slam_methods).rviz"/>
    </group>
</launch>
jetauto@jetauto-desktop:~$ rostopic hz /jetauto_1/rtabmap/cloud_map
subscribed to [/jetauto_1/rtabmap/cloud_map]
average rate: 2.517
        min: 0.397s max: 0.397s std dev: 0.00000s window: 2
no new messages
average rate: 1.419
        min: 0.321s max: 1.395s std dev: 0.48917s window: 4
average rate: 2.140
        min: 0.246s max: 1.395s std dev: 0.38195s window: 8
average rate: 2.519
        min: 0.246s max: 1.395s std dev: 0.31898s window: 12
average rate: 2.589
        min: 0.246s max: 1.395s std dev: 0.29455s window: 14
average rate: 2.264
        min: 0.246s max: 1.395s std dev: 0.34725s window: 15
average rate: 2.385
        min: 0.246s max: 1.395s std dev: 0.31918s window: 18
average rate: 2.414
        min: 0.246s max: 1.395s std dev: 0.31090s window: 19
average rate: 2.238
        min: 0.246s max: 1.395s std dev: 0.34672s window: 22
average rate: 2.329
        min: 0.246s max: 1.395s std dev: 0.32795s window: 25
average rate: 2.414
        min: 0.246s max: 1.395s std dev: 0.31227s window: 28
average rate: 2.434
        min: 0.246s max: 1.395s std dev: 0.30719s window: 29
average rate: 2.244
        min: 0.246s max: 1.526s std dev: 0.35844s window: 31
average rate: 2.311
        min: 0.234s max: 1.526s std dev: 0.34465s window: 34
average rate: 2.345
        min: 0.234s max: 1.526s std dev: 0.33571s window: 36
no new messages
^Caverage rate: 2.185
        min: 0.234s max: 1.551s std dev: 0.37914s window: 37
jetauto@jetauto-desktop:~$ ls ~/jetauto_ws/src/jetauto_slam/rviz
cartographer.rviz      hector.rviz
cartographer_sim.rviz  hector_sim.rviz
explore_desktop.rviz   karto.rviz
explore.rviz           karto_sim.rviz
explore_sim.rviz       rrt_exploration.rviz
frontier.rviz          rrt_exploration_sim.rviz
frontier_sim.rviz      rtabmap.rviz
gmapping_desktop.rviz  rtabmap_sim.rviz
gmapping.rviz          without_namespace
gmapping_sim.rviz
jetauto@jetauto-desktop:~$
```
