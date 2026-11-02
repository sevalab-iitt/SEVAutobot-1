# DOF 6 Robotic Arm – Hardware and Software Documentation

## Table of Contents

1. [Introduction](#1-introduction)
2. [Robotic Arm Overview](#2-robotic-arm-overview)
3. [Arm Components and Hardware](#3-arm-components-and-hardware)
4. [Hardware Connection](#4-hardware-connection)
5. [ROS Software Architecture](#5-ros-software-architecture)
6. [ROS Nodes and Controllers](#6-ros-nodes-and-controllers)
7. [ROS Communication Topics](#7-ros-communication-topics)
8. [Servo State Monitoring](#8-servo-state-monitoring)
9. [System Verification](#9-system-verification)
10. [Summary](#10-summary)

---

## 1. Introduction

The **DOF 6 Robotic Arm** is a robotic manipulator mounted on the JetAuto Pro mobile robot. It allows the robot to interact with objects in its surroundings by reaching, positioning, picking up, and moving objects.

DOF stands for *Degrees of Freedom*. It describes the number of independent movements a robotic mechanism can perform.

Each degree of freedom represents an independent movement or rotation. Multiple joints work together to position and orient the arm.

The robotic arm uses servo motors to control its movements. The JetAuto Pro runs ROS (Robot Operating System), which provides the software interfaces required to communicate with the servo hardware and control the arm.

### What can the robotic arm do?

- Reach objects at different positions.
- Change the orientation of its end point.
- Pick up and release objects using its gripper.
- Perform basic object manipulation tasks.

## 2. Robotic Arm Overview

The robotic arm consists of a series of connected sections, movable joints, and a gripper. Each joint contributes to the overall movement of the arm.

### 2.1 Arm Mounted on JetAuto Pro

<div align="center">
  <img src="https://github.com/user-attachments/assets/3edd407b-75db-4f9c-b7e1-c74d9a872f38" alt="Centered Image">
</div>

*Figure 1: DOF 6 robotic arm mounted on the JetAuto Pro platform.*

This view shows the complete robotic system and how the arm is positioned on the mobile robot.

### 2.2 Standalone Robotic Arm

<img align="center" width="557" height="514" alt="image" src="https://github.com/user-attachments/assets/7437a33d-5c93-4ce2-ae0e-831a4c5cd1c5" />

*Figure 2: Standalone view of the robotic arm assembly.*

The standalone view makes it easier to identify the arm structure, joints, servo motors, and gripper without the other robot components.

### 2.3 Understanding the Degrees of Freedom

**[INSERT IMAGE – LABELLED JOINT DIAGRAM]**

<!-- Image alignment: Center -->
<!-- Suggested image: Robotic arm with each joint labelled and its movement direction indicated -->

*Figure 3: Joint arrangement and movement of the robotic arm.*

The joints allow the arm to move and change its position. Their combined movements determine where the gripper can reach.

**Note:** The exact six-axis arrangement should be confirmed using the robot's mechanical design and URDF model.

## 3. Arm Components and Hardware

The robotic arm uses several mechanical and electronic components to perform its movements.

### 3.1 Servo Motors

Servo motors are the main actuators of the robotic arm. An actuator is a device that produces physical movement.

Each servo receives a target position and moves its connected joint towards that position.

<img align="center" width="379" height="373" alt="image" src="https://github.com/user-attachments/assets/1a88fbb5-0634-4ebf-8309-f6b7bfdbba2f" />

*Figure 4: Servo motor used in the robotic arm.*

The servo motor communicates with the control system through the servo controller. It can also provide feedback about its current position.


### 3.2 Main Mechanical Components

**[INSERT IMAGE – ARM COMPONENTS WITH LABELS]**

<!-- Image alignment: Center -->
<!-- Suggested image: Close-up of the arm showing base, links, joints, wrist and gripper -->

*Figure 5: Main mechanical sections of the robotic arm.*

| Component | Function |
|---|---|
| Base | Supports the robotic arm. |
| Arm links | Connect the different joints. |
| Joints | Allow the arm sections to rotate. |
| Servo motors | Produce controlled movement. |
| Wrist | Controls the orientation near the end of the arm. |
| Gripper | Holds and releases objects. |

### 3.3 Gripper

The gripper is attached to the end of the robotic arm. It allows the robot to hold and release objects.

**[INSERT IMAGE – GRIPPER CLOSE-UP]**

<!-- Image alignment: Right or Center -->
<!-- Suggested image: Close-up showing the gripper in open and closed positions -->

*Figure 6: Robotic arm gripper.*

## 4. Hardware Connection

The robotic arm communicates with the JetAuto computer through a USB-to-Serial connection.

A serial connection allows the computer to exchange commands and feedback with the servo control hardware.

### 4.1 Communication Hardware

**[INSERT IMAGE – USB-TO-SERIAL CONNECTION]**

<!-- Image alignment: Center -->
<!-- Suggested image: USB cable, serial adapter and arm control connection -->

*Figure 7: USB-to-Serial communication connection.*

During system inspection, the following device was detected:

| Parameter | Detected Value |
|---|---|
| Serial device | `/dev/ttyUSB0` |
| USB identifier | `usb-1a86_USB_Serial-if00-port0` |
| Connection type | USB-to-Serial |
| ROS version | ROS Melodic |

### 4.2 Verifying the Connection

The following commands were used to identify the connected serial device:

```bash
ls /dev/ttyUSB*
ls /dev/serial/by-id/
```

The system detected `/dev/ttyUSB0`, confirming that the USB serial device was available.

## 5. ROS Software Architecture

The robotic arm uses ROS packages to manage communication, servo control, and joint movement.

ROS acts as the communication layer between the software applications and the physical hardware.

### 5.1 Software Architecture Overview

**[INSERT IMAGE – ROS SOFTWARE ARCHITECTURE DIAGRAM]**

<!-- Image alignment: Center -->
<!-- Suggested image: Diagram showing computer, ROS packages, servo manager, controllers and servo hardware -->

*Figure 8: Software architecture of the robotic arm.*

The main software components identified in the JetAuto Pro workspace are:

| ROS Package | Purpose |
|---|---|
| `hiwonder_servo_driver` | Handles communication with servo hardware. |
| `hiwonder_servo_controllers` | Provides controllers for servo movement. |
| `hiwonder_servo_msgs` | Defines messages used for servo communication. |
| `jetauto_arm_kinematics` | Provides arm kinematics-related functionality. |
| `jetauto_moveit_config` | Contains MoveIt configuration for arm planning and control. |
| `jetauto_sdk` | Provides the JetAuto software development interface. |

### 5.2 How the Software Components Work Together

The following simplified structure explains the communication flow:

<img width="200" height="349" alt="roscomro1 drawio" src="https://github.com/user-attachments/assets/8115ada7-6203-4808-9964-ce1b51fc0c06" />


The servo manager handles communication with the servo hardware. Controllers receive movement commands and pass them to the appropriate servos.

## 6. ROS Nodes and Controllers

A **ROS node** is a running software process that performs a particular task.

A **controller** manages how a joint or group of joints responds to movement commands.

### 6.1 Servo Manager

The main servo management node identified during inspection was:

`/hiwonder_servo_manager`

This node was running and provided communication interfaces for the arm and gripper controllers.

### 6.2 Available Controllers

| Controller | Function |
|---|---|
| `/joint1_controller` | Controls joint 1. |
| `/joint2_controller` | Controls joint 2. |
| `/joint3_controller` | Controls joint 3. |
| `/joint4_controller` | Controls joint 4. |
| `/r_joint_controller` | Controls the rotational joint. |
| `/arm_controller` | Provides coordinated arm trajectory control. |
| `/gripper_controller` | Controls the gripper. |

**[INSERT IMAGE – ARM CONTROL INTERFACE]**

<!-- Image alignment: Center -->
<!-- Suggested image: Screenshot of the JetAuto arm control application or joystick interface -->

*Figure 9: Robotic arm control interface.*

The individual joint controllers allow separate joint commands, while the arm controller provides an interface for coordinated movement.

## 7. ROS Communication Topics

ROS topics allow different nodes to exchange information.

For example, an application can send a movement command through a topic, and the servo manager can process that command.

### 7.1 Important Topics

| Topic | Purpose |
|---|---|
| `/joint_states` | Publishes current joint states. |
| `/arm_controller/command` | Receives arm movement commands. |
| `/arm_controller/state` | Publishes arm controller feedback. |
| `/joint1_controller/command` | Sends commands to joint 1. |
| `/joint2_controller/command` | Sends commands to joint 2. |
| `/joint3_controller/command` | Sends commands to joint 3. |
| `/joint4_controller/command` | Sends commands to joint 4. |
| `/r_joint_controller/command` | Sends commands to the rotational joint. |
| `/servo_controllers/port_id_1/servo_states` | Publishes servo feedback. |

### 7.2 Understanding Command and Feedback

**[INSERT IMAGE – COMMAND AND FEEDBACK FLOW]**

<!-- Image alignment: Center -->
<!-- Suggested image: Two-way diagram showing movement commands going to the servo and feedback returning to ROS -->

*Figure 10: Command and feedback communication between ROS and the servo hardware.*

The communication process has two main parts:

1. **Command:** ROS sends a target position to the controller.
2. **Feedback:** The servo manager publishes information about the servo's reported position.

This allows the software to monitor the response of the hardware.

## 8. Servo State Monitoring

Servo feedback helps verify whether the hardware is communicating with ROS.

The following command was used to monitor servo states:

```bash
rostopic echo /servo_controllers/port_id_1/servo_states
```

### 8.1 Understanding Servo Feedback

**[INSERT IMAGE – TERMINAL SCREENSHOT OF SERVO STATES]**

<!-- Image alignment: Center -->
<!-- Suggested image: Actual terminal output showing servo IDs, goal, position, error and voltage -->

*Figure 11: Servo state information received through ROS.*

The output contains the following fields:

| Field | Meaning |
|---|---|
| `id` | Servo identifier. |
| `goal` | Requested target position. |
| `position` | Reported current position. |
| `error` | Difference between target and reported position. |
| `voltage` | Reported servo voltage. |
| `timestamp` | Time of the recorded state. |

### 8.2 Observed Servo Values

Five servo IDs were visible in the recorded output.

| Servo ID | Goal | Position | Error | Voltage |
|---|---:|---:|---:|---:|
| 1 | 500 | 500 | 0 | 9000 |
| 2 | 208 | 208 | 0 | 9000 |
| 3 | 42 | 42 | 0 | 9000 |
| 4 | 667 | 667 | 0 | 9000 |
| 5 | 500 | 500 | 0 | 9000 |

The recorded goal and position values matched for all five servos. Each servo also reported an error value of zero.

This confirms that the ROS system was receiving servo feedback and that the reported positions matched the requested targets during the observation.

*Note: These are raw servo position values, not angles in degrees.*

## 9. System Verification

Several ROS commands were used to inspect the hardware connection, running nodes, available packages, and communication topics.

### 9.1 Verification Results

| Test | Command | Observation |
|---|---|---|
| ROS node inspection | `rosnode list` | Servo manager was running. |
| Topic inspection | `rostopic list` | Arm, joint and servo topics were available. |
| Hardware connection | `ls /dev/ttyUSB*` | `/dev/ttyUSB0` was detected. |
| Serial identification | `ls /dev/serial/by-id/` | USB serial device was identified. |
| Servo feedback | `rostopic echo /servo_controllers/port_id_1/servo_states` | Five servo IDs reported position information. |
| Node inspection | `rosnode info /hiwonder_servo_manager` | Publishers, subscribers and services were identified. |
| Package inspection | `rospack list` | Arm and servo-related packages were available. |

### 9.2 ROS Node Inspection

**[INSERT IMAGE – ROS NODE LIST]**

<!-- Image alignment: Center -->
<!-- Suggested image: Terminal screenshot showing rosnode list output -->

*Figure 12: Running ROS nodes on the JetAuto Pro.*

### 9.3 ROS Topic Inspection

**[INSERT IMAGE – ROS TOPIC LIST]**

<!-- Image alignment: Center -->
<!-- Suggested image: Terminal screenshot showing arm and servo-related topics -->

*Figure 13: Available arm and servo communication topics.*

## 10. Summary

The DOF 6 robotic arm is integrated with the JetAuto Pro platform through a USB-to-Serial connection and ROS Melodic.

The system inspection confirmed that:

- The servo hardware was detected through `/dev/ttyUSB0`.
- The Hiwonder servo manager was running.
- Arm, joint and gripper controller interfaces were available.
- ROS topics provided interfaces for sending commands and receiving feedback.
- Five servo IDs were reporting position information.

These components provide the software foundation for controlling the robotic arm and developing manipulation applications.

**Configuration note:** The recorded ROS inspection identifies five arm joint controllers and a separate gripper controller. The exact six-DOF joint configuration should be confirmed using the robot's URDF or MoveIt configuration before publishing a final joint specification.

---

## Image Placement Checklist

Before publishing the documentation, add the following images:

| Figure | Image Required |
|---|---|
| 1 | Complete JetAuto Pro with mounted arm |
| 2 | Standalone robotic arm |
| 3 | Labelled joint and DOF diagram |
| 4 | Actual servo motor |
| 5 | Arm mechanical components |
| 6 | Gripper close-up |
| 7 | USB-to-Serial connection |
| 8 | ROS software architecture |
| 9 | Arm control software interface |
| 10 | Command and feedback flow |
| 11 | Servo state terminal output |
| 12 | Running ROS nodes |
| 13 | ROS arm and servo topics |

**Documentation tip:** Prefer actual photographs of your JetAuto Pro hardware and screenshots from your own ROS environment. Use diagrams only where they explain something that a photograph cannot show, such as joint movement or software communication.
