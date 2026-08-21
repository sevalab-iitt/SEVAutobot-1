```
JetAuto/
├── llama.cpp/
│   └── llamaJetsonNanoCUDA/
│
├── catkin_ws/
│   └── src/
│       ├── jetauto_software/
│       ├── jetauto_slam/
│       ├── yolov5/
│       └── ...
│
├── jetauto_software/
│   ├── servo_tool/
│   │   └── BusServoControl.py
│   └── ...
│
├── jetauto_third_party/
│   ├── ORB_SLAM2/
│   ├── ORB_SLAM3/
│   ├── YDLidar-SDK/
│   ├── AstraSDK/
│   ├── yolov5/
│   └── octomap/
│
├── scripts/
│   ├── camera/
│   ├── lidar/
│   ├── object_detection/
│   ├── slam/
│   ├── servo/
│   └── system/
│
├── datasets/
│
└── documentation/
```

```
Camera / Astra

camera_info.py
capture_images.py
capture_video.py
save_metadata.py

YOLO

YOLOv5 setup/testing scripts
model loading/testing code
camera/object-detection experiments

Servo

BusServoControl.py
servo testing commands/scripts
servo voltage testing

LiDAR

RPLiDAR/A1 launch/configuration
/scan testing
LiDAR data collection/testing
LiDAR-related Python scripts

SLAM

gmapping
RTAB-Map
Karto
Hector
Cartographer
SLAM launch/config modifications
RViz/TF/odom testing

ROS

catkin_ws packages
launch files
nodes/scripts
topic/service testing
robot control scripts

ORB-SLAM

ORB_SLAM2
ORB_SLAM3
build/configuration changes
camera-related experiments

Object detection / tracking

YOLOv5
DeepSORT/ByteTrack-related experiments
MOT-related scripts

System / Jetson

storage cleanup commands
CUDA checks
TensorRT checks
Python package checks
GPU/CPU testing
RAM/swap checks
```
