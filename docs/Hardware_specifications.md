# Hardware Specifications

## Overview

The JetAuto Pro is built around the NVIDIA Jetson Nano embedded computing platform and integrates multiple sensing, actuation, and communication modules to support autonomous navigation, robotic manipulation, and AI-based perception. Its modular hardware architecture enables the development and deployment of ROS-based robotics applications for research, education, and real-world experimentation.

---

# System Overview

| Component | Description |
|-----------|-------------|
| Compute Platform | NVIDIA Jetson Nano Developer Kit |
| Operating System | Ubuntu 18.04 LTS |
| Middleware | ROS Melodic |
| Chassis | Four-Wheel Mecanum Drive |
| Robotic Arm | 6 Degrees of Freedom (6-DOF) |
| Primary Sensors | LiDAR, RGB-D Camera, IMU, Wheel Encoders |

---

# Compute Module

| Component | Specification |
|-----------|---------------|
| Board | NVIDIA Jetson Nano Developer Kit |
| SoC | NVIDIA Tegra X1 |
| CPU | Quad-Core ARM Cortex-A57 |
| GPU | 128-Core NVIDIA Maxwell GPU |
| Memory | 4 GB LPDDR4 |
| Storage | microSD Card |
| Video Acceleration | Hardware H.264 / H.265 Encoding & Decoding |

---

# Sensor Suite

| Sensor | Purpose |
|---------|---------|
| SLAMTEC RPLiDAR A1 | Mapping, Localization, Obstacle Detection |
| Orbbec Astra Pro Plus | RGB-D Vision and Depth Perception |
| IMU | Orientation and Motion Estimation |
| Wheel Encoders | Odometry and Velocity Feedback |

---

# Mobility System

| Component | Description |
|-----------|-------------|
| Chassis | Omnidirectional Mecanum Wheel Base |
| Drive Motors | DC Geared Motors with Magnetic Encoders |
| Suspension | Pendulum Suspension System |
| Motion Modes | Forward, Backward, Sideways, Diagonal, Rotation |

---

# Robotic Arm

| Component | Description |
|-----------|-------------|
| Degrees of Freedom | 6-DOF |
| End Effector | Robotic Gripper |
| Arm Camera | Integrated Close-Range Camera |
| Servo Control | PWM-Based Servo Controller |

---

# Communication Interfaces

| Interface | Purpose |
|-----------|---------|
| USB 3.0 | High-Speed Peripheral Connectivity |
| USB 2.0 | Camera and Peripheral Devices |
| Gigabit Ethernet | Network Communication |
| HDMI | External Display Output |
| GPIO | General-Purpose Input/Output |
| UART | Serial Communication |
| I²C | Sensor Communication |
| SPI | Peripheral Communication |
| MIPI CSI | Camera Interface |
| M.2 Key-E | Optional Wi-Fi Expansion |

---

# Power System

| Component | Description |
|-----------|-------------|
| Battery | Rechargeable Battery Pack |
| Power Distribution | Separate Supply for Compute and Motor Control |
| Cooling | Heat Sink and Cooling Fan |
| Motor Controller | Dedicated Expansion Controller Board |

---

# Software Environment

- Ubuntu 18.04 LTS
- ROS Melodic
- Python
- C++
- OpenCV
- CUDA
- TensorRT
- RViz
- Gazebo
- MoveIt

---

# Key Hardware Capabilities

- AI-accelerated onboard computing
- Autonomous navigation
- LiDAR-based mapping and localization
- RGB-D perception
- Omnidirectional mobility
- Robotic manipulation
- Sensor fusion
- Remote operation through SSH and NoMachine

---



