# JetAuto Multi-Modal Robotics Dataset

## Overview

JetAuto — with its LiDAR, cameras, movement/odometry topics, and arm/gripper — can serve as a platform for collecting multi-modal robotics datasets. This README describes what data can be collected, how it should be stored, and the structure and principles the dataset should follow.

The LLM/model files and the dataset are kept **separate**. Models, the ROS workspace, and datasets are three distinct concerns:

- **Models** (e.g. `/mnt/llm/`) — LLM binaries, builds, and weights
- **ROS workspace** — the running robot software
- **Datasets** — recorded sensor/robot/LLM data, stored on the **external SD card**

The LLM is the brain/orchestrator; the dataset-collection layer runs alongside it, not inside it. The dataset can later be used by the LLM (or other models) for evaluation, retrieval, fine-tuning, behavior analysis, or training vision/robotics policies.

---

## 1. Candidate Datasets

One recording session can produce several of these datasets simultaneously.

| Dataset | What we collect | Main use |
|---|---|---|
| RGB image dataset | Camera frames | Classification, detection, segmentation |
| RGB video dataset | Continuous video | Tracking, action recognition |
| Color detection dataset | Red/green/blue/etc. objects + labels | Arm/object picking |
| Object detection dataset | Images + bounding boxes | YOLO/DETR |
| Object segmentation dataset | Images + masks | Precise object extraction |
| LiDAR scan dataset | `/scan` LaserScan | Obstacle detection, navigation |
| LiDAR obstacle dataset | Scan + obstacle labels | Obstacle avoidance |
| RGB + LiDAR dataset | Camera + LiDAR + timestamps | Sensor fusion |
| Camera + robot-motion dataset | Images + `cmd_vel`/odom | Visual navigation |
| Navigation dataset | LiDAR + odom + TF + commands | SLAM/navigation |
| SLAM dataset | `/scan` + TF + odometry | Mapping/localization |
| Robot action dataset | User command → LLM JSON → action | LLM robotics |
| LLM command dataset | Natural language → structured robot command | Fine-tuning/evaluation |
| Obstacle-avoidance dataset | Sensor state → safe action | Autonomous navigation |
| Arm movement dataset | Joint/servo positions + actions | Manipulation |
| Gripper dataset | Open/close + object state | Grasping |
| Vision-to-arm dataset | Camera → object location → arm action | Visual manipulation |
| Color-to-arm dataset | Color → target → arm movement | Pick-and-place |
| Robot telemetry dataset | CPU, RAM, temperature, etc. | Edge-performance analysis |
| Failure dataset | Sensor failure / invalid scan / bad command | Robustness |
| Multi-modal dataset | Camera + LiDAR + arm + commands + robot state | General robotics research |

This philosophy mirrors datasets such as KITTI, which combine camera, LiDAR, localization/IMU, calibration, and object annotations rather than treating each sensor independently.

```
Camera
   +
LiDAR
   +
Robot velocity
   +
TF
   +
LLM command
   +
Motor command
   +
Arm position
   ↓
MULTI-MODAL ROBOTICS DATASET
```

---

## 2. Recommended Core Datasets (Start Here)

Rather than building 20 separate datasets at once, start with **one master recording format** and derive datasets from it. The six core datasets to build first:

### Dataset 1 — RGB Vision

Record:
- Camera images
- Timestamps
- Camera parameters
- Scene information

Uses: YOLO, object detection, segmentation, color detection, tracking.

### Dataset 2 — LiDAR

Record (from `/scan`):
- `timestamp`
- `angle_min`
- `angle_max`
- `angle_increment`
- `ranges[]`

Current LiDAR performance:
- ~13–14 scans/sec
- 360° scan
- 0.15 m → 12 m range

### Dataset 3 — Robot Motion

Record:
- `cmd_vel`
- `odom`
- `TF`
- `timestamp`

This lets you answer *"What did the robot see while it was moving?"* — more useful than storing images alone.

### Dataset 4 — LLM Robotics

Record:
- `user_command`
- `LLM_response`
- `parsed_action`
- `execution_start`
- `execution_end`
- `actual_robot_action`
- `LiDAR_state`
- `success/failure`

Example:

```json
{
  "user_command": "Move forward for 2 seconds",
  "llm_output": {
    "action": "move",
    "direction": "forward",
    "duration": 2
  },
  "lidar_front": 1.42,
  "execution": "success"
}
```

This becomes a robot instruction-following dataset over time.

### Dataset 5 — Vision + Arm

Chain to record:

```
RGB image
  → red object detected
  → pixel coordinates
  → estimated real-world position
  → arm movement
  → gripper action
```

Example:

```json
{
  "image": "frame_00123.jpg",
  "object": "red_cube",
  "pixel": [421, 287],
  "target_position": [0.21, 0.08, 0.13],
  "arm_action": "pick",
  "gripper": "close",
  "success": true
}
```

This becomes a vision-to-action manipulation dataset.

### Dataset 6 — Full Multi-Modal Dataset

The ultimate target:

```
                    ┌── Camera
                    │
                    ├── LiDAR
                    │
User → LLM → Action ├── Robot motion
                    │
                    ├── Arm
                    │
                    ├── Gripper
                    │
                    └── Robot state
```

---

## 3. Storage Location

**Store datasets on the external SD card.**

Do **not** put datasets inside the LLM/model directory:

```
✗ /mnt/llm/
      models/
      datasets/
```

Instead, use the SD card's mount point:

```
/media/.../JET_AUTO_DATA/
```

```
JET_AUTO_DATA/
│
├── datasets/
│   ├── rgb/
│   ├── lidar/
│   ├── motion/
│   ├── llm_commands/
│   ├── arm/
│   └── multimodal/
│
├── raw/
│   ├── rosbag/
│   ├── camera/
│   └── lidar/
│
└── metadata/
```

The LLM model directory stays separate:

```
/mnt/llm/
├── builds/
└── models/
    └── qwen2.5-1.5b-instruct-q4_k_m.gguf
```

---

## 4. Raw Data Format: ROS Bags

Since JetAuto runs ROS1 Melodic, `rosbag` is the recommended raw-recording tool. ROS1 `rosbag` is specifically designed to record and replay ROS topic messages, and supports compression, splitting recordings, duration/size limits, and minimum-space protection.

Basic recording:

```bash
rosbag record \
/scan \
/cmd_vel \
/odom \
/tf
```

If the camera publishes on a topic such as `/camera/color/image_raw`:

```bash
rosbag record \
/scan \
/cmd_vel \
/odom \
/tf \
/camera/color/image_raw
```

Recorded bags can be replayed without physically moving the robot, enabling repeated experimentation on the same data:

```
Robot drives around
        ↓
ROS bag
        ↓
SD card
```

```
ROS bag
   ↓
Algorithm A
Algorithm B
Algorithm C
LLM
YOLO
SLAM
```

---

## 5. From Raw Bags to a Clean Dataset

ROS bags should **not** be treated as the final ML dataset directly. Extract and clean them into a proper dataset structure:

```
RAW DATA
   ↓
ROS BAG
   ↓
Extraction
   ↓
Clean Dataset
   ↓
Labels
   ↓
Train / Validation / Test
```

Example:

```
raw/
  run_001.bag
  run_002.bag
  run_003.bag
```

Extracted into:

```
dataset/
├── images/
├── lidar/
├── labels/
├── commands/
├── timestamps/
└── metadata/
```

---

## 6. Dataset Design Principles

### 6.1 Define the task first

Don't collect random data — define the task, input, output, and metrics before recording.

**Example — Obstacle avoidance:**

```
Task:   Obstacle avoidance
Input:  LiDAR scan + robot velocity
Output: safe / unsafe OR movement command
Metric: collision rate, successful navigation rate
```

**Example — Object detection:**

```
Task:    Object detection
Input:   RGB image
Output:  bounding boxes + class
Metrics: Precision, Recall, mAP
```

### 6.2 Prioritize diversity

Avoid collecting large volumes of near-identical data (e.g. 1000 images of the same object, in the same room, under the same lighting).

Vary the following:

**Environment:** room, corridor, open area, cluttered area

**Lighting:** bright, dark, artificial, natural, shadows

**Object:** near, far, small, large, partially hidden, different orientations

**Robot state:** stationary, slow, fast, turning, approaching obstacle

This mirrors real-world benchmarks such as KITTI, which are deliberately built around varied real-world conditions rather than laboratory-perfect examples, and provide task-specific benchmarks and evaluation metrics.

### 6.3 Train / Validation / Test split

Typical splits:

```
70% train / 15% validation / 15% test
```
or
```
80% train / 10% validation / 10% test
```

**Do not randomly split near-identical consecutive frames** — this produces artificially inflated results.

Bad:

```
video_001 frame 001 → train
video_001 frame 002 → train
video_001 frame 003 → test
```

Better — split by run/trajectory:

```
Run 01 → TRAIN
Run 02 → TRAIN
Run 03 → TRAIN

Run 04 → VALIDATION

Run 05 → TEST
```

This ensures the model is evaluated on a different trajectory/environment than it trained on.

### 6.4 Timestamp synchronization

Synchronizing sensor streams by timestamp is essential for building useful multi-modal samples.

Example raw timestamps:

```
Camera:  12:01:04.100
LiDAR:   12:01:04.102
cmd_vel: 12:01:04.105
```

Combined into one synchronized sample:

```
timestamp: 12:01:04.10

RGB:      frame_00125.jpg
LiDAR:    scan_00125
velocity: 0.10 m/s
LLM:      "move forward"
action:   forward
```

KITTI similarly provides synchronized sensor streams, timestamps, and calibration information.

### 6.5 Calibration metadata

Save calibration data for camera, LiDAR, and arm, at minimum:

- Camera resolution
- Camera FPS
- Camera intrinsics
- Camera distortion
- LiDAR frame
- Camera frame
- TF transforms
- Robot dimensions
- Arm coordinate system

This supports coordinate conversions such as:

```
pixel
  ↓
camera coordinate
  ↓
robot coordinate
  ↓
arm coordinate
```

This is directly relevant to converting RGB pixels into real-world centimeters and, in turn, into movement time given robot speed.

### 6.6 Label formats

Define label formats explicitly per task.

**Object detection:**
```
class
x_min
y_min
x_max
y_max
```

**Color detection:**
```
class = red
center_x
center_y
```

**LiDAR obstacle avoidance:**
```
front_distance
left_distance
right_distance
action
```

Example:
```
0.35 m
0.80 m
1.20 m
TURN_LEFT
```

**LLM robotics:**
```
natural_language
→ structured_command
→ execution
→ result
```

---

## 7. Dataset Documentation

Every dataset should include a README documenting:

```
Dataset name
Version
Purpose
Robot hardware
Sensors
Sensor specifications
ROS version
Collection date
Environment
Recording procedure
Topics
Sampling rates
Coordinate systems
Calibration
Label format
Train/validation/test split
Known limitations
License
```

This is especially important if the dataset is intended for eventual publication.

---

## 8. Target Directory Structure

```
JET_AUTO_DATASET_v1/
│
├── README.md
├── LICENSE
├── dataset.yaml
│
├── raw/
│   ├── rosbag/
│   │   ├── run_001.bag
│   │   ├── run_002.bag
│   │   └── run_003.bag
│   │
│   └── video/
│
├── sensors/
│   ├── camera/
│   │   ├── images/
│   │   └── timestamps.csv
│   │
│   └── lidar/
│       ├── scans/
│       └── timestamps.csv
│
├── robot/
│   ├── odom/
│   ├── cmd_vel/
│   ├── tf/
│   └── status/
│
├── llm/
│   ├── commands.jsonl
│   └── executions.jsonl
│
├── arm/
│   ├── joints/
│   ├── gripper/
│   └── actions/
│
├── annotations/
│   ├── detection/
│   ├── segmentation/
│   ├── colors/
│   └── obstacles/
│
├── calibration/
│   ├── camera.yaml
│   ├── lidar.yaml
│   └── transforms.yaml
│
└── splits/
    ├── train.txt
    ├── val.txt
    └── test.txt
```

---

## 9. How This Fits the JetAuto Project

```
                         ┌──────── CAMERA
                         │
                         ├──────── LiDAR
                         │
USER ──→ LLM ──→ BRAIN ──┼──────── ROBOT BASE
                         │
                         ├──────── ARM
                         │
                         ├──────── GRIPPER
                         │
                         └──────── VISION
                                  │
                                  ↓
                              DATA LOGGER
                                  │
                                  ↓
                              SD CARD
```

```
                         JET AUTO
                            │
                ┌───────────┴───────────┐
                ↓                       ↓
           REAL-TIME CONTROL       DATA COLLECTION
                │                       │
                ↓                       ↓
             Robot                  ROS bags
                                        │
                                        ↓
                                  Dataset Builder
                                        │
                    ┌───────────────────┼──────────────────┐
                    ↓                   ↓                  ↓
                  Vision             LiDAR              LLM
                    ↓                   ↓                  ↓
                 YOLO/etc.          SLAM/avoidance      Robot AI
```

The LLM architecture is **not** changed to "contain" the dataset. The LLM remains the brain/orchestrator, and a separate data-collection layer runs alongside it.

The most valuable long-term target is a **synchronized multi-modal robot interaction dataset**: camera + LiDAR + robot state + LLM command + action + arm/gripper + outcome. This provides a foundation for far more than object detection alone — it supports navigation, manipulation, and LLM-driven robot control research.

---

## References

- KITTI Vision Benchmark Suite — raw data: https://www.cvlibs.net/datasets/kitti/raw_data.php
- KITTI Vision Benchmark Suite: https://www.cvlibs.net/datasets//kitti/
- ROS `rosbag` documentation (Noetic): https://docs.ros.org/en/noetic/api/rosbag/html/c%2B%2B/index.html
- `ros_comm` rosbag record source: https://github.com/ros/ros_comm/blob/noetic-devel/tools/rosbag/src/record.cpp
