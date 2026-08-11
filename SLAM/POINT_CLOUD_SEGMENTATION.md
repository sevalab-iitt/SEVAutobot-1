# 3D Point Cloud Segmentation and Object Separation

## 1. Problem Statement

The JetAuto robot uses an **Orbbec Astra Pro Plus RGB-D camera** and RTAB-Map to construct a 3D representation of its environment.

Currently, the system can generate a point cloud containing 3D points represented by:

- X coordinate
- Y coordinate
- Z coordinate
- RGB information (when available)

However, the raw point cloud does not inherently distinguish between different physical objects.

For example, if a chair and a table are present in the environment, the point cloud may contain points belonging to both objects without explicitly identifying them as separate entities.

The objective of this project is to develop a **3D point-cloud segmentation system** that can:

1. Separate physically distinct objects into different clusters.
2. Assign a unique ID to each detected cluster.
3. Determine the 3D coordinates of the points belonging to each cluster.
4. Calculate the centroid and bounding box of each cluster.
5. Measure the distance between different objects.
6. Detect gaps/free space between objects.
7. Provide information that can later be used for navigation.
8. Provide an interactive 3D visualization tool where individual points and segmented objects can be inspected.

Semantic identification such as:

> "This object is a chair."

is **not initially required**.

The initial objective is geometric understanding:

> "These points belong to Object 1, these points belong to Object 2, and there is a measurable gap between them."

---

# 2. Current System

The current robotics pipeline is:

```text
Orbbec Astra Pro Plus
        |
        v
   RGB + Depth
        |
        v
      ROS
        |
        v
    RTAB-Map
        |
        v
    Point Cloud
        |
        v
 Point Cloud Segmentation
        |
        v
 Object Clusters
        |
        v
 Object Geometry
        |
        v
 Navigation

<img width="450" height="660" alt="image" src="https://github.com/user-attachments/assets/e1232f39-12f5-46a9-b397-55f9c614f3a7" />

<img width="616" height="86" alt="image" src="https://github.com/user-attachments/assets/5c474089-649d-4b6d-92af-b100772c311f" />

``` t
jetauto@jetauto-desktop:~$ rostopic list | grep astra
/astra_cam/astra_cam_nodelet_manager/bond
/astra_cam/astraplus/parameter_descriptions
/astra_cam/astraplus/parameter_updates
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
/astra_cam/driver/parameter_descriptions
/astra_cam/driver/parameter_updates
/astra_cam/ir/camera_info
/astra_cam/ir/image
/astra_cam/ir/image/compressed
/astra_cam/ir/image/compressed/parameter_descriptions
/astra_cam/ir/image/compressed/parameter_updates
/astra_cam/ir/image/compressedDepth
/astra_cam/ir/image/compressedDepth/parameter_descriptions
/astra_cam/ir/image/compressedDepth/parameter_updates
/astra_cam/ir/image/theora
/astra_cam/ir/image/theora/parameter_descriptions
/astra_cam/ir/image/theora/parameter_updates
/astra_cam/projector/camera_info
/astra_cam/rgb/camera_info
/astra_cam/rgb/image_raw
/astra_cam/rgb/image_raw/compressed
/astra_cam/rgb/image_raw/compressed/parameter_descriptions
/astra_cam/rgb/image_raw/compressed/parameter_updates
/astra_cam/rgb/image_raw/compressedDepth
/astra_cam/rgb/image_raw/compressedDepth/parameter_descriptions
/astra_cam/rgb/image_raw/compressedDepth/parameter_updates
/astra_cam/rgb/image_raw/theora
/astra_cam/rgb/image_raw/theora/parameter_descriptions
/astra_cam/rgb/image_raw/theora/parameter_updates
/astra_cam/rgb/image_rect_color
/astra_cam/rgb/image_rect_color/compressed
/astra_cam/rgb/image_rect_color/compressed/parameter_descriptions
/astra_cam/rgb/image_rect_color/compressed/parameter_updates
/astra_cam/rgb/image_rect_color/compressedDepth
/astra_cam/rgb/image_rect_color/compressedDepth/parameter_descriptions
/astra_cam/rgb/image_rect_color/compressedDepth/parameter_updates
/astra_cam/rgb/image_rect_color/theora
/astra_cam/rgb/image_rect_color/theora/parameter_descriptions
/astra_cam/rgb/image_rect_color/theora/parameter_updates
/astra_cam/rgb_rectify_color/parameter_descriptions
/astra_cam/rgb_rectify_color/parameter_updates
```

