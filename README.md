<p align="center">
  <img width="600" alt="JetAuto Pro" src="https://sevalab-iitt.github.io/project%20equipments/ground%20robo.JPG" />
</p>

<h1 align="center">JetAuto Pro</h1>
<p align="center"><b>AI-Powered Autonomous Mobile Robot with 6DOF Vision-Guided Robotic Arm</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/OS-Ubuntu-orange" />
  <img src="https://img.shields.io/badge/Framework-ROS-blue" />
  <img src="https://img.shields.io/badge/Compute-NVIDIA%20Jetson-76B900" />
  <img src="https://img.shields.io/badge/License-AGPL--3.0-lightgrey" />
</p>

---

## Table of Contents

- [Overview](#overview)
- [Why JetAuto Pro](#why-jetauto-pro)
- [Objectives](#objectives)
- [Key Features](#key-features)
- [Hardware Components](#hardware-components)
- [Software Stack](#software-stack)
- [Functional Capabilities](#functional-capabilities)
- [Typical Applications](#typical-applications)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Repository Structure](#repository-structure)
- [Documentation](#documentation)
- [Roadmap](#roadmap)
- [References](#references)
- [License](#license)

---

## Overview

**JetAuto Pro** is an AI-powered autonomous mobile robot built by **Hiwonder** for robotics education, research, and applied development. It combines an **NVIDIA Jetson** embedded computer, a **mecanum-wheel chassis**, a **6DOF robotic arm**, **2D LiDAR**, and a **3D depth camera** into a single ROS-based platform for building intelligent robotic systems.

The platform is designed to support work across autonomous navigation, robotic manipulation, computer vision, and applied AI — all on top of a modular, extensible software architecture.

## Why JetAuto Pro

Standing up a capable robotics research platform usually means stitching together a chassis, sensors, compute, and an arm — and then integrating all of it yourself. JetAuto Pro removes that overhead. Its ROS ecosystem and sensor suite arrive pre-integrated, so time goes into experimentation and development rather than hardware wiring, making it equally suited to classroom use and research prototyping.

---

## Objectives

- Develop autonomous robotic applications
- Learn and experiment with core ROS concepts
- Perform SLAM and autonomous navigation
- Implement AI and computer vision algorithms
- Build robotic manipulation and pick-and-place workflows
- Fuse multiple sensors for intelligent decision-making
- Explore embedded AI and robotics research

---

## Key Features

| Feature | Description |
|---|---|
| **Omnidirectional Mobility** | Mecanum-wheel chassis enables movement in any direction without turning |
| **AI Computing** | NVIDIA Jetson provides onboard compute for real-time inference |
| **ROS Architecture** | Modular, package-based software design |
| **2D LiDAR** | Supports mapping, localization, and obstacle detection |
| **3D Depth Camera** | Enables spatial perception and object recognition |
| **Vision-Guided Arm** | 6DOF arm capable of coordinated pick-and-place tasks |
| **Autonomous Navigation** | Path planning with real-time obstacle avoidance |
| **Remote Operation** | Accessible via SSH and NoMachine |
| **Extensibility** | Open hardware and software architecture for custom development |

---

## Hardware Components

| Component | Purpose |
|---|---|
| NVIDIA Jetson | AI computing and ROS execution |
| Mecanum Chassis | Omnidirectional movement |
| Encoder Motors | Motion control and odometry |
| 2D LiDAR | Mapping and localization |
| 3D Depth Camera | Vision and depth perception |
| Robotic Arm (6DOF) | Object manipulation |
| Servo Controller | Arm joint control |
| IMU | Orientation and motion sensing |
| Battery System | Power supply |
| Wireless Network Module | Remote communication |

---

## Software Stack

- Ubuntu Linux
- ROS (Robot Operating System)
- Python & C++
- OpenCV
- CUDA
- RViz
- Gazebo
- MoveIt
- SLAM and Navigation packages

---

## Functional Capabilities

- Robot motion control and odometry estimation
- LiDAR-based mapping and autonomous exploration
- Localization and path planning
- Autonomous navigation with obstacle avoidance
- Object detection and recognition
- Robotic arm control and object grasping
- Human–robot interaction
- Remote robot operation

---

## Typical Applications

- Robotics education and coursework
- Autonomous navigation research
- Computer vision applications
- AI and deep learning development
- SLAM research
- Warehouse automation prototyping
- Embedded AI experimentation
- Human–robot interaction studies

---

## Prerequisites

Before operating the robot, confirm the following:

- [ ] Battery is charged and connected
- [ ] LiDAR and camera are properly connected
- [ ] Robot is placed on a stable, level surface
- [ ] Robot and host computer are on the same network
- [ ] SSH access is available
- [ ] The ROS workspace (`jetauto_ws`) has been built successfully

---

## Quick Start

```bash
# 1. Power on the JetAuto Pro
#    (wait 30-60s for Ubuntu and ROS services to initialize)

# 2. Connect via SSH
ssh jetauto@<robot-ip-address>

# 3. Verify the ROS environment
roscore &
rosnode list

# 4. Launch the required ROS packages
roslaunch jetauto_bringup jetauto_bringup.launch
```

Alternatively, connect via **NoMachine** for a full remote desktop session.

For detailed setup and configuration instructions, refer to the [`docs/`](./docs) directory.

---

## Repository Structure

```
jetauto_ws/
├── src/                # ROS packages and source code
├── docs/               # Setup guides and technical documentation
├── config/             # Robot and sensor configuration files
├── launch/             # ROS launch files
└── scripts/            # Utility and helper scripts
```

---

## Documentation

Full technical documentation — including package references, TF frame hierarchy, and calibration guides — lives in the [`docs/`](./docs) directory and will be expanded as outlined in the [Roadmap](#roadmap).

---

## Roadmap

Planned additions to this documentation and platform include:

- [ ] Complete ROS package reference
- [ ] TF frame hierarchy documentation
- [ ] Launch file reference
- [ ] Sensor calibration guide
- [ ] Performance benchmarking
- [ ] Remote execution workflows
- [ ] System diagnostics guide
- [ ] Maintenance procedures
- [ ] Developer contribution guide

---

## References

- [Hiwonder Official Website](https://www.hiwonder.com)
- [ROS Documentation](https://www.ros.org)
- [NVIDIA Jetson Developer Resources](https://developer.nvidia.com/embedded-computing)

---

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

You are free to use, modify, and distribute this project under the terms of the AGPL-3.0. Any modified version made available over a network must also make its corresponding source code available under the same license.

See the [`LICENSE`](./LICENSE) file or the [official AGPL-3.0 license text](https://www.gnu.org/licenses/agpl-3.0.html) for full details.
