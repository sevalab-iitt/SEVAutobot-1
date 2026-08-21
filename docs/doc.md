# JetAuto Pro Complete Documentation

**Platform**
- JetAuto Pro
- NVIDIA Jetson Nano
- ROS Melodic
- Ubuntu
- Gazebo
- RViz

---

# Table of Contents

1. Introduction
2. Hardware Overview
3. Software Stack
4. ROS Architecture
5. Linux Basics
6. Workspace Structure
7. Development Philosophy

---

# Chapter 1 - Introduction

## Purpose

This documentation records every experiment, setup, troubleshooting step, command, and concept learned while working with the JetAuto Pro platform.

Rather than being a collection of notes, this document is intended to become a complete reference manual for future robotics projects involving:

- ROS
- Gazebo
- LiDAR
- SLAM
- Navigation
- Computer Vision
- Autonomous Robots

Every mistake encountered has been documented together with its diagnosis and solution so that the same problem can be solved quickly in the future.

---

# Project Goals

The primary objectives were:

- Learn ROS from scratch
- Understand Linux for robotics
- Understand robot architecture
- Build a complete SLAM pipeline
- Learn simulation before hardware
- Understand every component instead of simply following tutorials

---

# Why Learn Through Simulation First?

Simulation provides a safe environment where mistakes cannot damage hardware.

Advantages include:

- Unlimited testing
- Faster debugging
- Easy visualization
- Repeatable experiments
- Safe parameter tuning
- No battery limitations
- No hardware wear

Only after understanding simulation should the same workflow be transferred onto the physical robot.

---

# Chapter 2 - Hardware Overview

## JetAuto Pro

JetAuto Pro is an autonomous mobile robot platform developed by Hiwonder.

It combines:

- NVIDIA Jetson Nano
- Mecanum wheels
- Robotic arm
- Camera
- LiDAR
- IMU
- ROS software ecosystem

It is designed for learning:

- Autonomous Navigation
- Robot Vision
- SLAM
- Artificial Intelligence
- Mobile Robotics

---

## Main Components

### Jetson Nano

Role:

Main onboard computer.

Responsibilities:

- Runs Ubuntu
- Executes ROS nodes
- Performs SLAM
- Controls motors
- Runs computer vision algorithms

---

### LiDAR

Purpose:

Measures surrounding distances using laser beams.

Output:

LaserScan messages.

Applications:

- Mapping
- Obstacle avoidance
- Navigation
- Localization

---

### Camera

Purpose:

Visual perception.

Applications:

- Object Detection
- Tracking
- Face Recognition
- Color Detection
- Visual SLAM

---

### Mecanum Wheels

Unlike differential drive robots, JetAuto uses mecanum wheels.

Advantages:

- Forward
- Backward
- Sideways
- Diagonal
- Rotation

without changing robot orientation.

---

# Chapter 3 - Software Stack

The complete software architecture looks like:

```
                 User

                  │

              ROS Master

                  │

      ┌───────────┴────────────┐

      │                        │

 Simulation                 Real Robot

      │                        │

Gazebo                     Hardware Drivers

      │                        │

Robot Model             LiDAR / Camera / Motors

      │                        │

Topics                  Topics

      │                        │

      └───────────┬────────────┘

                  │

             SLAM Algorithms

                  │

              Occupancy Map
```

---

## Operating System

Ubuntu

Responsibilities:

- Device drivers
- Networking
- File management
- Process scheduling
- ROS execution

---

## ROS Melodic

ROS is not an operating system.

It is middleware that allows different robot components to communicate.

ROS provides:

- Nodes
- Topics
- Services
- Parameters
- TF
- Launch files

---

## Gazebo

Gazebo is a physics simulator.

It simulates:

- Gravity
- Friction
- Sensors
- Cameras
- LiDAR
- Robot dynamics

Instead of controlling a physical robot, Gazebo controls a virtual robot.

---

## RViz

RViz is not a simulator.

It is only a visualization tool.

It displays:

- Robot Model
- LiDAR
- TF
- Camera
- Occupancy Maps
- Planned Paths

---

# Chapter 4 - ROS Architecture

The most important concept in ROS is communication.

Every robot is divided into small programs called Nodes.

Example:

```
Camera Node

↓

Image Topic

↓

Object Detection Node

↓

Detected Objects Topic

↓

Navigation Node
```

Each node performs one task only.

Advantages:

- Easier debugging
- Better modularity
- Easy replacement
- Parallel execution

---

## ROS Master

The ROS Master acts like a phone directory.

It does NOT transport data.

Instead it tells nodes:

- Who publishes
- Who subscribes
- Where to connect

After connection, nodes communicate directly.

---

## Nodes

A Node is an independent executable.

Examples:

- Camera Driver
- LiDAR Driver
- Motor Controller
- SLAM
- Navigation

A robot typically runs dozens of nodes simultaneously.

---

## Topics

Topics are communication channels.

Example:

```
LiDAR

↓

/scan

↓

GMapping
```

The LiDAR publishes.

GMapping subscribes.

---

## Publisher

A Publisher creates data.

Examples:

- Camera
- LiDAR
- IMU

---

## Subscriber

A Subscriber receives data.

Examples:

- Mapping
- Navigation
- Visualization

---

## Services

Topics provide continuous communication.

Services provide request-response communication.

Example:

```
Save Map

↓

Request

↓

Server

↓

Response
```

---

## Parameters

Parameters store robot configuration.

Examples:

- Robot speed
- LiDAR range
- Camera resolution

---

# Chapter 5 - Linux Basics

Almost every robotics engineer spends significant time in the Linux terminal.

Important commands:

```
pwd
```

Print current directory.

---

```
ls
```

List files.

---

```
cd folder_name
```

Change directory.

---

```
mkdir folder
```

Create directory.

---

```
rm file
```

Delete file.

---

```
cp
```

Copy.

---

```
mv
```

Move.

---

```
nano file.txt
```

Simple terminal editor.

---

```
cat file
```

Display file contents.

---

```
find
```

Search files.

---

```
grep
```

Search text.

---

```
chmod
```

Modify permissions.

---

```
sudo
```

Execute command as administrator.

---

# Chapter 6 - ROS Workspace

The workspace used throughout this project:

```
~/jetauto_ws
```

Typical structure:

```
jetauto_ws/

├── build

├── devel

├── logs

└── src
```

---

## src

Contains source code.

---

## build

Temporary compilation files.

---

## devel

Generated executables.

---

## logs

Compilation logs.

---

# Development Philosophy

Throughout this project the goal was never to simply "make it work."

Instead, every command was investigated to answer:

- What does it do?
- Why is it required?
- What happens internally?
- What could go wrong?
- How can it be debugged?

Understanding these questions builds long-term robotics skills instead of temporary solutions.

---

**End of Part 1**

The next part begins with:

- Networking
- SSH
- VNC
- Static IP
- Router changes
- Camera failures
- USB debugging
- Every troubleshooting step performed on the JetAuto system.
