# JetAuto Pro AI Robot Car with 6DOF Vision Robotic Arm Documentation
<img width="1200" height="1200" alt="image" src="https://sevalab-iitt.github.io/project%20equipments/ground%20robo.JPG" />

# Getting Started

## Prerequisites

Before powering on the robot, ensure:

* Battery is connected
* LiDAR cable is connected
* Camera cable is connected
* Robot is placed on a stable surface
* Emergency stop procedure is known

---

## Powering On

1. Turn on the main power switch.
2. Wait for the Jetson Nano to boot.
3. Wait approximately 30–60 seconds.
4. Listen for the startup beep.
5. Verify that status LEDs are active.

---

## Verify Network Connection

Check the robot IP address:

```bash
hostname -I
```

Example:

```text
192.168.0.114
```

---

## Connect to the Robot

### SSH Connection

```bash
ssh jetauto@<robot_ip>
```

Example:

```bash
ssh jetauto@192.168.0.114
```

---

## Verify ROS Environment

Check ROS version:

```bash
rosversion -d
```

Expected:

```text
melodic
```

---

## Verify ROS Master

```bash
rostopic list
```

Expected:

A list of active ROS topics.

---

## Verify Workspace

Navigate to the workspace:

```bash
cd ~/jetauto_ws
```

Check workspace structure:

```bash
ls
```

Expected folders:

```text
build
devel
src
```

---

## Verify Connected Devices

Check USB devices:

```bash
lsusb
```

Check serial devices:

```bash
ls /dev/ttyUSB*
```

---

## System Information

Display system information:

```bash
neofetch
```

Useful information:

* Operating System
* Kernel Version
* CPU
* Memory
* Hostname

---

## Next Steps

After completing the above checks:

1. Verify LiDAR
2. Verify Camera
3. Verify Chassis Control
4. Verify Robotic Arm
5. Start application workflows

