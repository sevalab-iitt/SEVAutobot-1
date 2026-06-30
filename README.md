# JetAuto Pro AI Robot Car with 6DOF Vision Robotic Arm Documentation
<img width="1200" height="1200" alt="image" src="https://sevalab-iitt.github.io/project%20equipments/ground%20robo.JPG" />


# JetAuto Pro – Platform Overview

## Overview

JetAuto Pro is an AI-powered autonomous mobile robot developed by Hiwonder for robotics education, research, and application development. It combines a mecanum-wheel mobile base, an NVIDIA Jetson embedded computer, a vision-guided robotic arm, LiDAR, and a 3D depth camera into a single platform capable of performing autonomous navigation, perception, manipulation, and human–robot interaction. The platform is designed around the Robot Operating System (ROS), enabling modular software development and seamless communication between sensors, actuators, and control nodes.

The robot serves as a complete development platform for learning and implementing robotics concepts such as localization, mapping, path planning, computer vision, robotic manipulation, machine learning, and autonomous decision-making. Its open software architecture allows developers and researchers to customize existing ROS packages or integrate their own algorithms for advanced robotics applications.

---

# Primary Objectives

* Develop and test autonomous robotic applications.
* Learn ROS architecture, topics, services, actions, and node communication.
* Perform SLAM (Simultaneous Localization and Mapping).
* Implement autonomous navigation and obstacle avoidance.
* Develop computer vision and AI-based perception systems.
* Control a robotic manipulator for object detection, grasping, and sorting.
* Integrate multiple sensors for real-time robotic decision making.
* Provide an educational platform for robotics, AI, and embedded system development.

---

# Key Features

* Omnidirectional mecanum-wheel drive for smooth movement in all directions.
* NVIDIA Jetson-based onboard computing for AI inference and robotics applications.
* ROS-based modular software framework.
* 2D LiDAR for mapping, localization, and navigation.
* 3D depth camera for depth perception and object recognition.
* Vision-guided robotic arm for autonomous manipulation tasks.
* Real-time obstacle detection and avoidance.
* Autonomous path planning and waypoint navigation.
* Support for computer vision using OpenCV and deep learning frameworks.
* Wireless remote operation through SSH, NoMachine, and game controller.
* Expandable hardware and software architecture for research and development.

---

# Hardware Components

The JetAuto Pro integrates the following major hardware modules:

| Component                       | Purpose                                                   |
| ------------------------------- | --------------------------------------------------------- |
| NVIDIA Jetson Embedded Computer | Executes ROS nodes, AI models, and application software   |
| Mecanum Wheel Chassis           | Omnidirectional robot locomotion                          |
| High-Precision Encoder Motors   | Closed-loop motion control and odometry                   |
| 2D LiDAR                        | Environment scanning, SLAM, and navigation                |
| 3D Depth Camera                 | Object detection, depth estimation, and vision processing |
| Vision Robotic Arm              | Pick-and-place operations and object manipulation         |
| Servo Controller                | Controls robotic arm joints                               |
| IMU                             | Measures orientation and robot motion                     |
| Battery System                  | Supplies power to the onboard components                  |
| Wireless Communication          | Remote monitoring and robot control                       |

---

# Software Stack

The robot software ecosystem is primarily built upon ROS and consists of multiple interacting modules.

* Ubuntu Linux
* Robot Operating System (ROS)
* Python and C++
* OpenCV
* NVIDIA CUDA acceleration
* RViz
* Gazebo (simulation)
* MoveIt (robot arm planning)
* SLAM and Navigation packages
* Camera and LiDAR drivers

---

# Functional Capabilities

JetAuto Pro supports a wide range of robotic functionalities, including:

* Robot motion control
* Odometry estimation
* Sensor data acquisition
* LiDAR mapping
* Autonomous exploration
* Localization
* Autonomous navigation
* Obstacle avoidance
* Path planning
* Visual object detection
* Color recognition
* Gesture recognition
* Face and human detection
* Robotic arm control
* Autonomous object grasping
* AI-based perception
* Human–robot interaction
* Remote robot operation
* ROS-based distributed computing

---

# Typical Applications

JetAuto Pro can be used for:

* Robotics education
* Autonomous mobile robot research
* SLAM algorithm development
* Computer vision research
* AI and deep learning experiments
* Robot manipulation research
* Warehouse automation simulation
* Indoor autonomous navigation
* Human–robot interaction studies
* Embedded AI application development
* ROS learning and experimentation

---

# Why JetAuto Pro?

JetAuto Pro combines mobility, perception, manipulation, and onboard AI computing into a single integrated robotic platform. Its modular ROS architecture, rich sensor suite, and support for modern robotics software make it suitable for both beginners learning robotics fundamentals and researchers developing advanced autonomous systems. The platform enables rapid prototyping, testing, and deployment of robotics algorithms without requiring extensive hardware integration, allowing users to focus on software development and system-level experimentation.


