# JetAuto Gazebo Setup & Exploration (ROS Melodic)


## Objective

Learn how to install, verify, and use Gazebo with ROS Melodic and explore the JetAuto simulation packages.

---

# 1. Verify Gazebo Installation

Check whether Gazebo is installed.

```bash
gazebo --version
```

or

```bash
which gazebo
```

Launch Gazebo:

```bash
gazebo
```

---

# 2. Install Gazebo (if required)

```bash
sudo apt update
sudo apt install gazebo9
sudo apt install ros-melodic-gazebo-ros-pkgs
sudo apt install ros-melodic-gazebo-ros-control
```

Verify installation:

```bash
gazebo --version
```

---

# 3. Check ROS Workspace

Display ROS package path.

```bash
echo $ROS_PACKAGE_PATH
```

Display home directory.

```bash
echo $HOME
```

---

# 4. Find JetAuto Packages

List all JetAuto ROS packages.

```bash
rospack list | grep jetauto
```

Result:

Found packages including:

- jetauto_description
- jetauto_gazebo
- jetauto_moveit_config
- jetauto_navigation
- jetauto_slam
- jetauto_sdk
- jetauto_example
- jetauto_interfaces
- jetauto_controller
- jetauto_bringup
- jetauto_arm_kinematics

This confirms that the JetAuto simulation packages are already installed.

---

# 5. Navigate to Gazebo Package

```bash
roscd jetauto_gazebo
pwd
ls
```

Package contents:

```
CMakeLists.txt
launch/
meshes/
models/
worlds/
package.xml
```

---

# 6. Available Launch Files

Navigate into the launch directory.

```bash
cd launch
ls
```

Available launch files:

```
empty_world.launch
room_worlds.launch
spawn_model.launch
worlds.launch
```

---

# 7. Launch Simulation

Launch the simulation.

```bash
roslaunch jetauto_gazebo worlds.launch
```

This successfully launched:

- Gazebo
- Indoor room environment
- JetAuto robot

---

# 8. Simulation Controls

The simulation initially appeared paused.

To start physics:

- Click the ▶ Play button inside Gazebo.

---

# 9. Moving the Robot

First check for the velocity topic.

```bash
rostopic list | grep cmd_vel
```

Example command to move forward:

```bash
rostopic pub /cmd_vel geometry_msgs/Twist \
'{linear: {x: 0.3, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'
```

Example command to rotate:

```bash
rostopic pub /cmd_vel geometry_msgs/Twist \
'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}'
```

---

# 10. Important Observation

Instead of the simulated robot moving, the **actual JetAuto robot** moved.

Reason:

The computer was connected to the robot's ROS Master.

Current environment:

```
ROS_MASTER_URI=http://10.23.80.206:11311
```

Therefore:

```
PC
        │
        ▼
ROS Master (JetAuto)
        │
 ┌──────┴──────┐
 │             │
Gazebo      Real Robot
```

Publishing to `/cmd_vel` sent commands to the physical robot.

---

# 11. Prevent Controlling the Real Robot

Before experimenting with simulation:

Use a local ROS master.

```bash
export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=localhost
roscore
```

Then launch Gazebo again.

---

# 12. Check Topic Subscribers

Before sending motion commands, verify who is subscribed.

```bash
rostopic info /cmd_vel
```

This shows:

- Publishers
- Subscribers

Useful for confirming whether commands will affect the simulation or the real robot.

---

# 13. Learning Roadmap

## Phase 1
- ROS basics
- Nodes
- Topics
- Services
- Launch files

## Phase 2
- Gazebo basics
- Worlds
- Models
- Physics

## Phase 3
- URDF
- Xacro
- Robot links
- Joints

## Phase 4
- JetAuto Description package

## Phase 5
- Gazebo package
- Spawn robot
- Controllers
- Sensors

## Phase 6
- Navigation
- SLAM
- Autonomous operation

---

# Key ROS Commands

```bash
roscore
```

```bash
rosnode list
```

```bash
rostopic list
```

```bash
rostopic echo /topic_name
```

```bash
rostopic info /cmd_vel
```

```bash
rospack list | grep jetauto
```

```bash
roscd jetauto_gazebo
```

```bash
roslaunch jetauto_gazebo worlds.launch
```

---

# Lessons Learned

- Gazebo was successfully installed and functioning.
- JetAuto simulation packages were already present.
- The Gazebo world loaded successfully.
- The robot model was spawned correctly.
- ROS networking is shared between the simulator and the physical robot when using the same `ROS_MASTER_URI`.
- Publishing to `/cmd_vel` controlled the real JetAuto because both the simulator and hardware were connected to the same ROS Master.
- Future simulation experiments should use an isolated local ROS Master unless interaction with the physical robot is intended.
