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

<img width="1120" height="595" alt="image" src="https://github.com/user-attachments/assets/4ae21113-6b58-4c2d-a850-f9989d5b7b41" />

```
jetauto@jetauto-desktop:~$ cd ~/catkin_ws
atkin_makejetauto@jetauto-desktop:~/catkin_ws$ catkin_make
Base path: /home/jetauto/catkin_ws
Source space: /home/jetauto/catkin_ws/src
Build space: /home/jetauto/catkin_ws/build
Devel space: /home/jetauto/catkin_ws/devel
Install space: /home/jetauto/catkin_ws/install
####
#### Running command: "make cmake_check_build_system" in "/home/jetauto/catkin_ws/build"
####
####
#### Running command: "make -j4 -l4" in "/home/jetauto/catkin_ws/build"
####
jetauto@jetauto-desktop:~/catkin_ws$ cd ~/catkin_ws/src
jetauto@jetauto-desktop:~/catkin_ws/src$ catkin_create_pkg astra_demo rospy sensor_msgs cv_bridge
Created file astra_demo/package.xml
Created file astra_demo/CMakeLists.txt
Created folder astra_demo/src
Successfully created files in /home/jetauto/catkin_ws/src/astra_demo. Please adjust the values in package.xml.
jetauto@jetauto-desktop:~/catkin_ws/src$ rospack find astra_demo
/home/jetauto/catkin_ws/src/astra_demo
jetauto@jetauto-desktop:~/catkin_ws/src$ cd ~/catkin_ws/src/astra_demo
jetauto@jetauto-desktop:~/catkin_ws/src/astra_demo$ mkdir scripts
jetauto@jetauto-desktop:~/catkin_ws/src/astra_demo$ tree
.
├── CMakeLists.txt
├── package.xml
├── scripts
└── src

2 directories, 2 files
jetauto@jetauto-desktop:~/catkin_ws/src/astra_demo$ ls -R
.:
CMakeLists.txt  package.xml  scripts  src

./scripts:

./src:
jetauto@jetauto-desktop:~/catkin_ws/src/astra_demo$ touch image_viewer.py
jetauto@jetauto-desktop:~/catkin_ws/src/astra_demo$ nano image_viewer.py
jetauto@jetauto-desktop:~/catkin_ws/src/astra_demo$ chmod +x image_viewer.py
jetauto@jetauto-desktop:~/catkin_ws/src/astra_demo$ cd ~/catkin_ws
jetauto@jetauto-desktop:~/catkin_ws$ catkin_make
Base path: /home/jetauto/catkin_ws
Source space: /home/jetauto/catkin_ws/src
Build space: /home/jetauto/catkin_ws/build
Devel space: /home/jetauto/catkin_ws/devel
Install space: /home/jetauto/catkin_ws/install
####
#### Running command: "cmake /home/jetauto/catkin_ws/src -DCATKIN_DEVEL_PREFIX=/home/jetauto/catkin_ws/devel -DCMAKE_INSTALL_PREFIX=/home/jetauto/catkin_ws/install -G Unix Makefiles" in "/home/jetauto/catkin_ws/build"
####
-- Using CATKIN_DEVEL_PREFIX: /home/jetauto/catkin_ws/devel
-- Using CMAKE_PREFIX_PATH: /home/jetauto/catkin_ws/devel;/home/jetauto/jetauto_ws/devel;/opt/ros/melodic
-- This workspace overlays: /home/jetauto/catkin_ws/devel;/home/jetauto/jetauto_ws/devel;/opt/ros/melodic
-- Found PythonInterp: /usr/bin/python2 (found suitable version "2.7.17", minimum required is "2")
-- Using PYTHON_EXECUTABLE: /usr/bin/python2
-- Using Debian Python package layout
-- Using empy: /usr/bin/empy
-- Using CATKIN_ENABLE_TESTING: ON
-- Call enable_testing()
-- Using CATKIN_TEST_RESULTS_DIR: /home/jetauto/catkin_ws/build/test_results
-- Found gtest sources under '/usr/src/googletest': gtests will be built
-- Found gmock sources under '/usr/src/googletest': gmock will be built
-- Found PythonInterp: /usr/bin/python2 (found version "2.7.17")
-- Using Python nosetests: /usr/bin/nosetests-2.7
-- catkin 0.7.29
-- BUILD_SHARED_LIBS is on
-- BUILD_SHARED_LIBS is on
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- ~~  traversing 2 packages in topological order:
-- ~~  - astra_demo
-- ~~  - jetauto_pointcloud_mapping
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- +++ processing catkin package: 'astra_demo'
-- ==> add_subdirectory(astra_demo)
-- +++ processing catkin package: 'jetauto_pointcloud_mapping'
-- ==> add_subdirectory(jetauto_pointcloud_mapping)
-- Using these message generators: gencpp;geneus;genlisp;gennodejs;genpy
-- Configuring done
-- Generating done
-- Build files have been written to: /home/jetauto/catkin_ws/build
####
#### Running command: "make -j4 -l4" in "/home/jetauto/catkin_ws/build"
####
jetauto@jetauto-desktop:~/catkin_ws$ source devel/setup.bash
jetauto@jetauto-desktop:~/catkin_ws$ source ~/catkin_ws/devel/setup.bash
jetauto@jetauto-desktop:~/catkin_ws$ rosrun astra_demo image_viewer.py
jetauto@jetauto-desktop:~/catkin_ws$ nano ~/catkin_ws/src/astra_demo/image_viewer.py
jetauto@jetauto-desktop:~/catkin_ws$ python3 -c "import torch; print(torch.__version__)"
1.10.0a0+git36449ea
jetauto@jetauto-desktop:~/catkin_ws$ python3 -c "from ultralytics import YOLO; print('Ultralytics OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'ultralytics'
jetauto@jetauto-desktop:~/catkin_ws$ python3 -c "import torch; print(torch.cuda.is_available())"
True
jetauto@jetauto-desktop:~/catkin_ws$ python3 -c "import torch; print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU Only')"
NVIDIA Tegra X1
jetauto@jetauto-desktop:~/catkin_ws$ cat /etc/nv_tegra_release
# R32 (release), REVISION: 7.3, GCID: 31982016, BOARD: t210ref, EABI: aarch64, DATE: Tue Nov 22 17:30:08 UTC 2022
jetauto@jetauto-desktop:~/catkin_ws$ python3 -m pip --version
pip 21.3.1 from /usr/local/lib/python3.6/dist-packages/pip (python 3.6)
jetauto@jetauto-desktop:~/catkin_ws$ python3 -m pip list | grep -E "torch|torchvision|opencv|numpy"
/usr/lib/python3/dist-packages/secretstorage/dhcrypto.py:15: CryptographyDeprecationWarning: Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in cryptography and will be removed in a future release.
  from cryptography.utils import int_from_bytes
numpy                         1.19.4
opencv-contrib-python         4.6.0.66
torch                         1.10.0a0+git36449ea
torchvision                   0.11.0a0+fa347eb
jetauto@jetauto-desktop:~/catkin_ws$ git --version
git version 2.17.1
jetauto@jetauto-desktop:~/catkin_ws$ ping -c 4 github.com
PING github.com (20.207.73.82) 56(84) bytes of data.
64 bytes from 20.207.73.82 (20.207.73.82): icmp_seq=1 ttl=110 time=30.1 ms
64 bytes from 20.207.73.82 (20.207.73.82): icmp_seq=2 ttl=110 time=31.1 ms
64 bytes from 20.207.73.82 (20.207.73.82): icmp_seq=3 ttl=110 time=31.5 ms
^C
--- github.com ping statistics ---
4 packets transmitted, 3 received, 25% packet loss, time 3003ms
rtt min/avg/max/mdev = 30.114/30.946/31.583/0.615 ms
jetauto@jetauto-desktop:~/catkin_ws$ cd ~/catkin_ws/src
jetauto@jetauto-desktop:~/catkin_ws/src$ git clone https://github.com/ultralytics/yolov5.git
Cloning into 'yolov5'...
remote: Enumerating objects: 18689, done.
remote: Counting objects: 100% (286/286), done.
remote: Compressing objects: 100% (164/164), done.
Receiving objects:   2% (374/18689), 204.00 KiB | 390.00 KiB/s  Receiving objects:   3% (561/18689), 204.00 KiB | 390.00 KiB/s  Receiving objects:   4% (748/18689), 204.00 KiB | 390.00 KiB/s  Receiving objects:   4% (854/18689), 204.00 KiB | 390.00 KiB/s  Receiving objects:   5% (935/18689), 484.00 KiB | 452.00 KiB/s  Receiving objects:   6% (1122/18689), 484.00 KiB | 452.00 KiB/s Receiving objects:   7% (1309/18689), 484.00 KiB | 452.00 KiB/s Receiving objects:   8% (1496/18689), 484.00 KiB | 452.00 KiB/s Receiving objects:   9% (1683/18689), 692.00 KiB | 440.00 KiB/s Receiving objects:   9% (1812/18689), 692.00 KiB | 440.00 KiB/s Receiving objects:  10% (1869/18689), 900.00 KiB | 431.00 KiB/s Receiving objects:  11% (2056/18689), 900.00 KiB | 431.00 KiB/s Receiving objects:  39% (7452/18689), 10.00 MiB | 408.00 KiB/s  Receiving objects:  40% (7476/18689), 10.45 MiB | 428.00 KiB/s  Receiving objects:  40% (7543/18689), 10.81 MiB | 435.00 KiB/s  Receiving objects:  41% (7663/18689), 10.81 MiB | 435.00 KiB/s  Receiving objects:  41% (7802/18689), 11.14 MiB | 446.00 KiB/s  Receiving objects:  42% (7850/18689), 11.14 MiB | 446.00 KiB/s  Receiving objects:  43% (8037/18689), 11.43 MiB | 450.00 KiB/s  Receiving objects:  44% (8224/18689), 11.43 MiB | 450.00 KiB/s  Receiving objects:  45% (8411/18689), 11.43 MiB | 450.00 KiB/s  Receiving objects:  46% (8597/18689), 11.65 MiB | 769.00 KiB/s  Receiving objects:  47% (8784/18689), 11.65 MiB | 769.00 KiB/s  Receiving objects:  47% (8808/18689), 11.65 MiB | 769.00 KiB/s  Receiving objects:  48% (8971/18689), 11.89 MiB | 467.00 KiB/s  Receiving objects:  49% (9158/18689), 12.09 MiB | 487.00 KiB/s  Receiving objects:  49% (9217/18689), 12.09 MiB | 487.00 KiB/s  Receiving objects:  50% (9345/18689), 12.09 MiB | 487.00 KiB/s  Receiving objects:  51% (9532/18689), 12.28 MiB | 505.00 KiB/s  Receiving objects:  52% (9719/18689), 12.28 MiB | 505.00 KiB/s  Receiving objects:  53% (9906/18689), 12.28 MiB | 505.00 KiB/s  Receiving objects:  53% (10065/18689), 12.54 MiB | 525.00 KiB/s Receiving objects:  54% (10093/18689), 12.54 MiB | 525.00 KiB/s Receiving objects:  55% (10279/18689), 12.66 MiB | 488.00 KiB/s Receiving objects:  56% (10466/18689), 12.79 MiB | 438.00 KiB/s Receiving objects:  56% (10580/18689), 12.79 MiB | 438.00 KiB/s Receiving objects:  57% (10653/18689), 12.79 MiB | 438.00 KiB/s Receiving objects:  58% (10840/18689), 13.05 MiB | 423.00 KiB/s Receiving objects:  59% (11027/18689), 13.05 MiB | 423.00 KiB/s Receiving objects:  60% (11214/18689), 13.05 MiB | 423.00 KiB/s Receiving objects:  60% (11335/18689), 13.37 MiB | 428.00 KiB/s Receiving objects:  61% (11401/18689), 13.37 MiB | 428.00 KiB/s Receiving objects:  62% (11588/18689), 13.72 MiB | 458.00 KiB/s Receiving objects:  63% (11775/18689), 13.72 MiB | 458.00 KiB/s Receiving objects:  64% (11961/18689), 13.72 MiB | 458.00 KiB/s Receiving objects:  65% (12148/18689), 13.97 MiB | 462.00 KiB/s Receiving objects:  65% (12166/18689), 13.97 MiB | 462.00 KiB/s Receiving objects:  66% (12335/18689), 13.97 MiB | 462.00 KiB/s Receiving objects:  67% (12522/18689), 13.97 MiB | 462.00 KiB/s Receiving objects:  68% (12709/18689), 13.97 MiB | 462.00 KiB/s Receiving objects:  69% (12896/18689), 13.97 MiB | 462.00 KiB/s Receiving objects:  69% (13037/18689), 14.85 MiB | 512.00 KiB/s Receiving objects:  70% (13083/18689), 14.85 MiB | 512.00 KiB/s Receiving objects:  71% (13270/18689), 14.85 MiB | 512.00 KiB/s Receiving objects:  72% (13457/18689), 14.85 MiB | 512.00 KiB/s Receiving objects:  73% (13643/18689), 15.06 MiB | 533.00 KiB/s Receiving objects:  73% (13661/18689), 15.06 MiB | 533.00 KiB/s Receiving objects:  74% (13830/18689), 15.06 MiB | 533.00 KiB/s Receiving objects:  75% (14017/18689), 15.06 MiB | 533.00 KiB/s Receiving objects:  76% (14204/18689), 15.06 MiB | 533.00 KiB/s Receiving objects:  77% (14391/18689), 15.06 MiB | 533.00 KiB/s Receiving objects:  78% (14578/18689), 15.34 MiB | 565.00 KiB/s Receiving objects:  79% (14765/18689), 15.34 MiB | 565.00 KiB/s Receiving objects:  80% (14952/18689), 15.34 MiB | 565.00 KiB/s Receiving objects:  81% (15139/18689), 15.34 MiB | 565.00 KiB/s Receiving objects:  82% (15325/18689), 15.34 MiB | 565.00 KiB/s Receiving objects:  83% (15512/18689), 15.34 MiB | 565.00 KiB/s Receiving objects:  84% (15699/18689), 15.34 MiB | 565.00 KiB/s Receiving objects:  84% (15746/18689), 15.51 MiB | 542.00 KiB/s Receiving objects:  85% (15886/18689), 15.51 MiB | 542.00 KiB/s Receiving objects:  86% (16073/18689), 15.51 MiB | 542.00 KiB/s Receiving objects:  87% (16260/18689), 15.51 MiB | 542.00 KiB/s Receiving objects:  88% (16447/18689), 15.51 MiB | 542.00 KiB/s Receiving objects:  89% (16634/18689), 15.71 MiB | 510.00 KiB/s Receiving objects:  89% (16806/18689), 15.71 MiB | 510.00 KiB/s Receiving objects:  90% (16821/18689), 15.71 MiB | 510.00 KiB/s Receiving objects:  91% (17007/18689), 15.96 MiB | 487.00 KiB/s Receiving objects:  91% (17173/18689), 16.40 MiB | 439.00 KiB/s Receiving objects:  92% (17194/18689), 16.40 MiB | 439.00 KiB/s Receiving objects:  92% (17338/18689), 16.94 MiB | 448.00 KiB/s Receiving objects:  93% (17381/18689), 16.94 MiB | 448.00 KiB/s Receiving objects:  94% (17568/18689), 16.94 MiB | 448.00 KiB/s Receiving objects:  95% (17755/18689), 17.11 MiB | 440.00 KiB/s Receiving objects:  96% (17942/18689), 17.11 MiB | 440.00 KiB/s Receiving objects:  96% (18111/18689), 17.11 MiB | 440.00 KiB/s Receiving objects:  97% (18129/18689), 17.11 MiB | 440.00 KiB/s Receiving objects:  98% (18316/18689), 17.25 MiB | 409.00 KiB/s Receiving objects:  99% (18503/18689), 17.25 MiB | 409.00 KiB/s Receiving objects:  99% (18554/18689), 17.46 MiB | 420.00 KiB/s remote: Total 18689 (delta 234), reused 122 (delta 122), pack-reused 18403 (from 3)
Receiving objects: 100% (18689/18689), 17.46 MiB | 420.00 KiB/s Receiving objects: 100% (18689/18689), 17.68 MiB | 428.00 KiB/s, done.
Resolving deltas: 100% (12729/12729), done.
jetauto@jetauto-desktop:~/catkin_ws/src$ cd yolov5
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ git branch
* master
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ cat requirements.txt
# YOLOv5 requirements
# Usage: pip install -r requirements.txt

# Base ------------------------------------------------------------------------
matplotlib>=3.3
numpy>=1.23.5
opencv-python>=4.6.0
pillow>=10.3.0
psutil  # system resources
PyYAML>=5.3.1
requests>=2.32.2
scipy>=1.4.1
ultralytics-thop>=2.1.2  # FLOPs computation
torch>=1.8.0  # see https://pytorch.org/get-started/locally (recommended)
torchvision>=0.9.0
ultralytics>=8.4.110  # https://ultralytics.com
# protobuf<=3.20.1  # https://github.com/ultralytics/yolov5/issues/8012

# Logging ---------------------------------------------------------------------
# tensorboard>=2.4.1
# clearml>=1.2.0
# comet_ml

# Plotting --------------------------------------------------------------------
pandas>=1.1.4
seaborn>=0.11.0

# Export ----------------------------------------------------------------------
# coremltools>=6.0  # CoreML export
# onnx>=1.10.0  # ONNX export
# onnxslim>=0.1.82  # ONNX simplifier
# tensorrt  # TensorRT export
# scikit-learn<=1.1.2  # CoreML quantization
# tensorflow>=2.0.0,<=2.19.0  # TF exports (-cpu, -aarch64, -macos)
# tensorflowjs>=3.9.0  # TF.js export
# openvino>=2024.0.0  # OpenVINO export

# Deploy ----------------------------------------------------------------------
packaging  # Migration of deprecated pkg_resources packages
setuptools>=70.0.0 # Snyk vulnerability fix
# tritonclient[all]~=2.24.0

# Extras ----------------------------------------------------------------------
# ipython  # interactive notebook
# mss  # screenshots
# albumentations>=1.0.3
# pycocotools>=2.0.6  # COCO mAP
urllib3>=2.6.0 ; python_version > '3.8' # not directly required, pinned by Snyk to avoid a vulnerability
filelock>=3.20.3 ; python_version >= '3.10' # not directly required, pinned by Snyk to avoid a vulnerability
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ git tag | tail -20
v1.0
v2.0
v3.0
v3.1
v4.0
v5.0
v6.0
v6.1
v6.2
v7.0
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ git checkout v6.2
Note: checking out 'v6.2'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b <new-branch-name>

HEAD is now at d3ea0df8 New YOLOv5 Classification Models (#8956)
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ cat requirements.txt
# YOLOv5 requirements
# Usage: pip install -r requirements.txt

# Base ----------------------------------------
matplotlib>=3.2.2
numpy>=1.18.5
opencv-python>=4.1.1
Pillow>=7.1.2
PyYAML>=5.3.1
requests>=2.23.0
scipy>=1.4.1
torch>=1.7.0
torchvision>=0.8.1
tqdm>=4.64.0
protobuf<=3.20.1  # https://github.com/ultralytics/yolov5/issues/8012

# Logging -------------------------------------
tensorboard>=2.4.1
# wandb
# clearml

# Plotting ------------------------------------
pandas>=1.1.4
seaborn>=0.11.0

# Export --------------------------------------
# coremltools>=5.2  # CoreML export
# onnx>=1.9.0  # ONNX export
# onnx-simplifier>=0.4.1  # ONNX simplifier
# nvidia-pyindex  # TensorRT export
# nvidia-tensorrt  # TensorRT export
# scikit-learn==0.19.2  # CoreML quantization
# tensorflow>=2.4.1  # TFLite export (or tensorflow-cpu, tensorflow-aarch64)
# tensorflowjs>=3.9.0  # TF.js export
# openvino-dev  # OpenVINO export

# Extras --------------------------------------
ipython  # interactive notebook
psutil  # system utilization
thop>=0.1.1  # FLOPs computation
# albumentations>=1.0.3
# pycocotools>=2.0  # COCO mAP
# roboflow
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ python3 -c "
> import PIL
> import yaml
> import requests
> import scipy
> import tqdm
> import pandas
> import seaborn
> print('All Required Packages Found')
> "
Matplotlib created a temporary config/cache directory at /tmp/matplotlib-bsqi4z4s because the default path (/home/jetauto/.cache/matplotlib) is not a writable directory; it is highly recommended to set the MPLCONFIGDIR environment variable to a writable directory, in particular to speed up the import of Matplotlib and to better support multiprocessing.
Matplotlib is building the font cache; this may take a moment.
All Required Packages Found
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ cd ~/catkin_ws/src/yolov5
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ wget https://github.com/ultralytics/yolov5/releases/download/v6.2/yolov5s.pt
--2026-08-06 00:02:05--  https://github.com/ultralytics/yolov5/releases/download/v6.2/yolov5s.pt
Resolving github.com (github.com)... 20.207.73.82
Connecting to github.com (github.com)|20.207.73.82|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://release-assets.githubusercontent.com/github-production-release-asset/264818686/14327886-3839-4fa5-96c3-d52cfa73cdc5?sp=r&sv=2018-11-09&sr=b&spr=https&se=2026-08-05T19%3A14%3A08Z&rscd=attachment%3B+filename%3Dyolov5s.pt&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2026-08-05T18%3A13%3A26Z&ske=2026-08-05T19%3A14%3A08Z&sks=b&skv=2018-11-09&sig=b%2FNdynbCjkSpUDcJhXlVISTaQ5oqNdJoAZuSVYnjY1s%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc4NTk1NjUyNiwibmJmIjoxNzg1OTU0NzI2LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.8NmrHumV8dXPHQRoINLEjt5YfHafioKgsaPLtpGlhiw&response-content-disposition=attachment%3B%20filename%3Dyolov5s.pt&response-content-type=application%2Foctet-stream [following]
--2026-08-06 00:02:06--  https://release-assets.githubusercontent.com/github-production-release-asset/264818686/14327886-3839-4fa5-96c3-d52cfa73cdc5?sp=r&sv=2018-11-09&sr=b&spr=https&se=2026-08-05T19%3A14%3A08Z&rscd=attachment%3B+filename%3Dyolov5s.pt&rsct=application%2Foctet-stream&skoid=96c2d410-5711-43a1-aedd-ab1947aa7ab0&sktid=398a6654-997b-47e9-b12b-9515b896b4de&skt=2026-08-05T18%3A13%3A26Z&ske=2026-08-05T19%3A14%3A08Z&sks=b&skv=2018-11-09&sig=b%2FNdynbCjkSpUDcJhXlVISTaQ5oqNdJoAZuSVYnjY1s%3D&jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmVsZWFzZS1hc3NldHMuZ2l0aHVidXNlcmNvbnRlbnQuY29tIiwia2V5Ijoia2V5MSIsImV4cCI6MTc4NTk1NjUyNiwibmJmIjoxNzg1OTU0NzI2LCJwYXRoIjoicmVsZWFzZWFzc2V0cHJvZHVjdGlvbi5ibG9iLmNvcmUud2luZG93cy5uZXQifQ.8NmrHumV8dXPHQRoINLEjt5YfHafioKgsaPLtpGlhiw&response-content-disposition=attachment%3B%20filename%3Dyolov5s.pt&response-content-type=application%2Foctet-stream
Resolving release-assets.githubusercontent.com (release-assets.githubusercontent.com)... 185.199.108.133, 185.199.110.133, 185.199.111.133, ...
Connecting to release-assets.githubusercontent.com (release-assets.githubusercontent.com)|185.199.108.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 14808437 (14M) [application/octet-stream]
Saving to: ‘yolov5s.pt’

yolov5s.pt      100%[=======>]  14.12M   473KB/s    in 29s

2026-08-06 00:02:36 (497 KB/s) - ‘yolov5s.pt’ saved [14808437/14808437]

jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ ls -lh yolov5s.pt
-rw-rw-r-- 1 jetauto jetauto 15M Aug 17  2022 yolov5s.pt

jetauto@jetauto-desktop:~$ cd ~/catkin_ws/src/yolov5
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ source devel/setup.bash
-bash: devel/setup.bash: No such file or directory
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ source devel/setup.bash
-bash: devel/setup.bash: No such file or directory
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ clear
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ python3 -c "import torch; x=torch.rand(3,3).cuda(); print(x)"
tensor([[0.8535, 0.8998, 0.3317],
        [0.7363, 0.8729, 0.2894],
        [0.5501, 0.3719, 0.6239]], device='cuda:0')
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ python3 -c "import cv2; img=cv2.imread('data/images/zidane.jpg'); print(img.shape)"
(720, 1280, 3)
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ python3 -c "import torchvision; print(torchvision.__version__)"
0.11.0a0+fa347eb
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ python3 -c "import torch; m=torch.load('yolov5s.pt', map_location='cpu'); print(type(m))"
Segmentation fault (core dumped)
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ ls -lh yolov5s.pt
-rw-rw-r-- 1 jetauto jetauto 15M Aug 17  2022 yolov5s.pt
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ sha256sum yolov5s.pt
8b3b748c1e592ddd8868022e8732fde20025197328490623cc16c6f24d0782ee  yolov5s.pt
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ python3 -c "import torch; torch.save({'a':1}, 'test.pt'); print(torch.load('test.pt'))"
{'a': 1}
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ python3 -c "
> with open('yolov5s.pt','rb') as f:
>     print(f.read(16))
> "
b'PK\x03\x04\x00\x00\x08\x08\x00\x00\x00\x00\x00\x00\x00\x00'
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ python3 -c "
> import zipfile
> print(zipfile.is_zipfile('yolov5s.pt'))
> "
True
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ python3 -c "import torch; print(torch.__file__)"
/usr/local/lib/python3.6/dist-packages/torch/__init__.py
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ python3 -c "import torchvision; print(torchvision.__file__)"
/usr/local/lib/python3.6/dist-packages/torchvision/__init__.py
jetauto@jetauto-desktop:~/catkin_ws/src/yolov5$ git rev-parse HEAD
d3ea0df8b9f923685ce5f2555c303b8eddbf83fd
```

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
