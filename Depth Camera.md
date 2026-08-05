# Hand Gesture Control & Hand Trajectory 
# Hand Trajectory Recognition

 The system detects hand landmarks, recognizes predefined hand gestures, and records the fingertip trajectory in real time.
<img width="400" height="250" alt="Screenshot 2026-07-09 111044" src="https://github.com/user-attachments/assets/19a1548b-b953-4c65-adc8-acab2032a046" />
<img width="400" height="250" alt="Hand Trajectory 1" src="https://github.com/user-attachments/assets/2d8daace-2bcb-4642-877b-56500510d02d" />

---

## Prerequisites

- JetAuto robot
- ROS Melodic
- Astra Pro Plus camera
- MediaPipe Hands
- OpenCV

---

## Launch Instructions

### 1. Stop the APP Control Service

```bash
sudo systemctl stop start_app_node.service
```

### 2. Launch the Hand Trajectory Node

```bash
roslaunch jetauto_example hand_trajectory_node.launch
```

---

## Program Workflow

1. The camera captures live video.
2. MediaPipe detects the hand and extracts 21 hand landmarks.
3. The program recognizes predefined hand gestures.
4. When the **"1"** gesture is detected, the system begins recording the fingertip trajectory.
5. The fingertip path is drawn continuously on the live camera image.
6. When the **"5"** gesture is detected, the recorded trajectory is cleared.

---

## Gesture Functions

| Gesture | Function |
|----------|----------|
| **1** | Start recording fingertip trajectory |
| **5** | Clear recorded trajectory |

---

## Stop the Program

Press:

```text
Ctrl + C
```

---

## Restart the APP Service

```bash
sudo systemctl restart start_app_node.service
```

---

## Complete Workflow

```bash
sudo systemctl stop start_app_node.service

roslaunch jetauto_example hand_trajectory_node.launch
```

After completing the experiment:

```bash
sudo systemctl restart start_app_node.service
```

---

## Project Structure

```
jetauto_ws/
└── src/
    └── jetauto_example/
        └── scripts/
            └── hand_gesture_control/
                └── hand_trajectory_node.py
```

---

## Algorithm

1. Capture image from the Astra Pro Plus camera.
2. Detect hand landmarks using MediaPipe Hands.
3. Estimate the hand gesture based on finger joint angles.
4. If gesture **"1"** is detected:
   - Record the fingertip coordinates.
   - Append the coordinates to the trajectory list.
5. Draw the fingertip trajectory using OpenCV.
6. If gesture **"5"** is detected:
   - Clear the stored trajectory.
7. Display the processed frame.

---

## Key Technologies

- ROS Melodic
- Python 3
- OpenCV
- MediaPipe Hands
- Astra Pro Plus RGB Camera

---

## Notes

- Keep your hand within the camera's field of view for accurate detection.
- Ensure adequate lighting to improve hand landmark detection.
- The trajectory is stored only in memory during execution unless additional code is added to save the coordinates or images.
- To save the trajectory permanently, modify `hand_trajectory_node.py` to write the fingertip coordinates to a CSV file and save the processed image using `cv2.imwrite()`.
  ---
  
# Object Tracking
<img width="930" height="473" alt="Screenshot 2026-07-09 122216" src="https://github.com/user-attachments/assets/4e463a0f-1e67-4234-aef9-5e27c058b8cf" />
<img width="902" height="469" alt="Screenshot 2026-07-07 120449" src="https://github.com/user-attachments/assets/23181cf9-5d5e-4374-b095-0247d92f1bc2" />


## 1. Stop the APP service

```bash
sudo systemctl stop start_app_node.service
```

## 2. Launch the body tracking node

```bash
roslaunch jetauto_example body_track.launch
```

## 3. Open a new terminal and navigate to the tracker script

```bash
cd ~/jetauto_ws/src/jetauto_example/scripts/tracker/
```

## 4. Run the Object Tracking program

```bash
python3 object_tracking.py
```

If your system uses Python 3 as the default interpreter:

```bash
python object_tracking.py
```

## 5. Stop the program

Press:

```text
Ctrl + C
```

## 6. Restart the APP service

```bash
sudo systemctl restart start_app_node.service
```

---

## Complete Workflow

```bash
sudo systemctl stop start_app_node.service

roslaunch jetauto_example body_track.launch
```

Open another terminal:

```bash
cd ~/jetauto_ws/src/jetauto_example/scripts/tracker/

python3 object_tracking.py
```

After finishing:

```bash
sudo systemctl restart start_app_node.service
```
# Somatosensory Control
<img width="896" height="329" alt="Screenshot 2026-07-09 124113" src="https://github.com/user-attachments/assets/853ec4de-2b08-4504-aa63-d0c9329cb2bf" />

This example enables JetAuto to recognize human body poses using MediaPipe and control the robot through body movements.

## 1. Stop the APP service

```bash
sudo systemctl stop start_app_node.service
```

## 2. Launch the Somatosensory Control node

```bash
roslaunch jetauto_example body_control.launch
```

## 3. Program Behavior

After the launch file starts successfully:

- The Astra Pro Plus depth camera is initialized.
- MediaPipe Pose is loaded for body pose estimation.
- The robot begins tracking the user's body movements.
- Move your body to control the robot according to the predefined gestures.

## 4. Stop the Program

Press:

```text
Ctrl + C
```

## 5. Restart the APP service

```bash
sudo systemctl restart start_app_node.service
```

---

## Complete Workflow

```bash
sudo systemctl stop start_app_node.service

roslaunch jetauto_example body_control.launch
```

When finished:

```bash
sudo systemctl restart start_app_node.service
```

---

## Notes

- Ensure the **Astra Pro Plus** camera is connected before launching the program.
- Stand approximately **1–3 meters** in front of the camera for reliable body pose detection.
  ---
  
# Human Posture Control 

<img width="400" height="250" alt="Screenshot 2026-07-09 115607" src="https://github.com/user-attachments/assets/21c0170d-3a5a-4a00-9d9b-7da754cfac8b" />
<img width="400" height="250" alt="Screenshot 2026-07-08 224721" src="https://github.com/user-attachments/assets/3c0dc31f-7db3-416c-aee1-949716c31b57" />

## Launch Human Posture Control

Stop the default application before launching the demo.

```bash
sudo systemctl stop start_app_node.service
```

Launch the body tracking node.

```bash
roslaunch jetauto_example body_and_rgb_control.launch
```

or

```bash
roslaunch jetauto_example body_track.launch
```

---

## Verify Running Nodes

```bash
rosnode list
```

Expected nodes include:

```text
/body_control
/camera/*
/arm_controller
```

---

## List Available Topics

```bash
rostopic list
```

---

## Check Robot Motion Commands

Display the velocity commands generated from body posture.

```bash
rostopic echo /cmd_vel
```

Output:

```yaml
linear:
  x: 0.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: -0.081
```


---

## View Tracking Data 

```bash
rostopic echo /jetauto_controller/cmd_vel

```
---

## Stop Demo

Press

```text
Ctrl + C
```

Restart the default JetAuto service

```bash
sudo systemctl start start_app_node.service
```
---
# Body Tracking

## 1. Stop the APP Control Service

```bash
sudo systemctl stop start_app_node.service
```

## 2. Launch the Body Tracking Node

```bash
roslaunch jetauto_example body_track.launch
```

---

## Program Workflow

1. Initialize the Astra Pro Plus RGB-D camera.
2. Start the ROS Body Tracking node.
3. Detect the human body using MediaPipe Pose.
4. Track the user's body in real time.
5. Display the detected body landmarks and tracking results in the camera window.

---

## Stop the Program

Press:

```text
Ctrl + C
```

---

## Restart the APP Control Service

```bash
sudo systemctl restart start_app_node.service
```

---

## Complete Workflow

```bash
sudo systemctl stop start_app_node.service

roslaunch jetauto_example body_track.launch
```

After finishing the experiment:

```bash
sudo systemctl restart start_app_node.service
```
# Human Tracking 
<img width="959" height="515" alt="Screenshot 2026-07-09 120715" src="https://github.com/user-attachments/assets/d68d5765-e779-4838-954d-343c115e42b3" />

The robot detects and tracks a person in real time using the Astra Pro Plus RGB-D camera and MediaPipe Pose. The detected body is continuously tracked, allowing the robot to follow the user's movements.

---

## Prerequisites

- JetAuto Robot
- ROS Melodic
- Astra Pro Plus RGB-D Camera
- MediaPipe Pose
- OpenCV
- Python 3

---

## Launch Instructions

### 1. Stop the APP Control Service

```bash
sudo systemctl stop start_app_node.service
```

### 2. Launch the Human Tracking Node

```bash
roslaunch jetauto_example body_track.launch
```

---

## Program Workflow

1. Initialize the Astra Pro Plus RGB-D camera.
2. Start the ROS Human Tracking node.
3. Detect the human body using MediaPipe Pose.
4. Estimate the body center position.
5. Continuously track the detected person.
6. Display the tracking result with FPS in the camera window.

---

## Stop the Program

Press:

```text
Ctrl + C
```

---

## Restart the APP Control Service

```bash
sudo systemctl restart start_app_node.service
```

---

## Complete Workflow

```bash
# Stop the APP service
sudo systemctl stop start_app_node.service

# Launch Human Tracking
roslaunch jetauto_example body_track.launch
```

After completing the experiment:

```bash
# Restart the APP service
sudo systemctl restart start_app_node.service
```


---

## Project Structure

```text
jetauto_ws/
└── src/
    └── jetauto_example/
        ├── launch/
        │   └── body_track.launch
        └── scripts/
            └── body_control/
                └── body_track.py
```

---
# Astra Pro Plus RGB-D Camera Integration and Algorithm Validation

**Platform:** JetAuto Pro (Jetson Nano)  
**Operating System:** Ubuntu 18.04 (JetPack 4.6.3 - L4T R32.7.3)  
**ROS Version:** ROS Melodic

---

# Objective

Verify the output format of the Astra Pro Plus RGB-D camera and test whether its data can be consumed by a computer vision algorithm.

---

# Hardware

- JetAuto Pro (Jetson Nano)
- Orbbec Astra Pro Plus RGB-D Camera
- RPLiDAR A1

---

# Software

- ROS Melodic
- Python 3.6
- OpenCV 4.6
- cv_bridge
- PyTorch 1.10 (CUDA Enabled)

---

# Camera Verification

The Astra camera was launched using:

```bash
roslaunch astra_camera astra_pro_plus.launch
```

Verified topics:

| Topic | Message Type |
|--------|--------------|
| `/astra_cam/rgb/image_raw` | `sensor_msgs/Image` |
| `/astra_cam/depth/image_raw` | `sensor_msgs/Image` |
| `/astra_cam/depth/points` | `sensor_msgs/PointCloud2` |

Commands used:

```bash
rostopic type /astra_cam/rgb/image_raw
rostopic type /astra_cam/depth/image_raw
rostopic type /astra_cam/depth/points
```

Output:

```text
sensor_msgs/Image
sensor_msgs/Image
sensor_msgs/PointCloud2
```

---

# Message Format Verification

Command:

```bash
rosmsg show sensor_msgs/Image
```

Output:

```text
std_msgs/Header header
uint32 height
uint32 width
string encoding
uint8 is_bigendian
uint32 step
uint8[] data
```

---

# OpenCV Integration

A custom ROS node (`image_viewer.py`) was created.

Pipeline:

```
Astra Camera
      │
      ▼
/astra_cam/rgb/image_raw
      │
      ▼
ROS Subscriber
      │
      ▼
cv_bridge
      │
      ▼
OpenCV
      │
      ▼
Live RGB Display
```

Result:

- Successfully subscribed to the RGB topic.
- Converted ROS Image messages into OpenCV images.
- Displayed the live RGB stream successfully.

> **Insert Screenshot:** `images/astra_rgb_output.png`

---

# YOLO Investigation

YOLOv5 v6.2 repository was cloned.

Environment verification:

```bash
python3 -c "import torch; print(torch.cuda.is_available())"
```

Output:

```text
True
```

GPU:

```text
NVIDIA Tegra X1
```

---

# Debugging Performed

The following components were verified successfully:

- CUDA
- OpenCV
- TorchVision
- PyTorch Tensor Operations
- ROS Camera Pipeline

The issue occurred only when loading the YOLO checkpoint:

```bash
python3 -c "import torch; m=torch.load('yolov5s.pt', map_location='cpu')"
```

Result:

```text
Segmentation fault (core dumped)
```

A simple PyTorch save/load test executed successfully:

```bash
python3 -c "import torch; torch.save({'a':1},'test.pt'); print(torch.load('test.pt'))"
```

Output:

```text
{'a': 1}
```

This indicates that the failure is specific to loading the YOLO checkpoint rather than the PyTorch installation itself.

---

# Conclusion

The objective was successfully achieved.

Completed:

- Verified Astra RGB-D camera topics.
- Verified ROS message formats.
- Successfully subscribed to Astra RGB images.
- Converted ROS Image messages to OpenCV format using `cv_bridge`.
- Demonstrated that Astra data can be consumed by a computer vision algorithm (OpenCV).

YOLO integration was attempted, but a checkpoint compatibility issue caused a segmentation fault while loading the pretrained model. The camera pipeline and ROS integration remain fully functional.

---

# Future Work

- RGB-D SLAM using RTAB-Map
- Point Cloud Processing (PCL)
- ORB-SLAM2 / ORB-SLAM3
- Object Detection using a Jetson-compatible framework
- Semantic Mapping
