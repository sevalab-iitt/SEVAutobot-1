# JetAuto Pro AI Robot Car with 6DOF Vision Robotic Arm Documentation
<img width="1200" height="1200" alt="image" src="https://sevalab-iitt.github.io/project%20equipments/ground%20robo.JPG" />


# JetAuto Pro

## Table of Contents

* Platform Overview
* Primary Objectives
* Key Features
* Hardware Components
* Software Stack
* Functional Capabilities
* Typical Applications
* Prerequisites
* Quick Start
* Repository Structure
* Documentation
* Future Enhancements
* References
* License

---

# Platform Overview

## Overview

JetAuto Pro is an AI-powered autonomous mobile robot developed by Hiwonder for robotics education, research, and application development. It integrates an NVIDIA Jetson embedded computer, mecanum-wheel chassis, robotic arm, LiDAR, and 3D depth camera into a unified ROS-based platform for developing intelligent robotic systems.

The platform enables users to explore autonomous navigation, robotic manipulation, computer vision, artificial intelligence, and embedded robotics through a modular and extensible software architecture.

## Why JetAuto Pro?

JetAuto Pro provides an integrated environment for learning, developing, and testing robotics applications without requiring extensive hardware integration. Its ROS ecosystem and rich sensor suite make it suitable for both educational and research purposes.

---

# Primary Objectives

* Develop autonomous robotic applications.
* Learn and experiment with ROS concepts.
* Perform SLAM and autonomous navigation.
* Implement AI and computer vision algorithms.
* Develop robotic manipulation and pick-and-place applications.
* Integrate multiple sensors for intelligent decision-making.
* Explore embedded AI and robotics research.

---

# Key Features

* Omnidirectional mecanum-wheel mobility
* NVIDIA Jetson-based AI computing
* ROS-based modular software architecture
* 2D LiDAR for mapping and navigation
* 3D depth camera for perception
* Vision-guided robotic arm
* Autonomous navigation and obstacle avoidance
* AI and computer vision support
* Remote operation via SSH and NoMachine
* Expandable hardware and software architecture

---

# Hardware Components

| Component        | Purpose                        |
| ---------------- | ------------------------------ |
| NVIDIA Jetson    | AI computing and ROS execution |
| Mecanum Chassis  | Omnidirectional movement       |
| Encoder Motors   | Motion control and odometry    |
| 2D LiDAR         | Mapping and localization       |
| 3D Depth Camera  | Vision and depth perception    |
| Robotic Arm      | Object manipulation            |
| Servo Controller | Arm joint control              |
| IMU              | Orientation and motion sensing |
| Battery System   | Power supply                   |
| Wireless Network | Remote communication           |

---

# Software Stack

* Ubuntu Linux
* ROS (Robot Operating System)
* Python
* C++
* OpenCV
* CUDA
* RViz
* Gazebo
* MoveIt
* SLAM and Navigation Packages

---

# Functional Capabilities

* Robot motion control
* Odometry estimation
* LiDAR mapping
* Autonomous exploration
* Localization
* Path planning
* Autonomous navigation
* Obstacle avoidance
* Object detection
* Robotic arm control
* Object grasping
* Human–robot interaction
* Remote robot operation

---

# Typical Applications

* Robotics education
* Autonomous navigation research
* Computer vision applications
* AI and deep learning development
* SLAM research
* Warehouse automation
* Embedded AI experimentation
* Human–robot interaction

---

# Prerequisites

Before operating the robot, ensure:

* Battery is charged and connected.
* LiDAR and camera are properly connected.
* Robot is placed on a stable surface.
* Robot and host computer are connected to the same network.
* SSH access is available.
* The ROS workspace (`jetauto_ws`) has been built successfully.

---

# Quick Start

1. Power on the JetAuto Pro.
2. Wait 30–60 seconds for Ubuntu and ROS services to initialize.
3. Connect using SSH or NoMachine.
4. Verify the ROS environment.
5. Launch the required ROS packages or applications.

For detailed setup and configuration instructions, refer to the **docs/** directory.

---

# Repository Structure


---

# Documentation



---

# Future Enhancements

Planned additions include:

* Complete ROS package documentation
* TF frame hierarchy
* Launch file reference
* Sensor calibration guide
* Performance benchmarking
* Remote execution workflows
* System diagnostics
* Maintenance procedures
* Developer contribution guide

---

# References



---

# License

# License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

You are free to use, modify, and distribute this project under the terms of the AGPL-3.0. Any modified versions made available over a network must also make their corresponding source code available under the same license.

For the full license text, see the `LICENSE` file or visit the official GNU AGPL-3.0 license page.






