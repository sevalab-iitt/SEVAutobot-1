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

```
```
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

<img width="874" height="238" alt="image" src="https://github.com/user-attachments/assets/086700c1-6704-4d2d-b529-22d1f8b68dea" />

<img width="900" height="878" alt="image" src="https://github.com/user-attachments/assets/b7962f06-8451-4fff-b025-449c2d058074" />

<img width="912" height="138" alt="image" src="https://github.com/user-attachments/assets/1b3d733c-713b-4e3f-b677-7e7d1f960e47" />


<img width="852" height="602" alt="image" src="https://github.com/user-attachments/assets/7de81274-1413-4ba6-b24b-67a180347616" />


<img width="829" height="803" alt="image" src="https://github.com/user-attachments/assets/8f2ae198-ff14-4c72-8f39-b85bf2b22456" />


GitHub Markdown — Point Cloud Verification

You can paste this directly into your .md file:

## Point Cloud Verification

Before implementing point-cloud processing, the actual PointCloud2 message published by RTAB-Map was inspected on the JetAutoPro.

### RTAB-Map Point Cloud Topic

```text
/jetauto_1/rtabmap/cloud_map

Message type:

sensor_msgs/PointCloud2

The topic is published by:

/jetauto_1/rtabmap/rtabmap

This confirms that the RTAB-Map node is actively publishing the 3D map point cloud.

PointCloud2 Fields

The actual fields reported by the robot are:

Field	Offset	Datatype	Count
x	0 bytes	FLOAT32	1
y	4 bytes	FLOAT32	1
z	8 bytes	FLOAT32	1
rgb	16 bytes	FLOAT32	1

In ROS sensor_msgs/PointField, datatype 7 corresponds to FLOAT32.

Therefore, each point contains:

X
Y
Z
RGB

Conceptually:

P = (x, y, z, rgb)

The exact field layout was verified directly from the robot instead of being assumed.

Point Cloud Publication Rate

The following command was used:

rostopic hz /jetauto_1/rtabmap/cloud_map

Measured result:

average rate: 4.758 Hz
min: 0.165 s
max: 0.248 s
std dev: 0.01805 s
window: 48
Meaning of the Measurements
Average rate: 4.758 Hz
RTAB-Map published approximately 4.76 point-cloud messages per second.

Average interval:
Approximately:

1 / 4.758 ≈ 0.210 s

Therefore, a new point-cloud message arrived approximately every 210 ms on average.

Minimum interval: 0.165 s
The shortest observed time between two consecutive cloud messages was 165 ms.
Maximum interval: 0.248 s
The longest observed time between two consecutive cloud messages was 248 ms.
Standard deviation: 0.01805 s
The standard deviation of the message intervals was approximately 18 ms, indicating the amount of variation in the cloud publication timing.
Window: 48
The statistics were calculated using 48 received cloud messages.
Result

The RTAB-Map point-cloud topic is confirmed to be active and contains the required geometric information:

RTAB-Map
    ↓
/jetauto_1/rtabmap/cloud_map
    ↓
sensor_msgs/PointCloud2
    ↓
X + Y + Z + RGB

This provides the required 3D point representation for the next stage of the project.


## One thing we still need to verify

We have **not yet checked** the RTAB-Map cloud's:

- `width`
- `height`
- `point_step`
- `row_step`
- `is_dense`
- actual `frame_id`

We checked those for the Astra camera cloud, but **RTAB-Map's `cloud_map` can have a different structure**.

So let's finish this verification before writing the Python node.

Run:

```bash
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/header
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/width
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/height
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/point_step
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/row_step
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/is_dense

After these, we'll have the complete RTAB-Map PointCloud2 specification. Then we can finally write our first small Python program to extract actual (x, y, z, rgb) points.

this findings can you write me an .md for these also the height 1 and width etc what are those included. also the previuos ones too. 

Yes. We should document both sets of findings:

Astra camera PointCloud2 — all metadata we actually verified.
RTAB-Map /cloud_map — fields, publisher, rate, and the metadata we know so far.
Explain what height, width, point_step, row_step, is_dense, fields, offsets, datatype mean.
Clearly distinguish what is verified from what we have not checked yet.

You can paste this directly into GitHub as an .md file.

# Point Cloud Investigation

## 1. Objective

Before implementing point-cloud segmentation, the actual `sensor_msgs/PointCloud2` messages published by the Astra Pro Plus camera and RTAB-Map were inspected.

The purpose was to determine:

- Which point-cloud topics are available
- PointCloud2 message type
- Point-cloud dimensions
- Coordinate frame
- Available fields
- Field datatypes and offsets
- Point size
- Row size
- Whether invalid points are present
- RTAB-Map point-cloud publication rate

The point-cloud format was verified directly on the JetAutoPro instead of being assumed.

---

# 2. Astra Camera Point Cloud

The Astra camera was already running before RTAB-Map was launched.

The available point-cloud topics were:

```text
/astra_cam/depth/points
/astra_cam/depth_registered/points

Both topics were verified as:

sensor_msgs/PointCloud2

For the initial investigation, the registered point cloud was used:

/astra_cam/depth_registered/points
3. Astra PointCloud2 Publisher

Command:

rostopic info /astra_cam/depth_registered/points

Result:

Type: sensor_msgs/PointCloud2

Publishers:

- /astra_cam/astra_cam_nodelet_manager

Subscribers: None

This confirms that the Astra camera nodelet manager publishes the PointCloud2 data.

4. Astra PointCloud2 Header

Command:

rostopic echo -n 1 /astra_cam/depth_registered/points/header

Important result:

frame_id: "astra_cam_rgb_optical_frame"

Therefore, the point cloud is expressed in:

astra_cam_rgb_optical_frame

The header also contains:

seq
stamp
frame_id

The timestamp allows the point cloud to be associated with a particular moment in time.

5. Astra PointCloud2 Dimensions

The following values were verified:

height = 480
width  = 640

Therefore:

Total organized point positions = width × height

= 640 × 480

= 307,200

So the cloud contains up to:

307,200 point positions
5.1 What does width mean?

For an organized PointCloud2, width represents the number of points in each row.

In this case:

width = 640

This corresponds to the horizontal resolution of the camera.

Conceptually:

640 points per row
5.2 What does height mean?

For an organized PointCloud2, height represents the number of rows.

In this case:

height = 480

Therefore:

480 rows

The cloud can be thought of as a 2D grid:

             width = 640
       ┌──────────────────────┐
       │ • • • • • • • • • •  │
       │ • • • • • • • • • •  │
       │ • • • • • • • • • •  │
       │          ...         │
       │ • • • • • • • • • •  │
       └──────────────────────┘
              height = 480

This is called an organized point cloud.

The point at image position (u, v) can correspond to the 3D point generated from that camera pixel.

6. Astra PointCloud2 Fields

Command:

rostopic echo -n 1 /astra_cam/depth_registered/points/fields

Verified result:

- name: "x"
  offset: 0
  datatype: 7
  count: 1

- name: "y"
  offset: 4
  datatype: 7
  count: 1

- name: "z"
  offset: 8
  datatype: 7
  count: 1

- name: "rgb"
  offset: 16
  datatype: 7
  count: 1

Therefore, each point contains:

x
y
z
rgb

Conceptually:

P = (x, y, z, rgb)
7. Meaning of PointCloud2 Fields
7.1 X
name: x
offset: 0
datatype: 7

x represents the point's X coordinate.

7.2 Y
name: y
offset: 4
datatype: 7

y represents the point's Y coordinate.

7.3 Z
name: z
offset: 8
datatype: 7

z represents the point's Z coordinate/depth.

7.4 RGB
name: rgb
offset: 16
datatype: 7

The point cloud also contains RGB information.

The RGB field is stored using a 32-bit field represented by ROS as FLOAT32.

It should not be interpreted as an ordinary floating-point color value.

When processing the cloud in Python, the RGB field should be decoded appropriately.

8. What Does datatype: 7 Mean?

ROS sensor_msgs/PointField assigns numeric values to datatypes.

For this point cloud:

datatype = 7

means:

FLOAT32

Therefore:

x   → FLOAT32
y   → FLOAT32
z   → FLOAT32
rgb → FLOAT32 field representation

Each FLOAT32 occupies:

4 bytes
9. What Does offset Mean?

The offset specifies where a field starts inside one point's binary data.

The verified layout is:

x   → offset 0
y   → offset 4
z   → offset 8
rgb → offset 16

Therefore:

Point memory layout

Byte 0  ───── x
Byte 4  ───── y
Byte 8  ───── z
...
Byte 16 ───── rgb

There are unused/reserved bytes between some fields.

The complete size of one point is determined by:

point_step = 32 bytes
10. Astra Point Step

Command:

rostopic echo -n 1 /astra_cam/depth_registered/points/point_step

Result:

32

Therefore:

point_step = 32 bytes

point_step means:

The number of bytes occupied by one complete point.

So every point occupies:

32 bytes

even though the important fields are only:

x
y
z
rgb
11. Astra Row Step

Command:

rostopic echo -n 1 /astra_cam/depth_registered/points/row_step

Result:

20480

Therefore:

row_step = 20,480 bytes

This represents the number of bytes occupied by one complete row.

We can verify it:

row_step = width × point_step

         = 640 × 32

         = 20,480 bytes

The calculated value exactly matches the value reported by the robot.

12. Astra is_dense

Command:

rostopic echo -n 1 /astra_cam/depth_registered/points/is_dense

Result:

False

This is important.

is_dense: False means that the point cloud may contain invalid points.

For example, some points may contain:

NaN

or otherwise invalid coordinates.

Therefore, before performing clustering, invalid points must be removed.

Conceptually:

Raw Point Cloud
      ↓
Remove invalid XYZ
      ↓
Valid Point Cloud
      ↓
Clustering
13. Astra Point Cloud Summary
Property	Verified Value
Topic	/astra_cam/depth_registered/points
Type	sensor_msgs/PointCloud2
Frame	astra_cam_rgb_optical_frame
Width	640
Height	480
Point positions	307,200
Point step	32 bytes
Row step	20,480 bytes
Dense	False
X	FLOAT32, offset 0
Y	FLOAT32, offset 4
Z	FLOAT32, offset 8
RGB	FLOAT32 field, offset 16
14. RTAB-Map Point Cloud

After launching the RTAB-Map setup, the following topic became available:

/jetauto_1/rtabmap/cloud_map

The topic was verified using:

rostopic type /jetauto_1/rtabmap/cloud_map

Result:

sensor_msgs/PointCloud2

Therefore, RTAB-Map publishes its map cloud using the standard ROS PointCloud2 message.

15. RTAB-Map Point Cloud Publisher

Command:

rostopic info /jetauto_1/rtabmap/cloud_map

Result:

Type: sensor_msgs/PointCloud2

Publishers:

- /jetauto_1/rtabmap/rtabmap

Subscribers: None

This confirms that the RTAB-Map node itself is publishing the cloud.

16. RTAB-Map Point Cloud Publication Rate

Command:

rostopic hz /jetauto_1/rtabmap/cloud_map

Measured result:

average rate: 4.758
min: 0.165s
max: 0.248s
std dev: 0.01805s
window: 48
16.1 Average Rate
average rate = 4.758 Hz

This means RTAB-Map published approximately:

4.758 point-cloud messages per second

The approximate average interval is:

1 / 4.758
≈ 0.210 seconds

Therefore, a new cloud was published approximately every:

210 ms

on average.

16.2 Minimum Interval
min = 0.165 s

The shortest observed interval between two consecutive messages was:

165 ms
16.3 Maximum Interval
max = 0.248 s

The longest observed interval was:

248 ms
16.4 Standard Deviation
std dev = 0.01805 s

This is approximately:

18 ms

It represents the variation in the time interval between consecutive cloud messages.

A smaller standard deviation generally indicates more consistent timing.

16.5 Window
window = 48

This means the reported statistics were calculated using:

48 received messages
17. RTAB-Map PointCloud2 Fields

Command:

rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/fields

Verified result:

- name: "x"
  offset: 0
  datatype: 7
  count: 1

- name: "y"
  offset: 4
  datatype: 7
  count: 1

- name: "z"
  offset: 8
  datatype: 7
  count: 1

- name: "rgb"
  offset: 16
  datatype: 7
  count: 1

Therefore, the RTAB-Map cloud contains:

X
Y
Z
RGB

Conceptually:

P = (x, y, z, rgb)

This is exactly the type of information required for the planned geometric segmentation pipeline.

18. Camera Cloud vs RTAB-Map Cloud

The two point-cloud sources serve different purposes.

Astra Live Point Cloud
Astra Camera
      ↓
/astra_cam/depth_registered/points
      ↓
640 × 480 organized cloud
      ↓
Current camera view

This represents the current RGB-D camera observation.

RTAB-Map Map Cloud
Astra RGB-D
      ↓
RTAB-Map
      ↓
/jetauto_1/rtabmap/cloud_map
      ↓
3D map cloud

This represents the point cloud generated by RTAB-Map's mapping process.

Therefore, they should not automatically be treated as identical data sources.

19. Why cloud_map Is Important

The project eventually aims to perform:

3D Point Cloud
      ↓
Segmentation
      ↓
Object Clusters
      ↓
Object Geometry
      ↓
Distance / Gap Analysis

The RTAB-Map topic:

/jetauto_1/rtabmap/cloud_map

is therefore a potential input to the segmentation pipeline.

However, the exact dimensions and other metadata of the RTAB-Map cloud should still be inspected before implementing the processing node.

20. Important Difference: Width and Height

width and height do not necessarily mean the same thing for every PointCloud2 topic.

For the Astra cloud:

width = 640
height = 480

This is an organized camera-style point cloud:

640 × 480

For another PointCloud2 topic, such as an accumulated map cloud, it is possible for the structure to be different.

For example, a point cloud can conceptually have:

height = 1
width = N

This means:

N points

stored as a single row.

Therefore:

height = 1 does NOT mean that the point cloud contains only one point.

It means that the PointCloud2 is unorganized and contains one row containing width points.

For example:

height = 1
width = 100000

means approximately:

100,000 points

stored as:

1 × 100000

rather than:

480 × 640

This distinction is important when we write the Python point-cloud reader.

21. PointCloud2 Structure

A PointCloud2 message can be thought of as:

PointCloud2
│
├── Header
│   ├── timestamp
│   └── frame_id
│
├── height
│
├── width
│
├── fields
│   ├── x
│   ├── y
│   ├── z
│   └── rgb
│
├── point_step
│
├── row_step
│
├── data
│
└── is_dense

The important components for our project are:

Header
   ↓
Coordinate frame

Width / Height
   ↓
Point-cloud organization

Fields
   ↓
What information each point contains

Point Step
   ↓
Bytes per point

Row Step
   ↓
Bytes per row

Data
   ↓
Actual binary point data

is_dense
   ↓
Whether invalid points may exist
22. Current Verified Pipeline

At this stage, the verified system is:

Astra Pro Plus RGB-D Camera
          ↓
   RGB + Depth
          ↓
   Astra PointCloud2
          ↓
/astra_cam/depth_registered/points
          ↓
       RTAB-Map
          ↓
/jetauto_1/rtabmap/cloud_map
          ↓
    X + Y + Z + RGB

The next processing stage will be:

RTAB-Map PointCloud2
          ↓
Read actual points
          ↓
Remove invalid points
          ↓
Point-cloud visualization
          ↓
Euclidean clustering
23. Current Status
Verified
 Astra PointCloud2 exists
 Astra point-cloud topic identified
 Astra PointCloud2 message type verified
 Astra frame verified
 Astra width verified
 Astra height verified
 Astra X field verified
 Astra Y field verified
 Astra Z field verified
 Astra RGB field verified
 Astra point step verified
 Astra row step verified
 Astra is_dense verified
 RTAB-Map cloud_map exists
 RTAB-Map cloud_map message type verified
 RTAB-Map publisher verified
 RTAB-Map publication rate measured
 RTAB-Map X/Y/Z/RGB fields verified
Still to verify for RTAB-Map
 RTAB-Map width
 RTAB-Map height
 RTAB-Map point_step
 RTAB-Map row_step
 RTAB-Map is_dense
 RTAB-Map frame_id

These values should be obtained directly from:

rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/header
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/width
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/height
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/point_step
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/row_step
rostopic echo -n 1 /jetauto_1/rtabmap/cloud_map/is_dense
24. Next Development Step

Do not implement segmentation yet.

First create a small Python ROS subscriber that reads:

/jetauto_1/rtabmap/cloud_map

and extracts a few actual points:

(x, y, z, rgb)

The initial program should:

Subscribe to the PointCloud2 topic.
Read the actual fields.
Ignore invalid points.
Print a small number of valid points.
Display basic statistics such as the number of valid points.

After this is verified, the next stages will be:

PointCloud2
     ↓
Python Point Reader
     ↓
Raw 3D Points
     ↓
Visualization
     ↓
Euclidean Clustering
     ↓
Cluster Geometry
     ↓
Gap Detection
