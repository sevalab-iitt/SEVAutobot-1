# JetAuto 3D Point Cloud Segmentation — Project Documentation

## 1. Overview

This project builds a 3D point-cloud processing and segmentation pipeline for the JetAuto robotics platform. The robot uses an **Orbbec Astra Pro Plus RGB-D camera** together with **RTAB-Map** to construct a 3D representation of its environment, but the raw point cloud produced by this pipeline does not distinguish between separate physical objects. If a chair and a table are both in view, their points are mixed together with no indication of which points belong to which object.

The goal of this project is to take that raw point cloud and turn it into a set of clearly separated, geometrically described objects. Specifically, the system should:

1. Separate physically distinct objects into different clusters.
2. Assign a unique ID to each detected cluster.
3. Determine the 3D coordinates of the points in each cluster.
4. Calculate the centroid and bounding box of each cluster.
5. Measure the distance between different objects.
6. Detect gaps or free space between objects.
7. Provide information that can later be used for navigation.
8. Provide an interactive 3D visualization tool for inspecting individual points and segmented objects.

At this stage, the project is **not** concerned with semantic labels such as "this is a chair." The goal is purely geometric: to establish that "these points belong to Object 1, these points belong to Object 2, and there is a measurable gap between them." Semantic identification can be added later.

### Target Pipeline

```text
Orbbec Astra Pro Plus
        │
        ▼
    RGB + Depth
        │
        ▼
        ROS
        │
        ▼
    RTAB-Map
        │
        ▼
   Point Cloud
        │
        ▼
Point Cloud Segmentation
        │
        ▼
  Object Clusters
        │
        ▼
  Object Geometry
        │
        ▼
   Navigation
```

---

## 2. Verifying the Point Cloud Data

Before writing any processing code, the actual `sensor_msgs/PointCloud2` messages produced by the Astra camera and by RTAB-Map were inspected directly on the robot. This ensured that the pipeline was built against the real message structure rather than assumptions.

### 2.1 Available Topics

Running `rostopic list | grep astra` confirmed that the Astra camera publishes a large number of topics, including two point-cloud topics of interest:

```text
/astra_cam/depth/points
/astra_cam/depth_registered/points
```

Both were confirmed to be of type `sensor_msgs/PointCloud2`. The registered cloud, `/astra_cam/depth_registered/points`, was used for the initial investigation because its depth data is aligned with the RGB image.

### 2.2 Understanding PointCloud2 Fields

A `PointCloud2` message packs each point's data into a fixed number of bytes, described by a set of **fields**. Each field has:

- **name** — what the value represents (e.g. `x`, `y`, `z`, `rgb`)
- **offset** — the byte position where the field starts within one point's data
- **datatype** — the numeric encoding used (datatype `7` corresponds to a 32-bit float, `FLOAT32`)
- **count** — how many values of that type the field holds (normally `1`)

The message also carries several structural properties:

| Property | Meaning |
|---|---|
| `height` | Number of rows in the cloud. For an organized, camera-style cloud this is the vertical pixel resolution. For an unorganized cloud (such as an accumulated map), `height` is `1`. |
| `width` | Number of points per row. For an organized cloud this is the horizontal pixel resolution. For an unorganized cloud, `width` is the total number of points. |
| `point_step` | Number of bytes used to store one complete point. |
| `row_step` | Number of bytes used to store one complete row (`width × point_step`). |
| `is_dense` | `True` if every point has valid coordinates; `False` if the cloud may contain invalid points such as `NaN`. |
| `data` | The raw binary buffer containing all point values. |

**Important distinction:** `height = 1` does not mean the cloud contains only one point. It means the cloud is *unorganized* — stored as a single row containing `width` points. For example, `height = 1, width = 100000` describes roughly 100,000 points stored in one row, as opposed to a `480 × 640` organized grid.

### 2.3 Astra Camera Point Cloud — Verified Metadata

Using `rostopic echo` on the header, fields, and structural properties, the following was confirmed for `/astra_cam/depth_registered/points`:

| Property | Verified Value |
|---|---|
| Topic | `/astra_cam/depth_registered/points` |
| Message type | `sensor_msgs/PointCloud2` |
| Frame | `astra_cam_rgb_optical_frame` |
| Width | 640 |
| Height | 480 |
| Total point positions | 307,200 (640 × 480) |
| Point step | 32 bytes |
| Row step | 20,480 bytes (640 × 32) |
| Dense | `False` |
| x | FLOAT32, offset 0 |
| y | FLOAT32, offset 4 |
| z | FLOAT32, offset 8 |
| rgb | FLOAT32-encoded, offset 16 |

Since `is_dense` is `False`, some points may contain `NaN` or otherwise invalid coordinates. These must be filtered out before clustering:

```text
Raw Point Cloud → Remove Invalid XYZ → Valid Point Cloud → Clustering
```

The `rgb` field, although stored as a 32-bit float, is not a plain color value — it is a packed representation that needs to be decoded correctly when read in Python.

### 2.4 RTAB-Map Point Cloud — Verified Metadata

RTAB-Map publishes its own accumulated map cloud on:

```text
/jetauto_1/rtabmap/cloud_map
```

This is a separate data source from the live Astra feed: the Astra topic reflects the camera's *current* view, while the RTAB-Map topic reflects the *accumulated 3D map* built from mapping over time. The two should not be treated as interchangeable.

Verification steps and results:

- **Message type** (`rostopic type`): `sensor_msgs/PointCloud2`
- **Publisher** (`rostopic info`): published by `/jetauto_1/rtabmap/rtabmap`
- **Publish rate** (`rostopic hz`):

  ```text
  average rate: 4.758 Hz
  min: 0.165 s
  max: 0.248 s
  std dev: 0.01805 s
  window: 48
  ```

  This means a new map cloud arrived roughly every 210 ms on average (1 / 4.758 ≈ 0.210 s), with the fastest interval at 165 ms and the slowest at 248 ms. The 18 ms standard deviation indicates the timing was reasonably consistent, and the statistics were computed over 48 received messages.

- **Fields** (`rostopic echo .../fields`): `x`, `y`, `z`, `rgb`, each `FLOAT32`, at the same offsets as the Astra cloud (0, 4, 8, 16).

A later, more complete check of the RTAB-Map cloud's structural fields returned:

```text
Frame ID  : jetauto_1/map
Width     : 76
Height    : 1
Fields    : x, y, z, rgb
Point step: 32
Row step  : 2432
Dense     : True
```

This confirmed the RTAB-Map cloud is an *unorganized* cloud (`height = 1`) containing 76 points at that particular moment, and that it was reported as fully dense (`is_dense = True`).

### 2.5 Summary of Verified Data

Both the Astra camera cloud and RTAB-Map map cloud provide the fields required for geometric segmentation:

```text
P = (x, y, z, rgb)
```

with the key structural difference being that the Astra cloud is a large, organized 640×480 grid captured live, while the RTAB-Map cloud is a smaller, unorganized accumulated map.

---

## 3. Development Roadmap

The project was broken into incremental, independently verifiable phases:

```text
Phase 1 — Read raw PointCloud2 data
Phase 2 — Remove invalid points
Phase 3 — Downsample the cloud
Phase 4 — Euclidean clustering
Phase 5 — Cluster geometry (centroid, bounding box)
Phase 6 — Distance / gap detection
Phase 7 — Interactive 3D viewer
Phase 8 — Compare against DBSCAN, region growing, supervoxels
Phase 9 — Explore SAM + depth for semantic segmentation
```

### ROS Environment

```text
ROS version         : 1.14.13 (Melodic)
Python (ROS/catkin)  : 2.7.17
Python 3 (available) : 3.6.9
```

The project package was created with:

```bash
cd ~/catkin_ws/src
catkin_create_pkg pointcloud_segmentation rospy sensor_msgs
```

and built and sourced in the usual way:

```bash
cd ~/catkin_ws
catkin_make
source ~/catkin_ws/devel/setup.bash
```

---

## 4. Phase 1 — Reading the Point Cloud

A ROS node, `pointcloud_reader.py`, was created at:

```text
~/catkin_ws/src/pointcloud_segmentation/scripts/pointcloud_reader.py
```

The node subscribes to a `PointCloud2` topic, prints the cloud's metadata (frame, width, height, fields, point step, row step, density), and prints the first ten points using `sensor_msgs.point_cloud2.read_points()`. To keep the initial test simple, it processes only the first message received and ignores all subsequent ones.

Running the node against `/jetauto_1/rtabmap/cloud_map` confirmed that real `(x, y, z, rgb)` values could be read successfully, completing Phase 1.

---

## 5. Phase 2 — Removing Invalid Points

Since the Astra cloud is not guaranteed to be dense, the reader was extended to check every point's `x`, `y`, and `z` values for `NaN` or infinity before accepting it. Because the ROS Melodic environment uses Python 2.7, which lacks `math.isfinite()`, the check was implemented using `math.isnan()` and `math.isinf()` on each coordinate individually.

Points that fail this check are discarded; all others are counted as valid. Running the updated node against the RTAB-Map cloud produced:

```text
Total points  : 818
Valid XYZ     : 818
Invalid XYZ   : 0
```

The `rgb` field itself sometimes contained `NaN`, but this did not disqualify a point, since only the geometric coordinates matter for this stage of the project. This completed Phase 2.

---

## 6. Phase 3 — Voxel Downsampling

Processing the full 640×480 (307,200-point) Astra cloud on every frame is computationally expensive, so a voxel-grid downsampling step was added before any further processing.

**How it works:** the 3D space is divided into cubic voxels of a fixed size. All points falling inside the same voxel are replaced by a single representative point — the average (centroid) of that voxel's points. This preserves the overall shape of the cloud while dramatically reducing the point count.

The current voxel size is:

```text
0.02 m (2 cm)
```

A representative run against the live Astra cloud produced:

```text
Frame ID   : camera_rgb_optical_frame
Width      : 640
Height     : 480
Fields     : x, y, z
Point step : 16
Row step   : 10240
Dense      : False

Total points  : 307,200
Valid XYZ     : 252,836
Invalid XYZ   : 54,364

Original valid points : 252,836
Downsampled points    : 7,229
Point reduction        : 97.14%
```

This is a substantial reduction — from roughly a quarter-million points down to about seven thousand — while retaining the overall spatial structure of the scene. This completed Phase 3.

---

## 7. Phase 4 — Euclidean Clustering

With a manageable number of points available, the next step was to group them into clusters representing distinct objects. This was implemented using `sklearn.neighbors.NearestNeighbors` (scikit-learn version `0.19.1`, confirmed available in the environment).

### 7.1 Algorithm

For each point, all neighboring points within a fixed radius (the *cluster tolerance*) are found. Starting from an unvisited point, the algorithm expands outward through connected neighbors — similar to a flood fill — marking points as visited and grouping them into a single cluster. This continues until no more connected points remain, at which point the next unvisited point starts a new cluster. Clusters outside a configured size range are discarded as either noise (too small) or merged background (too large).

### 7.2 Parameters

```text
Cluster tolerance     : 0.05 m (5 cm) — maximum distance for two points to be considered connected
Minimum cluster size   : 20 points   — smaller groups are treated as noise
Maximum cluster size   : 5000 points — larger groups are excluded
```

### 7.3 Results

A representative run on 7,079 downsampled points produced:

```text
Number of clusters : 9

Cluster 1 : 3,912 points
Cluster 2 : 1,783 points
Cluster 3 :   184 points
Cluster 4 :   286 points
Cluster 5 :   196 points
Cluster 6 :   194 points
Cluster 7 :   206 points
Cluster 8 :   218 points
Cluster 9 :    76 points

Clustered points  : 7,055
Noise/unclustered : 24

Largest cluster   : 3,912
Smallest cluster  : 76
Average cluster   : 783.89
```

This confirmed that the pipeline could successfully separate a downsampled cloud into distinct, connected regions, completing Phase 4.

**Note on variability:** later runs on different scenes produced noticeably different cluster counts and sizes (for example, one run found 4 clusters from 10,749 points, with over 10,000 points classified as noise). This is expected — Euclidean clustering results depend heavily on the actual scene geometry, not just the algorithm parameters — and is treated as an observation for later experimental analysis rather than a bug.

---

## 8. Phase 5 — Cluster Geometry Analysis

Once clusters are identified, each one is analyzed to extract useful geometric properties: point count, centroid, axis-aligned bounding box, and overall dimensions.

- **Centroid** — the mean X, Y, and Z coordinate of all points in the cluster; an approximate center point.
- **Bounding box** — the minimum and maximum X, Y, and Z values within the cluster.
- **Dimensions** — the width, depth, and height of the bounding box:

  ```text
  Width  = Max X − Min X
  Depth  = Max Y − Min Y
  Height = Max Z − Min Z
  ```

### Example Results

A verified run produced four clusters with the following geometry (all values in the camera coordinate frame):

**Cluster 1** — 196 points
Centroid: (−0.023, 0.195, 0.684) m · Bounds: X [−0.190, 0.146], Y [−0.029, 0.285], Z [0.637, 0.730] · Dimensions: 0.336 × 0.314 × 0.093 m

**Cluster 2** — 154 points
Centroid: (0.133, 0.204, 1.755) m · Bounds: X [0.029, 0.246], Y [0.126, 0.284], Z [1.714, 1.795] · Dimensions: 0.217 × 0.159 × 0.081 m

**Cluster 3** — 258 points
Centroid: (0.312, 0.212, 1.075) m · Bounds: X [0.156, 0.501], Y [0.056, 0.423], Z [1.037, 1.128] · Dimensions: 0.345 × 0.368 × 0.091 m

**Cluster 4** — 93 points
Centroid: (0.331, 0.230, 0.879) m · Bounds: X [0.277, 0.446], Y [0.139, 0.349], Z [0.863, 0.902] · Dimensions: 0.168 × 0.211 × 0.040 m

This moved the project from simply detecting *how many* clusters exist to describing *where* each one is and *how large* it is — geometric information that can later support navigation and gap detection. This completed Phase 5.

---

## 9. Camera Performance Check

To make sure the live camera feed itself was healthy, its publish rate was checked separately:

```bash
rostopic hz /jetauto_1/camera/depth/points
```

This measured a steady rate of approximately **24–25 Hz**. This confirmed that when the segmentation node appeared to stop producing new output, the camera itself was not at fault — the node was intentionally written to process only the first received frame (`if self.received: return`), so the camera continued streaming at full rate in the background while the segmentation logic ran once.

---

## 10. Phase 6 — Colored Cluster Output

To prepare for visualization, a second publisher was added that outputs the segmented, colored cloud on a new topic:

```text
/pointcloud_segmentation/clusters   (sensor_msgs/PointCloud2)
```

Each accepted cluster is assigned a distinct RGB color so that clusters can be told apart visually. In one verified run, the published cloud contained 678 colored points, and the topic was confirmed to be active using `rostopic list`, `rostopic info`, and `rostopic echo -n 1 .../fields` (returning `x`, `y`, `z`, `rgb` as expected).

---

## 11. Phase 7 — RViz Visualization (In Progress)

### 11.1 Display Requirement

The processing stages up to this point can all be run over SSH. RViz, however, requires a graphical display, so this stage uses the robot's main display.

### 11.2 Fixed Frame

The live Astra cloud is published in the `camera_rgb_optical_frame`. An early attempt to visualize the cloud with RViz's Fixed Frame set to `map` failed, because that TF frame was not available in the current setup. Changing the Fixed Frame to `camera_rgb_optical_frame` resolved the mismatch.

### 11.3 Current Status

The segmented cloud display was added via **Add → By topic → `/pointcloud_segmentation/clusters` → PointCloud2**, configured with:

```text
Style             : Points
Size              : 3
Color Transformer : RGB8
```

However, the Color Transformer field currently appears blank in RViz, which suggests the published RGB field needs further verification for compatibility with this ROS Melodic/RViz environment. **This is the current unresolved item in the pipeline.**

Recommended next diagnostic steps:

```bash
rostopic type /pointcloud_segmentation/clusters
rostopic echo -n 1 /pointcloud_segmentation/clusters/fields
rostopic hz /pointcloud_segmentation/clusters
```

The last check is expected to show that the topic is not continuously publishing, since the node currently processes only one frame — continuous publishing is planned as the next implementation improvement.

---

## 12. Current Verified Architecture

```text
                Astra RGB-D Camera
                        │
                        ▼
        /jetauto_1/camera/depth/points
                        │
                        ▼
             sensor_msgs/PointCloud2
                        │
                        ▼
              Read XYZ coordinates
                        │
                        ▼
               Remove invalid XYZ
                        │
                        ▼
                 NumPy array
                        │
                        ▼
              Voxel Downsampling
                 (voxel = 0.02 m)
                        │
                        ▼
              ~7,000–11,000 points
                        │
                        ▼
            Euclidean Clustering
              (tolerance = 0.05 m)
                        │
                        ▼
                  Clusters
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
       Cluster Geometry       Colored Cloud
       • centroid              • XYZ
       • bounding box          • RGB
       • dimensions                  │
             │                        ▼
             │           /pointcloud_segmentation/clusters
             │                        │
             └────────────────────────┤
                                       ▼
                                     RViz
```

---

## 13. Current Parameters

| Parameter | Current Value |
|---|---:|
| Camera resolution | 640 × 480 |
| Raw points per frame | 307,200 |
| Voxel size | 0.020 m |
| Cluster tolerance | 0.050 m |
| Minimum cluster size | 20 points |
| Maximum cluster size | 5,000 points |
| Camera frame | `camera_rgb_optical_frame` |
| Input topic | `/jetauto_1/camera/depth/points` |
| Output topic | `/pointcloud_segmentation/clusters` |
| ROS distribution | Melodic |
| Python version | 2.7.17 |
| scikit-learn version | 0.19.1 |

---

## 14. Key Findings

1. **Point cloud acquisition works reliably.** The Astra RGB-D camera publishes valid `PointCloud2` data at roughly 24–25 Hz.
2. **A substantial fraction of raw points are invalid.** In one representative frame, of 307,200 possible points, only 188,592 had valid coordinates (about 61% valid, 39% invalid) — a ratio that varies frame to frame and must always be filtered before further processing.
3. **Voxel downsampling is highly effective.** A 2 cm voxel size reduced point counts by roughly 94–97% across tested frames, making downstream clustering computationally practical.
4. **Euclidean clustering successfully separates distinct regions**, but its output is strongly scene-dependent: one test produced 9 clusters from 7,079 points with only 24 points of noise, while another produced just 4 clusters from 10,706 points with over 10,000 points left unclustered. This sensitivity to scene content is an expected characteristic of the algorithm and is being treated as a subject for future experimental comparison rather than a defect.
5. **Per-cluster geometry can be reliably extracted**, giving each detected object a point count, centroid, bounding box, and dimensions — moving the pipeline beyond simple detection toward information usable for localization and navigation.

---

## 15. Project Status

| Phase | Status |
|---|---|
| 1 — ROS / PointCloud2 verification | Complete |
| 2 — PointCloud2 reader | Complete |
| 3 — Invalid point removal | Complete |
| 4 — NumPy conversion | Complete |
| 5 — Voxel downsampling | Complete |
| 6 — Euclidean clustering | Complete |
| 7 — Cluster geometry analysis | Complete |
| 8 — Colored cluster publisher | Implemented |
| 9 — RViz visualization | In progress |

**Immediate next step:** resolve the blank Color Transformer field in RViz for the `/pointcloud_segmentation/clusters` topic, using the diagnostic commands listed in Section 11.3, then extend the publisher to run continuously rather than on a single frame.

---

## 16. Research Direction

Beyond the working implementation, this project is being developed as a potential research contribution. A candidate research question is:

> How can lightweight geometric point-cloud segmentation be optimized for real-time RGB-D perception on resource-constrained edge robotic hardware?

The current Euclidean clustering implementation serves as the **baseline method** for a planned comparative study against:

1. Euclidean Clustering (baseline)
2. DBSCAN
3. Region Growing
4. Supervoxel-based segmentation

### Planned Evaluation Metrics

```text
Processing time          Number of clusters
Segmentation FPS          Noise percentage
Input FPS                 Cluster size
CPU utilization            Cluster dimensions
RAM usage                  Segmentation quality
```

### Planned Parameter Sweeps

- **Voxel size:** 0.01 m, 0.02 m, 0.03 m, 0.05 m
- **Euclidean tolerance:** 0.03 m, 0.05 m, 0.07 m, 0.10 m

The same scenes will be used across all parameter combinations and algorithms to keep results comparable.

```text
                 Point Cloud
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Euclidean     DBSCAN    Region Growing
      Clustering
          │           │           │
          └───────────┼───────────┘
                      ▼
              Compare Results
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       Runtime     Clusters     Quality
          │           │           │
          └───────────┼───────────┘
                      ▼
              Edge-Robot Analysis
```

---

## 17. Repository Structure

```text
catkin_ws/
└── src/
    └── pointcloud_segmentation/
        ├── package.xml
        ├── CMakeLists.txt
        └── scripts/
            └── pointcloud_reader.py
```

The script implements the full pipeline in sequence:

```text
PointCloud2 subscriber
        ↓
Invalid point filtering
        ↓
NumPy conversion
        ↓
Voxel downsampling
        ↓
Euclidean clustering
        ↓
Cluster analysis
        ↓
Colored PointCloud2 publisher
```

---

## 18. Reproducibility Commands

**Build and source the workspace:**

```bash
cd ~/catkin_ws
catkin_make
source ~/catkin_ws/devel/setup.bash
```

**Make the script executable:**

```bash
chmod +x ~/catkin_ws/src/pointcloud_segmentation/scripts/pointcloud_reader.py
```

**Run the segmentation node:**

```bash
rosrun pointcloud_segmentation pointcloud_reader.py
```

**Verify the input cloud:**

```bash
rostopic type /jetauto_1/camera/depth/points
rostopic hz /jetauto_1/camera/depth/points
```

**Verify the segmented output cloud:**

```bash
rostopic type /pointcloud_segmentation/clusters
rostopic info /pointcloud_segmentation/clusters
rostopic hz /pointcloud_segmentation/clusters
rostopic echo -n 1 /pointcloud_segmentation/clusters/fields
```

---

## 19. Summary

The project has progressed from raw RGB-D point-cloud acquisition to geometric object segmentation. The verified pipeline is:

```text
Astra RGB-D
    ↓
ROS PointCloud2
    ↓
Invalid XYZ removal
    ↓
NumPy conversion
    ↓
2 cm voxel downsampling
    ↓
5 cm Euclidean clustering
    ↓
Cluster geometry analysis
    ↓
Colored PointCloud2
    ↓
RViz visualization (in progress)
```

The core computational stages — acquisition, filtering, downsampling, clustering, and geometry extraction — are complete and verified. The remaining task is to make the colored PointCloud2 output fully compatible with RViz's color transformer and achieve stable visualization. Once that is resolved, the project can move on to systematic parameter evaluation and a comparison against alternative segmentation algorithms such as DBSCAN and region growing.
