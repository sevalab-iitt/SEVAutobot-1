# JetAuto Pro Overview

## Introduction

JetAuto Pro is an autonomous mobile robot platform powered by the NVIDIA Jetson Nano Developer Kit. The platform integrates computer vision, depth sensing, robotic manipulation, and autonomous navigation capabilities into a single system.

It is designed for robotics development, artificial intelligence applications, computer vision projects, mapping, navigation, and ROS-based research.

---

## Hardware Components

| Component    | Description                          |
| ------------ | ------------------------------------ |
| Compute Unit | NVIDIA Jetson Nano Developer Kit     |
| LiDAR        | SLAMTEC RPLiDAR A1                   |
| Depth Camera | Orbbec Astra Pro Plus                |
| Mobile Base  | Mecanum-Wheel Chassis                |
| Robotic Arm  | 6-DOF Robotic Arm                    |
| Controller   | Expansion Board and Motor Controller |
| Power System | Rechargeable Battery Pack            |

---

## Software Environment

| Component        | Details                    |
| ---------------- | -------------------------- |
| Operating System | Ubuntu 18.04.6 LTS         |
| ROS Version      | ROS Melodic Morenia        |
| Architecture     | ARM64 (aarch64)            |
| Username         | jetauto                    |
| ROS Workspace    | `/home/jetauto/jetauto_ws` |

---

## System Architecture

```text
JetAuto Pro
│
├── Jetson Nano
│
├── Sensors
│   ├── RPLiDAR A1
│   ├── Astra Pro Plus Camera
│   └── IMU
│
├── Actuators
│   ├── Mecanum Wheels
│   └── 6-DOF Robotic Arm
│
└── ROS Software Stack
```

---

## Main Capabilities

The JetAuto Pro platform supports:

* Object Detection
* Object Tracking
* Autonomous Navigation
* Obstacle Avoidance
* SLAM (Simultaneous Localization and Mapping)
* Robotic Arm Control
* Sensor Data Collection
* ROS Application Development

---

## Documentation Scope

This documentation covers:

1. Hardware Specifications
2. Powering On and Connecting to the Robot
3. Sensor Overview
4. ROS Workspace Structure
5. Sensor Verification
6. Data Collection and Recording
7. Object Detection and Tracking Workflows
8. Mapping and Navigation
9. Troubleshooting and Maintenance

The purpose of this documentation is to provide a practical guide for understanding, operating, and developing applications on the JetAuto Pro platform.

