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
