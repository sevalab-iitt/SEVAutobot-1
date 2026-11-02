# DOF 6 Robotic Arm

## 1. Introduction

A **6-DOF (Six Degrees of Freedom) Robotic Arm** is a robotic manipulator designed to move its end point in different directions and perform tasks that require controlled movement.

The term *Degrees of Freedom (DOF)* describes the number of independent movements a robot can make. Each degree of freedom represents one independent movement or rotation.

A robotic arm can use these movements to:
- Reach objects at different positions.
- Change the orientation of its end effector.
- Pick up and move objects.
- Perform basic manipulation tasks.

On the JetAuto Pro platform, the robotic arm uses servo motors for movement. ROS (Robot Operating System) provides the software interface to communicate with these motors, control individual joints, and coordinate arm movements.

## 2. Robotic Arm Overview

**[Insert Image: DOF 6 Robotic Arm mounted on JetAuto Pro]**

*Figure 1: Robotic arm assembly mounted on the JetAuto Pro platform.*

The arm consists of multiple movable joints connected to form a mechanical structure. Each joint controls a particular part of the arm.

The gripper at the end allows the robot to hold and release objects.

### Main Components

| Component | Description |
|---|---|
| Robotic arm | Mechanical structure used to reach and move objects. |
| Servo motors | Control the movement of individual joints. |
| Joints | Provide rotational movement to the arm. |
| Gripper | Holds and releases objects. |
| USB-to-Serial connection | Connects the servo control hardware to the JetAuto computer. |
| Servo controller | Receives commands and communicates with the servos. |

## 3. Hardware Communication

The robotic arm communicates with the JetAuto computer through a USB-to-Serial connection.

During system inspection, the following device was identified:

| Parameter | Detected Value |
|---|---|
| Serial device | `/dev/ttyUSB0` |
| USB identifier | `usb-1a86_USB_Serial-if00-port0` |
| Connection type | USB-to-Serial |
| ROS version | ROS Melodic |

The serial connection allows the computer to send movement commands to the servo controller and receive information about servo positions.

**Connection verification:**

```bash
ls /dev/ttyUSB*
ls /dev/serial/by-id/
```

The output confirmed that `/dev/ttyUSB0` was available.

## 4. ROS Software Architecture

The robotic arm uses several ROS packages to manage servo communication, joint control, and movement.

The main packages identified in the JetAuto Pro ROS workspace are:

| ROS Package | Purpose |
|---|---|
| `hiwonder_servo_driver` | Handles communication with the servo hardware. |
| `hiwonder_servo_controllers` | Provides ROS controllers for servo movement. |
| `hiwonder_servo_msgs` | Defines messages used for servo communication. |
| `jetauto_arm_kinematics` | Provides the arm's kinematics-related functionality. |
| `jetauto_moveit_config` | Contains the MoveIt configuration for robotic arm planning and control. |
| `jetauto_sdk` | Provides the JetAuto software development interface. |

### ROS Communication Structure

The following diagram shows the main software components identified during inspection.

```text
              JetAuto Pro
                   |
             USB Connection
                   |
              /dev/ttyUSB0
                   |
          Servo Communication
                   |
          hiwonder_servo_driver
                   |
          hiwonder_servo_manager
                   |
       hiwonder_servo_controllers
                   |
          +--------+--------+
          |                 |
     Arm Controllers   Gripper Controller
          |                 |
     Joint Commands     Gripper Commands
          |                 |
       Servo Motors      Gripper
```

*Figure 2: Simplified ROS communication structure of the robotic arm.*

## 5. ROS Nodes and Controllers

A ROS node is a running program that performs a particular task. Controllers manage the movement of individual joints or groups of joints.

During system inspection, the following node was identified:

| Node | Status / Purpose |
|---|---|
| `/hiwonder_servo_manager` | Running; manages servo communication and controller interfaces. |

The following controllers were available:

| Controller | Function |
|---|---|
| `/joint1_controller` | Controls joint 1. |
| `/joint2_controller` | Controls joint 2. |
| `/joint3_controller` | Controls joint 3. |
| `/joint4_controller` | Controls joint 4. |
| `/r_joint_controller` | Controls the rotational joint. |
| `/arm_controller` | Provides coordinated arm trajectory control. |
| `/gripper_controller` | Controls the gripper movement. |

The individual joint controllers allow separate joint commands, while the arm controller provides an interface for coordinated movement.

## 6. ROS Topics

ROS topics allow nodes to exchange information through messages.

The following topics were identified using:

```bash
rostopic list | grep -Ei "servo|arm|joint|kinematic"
```

### Important Topics

| Topic | Purpose |
|---|---|
| `/joint_states` | Publishes the current joint states. |
| `/arm_controller/command` | Receives arm movement commands. |
| `/arm_controller/state` | Publishes arm controller feedback. |
| `/joint1_controller/command` | Sends commands to joint 1. |
| `/joint2_controller/command` | Sends commands to joint 2. |
| `/joint3_controller/command` | Sends commands to joint 3. |
| `/joint4_controller/command` | Sends commands to joint 4. |
| `/r_joint_controller/command` | Sends commands to the rotational joint. |
| `/gripper_controller/follow_joint_trajectory/goal` | Receives gripper trajectory goals. |
| `/servo_controllers/port_id_1/servo_states` | Publishes servo feedback information. |

The arm also provides trajectory-related topics such as `goal`, `feedback`, `result`, and `status`. These support communication between the controller and ROS applications.

## 7. Servo State Monitoring

The servo state topic was used to verify communication between ROS and the servo hardware.

```bash
rostopic echo /servo_controllers/port_id_1/servo_states
```

The output contained the following information:

| Field | Meaning |
|---|---|
| `id` | Unique identifier of the servo. |
| `goal` | Target position requested for the servo. |
| `position` | Current reported servo position. |
| `error` | Difference between the target and reported position. |
| `voltage` | Reported servo supply voltage. |
| `timestamp` | Time at which the state was recorded. |

### Observed Test Results

Five servo IDs were visible in the recorded output.

| Servo ID | Goal | Position | Error | Voltage |
|---|---:|---:|---:|---:|
| 1 | 500 | 500 | 0 | 9000 |
| 2 | 208 | 208 | 0 | 9000 |
| 3 | 42 | 42 | 0 | 9000 |
| 4 | 667 | 667 | 0 | 9000 |
| 5 | 500 | 500 | 0 | 9000 |

The reported goal and position values matched for all five servos, with an error of zero.

This confirms that ROS was receiving servo state information and that the reported positions matched their requested targets during this observation.

*Note: The values above are raw servo feedback values, not joint angles in degrees.*

## 8. System Verification

The following checks were performed to inspect the robotic arm integration.

| Test | Command | Observation |
|---|---|---|
| ROS node inspection | `rosnode list` | Servo manager was running. |
| Topic inspection | `rostopic list` | Arm, joint, gripper, and servo topics were available. |
| Hardware connection | `ls /dev/ttyUSB*` | `/dev/ttyUSB0` was detected. |
| Serial identification | `ls /dev/serial/by-id/` | USB serial device was identified. |
| Servo feedback | `rostopic echo /servo_controllers/port_id_1/servo_states` | Five servo IDs reported position information. |
| Node inspection | `rosnode info /hiwonder_servo_manager` | Publishers, subscribers, and services were identified. |
| Package inspection | `rospack list` | Arm and servo-related ROS packages were available. |

## 9. Summary

The DOF 6 robotic arm is integrated with the JetAuto Pro platform through a USB-to-Serial connection and ROS Melodic.

The inspection confirmed that:
- The servo hardware was detected through `/dev/ttyUSB0`.
- The Hiwonder servo manager was running.
- Arm, joint, and gripper controller interfaces were available.
- ROS topics provided interfaces for sending commands and receiving feedback.
- Five servo IDs were reporting position information.

These components provide the software foundation required to control the robotic arm and develop manipulation applications.

**Configuration note:** The recorded ROS inspection identifies five arm joint controllers and a separate gripper controller. The exact six-DOF joint configuration should be confirmed from the robot's URDF or MoveIt configuration before publishing a final joint specification.
