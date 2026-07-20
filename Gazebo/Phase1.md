Phase 1 – ROS Basics (Robot Operating System)
Goal

By the end of Phase 1, you should understand

What ROS actually is
Why every robotics company uses it
How ROS programs communicate
How to write your own ROS nodes
Topics
Publishers
Subscribers
Services
Parameters
Launch files
ROS package structure
ROS tools for debugging

Only after this should you move to Gazebo.

What is ROS?

Imagine you are building a robot.

Your robot has

Camera
LiDAR
Motors
IMU
GPS
Arm
Speaker
Microphone

Without ROS...

Every sensor has different code.

Every device has different APIs.

Everything becomes messy.

Instead ROS acts like the operating system for robots.

Exactly like Windows manages software,
ROS manages robot programs.

Think of ROS like this

Windows
│
├── Chrome
├── VS Code
├── Spotify


ROS

ROS Master
│
├── Camera Node
├── LiDAR Node
├── Motor Node
├── Mapping Node
├── Navigation Node
├── AI Detection Node

Every program becomes independent.

These independent programs are called

Nodes
What is a Node?

A node is simply

One program that performs one job.

Examples

Camera node

Captures images

Motor node

Moves wheels

GPS node

Reads location

YOLO node

Detects objects

Navigation node

Plans path

Instead of writing one huge program

main.cpp

Camera

Motor

Navigation

AI

Mapping

Speech

Bluetooth

ROS splits everything.

Camera Node

Motor Node

Navigation Node

YOLO Node

Speech Node

Each runs independently.

This is why ROS is scalable.

Why split into Nodes?

Suppose camera crashes.

Without ROS

Everything crashes.

With ROS

Only

camera_node

dies.

Navigation still works.

Motor still works.

SLAM still works.

Communication between Nodes

How do nodes talk?

ROS provides three main methods.

Topics

Services

Actions (later)

We'll study Topics first.

Topics

Imagine WhatsApp groups.

Everyone who joins receives messages.

ROS Topics work exactly like this.

Example

Camera Node

publishes

Image

Topic

/camera/image_raw

Subscribers

YOLO

Lane Detection

Recorder

All receive images.

Diagram

Camera Node

        |

        |

/camera/image_raw

   /      |       \

YOLO  Recorder  Display

Publisher

Camera

Subscribers

YOLO

Display

Recorder

Publisher never knows who receives.

Very powerful.

Publisher

Publisher sends data continuously.

Example

Temperature sensor

22

22.1

22.4

22.5

22.7

Every second

Publisher publishes.

Subscriber

Subscriber listens.

Example

Motor speed

Topic

/wheel_speed

Controller receives

5

6

7

8
Message Types

ROS uses predefined message formats.

Examples

std_msgs/String

std_msgs/Int32

geometry_msgs/Twist

sensor_msgs/Image

sensor_msgs/LaserScan

nav_msgs/Odometry

Example

String

Hello

Twist

Linear velocity

Angular velocity

LaserScan

Distances from LiDAR
Example

Publisher

Camera Node

publishes

sensor_msgs/Image

Subscriber

YOLO

receives Image

runs inference

publishes detections
Topic Example in JetAuto
Camera

↓

/camera/image_raw

↓

YOLO

↓

/detections

↓

Navigation
ROS Master (ROS 1)

ROS1 has a master.

Everything first registers here.

ROS Master

        |

--------------------------

|      |        |

Camera Motor LiDAR

Master keeps track of

Who exists

Who publishes

Who subscribes

ROS2 Difference

ROS2 removed ROS Master.

Instead uses DDS.

Much faster.

More reliable.

Industry standard now.

Commands

List running nodes

rosnode list

Information

rosnode info /camera_node

List topics

rostopic list

Check topic

rostopic echo /camera/image_raw

Topic frequency

rostopic hz /camera/image_raw

Topic info

rostopic info /camera/image_raw
Services

Topics are continuous.

Sometimes you only want one request.

Like

Take photo.

Reset odometry.

Open gripper.

Start recording.

This is Service.

Diagram

Client

|

Request

|

Server

|

Response

Example

Client

Open Gripper

↓

Server

Returns

Done
Difference

Topics

Continuous

Publisher → Subscriber

Services

One request

One response
Example

Robot Arm

Open Gripper

Request

Open

Response

Completed
Commands

List services

rosservice list

Call service

rosservice call

Service type

rosservice type
Parameters

Parameters are global variables.

Instead of hardcoding

Camera Resolution = 640x480

Store in ROS Parameter Server.

Example

camera_fps

camera_width

camera_height

robot_name

Commands

rosparam list
rosparam get
rosparam set
Launch Files

Suppose robot needs

Camera

Motor

LiDAR

Navigation

YOLO

SLAM

Running individually

rosrun camera

rosrun motor

rosrun lidar

rosrun slam

rosrun navigation

rosrun yolo

Very annoying.

Launch file

roslaunch robot bringup.launch

Everything starts automatically.

Example launch

<launch>

<node pkg="camera_pkg"
      type="camera_node"
      name="camera"/>

<node pkg="motor_pkg"
      type="motor_node"
      name="motor"/>

</launch>
ROS Package

Everything lives inside packages.

robot_ws

src

camera_pkg

motor_pkg

navigation_pkg

slam_pkg

Each package has

src/

include/

launch/

config/

msg/

srv/

package.xml

CMakeLists.txt
Workspace

ROS project

catkin_ws

src

build

devel

You write code inside

src

Then

catkin_make
Visualization Tools
RViz

Visualize

Robot

Camera

LiDAR

Maps

TF

Odometry

Markers

No physics.

Just visualization.

rqt_graph

Most important beginner tool.

Shows node connections.

Camera

↓

Topic

↓

YOLO

↓

Detections

↓

Navigation

Instantly.

rqt_console

Shows logs.

rqt_plot

Plots sensor values.

Real Example (JetAuto)

When JetAuto starts

USB Camera Node

↓

camera/image_raw

↓

YOLO Node

↓

detections

↓

Navigation

↓

Motor Driver

↓

Robot Moves

Everything is separate.

Mini Project (Recommended)

Build these in order:

Hello ROS Node
Publisher printing "Hello Robot"
Subscriber receiving it
Publisher sending numbers
Subscriber plotting numbers
Service to turn LED ON/OFF (or simulate it)
Launch file that starts multiple nodes
Visualize communication with rqt_graph
Use parameters to change publish frequency without modifying code

By the end of these, you'll have a solid grasp of the ROS communication model.

Learning Resources
Official Documentation
ROS Wiki (ROS 1)
ROS 2 Documentation
ROS Tutorials
Interactive Learning
The Construct (ROS Academy) — One of the best platforms for learning ROS with browser-based simulations.
Automatic Addison — Beginner-friendly ROS, robotics, and computer vision tutorials.
Articulated Robotics — Excellent explanations, especially for ROS 2 and navigation.
YouTube Channels
Articulated Robotics YouTube
The Construct YouTube
Robotics Back-End YouTube
Automatic Addison YouTube
Books (Free / Highly Recommended)
Programming Robots with ROS (O'Reilly)
A Gentle Introduction to ROS
Practice Repositories
ROS Tutorials Repository
ROS 2 Examples Repository
Suggested Learning Order (1–2 Weeks)
Day	Topics
1	What is ROS, Workspaces, Packages
2	Nodes and ROS commands
3	Publishers and Subscribers
4	Message types and custom messages
5	Services and Parameters
6	Launch files and package organization
7	RViz, rqt_graph, rqt_plot, debugging
8–10	Build small ROS projects from scratch
11–14	Apply the concepts on your JetAuto Pro (camera, motors, sensors)
Before moving to Phase 2 (Gazebo), you should be able to answer these questions
What problem does ROS solve compared to writing one large robot program?
What is a node, and why is it kept small and independent?
When should you use a topic versus a service?
What is the role of a publisher and a subscriber?
What are ROS message types, and why are they important?
How does a launch file simplify running a robot?
What is a ROS package, and what files does it typically contain?
How do you inspect and debug topics and node connections using rostopic and rqt_graph?
What is the difference between ROS 1 (ROS Master) and ROS 2 (DDS-based communication)?
