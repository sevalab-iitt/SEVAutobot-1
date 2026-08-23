# JetAutoPro + ROS Melodic + LLM Robot-Control Project

## 1. Project Goal

The objective of this project is to build an LLM-controlled physical robot in which a large language model (LLM) acts as the "brain" and the JetAuto hardware acts as its "body."

The LLM should eventually be able to understand and control:

- Movement
- LiDAR
- Obstacle avoidance
- Cameras
- Computer vision
- Arm
- Gripper
- Autonomous behaviors
- Multi-step commands

**Status: PLANNED/FUTURE for camera, vision, arm, and full autonomy — see Section 19 for what is currently working.**

---

## 2. Initial ROS Package

**Status: WORKING NOW**

The base ROS package was created with:

```bash
catkin_create_pkg jetauto_llm rospy geometry_msgs std_msgs
```

This generated the standard catkin package structure, including:

- `package.xml`
- `CMakeLists.txt`
- `scripts/`
- `src/`

The package was verified with:

```bash
rospack find jetauto_llm
```

which returned:

```
~/catkin_ws/src/jetauto_llm
```

---

## 3. Stage 1 — Basic LLM Command Pipeline

**Status: WORKING NOW**

The first working system accepted natural-language robot commands, sent them to the LLM, received JSON, parsed the JSON, and converted it into a robot command.

**Example input:**

```
"Move forward for 2 seconds."
```

**LLM response:**

```json
{"action":"move","direction":"forward","duration":2}
```

Initially `DRY_RUN` was enabled, so no real robot motion occurred. Example output:

```
[DRY RUN] Would execute: move forward for 2.0 seconds
```

This established the core pipeline:

```
Natural language → LLM → JSON → parser → robot command
```

---

## 4. Stage 2 — LiDAR Integration

**Status: WORKING NOW**

The `/scan` topic was integrated into the LLM robot node.

### Bug fix

The code initially used `rospy.isinf()`, which caused:

```
AttributeError: module 'rospy' has no attribute 'isinf'
```

This was corrected by using Python's built-in `math` module functionality instead.

### Verification

LiDAR data reception was confirmed using:

```bash
rostopic hz /scan
```

Observed rate: approximately **13–14 Hz**.

Scan contents were inspected with:

```bash
rostopic echo -n 1 /scan
```

### Key LiDAR parameters

| Parameter | Value |
|---|---|
| `angle_min` | ≈ -3.14159 |
| `angle_max` | ≈ 3.14159 |
| `angle_increment` | ≈ 0.00548 |
| `range_min` | 0.15 m |
| `range_max` | 12.0 m |
| Frame | `lidar_frame` |

Scans contained a mix of valid range readings and `inf` values where no return was detected.

---

## 5. Stage 3/4 — Real Robot Control

**Status: WORKING NOW**

The system was transitioned from:

```
DRY_RUN = True
```

to:

```
DRY_RUN = False
```

Before enabling real robot control, the `/jetauto_controller/cmd_vel` topic was manually tested:

```bash
rostopic pub -1 /jetauto_controller/cmd_vel geometry_msgs/Twist \
'{linear: {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'
```

```bash
rostopic pub -1 /jetauto_controller/cmd_vel geometry_msgs/Twist \
'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'
```

This confirmed the robot responded correctly to `cmd_vel` messages.

Real robot behaviors successfully demonstrated:

- Forward
- Backward
- Left turn
- Right turn
- Stop

Example log output:

```
Executing REAL robot movement.
Robot STOPPED
```

---

## 6. Multi-Command Support

**Status: WORKING NOW**

The system was extended beyond single-action execution to support **sequences of commands**.

Example tested input:

```
"Move forward for 2 seconds then turn left for 1 second."
```

Sequences of up to 3 commands were tested, e.g.:

```
COMMAND 1 — move forward
COMMAND 2 — turn left
COMMAND 3 — move backward
```

The final system executed commands sequentially, one after another.

---

## 7. llama.cpp Local LLM

**Status: WORKING NOW**

The local LLM backend runs on `llama.cpp` using the `llama-server` binary.

Server startup command:

```bash
bin/llama-server \
  -m /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf \
  -ngl 99 \
  -c 2048 \
  -t 4 \
  -tb 4 \
  --host 127.0.0.1 \
  --port 8081
```

### Bug fix

Using `-port 8081` (single dash) produced:

```
error: invalid argument: -port
```

The correct flag is `--port 8081` (double dash).

### Health check

```bash
curl http://127.0.0.1:8081/health
```

Result:

```json
{"status":"ok"}
```

---

## 8. LLM Performance / Problem

**Status: WORKING, WITH KNOWN LIMITATIONS**

The local model was reachable over HTTP but inference was relatively slow.

A simple test generating the text `"Hello."` measured approximately **1.86 tokens/sec**.

A separate test produced unreliable, malformed output, e.g.:

```
GGGGGGGGGGGGGGGGGGGG
```

This confirmed the bottleneck was **local LLM inference/output quality**, not ROS connectivity.

Observed LLM output issues included:

- Extra, unrequested text
- Malformed JSON
- Multiple JSON objects in one response
- Natural language mixed with JSON
- Truncated JSON
- Other unexpected outputs

These issues motivated stronger JSON parsing and, eventually, multi-command parsing (see Section 6).

---

## 9. llama.cpp JSON Test

**Status: WORKING NOW**

A direct test of the llama.cpp HTTP completion endpoint was performed:

```bash
curl http://127.0.0.1:8081/completion \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "You control a mobile robot. Output ONLY valid JSON. No explanation. User command: Move forward for 2 seconds.",
    "n_predict": 20,
    "temperature": 0
  }'
```

Response:

```json
{"command": "Move forward for 2 seconds"}
```

This confirmed the full chain was functional:

```
ROS → local llama.cpp → HTTP API → response
```

---

## 10. Safety / Obstacle Avoidance

**Status: INTEGRATION IN PROGRESS**

A key limitation was identified: the LLM node could read LiDAR data, but simply reading LiDAR does **not** automatically prevent collisions. A dedicated obstacle-avoidance layer is required.

A senior-provided JetAuto obstacle-avoidance implementation was identified, using:

- `jetauto_controller`
- LiDAR driver
- `/scan`
- `lidar_frame`
- An autonomous obstacle-avoidance node
- A pause/resume topic

**Pause:**

```bash
rostopic pub /auto_explore/pause std_msgs/Bool "data: true"
```

**Resume:**

```bash
rostopic pub /auto_explore/pause std_msgs/Bool "data: false"
```

### Intended architecture

```
LLM command
  → navigation/movement
  → LiDAR safety layer
  → obstacle detection
  → stop/avoid
  → continue
```

The LLM should **not** be solely responsible for millisecond-level collision safety; that responsibility belongs to the dedicated safety layer.

---

## 11. Current Modularization (Target Architecture)

**Status: PLANNED — target structure, not fully implemented**

The original monolithic `scripts/llm_robot_node.py` is being refactored into modular components. The intended (target) structure is:

```
jetauto_llm/
├── scripts/
│   ├── llm_robot_node.py
│   ├── robot/
│   │   ├── __init__.py
│   │   ├── movement.py
│   │   ├── obstacle_avoidance.py
│   │   └── robot_status.py
│   ├── sensors/
│   │   ├── __init__.py
│   │   ├── lidar.py
│   │   └── camera.py
│   ├── vision/
│   │   ├── __init__.py
│   │   ├── color_detection.py
│   │   ├── object_detection.py
│   │   └── vision_manager.py
│   ├── arm/
│   │   ├── __init__.py
│   │   ├── arm_controller.py
│   │   └── gripper.py
│   └── llm/
│       ├── __init__.py
│       └── llm_client.py
├── launch/
│   └── llm_robot.launch
├── config/
│   └── robot_config.yaml
├── CMakeLists.txt
└── package.xml
```

**This is the target modular architecture. Not all modules listed above have been implemented yet.**

---

## 12. Modularization Progress

**Status: STARTED**

The following directories have been created:

```
scripts/robot/
scripts/sensors/
scripts/vision/
scripts/arm/
scripts/llm/
```

Each directory contains an `__init__.py` file.

Pre-existing files (before modularization began):

```
scripts/llm_robot_node.py
scripts/llm_robot_node.py.save
scripts/llm_robot_node.py.save.1
```

The `.save` files are retained as backups of the original monolithic node.

---

## 13. Movement Module

**Status: CREATED**

`scripts/robot/movement.py` was created to handle low-level movement through `/jetauto_controller/cmd_vel`.

Functions included:

- `forward()`
- `backward()`
- `left()`
- `right()`
- `stop()`
- `execute()`
- `emergency_stop()`
- `set_velocity()`

The purpose of this module is to isolate motor-control logic from the LLM, LiDAR, camera, vision, and arm code.

The module is ROS Melodic / Python 2 compatible.

---

## 14. Future Camera + Computer Vision

**Status: PLANNED/FUTURE — not implemented yet**

Camera functionality will be isolated in `sensors/camera.py`.

Computer vision will be separated into:

- `vision/color_detection.py`
- `vision/object_detection.py`
- `vision/vision_manager.py`

Planned capabilities include:

- RGB camera input
- Color detection
- Object detection
- Future YOLO integration
- Pixel coordinates / object position
- Eventual pixel-to-real-world distance conversion

---

## 15. RGB → Real-World cm → Time Requirement

**Status: PLANNED/FUTURE**

This is framed as a future computer-vision / robot-control task rather than a purely LLM-driven task.

Expected pipeline:

```
RGB image
  → detect object
  → pixel coordinates / bounding box
  → estimate real-world distance
  → convert distance to movement requirement
  → use robot speed
  → calculate movement time
```

Basic relationship:

```
time = distance / speed
```

Calibration and/or depth information will be needed to reliably convert image pixels into centimeters. The LLM can interpret the high-level goal ("go to that object"), but the actual pixel-to-distance conversion and motion calculation belong to the perception and control layers, not the LLM itself.

---

## 16. Future Arm Integration

**Status: PLANNED/FUTURE**

The JetAuto arm hardware is already known to be operational (independent of this LLM project).

Future modules:

- `arm_controller.py`
- `gripper.py`

Goal: the LLM should eventually issue high-level commands such as:

```
"Find the red object and pick it up."
```

Intended architecture:

```
LLM
  → Vision
  → object/color detection
  → target position
  → movement
  → arm
  → gripper
```

---

## 17. Final System Concept

**Status: PLANNED/FUTURE (target end-state architecture)**

```
                LLM / BRAIN
                     |
             llm_robot_node.py
                     |
       +-------------+-------------+
       |             |             |
   Movement       Sensors        Arm
       |             |             |
    Motors      LiDAR/Camera   Servos
                     |
                   Vision
                     |
              World understanding
```

In the intended final system:

- The LLM provides high-level intelligence and planning
- ROS provides communication between components
- LiDAR provides spatial safety and environment sensing
- Cameras provide visual perception
- Computer vision interprets visual information
- The movement controller controls the base
- The arm controller controls manipulation
- A dedicated obstacle-avoidance layer provides safety
- The local llama.cpp server provides LLM inference

---

## 18. Important Development Principle

The project is being developed **incrementally**. Each new module must first be tested independently before being connected to the main LLM node. Future modules are not claimed to be working until they have been implemented and verified.

---

## 19. Current Status

| Component | Status |
|---|---|
| ROS package | Working |
| LLM natural-language input | Working |
| JSON command parsing | Working |
| DRY_RUN | Working |
| Real robot movement | Working |
| Forward/backward | Working |
| Left/right turning | Working |
| Stop | Working |
| Multi-command sequence | Working |
| Local llama.cpp server | Working |
| /scan LiDAR | Working |
| LiDAR ~13–14 Hz | Verified |
| Obstacle avoidance | Being integrated |
| Modular architecture | Started |
| Movement module | Created |
| Camera module | Not implemented yet |
| Computer vision | Not implemented yet |
| Object detection | Future |
| Arm module | Future integration |
| Pixel → cm conversion | Future |
| Autonomous goal-based behavior | Future |
