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
```
---
```
PHASE 1
RTAB-Map PointCloud2
        ↓
Python Point Reader
        ↓
Actual (X, Y, Z, RGB)
        ↓
Verify
        │
        ▼
PHASE 2
Remove Invalid Points
        ↓
Valid XYZ points
        ↓
Verify
        │
        ▼
PHASE 3
Downsampling
        ↓
Reduced point cloud
        ↓
Verify
        │
        ▼
PHASE 4
Euclidean Clustering
        ↓
Cluster 1
Cluster 2
Cluster 3
...
        │
        ▼
PHASE 5
Cluster Geometry
        ↓
Centroid
Bounding Box
Dimensions
        │
        ▼
PHASE 6
Distance / Gap Detection
        │
        ▼
PHASE 7
Interactive 3D Viewer
        │
        ▼
PHASE 8
Compare
DBSCAN
Region Growing
Supervoxels
        │
        ▼
PHASE 9
SAM + Depth
```
---
cd ~/catkin_ws/src/pointcloud_segmentation/scripts
nano pointcloud_reader.py (inside put this code initially)
for reader used this code 
```
#!/usr/bin/env python

import rospy
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2


class PointCloudReader:

    def __init__(self):

        self.subscriber = rospy.Subscriber(
            "/jetauto_1/rtabmap/cloud_map",
            PointCloud2,
            self.pointcloud_callback,
            queue_size=1
        )

        self.received = False

    def pointcloud_callback(self, msg):

        if self.received:
            return

        self.received = True

        rospy.loginfo("Received PointCloud2")

        print("\n========== POINT CLOUD INFO ==========")

        print("Frame ID :", msg.header.frame_id)
        print("Width    :", msg.width)
        print("Height   :", msg.height)
        print("Fields   :", [field.name for field in msg.fields])
        print("Point step:", msg.point_step)
        print("Row step  :", msg.row_step)
        print("Dense     :", msg.is_dense)

        print("\n========== FIRST 10 POINTS ==========")

        count = 0

        for point in pc2.read_points(
                msg,
                field_names=("x", "y", "z", "rgb"),
                skip_nans=False):

            print(
                "Point {}: X={:.4f}, Y={:.4f}, Z={:.4f}, RGB={}".format(
                    count,
                    point[0],
                    point[1],
                    point[2],
                    point[3]
                )
            )

            count += 1

            if count >= 10:
                break

        print("\n=====================================\n")


def main():

    rospy.init_node(
        "pointcloud_reader",
        anonymous=True
    )

    PointCloudReader()

    rospy.spin()


if __name__ == "__main__":
    main()
```
phase 1 completed 

<img width="954" height="817" alt="image" src="https://github.com/user-attachments/assets/0fcb97ca-a0c0-4b6b-8e82-bdc1bd3bb348" />
---
for phase 2 

we have to make some changes as we are going to remove those invalid points that we intentionally let slide in.

nano ~/catkin_ws/src/pointcloud_segmentation/scripts/pointcloud_reader.py

```
#!/usr/bin/env python

import rospy
import math
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2


class PointCloudReader:

    def __init__(self):

        self.subscriber = rospy.Subscriber(
            "/jetauto_1/rtabmap/cloud_map",
            PointCloud2,
            self.pointcloud_callback,
            queue_size=1
        )

        self.received = False

    def pointcloud_callback(self, msg):

        # Process only the first received message
        if self.received:
            return

        self.received = True

        rospy.loginfo("Received PointCloud2")

        # -----------------------------------------
        # Point Cloud Information
        # -----------------------------------------

        print("\n========== POINT CLOUD INFO ==========")

        print("Frame ID :", msg.header.frame_id)
        print("Width    :", msg.width)
        print("Height   :", msg.height)

        print(
            "Fields   :",
            [field.name for field in msg.fields]
        )

        print("Point step:", msg.point_step)
        print("Row step  :", msg.row_step)
        print("Dense     :", msg.is_dense)

        # -----------------------------------------
        # Point Cloud Processing
        # -----------------------------------------

        print("\n========== POINT CLOUD PROCESSING ==========")

        total_points = 0
        valid_points = 0
        invalid_points = 0

        sample_count = 0

        # Read individual points from PointCloud2
        for point in pc2.read_points(
                msg,
                field_names=("x", "y", "z", "rgb"),
                skip_nans=False):

            total_points += 1

            x = point[0]
            y = point[1]
            z = point[2]
            rgb = point[3]

            # -----------------------------------------
            # Check XYZ validity
            #
            # Python 2.7 does not have math.isfinite().
            # Therefore check NaN and infinity separately.
            # -----------------------------------------

            if (
                math.isnan(x) or math.isinf(x) or
                math.isnan(y) or math.isinf(y) or
                math.isnan(z) or math.isinf(z)
            ):

                invalid_points += 1
                continue

            # Point has valid XYZ
            valid_points += 1

            # Print only first 10 valid points
            if sample_count < 10:

                print(
                    "Valid Point {}: "
                    "X={:.4f}, "
                    "Y={:.4f}, "
                    "Z={:.4f}, "
                    "RGB={}".format(
                        sample_count,
                        x,
                        y,
                        z,
                        rgb
                    )
                )

                sample_count += 1

        # -----------------------------------------
        # Statistics
        # -----------------------------------------

        print("\n========== POINT STATISTICS ==========")

        print("Total points   :", total_points)
        print("Valid XYZ      :", valid_points)
        print("Invalid XYZ    :", invalid_points)

        print("======================================\n")


def main():

    # Initialize ROS node
    rospy.init_node(
        "pointcloud_reader",
        anonymous=True
    )

    # Create subscriber
    PointCloudReader()

    # Keep node running
    rospy.spin()


if __name__ == "__main__":
    main()
```
Ctrl + O
Enter
Ctrl + X

run it using 

chmod +x ~/catkin_ws/src/pointcloud_segmentation/scripts/pointcloud_reader.py
source ~/catkin_ws/devel/setup.bash
rosrun pointcloud_segmentation pointcloud_reader.py

<img width="930" height="670" alt="image" src="https://github.com/user-attachments/assets/0feff709-d6a9-41f1-9670-e09d4943c9a7" />

phase 2 is completed 

So for this particular RTAB-Map cloud:

818 points received
818 have valid X/Y/Z
0 invalid XYZ points
RGB = nan is present, but we're correctly not rejecting points because of RGB, since we're doing geometric segmentation.
---

phase 3 - Downsampling 
need to change the code again
nano ~/catkin_ws/src/pointcloud_segmentation/scripts/pointcloud_reader.py

```
#!/usr/bin/env python

import rospy
import math
import numpy as np

import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2


class PointCloudReader:

    def __init__(self):

        self.subscriber = rospy.Subscriber(
            "/jetauto_1/camera/depth/points",
            PointCloud2,
            self.pointcloud_callback,
            queue_size=1
        )

        self.received = False

    def voxel_downsample(self, points, voxel_size):

        """
        Voxel-grid downsampling.

        Points are grouped into 3D voxels.
        One representative point (centroid) is
        calculated for each occupied voxel.
        """

        if len(points) == 0:
            return points

        # Calculate voxel coordinates
        voxel_indices = np.floor(
            points / voxel_size
        ).astype(np.int32)

        # Find unique voxels
        unique_voxels, inverse_indices = np.unique(
            voxel_indices,
            axis=0,
            return_inverse=True
        )

        # Allocate array for downsampled points
        downsampled = np.zeros(
            (len(unique_voxels), 3),
            dtype=np.float32
        )

        # Calculate centroid of each voxel
        for i in range(len(unique_voxels)):

            voxel_points = points[
                inverse_indices == i
            ]

            downsampled[i] = np.mean(
                voxel_points,
                axis=0
            )

        return downsampled

    def pointcloud_callback(self, msg):

        # Process only the first received cloud
        if self.received:
            return

        self.received = True

        rospy.loginfo(
            "Received Astra PointCloud2"
        )

        # ==================================================
        # POINT CLOUD INFORMATION
        # ==================================================

        print("\n========== POINT CLOUD INFO ==========")

        print(
            "Topic    : /jetauto_1/camera/depth/points"
        )

        print(
            "Frame ID :",
            msg.header.frame_id
        )

        print(
            "Width    :",
            msg.width
        )

        print(
            "Height   :",
            msg.height
        )

        print(
            "Fields   :",
            [field.name for field in msg.fields]
        )

        print(
            "Point step:",
            msg.point_step
        )

        print(
            "Row step  :",
            msg.row_step
        )

        print(
            "Dense     :",
            msg.is_dense
        )

        # ==================================================
        # READ AND VALIDATE POINTS
        # ==================================================

        print(
            "\n========== READING POINTS =========="
        )

        points = []

        total_points = 0
        invalid_points = 0

        for point in pc2.read_points(
                msg,
                field_names=("x", "y", "z"),
                skip_nans=False):

            total_points += 1

            x = point[0]
            y = point[1]
            z = point[2]

            # Python 2.7 compatible validity check
            if (
                math.isnan(x) or math.isinf(x) or
                math.isnan(y) or math.isinf(y) or
                math.isnan(z) or math.isinf(z)
            ):
                invalid_points += 1
                continue

            points.append(
                [x, y, z]
            )

        # ==================================================
        # NUMPY ARRAY
        # ==================================================

        points = np.array(
            points,
            dtype=np.float32
        )

        valid_points = len(points)

        print(
            "Total points   :",
            total_points
        )

        print(
            "Valid XYZ      :",
            valid_points
        )

        print(
            "Invalid XYZ    :",
            invalid_points
        )

        if valid_points == 0:

            rospy.logwarn(
                "No valid XYZ points were found."
            )

            return

        # ==================================================
        # ORIGINAL CLOUD INFORMATION
        # ==================================================

        print(
            "\n========== ORIGINAL CLOUD =========="
        )

        print(
            "Array shape :",
            points.shape
        )

        print(
            "Array dtype :",
            points.dtype
        )

        # ==================================================
        # ORIGINAL BOUNDS
        # ==================================================

        min_x = np.min(points[:, 0])
        max_x = np.max(points[:, 0])

        min_y = np.min(points[:, 1])
        max_y = np.max(points[:, 1])

        min_z = np.min(points[:, 2])
        max_z = np.max(points[:, 2])

        print(
            "X range : {:.4f} m".format(
                max_x - min_x
            )
        )

        print(
            "Y range : {:.4f} m".format(
                max_y - min_y
            )
        )

        print(
            "Z range : {:.4f} m".format(
                max_z - min_z
            )
        )

        # ==================================================
        # VOXEL DOWNSAMPLING
        # ==================================================

        voxel_size = 0.02

        print(
            "\n========== VOXEL DOWNSAMPLING =========="
        )

        print(
            "Voxel size : {:.3f} m".format(
                voxel_size
            )
        )

        downsampled_points = self.voxel_downsample(
            points,
            voxel_size
        )

        downsampled_count = len(
            downsampled_points
        )

        # ==================================================
        # DOWNSAMPLING RESULTS
        # ==================================================

        print(
            "Original valid points :",
            valid_points
        )

        print(
            "Downsampled points    :",
            downsampled_count
        )

        reduction = (
            1.0 -
            float(downsampled_count) /
            float(valid_points)
        ) * 100.0

        print(
            "Point reduction       : {:.2f}%".format(
                reduction
            )
        )

        # ==================================================
        # DOWNSAMPLED BOUNDS
        # ==================================================

        print(
            "\n========== DOWNSAMPLED BOUNDS =========="
        )

        down_min_x = np.min(
            downsampled_points[:, 0]
        )

        down_max_x = np.max(
            downsampled_points[:, 0]
        )

        down_min_y = np.min(
            downsampled_points[:, 1]
        )

        down_max_y = np.max(
            downsampled_points[:, 1]
        )

        down_min_z = np.min(
            downsampled_points[:, 2]
        )

        down_max_z = np.max(
            downsampled_points[:, 2]
        )

        print(
            "Minimum X : {:.4f} m".format(
                down_min_x
            )
        )

        print(
            "Maximum X : {:.4f} m".format(
                down_max_x
            )
        )

        print(
            "Minimum Y : {:.4f} m".format(
                down_min_y
            )
        )

        print(
            "Maximum Y : {:.4f} m".format(
                down_max_y
            )
        )

        print(
            "Minimum Z : {:.4f} m".format(
                down_min_z
            )
        )

        print(
            "Maximum Z : {:.4f} m".format(
                down_max_z
            )
        )

        # ==================================================
        # SAMPLE DOWNSAMPLED POINTS
        # ==================================================

        print(
            "\n========== DOWNSAMPLED SAMPLES =========="
        )

        sample_count = min(
            10,
            downsampled_count
        )

        for i in range(sample_count):

            print(
                "Point {}: X={:.4f}, "
                "Y={:.4f}, "
                "Z={:.4f}".format(
                    i,
                    downsampled_points[i][0],
                    downsampled_points[i][1],
                    downsampled_points[i][2]
                )
            )

        print(
            "\n==========================================\n"
        )


def main():

    rospy.init_node(
        "pointcloud_reader",
        anonymous=True
    )

    PointCloudReader()

    rospy.spin()


if __name__ == "__main__":
    main()
```
```
jetauto@jetauto-desktop:~/catkin_ws/src/pointcloud_segmentation/scripts$ rosrun pointcloud_segmentation pointcloud_reader.py
[INFO] [1786705846.004574]: Received Astra PointCloud2

========== POINT CLOUD INFO ==========
Topic    : /jetauto_1/camera/depth/points
('Frame ID :', 'camera_rgb_optical_frame')
('Width    :', 640)
('Height   :', 480)
('Fields   :', ['x', 'y', 'z'])
('Point step:', 16)
('Row step  :', 10240)
('Dense     :', False)

========== READING POINTS ==========
('Total points   :', 307200)
('Valid XYZ      :', 252836)
('Invalid XYZ    :', 54364)

========== ORIGINAL CLOUD ==========
('Array shape :', (252836, 3))
('Array dtype :', dtype('float32'))
X range : 1.5394 m
Y range : 1.4364 m
Z range : 1.3180 m

========== VOXEL DOWNSAMPLING ==========
Voxel size : 0.020 m
('Original valid points :', 252836)
('Downsampled points    :', 7229)
Point reduction       : 97.14%

========== DOWNSAMPLED BOUNDS ==========
Minimum X : -1.0938 m
Maximum X : 0.4403 m
Minimum Y : -0.6618 m
Maximum Y : 0.7667 m
Minimum Z : 0.8525 m
Maximum Z : 2.1660 m

========== DOWNSAMPLED SAMPLES ==========
Point 0: X=0.0018, Y=0.0044, Z=1.5390
Point 1: X=0.0100, Y=0.0099, Z=1.5460
Point 2: X=0.0099, Y=0.0299, Z=1.5460
Point 3: X=0.0053, Y=0.0557, Z=1.5390
Point 4: X=0.0110, Y=0.0485, Z=1.5460
Point 5: X=0.0033, Y=0.0686, Z=1.5390
Point 6: X=0.0125, Y=0.0706, Z=1.5460
Point 7: X=0.0178, Y=0.0951, Z=1.5390
Point 8: X=0.0097, Y=0.0901, Z=1.5460
Point 9: X=0.0079, Y=0.1145, Z=1.5390

==========================================

```
---

new code for clustering 

```
#!/usr/bin/env python

import rospy
import math
import numpy as np

import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2

from sklearn.neighbors import NearestNeighbors


class PointCloudSegmentation:

    def __init__(self):

        self.subscriber = rospy.Subscriber(
            "/jetauto_1/camera/depth/points",
            PointCloud2,
            self.pointcloud_callback,
            queue_size=1
        )

        self.received = False

        # ==============================================
        # PARAMETERS
        # ==============================================

        self.voxel_size = 0.02

        self.cluster_tolerance = 0.05

        self.min_cluster_size = 20

        self.max_cluster_size = 5000

    # ==================================================
    # VOXEL DOWNSAMPLING
    # ==================================================

    def voxel_downsample(self, points):

        if len(points) == 0:
            return points

        voxel_indices = np.floor(
            points / self.voxel_size
        ).astype(np.int32)

        unique_voxels, inverse_indices = np.unique(
            voxel_indices,
            axis=0,
            return_inverse=True
        )

        downsampled = np.zeros(
            (len(unique_voxels), 3),
            dtype=np.float32
        )

        for i in range(len(unique_voxels)):

            voxel_points = points[
                inverse_indices == i
            ]

            downsampled[i] = np.mean(
                voxel_points,
                axis=0
            )

        return downsampled

    # ==================================================
    # EUCLIDEAN CLUSTERING
    # ==================================================

    def euclidean_clustering(self, points):

        number_of_points = len(points)

        if number_of_points == 0:
            return []

        print(
            "\n========== NEAREST NEIGHBOR SEARCH =========="
        )

        print(
            "Number of points :",
            number_of_points
        )

        print(
            "Cluster tolerance : {:.3f} m".format(
                self.cluster_tolerance
            )
        )

        # ----------------------------------------------
        # Build nearest-neighbor search structure
        # ----------------------------------------------

        neighbors_model = NearestNeighbors(
            radius=self.cluster_tolerance,
            algorithm="kd_tree"
        )

        neighbors_model.fit(points)

        # Find neighbors within tolerance
        neighbor_indices = neighbors_model.radius_neighbors(
            points,
            return_distance=False
        )

        # ----------------------------------------------
        # Track visited points
        # ----------------------------------------------

        visited = np.zeros(
            number_of_points,
            dtype=np.bool
        )

        clusters = []

        # ----------------------------------------------
        # Region expansion
        # ----------------------------------------------

        for point_index in range(number_of_points):

            if visited[point_index]:
                continue

            # Start a new cluster
            cluster = []

            queue = [point_index]

            visited[point_index] = True

            while len(queue) > 0:

                current_index = queue.pop()

                cluster.append(current_index)

                # Check all neighboring points
                for neighbor_index in neighbor_indices[
                        current_index]:

                    neighbor_index = int(
                        neighbor_index
                    )

                    if not visited[neighbor_index]:

                        visited[neighbor_index] = True

                        queue.append(
                            neighbor_index
                        )

            cluster_size = len(cluster)

            # ------------------------------------------
            # Apply cluster size limits
            # ------------------------------------------

            if (
                cluster_size >= self.min_cluster_size
                and
                cluster_size <= self.max_cluster_size
            ):

                clusters.append(cluster)

        return clusters

    # ==================================================
    # POINT CLOUD CALLBACK
    # ==================================================

    def pointcloud_callback(self, msg):

        if self.received:
            return

        self.received = True

        rospy.loginfo(
            "Received Astra PointCloud2"
        )

        # ==============================================
        # POINT CLOUD INFORMATION
        # ==============================================

        print(
            "\n========== POINT CLOUD INFO =========="
        )

        print(
            "Topic    : /jetauto_1/camera/depth/points"
        )

        print(
            "Frame ID :",
            msg.header.frame_id
        )

        print(
            "Width    :",
            msg.width
        )

        print(
            "Height   :",
            msg.height
        )

        print(
            "Fields   :",
            [field.name for field in msg.fields]
        )

        print(
            "Point step:",
            msg.point_step
        )

        print(
            "Row step  :",
            msg.row_step
        )

        print(
            "Dense     :",
            msg.is_dense
        )

        # ==============================================
        # READ VALID XYZ POINTS
        # ==============================================

        print(
            "\n========== READING POINTS =========="
        )

        points = []

        total_points = 0
        invalid_points = 0

        for point in pc2.read_points(
                msg,
                field_names=("x", "y", "z"),
                skip_nans=False):

            total_points += 1

            x = point[0]
            y = point[1]
            z = point[2]

            if (
                math.isnan(x) or math.isinf(x) or
                math.isnan(y) or math.isinf(y) or
                math.isnan(z) or math.isinf(z)
            ):

                invalid_points += 1

                continue

            points.append(
                [x, y, z]
            )

        points = np.array(
            points,
            dtype=np.float32
        )

        valid_points = len(points)

        print(
            "Total points   :",
            total_points
        )

        print(
            "Valid XYZ      :",
            valid_points
        )

        print(
            "Invalid XYZ    :",
            invalid_points
        )

        if valid_points == 0:

            rospy.logwarn(
                "No valid XYZ points found."
            )

            return

        # ==============================================
        # DOWNSAMPLING
        # ==============================================

        print(
            "\n========== VOXEL DOWNSAMPLING =========="
        )

        print(
            "Voxel size : {:.3f} m".format(
                self.voxel_size
            )
        )

        downsampled_points = self.voxel_downsample(
            points
        )

        downsampled_count = len(
            downsampled_points
        )

        reduction = (
            1.0 -
            float(downsampled_count) /
            float(valid_points)
        ) * 100.0

        print(
            "Original valid points :",
            valid_points
        )

        print(
            "Downsampled points    :",
            downsampled_count
        )

        print(
            "Point reduction       : {:.2f}%".format(
                reduction
            )
        )

        # ==============================================
        # EUCLIDEAN CLUSTERING
        # ==============================================

        print(
            "\n========== EUCLIDEAN CLUSTERING =========="
        )

        print(
            "Cluster tolerance : {:.3f} m".format(
                self.cluster_tolerance
            )
        )

        print(
            "Minimum cluster size :",
            self.min_cluster_size
        )

        print(
            "Maximum cluster size :",
            self.max_cluster_size
        )

        clusters = self.euclidean_clustering(
            downsampled_points
        )

        # ==============================================
        # CLUSTER RESULTS
        # ==============================================

        print(
            "\n========== CLUSTER RESULTS =========="
        )

        print(
            "Number of clusters :",
            len(clusters)
        )

        clustered_points = 0

        for i, cluster in enumerate(clusters):

            cluster_size = len(cluster)

            clustered_points += cluster_size

            print(
                "Cluster {:3d} : {:5d} points".format(
                    i + 1,
                    cluster_size
                )
            )

        noise_points = (
            downsampled_count -
            clustered_points
        )

        print(
            "\nClustered points :",
            clustered_points
        )

        print(
            "Noise/unclustered:",
            noise_points
        )

        # ==============================================
        # CLUSTER SIZE SUMMARY
        # ==============================================

        if len(clusters) > 0:

            cluster_sizes = [
                len(cluster)
                for cluster in clusters
            ]

            print(
                "\n========== CLUSTER SIZE SUMMARY =========="
            )

            print(
                "Largest cluster :",
                max(cluster_sizes)
            )

            print(
                "Smallest cluster:",
                min(cluster_sizes)
            )

            print(
                "Average cluster : {:.2f}".format(
                    np.mean(cluster_sizes)
                )
            )

        print(
            "\n============================================\n"
        )


def main():

    rospy.init_node(
        "pointcloud_segmentation",
        anonymous=True
    )

    PointCloudSegmentation()

    rospy.spin()


if __name__ == "__main__":
    main()
```
chmod +x ~/catkin_ws/src/pointcloud_segmentation/scripts/pointcloud_reader.py
source ~/catkin_ws/devel/setup.bash
rosrun pointcloud_segmentation pointcloud_reader.py

```
[INFO] [1786707714.537116]: Received Astra PointCloud2

========== POINT CLOUD INFO ==========
Topic    : /jetauto_1/camera/depth/points
('Frame ID :', 'camera_rgb_optical_frame')
('Width    :', 640)
('Height   :', 480)
('Fields   :', ['x', 'y', 'z'])
('Point step:', 16)
('Row step  :', 10240)
('Dense     :', False)

========== READING POINTS ==========
('Total points   :', 307200)
('Valid XYZ      :', 252648)
('Invalid XYZ    :', 54552)

========== VOXEL DOWNSAMPLING ==========
Voxel size : 0.020 m
('Original valid points :', 252648)
('Downsampled points    :', 7079)
Point reduction       : 97.20%

========== EUCLIDEAN CLUSTERING ==========
Cluster tolerance : 0.050 m
('Minimum cluster size :', 20)
('Maximum cluster size :', 5000)

========== NEAREST NEIGHBOR SEARCH ==========
('Number of points :', 7079)
Cluster tolerance : 0.050 m

========== CLUSTER RESULTS ==========
('Number of clusters :', 9)
Cluster   1 :  3912 points
Cluster   2 :  1783 points
Cluster   3 :   184 points
Cluster   4 :   286 points
Cluster   5 :   196 points
Cluster   6 :   194 points
Cluster   7 :   206 points
Cluster   8 :   218 points
Cluster   9 :    76 points
('\nClustered points :', 7055)
('Noise/unclustered:', 24)

========== CLUSTER SIZE SUMMARY ==========
('Largest cluster :', 3912)
('Smallest cluster:', 76)
Average cluster : 783.89

============================================
```



