 
> **ROS Melodic** · Workspace: `~/jetauto_ws` · Ubuntu 18.04

## Table of Contents
1. [What is a Driver in ROS?](#1-what-is-a-driver-in-ros)
2. [Step 1 — SSH Into the Robot](#2-step-1--ssh-into-the-robot)
3. [Step 2 — Find All Packages](#3-step-2--find-all-packages-driver-containers)
4. [Step 3 — Find All Driver Python Files](#4-step-3--find-all-driver-python-files)
5. [Step 4 — Find Each Specific Driver Path](#5-step-4--find-each-specific-driver-path)
6. [Step 5 — Read Each Driver File](#6-step-5--read-each-driver-file)
7. [Step 6 — Find Hardware Device Ports](#7-step-6--find-hardware-device-ports)
8. [Step 7 — Run the Auto-Scanner Script](#8-step-7--run-the-auto-scanner-script)
9. [Step 8 — Copy Report to Your Laptop](#9-step-8--copy-report-to-your-laptop)
10. [Step 9 — Fill This Table With Your Findings](#10-step-9--fill-this-table-with-your-findings)
11. [Quick Command Reference](#11-quick-command-reference)

---

## 1. What is a Driver in ROS?

In ROS, a **driver** is a Python or C++ node that:

- Talks directly to a hardware device (camera, LiDAR, motors, servos)
- Reads sensor data and publishes it to a ROS topic
- Receives ROS commands and sends them to the hardware

Every driver lives as a `.py` or `.cpp` file inside a ROS package under `~/jetauto_ws/src/`.

---

## 2. Step 1 — SSH Into the Robot

```bash
# From your laptop
ssh jetauto@192.168.0.114        
  password: hiwonder

# Source the workspace immediately
source ~/jetauto_ws/devel/setup.bash
```

---

## 3. Step 2 — Find All Packages (Driver Containers)

```bash
# List all packages in the workspace
ls ~/jetauto_ws/src/

# List ONLY directory names (clean output)
find ~/jetauto_ws/src/ -maxdepth 1 -type d | sort

# Find every package.xml (one per package)
find ~/jetauto_ws/src/ -name "package.xml" \
  | sed 's|/package.xml||' \
  | sed 's|.*/||' \
  | sort
```

> ## Expected:
> <img width="928" height="283" alt="image" src="https://github.com/user-attachments/assets/526eb275-a5e7-4268-9721-fcb1415f17cd" />


---

## 4. Step 3 — Find All Driver Python Files

```bash
# ALL Python files — full paths
find ~/jetauto_ws/src/ -name "*.py" | sort

# Count total
find ~/jetauto_ws/src/ -name "*.py" | wc -l

# ALL launch files ( it show how drivers are started)
find ~/jetauto_ws/src/ -name "*.launch" | sort
```
 ## Expected:
 <img width="607" height="230" alt="image" src="https://github.com/user-attachments/assets/024c17e8-530f-4f24-a06d-e1f17f0246e7" />

 <img width="624" height="137" alt="image" src="https://github.com/user-attachments/assets/1bfdab74-18c8-489d-b2f9-6b2161d3eaa2" />

 

---

## 5. Step 4 — Find Each Specific Driver Path

Run each command to find the exact file path of each driver:

### Camera Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "image_raw\|usb_cam\|VideoCapture" 2>/dev/null
```
## Expected:
<img width="656" height="176" alt="image" src="https://github.com/user-attachments/assets/618b106e-3589-479c-afd1-3cb17a1bfcb1" />

### LiDAR Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "LaserScan\|/scan\|ydlidar" 2>/dev/null
```
## Expected:
<img width="736" height="97" alt="image" src="https://github.com/user-attachments/assets/34625651-81a5-4234-983d-b0c4dab23f49" />

### Motor / Chassis Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "cmd_vel\|Twist\|motor" 2>/dev/null
```
## Expected:
<img width="905" height="216" alt="image" src="https://github.com/user-attachments/assets/1511e1b5-75f7-4842-a88e-d6a78b7f662d" />

### Servo / Arm Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "servo\|HTD\|bus_servo\|MultiRawIdPosDur" 2>/dev/null
```
## Expected: 
 <img width="944" height="217" alt="image" src="https://github.com/user-attachments/assets/40502971-acf8-44db-ad2e-525e02c826fa" />


### IMU Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "Imu\|imu\|accelerometer" 2>/dev/null
```
## Expected:
 <img width="957" height="239" alt="image" src="https://github.com/user-attachments/assets/7f34866a-96b7-406f-b3ef-e187ad18d9b4" />

 
### Depth Camera Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "depth\|PointCloud\|astra\|openni" 2>/dev/null
```
## Expected:
 <img width="747" height="218" alt="image" src="https://github.com/user-attachments/assets/21dc7820-15ff-4eeb-b244-0fb7bff93035" />

---

## 6. Step 5 — Read Each Driver File

Once you have the path from Step 4, read it:

```bash
# Read full file
cat ~/jetauto_ws/src/PACKAGE_NAME/scripts/DRIVER_FILE.py
 
# Read with line numbers
cat -n ~/jetauto_ws/src/PACKAGE_NAME/scripts/DRIVER_FILE.py
 
# Read only first 50 lines (see imports + node init)
head -50 ~/jetauto_ws/src/PACKAGE_NAME/scripts/DRIVER_FILE.py
 
# Search for subscriber/publisher lines inside the file
grep -n "Subscriber\|Publisher\|rospy.init" \
  ~/jetauto_ws/src/PACKAGE_NAME/scripts/DRIVER_FILE.py
```
## Expected:
<img width="874" height="114" alt="image" src="https://github.com/user-attachments/assets/1f5f6fa8-a995-4a1c-8f9e-2d8f5af0b2ac" />

>  **Note — What to look for inside each driver**
>
> | Pattern | Meaning |
> |---|---|
> | `rospy.init_node(...)` | Node name |
> | `rospy.Subscriber(...)` | Topics it reads from |
> | `rospy.Publisher(...)` | Topics it publishes to |
> | `rospy.Rate(...)` | Publishing frequency |
> | `/dev/ttyUSB*` | Hardware port it uses |

---

## 7. Step 6 — Find Hardware Device Ports

```bash
# All connected USB serial ports
ls /dev/ttyUSB*
ls /dev/ttyACM*

# All cameras
ls /dev/video*

# See what is on each port (vendor/product ID)
dmesg | grep tty  | tail -20
dmesg | grep usb  | tail -20
dmesg | grep video| tail -10

# Detailed USB device list
lsusb

# Match port to device automatically
for port in /dev/ttyUSB*; do
  echo "Port: $port"
  udevadm info -a -n $port | grep -E "idVendor|idProduct|product" | head -4
  echo "---"
done
```

---

## 8. Step 7 — Run the Auto-Scanner Script

Save and run this script — it maps all drivers automatically:

```bash
nano ~/jetauto_ws/src/scan_drivers.py
```

 ## Expected :

 <img width="599" height="422" alt="image" src="https://github.com/user-attachments/assets/820f549e-8e8e-46ae-9c20-711c58e38908" />

<img width="601" height="391" alt="image" src="https://github.com/user-attachments/assets/1b42335a-0391-4f58-b033-ab9b32ad99ec" />


Run it:
 
python3 ~/jetauto_ws/src/scan_drivers.py

## Expected:
 <img width="854" height="437" alt="image" src="https://github.com/user-attachments/assets/df87a37a-2e17-495d-9cc3-c99b078fbd3b" />

# View the saved report
cat ~/driver_report.txt

## Expected:
 <img width="737" height="365" alt="image" src="https://github.com/user-attachments/assets/943c3920-5e19-42df-b920-4339bcd9c80b" />

---

## 9. Step 8 — Copy Report to Your Laptop

```bash
# Run this on YOUR LAPTOP (not robot)
scp jetauto@192.168.1.xxx:~/driver_report.txt ./
 

---

## 10. Step 9 —  Driver Table
 
| Driver | File Path | Launch File | Node Name |
|---|---|---|---|
| **Camera (RGB)** | `jetauto_ws/src/third_party/ros_astra_camera/ros/astra_camera_node.cpp` | `jetauto_peripherals/launch/astrapro.launch` | `astra_camera_node` |
| **Depth Camera** | `jetauto_ws/src/third_party/ros_astra_camera/ros/astra_camera_node.cpp` | `jetauto_peripherals/launch/astrapro.launch` | `astra_camera_node` |
| **LiDAR (RPLiDAR)** | `jetauto_ws/src/third_party/rplidar_ros/sdk/src/rplidar_driver.cpp` | `jetauto_peripherals/launch/include/rplidar.launch` | `rplidarNode` |
| **LiDAR (YDLiDAR alt.)** | `jetauto_ws/src/third_party/ydlidar_ros_driver/` | `jetauto_peripherals/launch/include/ydlidar.launch` | `ydlidar_lidar_publisher` |
| **Motor Control** | `jetauto_ws/src/jetauto_driver/jetauto_controller/scripts/jetauto_controller_main.py` | — | `jetauto_controller` |
| **Servo / Arm** | `jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py` | — | `hiwonder_servo_manager` |
| **IMU** | `jetauto_ws/src/third_party/mpu_6050_driver/scripts/imu_node.py` | `jetauto_peripherals/launch/imu.launch` | `imu_node` |

---
 
## Verifying Live Topics  

 
roslaunch jetauto_bringup bringup.launch

<img width="877" height="448" alt="image" src="https://github.com/user-attachments/assets/43202725-5868-4104-9395-8f59dbd38940" />
<img width="839" height="460" alt="image" src="https://github.com/user-attachments/assets/f1bcac62-f03e-4d03-a576-0a91d0402772" />
<img width="591" height="470" alt="image" src="https://github.com/user-attachments/assets/15467040-5617-44b9-8844-4e2c6213b841" />
<img width="635" height="440" alt="image" src="https://github.com/user-attachments/assets/022e6211-74dc-410f-9b4e-9ef5c9990dfd" />
 
rostopic list | grep -i "camera\|scan\|imu"

<img width="522" height="65" alt="image" src="https://github.com/user-attachments/assets/af4aa713-acc8-4645-9ed3-ce95d65ad61a" />

```

| Expected Topic | Source Node |
|---|---|
| `/scan` | RPLiDAR or YDLiDAR node |
| `/camera/rgb/image_raw` | `astra_camera_node` |
| `/camera/depth/image_raw` | `astra_camera_node` |
| `/imu/data` | `imu_node` |
| `/jetauto_controller/cmd_vel` | `jetauto_controller` |
---

## 11. Quick Command Reference

| Goal | Command |
|---|---|
| List all packages | `ls ~/jetauto_ws/src/` |
| Find all .py files | `find ~/jetauto_ws/src/ -name "*.py" \| sort` |
| Find camera driver | `grep -rl "image_raw" ~/jetauto_ws/src/` |
| Find LiDAR driver | `grep -rl "LaserScan" ~/jetauto_ws/src/` |
| Find motor driver | `grep -rl "cmd_vel" ~/jetauto_ws/src/` |
| Find servo driver | `grep -rl "servo" ~/jetauto_ws/src/` |
| Read a driver file | `cat -n PATH/driver.py` |
| Find USB ports | `ls /dev/ttyUSB* /dev/video*` |
| Run auto-scanner | `python3 ~/jetauto_ws/src/scan_drivers.py` |
| Copy report to laptop | `scp jetauto@IP:~/driver_report.txt ./` |

> 
