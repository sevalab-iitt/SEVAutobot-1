 
# JetAuto Pro — System Architecture  

> Full boot-to-application software stack, and how to inspect what the `bringup` launch file actually starts.
> **ROS Melodic** · Workspace: `~/jetauto_ws` · Jetson Nano

## Table of Contents
1. [System Architecture Overview](#1-system-architecture-overview)
2. [Architecture Layers Explained](#2-architecture-layers-explained)
3. [Inspecting the Bringup Launch File](#3-inspecting-the-bringup-launch-file)
4. [Typical Nodes Started by Bringup](#4-typical-nodes-started-by-bringup)
5. [Topics & Services After Bringup](#5-topics--services-after-bringup)
6. [Application Layer](#6-application-layer)

---

## 1. System Architecture Overview

```mermaid
flowchart TD
    A[Power ON Robot] --> B[Ubuntu OS Boots]
    B --> C[ROS Environment Loaded<br/>setup.bash sourced]
    C --> D[Bringup Launch File Starts<br/>roslaunch jetauto_xxx bringup.launch]
    D --> E[ROS Master Starts<br/>roscore]
    E --> F[Drivers Initialize]
    F --> F1[Camera]
    F --> F2[LiDAR]
    F --> F3[IMU]
    F --> F4[Motors]
    F --> F5[Servo / Arm]
    F1 --> G[ROS Nodes Launched]
    F2 --> G
    F3 --> G
    F4 --> G
    F5 --> G
    G --> H[Topics & Services Available]
    H --> I[Run Application Layer]
    I --> I1[Object Detection]
    I --> I2[Object Tracking]
    I --> I3[Navigation]
    I --> I4[SLAM]
```

---

## 2. Architecture Layers Explained

| Layer | What Happens | Key File / Command |
|---|---|---|
| **1. Power ON** | Jetson Nano boots from SD/eMMC | — |
| **2. Ubuntu OS** | Ubuntu 18.04 kernel + services start | `systemctl status` |
| **3. ROS Environment** | Workspace env vars loaded into shell | `source ~/jetauto_ws/devel/setup.bash` |
| **4. Bringup Launch** | Master launch file is triggered (often on boot via systemd/autostart, or manually) | `roslaunch jetauto_bringup bringup.launch` (exact package/name to confirm — see Section 3) |
| **5. ROS Master** | `roscore` starts (usually auto-started inside the bringup launch via `<master>` or implicitly) | `rosnode list` to confirm it's up |
| **6. Drivers Initialize** | Each hardware driver node starts: camera, LiDAR, IMU, motor controller, servo controller | See driver paths from the [Driver Documentation Guide] |
| **7. Nodes Launched** | All driver + utility nodes register with the master | `rosnode list` |
| **8. Topics & Services** | Sensor topics and control services become available for subscription | `rostopic list`, `rosservice list` |
| **9. Application Layer** | Higher-level packages (detection, tracking, nav, SLAM) subscribe to topics and publish commands | `roslaunch jetauto_app <app>.launch` |

---
## 3. Inspecting the Bringup Launch File

Actual trace performed on the robot (`jetauto@jetauto-desktop`):

### Step 1 — List All Packages in the Workspace
```bash
cd ~/jetauto_ws/src
ls
```
 ## Output:
<img width="350" height="53" alt="image" src="https://github.com/user-attachments/assets/6b8d58a1-1302-4377-9268-0afe8d007309" />
 

### Step 2 — Enter the Bringup Package
```bash
cd jetauto_bringup
ls
```
  ## Output:
 <img width="310" height="26" alt="image" src="https://github.com/user-attachments/assets/2b00d34e-11f1-46d7-9f50-3d5cf19e536e" />

> The `service` folder is the giveaway — this package also manages a **systemd service**, not just a launch file. See Step 4.

### Step 3 — Enter the Launch Folder
```bash
cd launch
ls
```
  ## Output:
 <img width="274" height="29" alt="image" src="https://github.com/user-attachments/assets/7a1ea97a-2607-4025-84ff-bac652982504" />


### Step 4 — Read bringup.launch
```bash
cat bringup.launch
```
 ## Key contents found: 
 
 <img width="358" height="250" alt="image" src="https://github.com/user-attachments/assets/0aaf1bed-362e-4510-8105-94eda364a880" />
<img width="360" height="349" alt="image" src="https://github.com/user-attachments/assets/fa5a948f-1d62-449b-8734-ab05c8a604f5" />


> **Important finding:** `bringup.launch` is wired to **`start_app_node.service`** — a systemd service. This means bringup is normally started **automatically on boot**, not by manually running `roslaunch`. Manage it with:

 
### Step 5 — See the Full Argument / Include List
```bash
# View the rest of the file (it was cut off above)
cat ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch | less

# Pull out just the <arg> definitions (camera/device names, topics)
grep -n "<arg name" ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch

# Pull out every <include> — these are the real driver launch files being pulled in
grep -n "<include\|file=" ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch

# Also check the second launch file in this package
cat ~/jetauto_ws/src/jetauto_bringup/launch/rosbridge.launch
```
 
```bash
# Recursively trace every included launch file from bringup
python3 - <<'EOF'
import re, os

start = os.path.expanduser("~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch")
seen = set()

def trace(path, depth=0):
    if path in seen or not os.path.exists(path):
        return
    seen.add(path)
    print("  " * depth + f"-> {path}")
    txt = open(path, errors="ignore").read()
    for inc in re.findall(r'file="\$\(find (\w+)\)/(.*?)"', txt):
        pkg, rel = inc
        # crude resolve - adjust WS path if packages aren't directly under src/<pkg>
        guess = os.path.expanduser(f"~/jetauto_ws/src/{pkg}/{rel}")
        trace(guess, depth + 1)

trace(start)
EOF
```
## Output:
<img width="631" height="196" alt="image" src="https://github.com/user-attachments/assets/8811afe0-6ee3-4c0f-8fed-f4e2f6ab279c" />

---

## 4. Typical Nodes Started by Bringup

| Driver | Node Name | Launch File | Hardware Port |
|--------|-----------|-------------|---------------|
| Camera | `usb_cam` (from `$(arg usb_cam_name)`) | `jetauto_peripherals/launch/usb_cam.launch` | `/dev/usb_cam` |
| LiDAR | `rplidarNode` | `jetauto_peripherals/launch/include/rplidar.launch` | `/dev/lidar` (mapped from `/dev/ttyUSB0` using udev rules) |
| IMU | `imu` | `jetauto_peripherals/launch/imu.launch` | `I2C` |
| Motor Control | `jetauto_controller` | `jetauto_driver/jetauto_controller/launch/jetauto_controller.launch` |  |
| Servo / Arm | `hiwonder_servo_manager` | `jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/launch/controller_manager.launch` | `/dev/ttyTHS1` |
| Robot Description | `robot_state_publisher` | `jetauto_peripherals/launch/imu.launch` | — |

---

## 5. Topics & Services After Bringup

 
## Once bringup is running,  to list everything live

rostopic list

<img width="461" height="458" alt="image" src="https://github.com/user-attachments/assets/a9da590f-2b95-4b2a-a24f-8025266c7c1e" />
<img width="424" height="464" alt="image" src="https://github.com/user-attachments/assets/3dba6158-f400-46ce-992e-127358e9ffd1" />


rosservice list

<img width="540" height="463" alt="image" src="https://github.com/user-attachments/assets/7612a975-4e13-4498-b89f-297907e53742" />

rosnode list

<img width="402" height="464" alt="image" src="https://github.com/user-attachments/assets/697be8af-39bc-4252-af48-578867ea56cc" />

## Check publish rate of a sensor topic  

rostopic hz /scan

<img width="494" height="363" alt="image" src="https://github.com/user-attachments/assets/01363051-b2df-4346-96ab-6193e8f22c6a" />

rostopic hz /camera/rgb/image_raw
rostopic hz /imu/data
```

| Common Topic | Published By | Typical Use |
|---|---|---|
| `/scan` | LiDAR driver | Obstacle detection, SLAM |
| `/camera/rgb/image_raw` | Camera driver | Object detection/tracking |
| `/imu/data` | IMU driver | Orientation, odometry fusion |
| `/cmd_vel` | Navigation / teleop | Motor control input |
| `/odom` | Motor controller | Position estimate |
| `/joint_states` | Servo/arm driver | Arm position feedback |

---

## 6. Application Layer

Everything above is infrastructure — the application layer is what we actually run on top of it:

| Application | Subscribes To | Publishes To |
|---|---|---|
| Object Detection | `/camera/rgb/image_raw` | `/detected_objects` |
| Object Tracking | `/camera/rgb/image_raw`, `/detected_objects` | `/tracked_objects` |
| Navigation | `/scan`, `/odom`, `/map` | `/cmd_vel` |
| SLAM | `/scan`, `/odom`, `/imu/data` | `/map` |

```bash
# Launch an application on top of an already-running bringup
roslaunch jetauto_app object_detection.launch
roslaunch jetauto_navigation navigation.launch
roslaunch jetauto_slam slam.launch
```

 
