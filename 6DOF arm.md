```
jetauto@jetauto-desktop:~$ rosnode list
/ar_app
/astra_cam/astra_cam_nodelet_manager
/astra_cam/astraplus
/astra_cam/depth_metric
/astra_cam/depth_metric_rect
/astra_cam/depth_points
/astra_cam/depth_rectify_depth
/astra_cam/depth_registered_hw_metric_rect
/astra_cam/depth_registered_metric
/astra_cam/depth_registered_rectify_depth
/astra_cam/driver
/astra_cam/points_xyzrgb_hw_registered
/astra_cam/rgb_rectify_color
/astra_cam_base_link
/astra_cam_base_link1
/astra_cam_base_link2
/astra_cam_base_link3
/hiwonder_servo_manager
/jetauto_controller
/joint_states_publisher
/joystick
/joystick_control
/lidar_app
/line_following
/object_tracking
/patrol_app
/rosapi
/rosbridge_websocket
/rosout
/rplidarNode
/usb_cam
/usb_cam/image_proc
/web_video_server
jetauto@jetauto-desktop:~$ rostopic list | grep -Ei "servo|arm|joint|kinematic"
/arm_controller/command
/arm_controller/follow_joint_trajectory/cancel
/arm_controller/follow_joint_trajectory/feedback
/arm_controller/follow_joint_trajectory/goal
/arm_controller/follow_joint_trajectory/result
/arm_controller/follow_joint_trajectory/status
/arm_controller/state
/gripper_controller/follow_joint_trajectory/cancel
/gripper_controller/follow_joint_trajectory/feedback
/gripper_controller/follow_joint_trajectory/goal
/gripper_controller/follow_joint_trajectory/result
/gripper_controller/follow_joint_trajectory/status
/joint1_controller/command
/joint1_controller/command_duration
/joint1_controller/state
/joint2_controller/command
/joint2_controller/command_duration
/joint2_controller/state
/joint3_controller/command
/joint3_controller/command_duration
/joint3_controller/state
/joint4_controller/command
/joint4_controller/command_duration
/joint4_controller/state
/joint_states
/jointr_controller/state
/r_joint_controller/command
/r_joint_controller/command_duration
/r_joint_controller/state
/servo_control/set_servo_state
/servo_controllers/port_id_1/id_pos_dur
/servo_controllers/port_id_1/multi_id_pos_dur
/servo_controllers/port_id_1/servo_states
jetauto@jetauto-desktop:~$ ls /dev/ttyUSB*
/dev/ttyUSB0
jetauto@jetauto-desktop:~$ ls /dev/ttyACM*
ls: cannot access '/dev/ttyACM*': No such file or directory
jetauto@jetauto-desktop:~$ ls /dev/ttyACM*
ls: cannot access '/dev/ttyACM*': No such file or directory
jetauto@jetauto-desktop:~$ ls /dev/ttyACM*
ls: cannot access '/dev/ttyACM*': No such file or directory
jetauto@jetauto-desktop:~$ ls /dev/serial/by-id/
usb-1a86_USB_Serial-if00-port0
jetauto@jetauto-desktop:~$ find ~/ -maxdepth 3 -type d \( -iname "*arm*" -o -iname "*servo*" \) 2>/dev/null
/home/jetauto/.pycharm_helpers
/home/jetauto/.pycharm_helpers/pycharm_display
/home/jetauto/.pycharm_helpers/pycharm
/home/jetauto/.pycharm_helpers/pycharm/pycharm_commands
/home/jetauto/.pycharm_helpers/pycharm_matplotlib_backend
/home/jetauto/jetauto_third_party/Astra_OpenNI/Arm64
/home/jetauto/jetauto_software/servo_tool
/home/jetauto/jetauto_software/jetauto_arm_pc
/home/jetauto/jetauto_ws/logs/hiwonder_servo_msgs
/home/jetauto/jetauto_ws/logs/hiwonder_servo_controllers
/home/jetauto/jetauto_ws/logs/jetauto_arm_kinematics
/home/jetauto/jetauto_ws/logs/hiwonder_servo_driver
/home/jetauto/jetauto_ws/build/hiwonder_servo_msgs
/home/jetauto/jetauto_ws/build/hiwonder_servo_controllers
/home/jetauto/jetauto_ws/build/jetauto_arm_kinematics
/home/jetauto/jetauto_ws/build/hiwonder_servo_driver
jetauto@jetauto-desktop:~$ find ~/ -maxdepth 4 -type f \( -iname "*servo*.py" -o -iname "*arm*.launch" -o -iname "*arm*.yaml" \) 2>/dev/null
/home/jetauto/jetauto_software/servo_tool/BusServoControl.py
/home/jetauto/jetauto_software/servo_tool/BusServoCmd.py
/home/jetauto/jetauto_software/servo_tool/servo_controller.py
/home/jetauto/jetauto_software/jetauto_arm_pc/BusServoControl.py
/home/jetauto/jetauto_software/jetauto_arm_pc/BusServoCmd.py
/home/jetauto/jetauto_software/jetauto_arm_pc/servo_controller.py
jetauto@jetauto-desktop:~$ rospack list | grep -Ei "servo|arm|kinematic|hiwonder|jetauto"
astra_camera /home/jetauto/jetauto_ws/src/third_party/ros_astra_camera
astra_demo /home/jetauto/catkin_ws/src/astra_demo
cartographer /home/jetauto/jetauto_ws/src/third_party/cartographer
cartographer_ros /home/jetauto/jetauto_ws/src/third_party/cartographer_ros/cartographer_ros
cartographer_ros_msgs /home/jetauto/jetauto_ws/src/third_party/cartographer_ros/cartographer_ros_msgs
cartographer_rviz /home/jetauto/jetauto_ws/src/third_party/cartographer_ros/cartographer_rviz
cv_bridge /home/jetauto/jetauto_ws/src/third_party/vision_opencv/cv_bridge
depth_image_proc /home/jetauto/jetauto_ws/src/third_party/image_pipeline/depth_image_proc
exploration_msgs /home/jetauto/jetauto_ws/src/third_party/frontier_exploration/exploration_msgs
exploration_server /home/jetauto/jetauto_ws/src/third_party/frontier_exploration/exploration_server
explore_lite /home/jetauto/jetauto_ws/src/third_party/explore
frontier_exploration /home/jetauto/jetauto_ws/src/third_party/frontier_exploration/frontier_exploration
hiwonder_servo_controllers /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers
hiwonder_servo_driver /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver
hiwonder_servo_msgs /home/jetauto/jetauto_ws/src/jetauto_driverhiwonder_servo/hiwonder_servo_msgs
image_geometry /home/jetauto/jetauto_ws/src/third_party/vision_opencv/image_geometry
image_proc /home/jetauto/jetauto_ws/src/third_party/image_pipeline/image_proc
image_publisher /home/jetauto/jetauto_ws/src/third_party/image_pipeline/image_publisher
image_rotate /home/jetauto/jetauto_ws/src/third_party/image_pipeline/image_rotate
image_view /home/jetauto/jetauto_ws/src/third_party/image_pipeline/image_view
imu_calib /home/jetauto/jetauto_ws/src/third_party/imu_calib
jetauto_app /home/jetauto/jetauto_ws/src/jetauto_app
jetauto_arm_kinematics /home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_arm_kinematics
jetauto_bringup /home/jetauto/jetauto_ws/src/jetauto_bringup
jetauto_calibration /home/jetauto/jetauto_ws/src/jetauto_calibration
jetauto_controller /home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller
jetauto_description /home/jetauto/jetauto_ws/src/jetauto_simulations/jetauto_description
jetauto_example /home/jetauto/jetauto_ws/src/jetauto_example
jetauto_gazebo /home/jetauto/jetauto_ws/src/jetauto_simulationsjetauto_gazebo
jetauto_interfaces /home/jetauto/jetauto_ws/src/jetauto_interfaces
jetauto_moveit_config /home/jetauto/jetauto_ws/src/jetauto_simulations/jetauto_moveit_config
jetauto_multi /home/jetauto/jetauto_ws/src/jetauto_multi
jetauto_navigation /home/jetauto/jetauto_ws/src/jetauto_navigation
jetauto_peripherals /home/jetauto/jetauto_ws/src/jetauto_peripherals
jetauto_pointcloud_mapping /home/jetauto/catkin_ws/src/jetauto_pointcloud_mapping
jetauto_sdk /home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_sdk
jetauto_slam /home/jetauto/jetauto_ws/src/jetauto_slam
lidar_cloud /home/jetauto/jetauto_ws/src/lidar_cloud
moveit_kinematics /opt/ros/melodic/share/moveit_kinematics
mpu_6050_driver /home/jetauto/jetauto_ws/src/third_party/mpu_6050_driver
opencv_tests /home/jetauto/jetauto_ws/src/third_party/vision_opencv/opencv_tests
pointcloud_segmentation /home/jetauto/catkin_ws/src/pointcloud_segmentation
polygon_layer /home/jetauto/jetauto_ws/src/third_party/frontier_exploration/polygon_layer
rplidar_ros /home/jetauto/jetauto_ws/src/third_party/rplidar_ros
rrt_exploration /home/jetauto/jetauto_ws/src/third_party/rrt_exploration
rviz_plugin /home/jetauto/jetauto_ws/src/third_party/rviz_plugin
sparse_bundle_adjustment /home/jetauto/jetauto_ws/src/third_party/sparse_bundle_adjustment
stereo_image_proc /home/jetauto/jetauto_ws/src/third_party/image_pipeline/stereo_image_proc
trac_ik_kinematics_plugin /opt/ros/melodic/share/trac_ik_kinematics_plugin
virtual_wall /home/jetauto/jetauto_ws/src/third_party/virtual_wall
xf_mic_asr_offline /home/jetauto/jetauto_ws/src/xf_mic_asr_offline
ydlidar_ros_driver /home/jetauto/jetauto_ws/src/third_party/ydlidar_ros_driver
jetauto@jetauto-desktop:~$ rospack find jetauto_sdk
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_sdk
jetauto@jetauto-desktop:~$ rospack find hiwonder_interfaces
[rospack] Error: package 'hiwonder_interfaces' not found
jetauto@jetauto-desktop:~$ rosnode list | grep -Ei "servo|arm|kinematic|sdk"
/hiwonder_servo_manager
jetauto@jetauto-desktop:~$ rosnode info /jetauto_sdk
--------------------------------------------------------------------------------
Node [/jetauto_sdk]
Publications: None

Subscriptions: None

Services: None

cannot contact [/jetauto_sdk]: unknown node
```
```
JetAuto Pro
│
├── /dev/ttyUSB0
│     └── USB-Serial
│          └── usb-1a86_USB_Serial-if00-port0
│
├── ROS Melodic
│
├── hiwonder_servo_driver
├── hiwonder_servo_controllers
├── hiwonder_servo_msgs
│
├── /hiwonder_servo_manager        ← RUNNING
│
├── jetauto_arm_kinematics
├── jetauto_moveit_config
│
├── /arm_controller
├── /gripper_controller
├── /joint1_controller
├── /joint2_controller
├── /joint3_controller
├── /joint4_controller
└── /r_joint_controller
```
```
jetauto@jetauto-desktop:~$ rosnode list
/ar_app
/astra_cam/astra_cam_nodelet_manager
/astra_cam/astraplus
/astra_cam/depth_metric
/astra_cam/depth_metric_rect
/astra_cam/depth_points
/astra_cam/depth_rectify_depth
/astra_cam/depth_registered_hw_metric_rect
/astra_cam/depth_registered_metric
/astra_cam/depth_registered_rectify_depth
/astra_cam/driver
/astra_cam/points_xyzrgb_hw_registered
/astra_cam/rgb_rectify_color
/astra_cam_base_link
/astra_cam_base_link1
/astra_cam_base_link2
/astra_cam_base_link3
/hiwonder_servo_manager
/jetauto_controller
/joint_states_publisher
/joystick
/joystick_control
/lidar_app
/line_following
/object_tracking
/patrol_app
/rosapi
/rosbridge_websocket
/rosout
/rplidarNode
/usb_cam
/usb_cam/image_proc
/web_video_server
jetauto@jetauto-desktop:~$ rostopic list | grep -Ei "servo|arm|joint|kinematic"
/arm_controller/command
/arm_controller/follow_joint_trajectory/cancel
/arm_controller/follow_joint_trajectory/feedback
/arm_controller/follow_joint_trajectory/goal
/arm_controller/follow_joint_trajectory/result
/arm_controller/follow_joint_trajectory/status
/arm_controller/state
/gripper_controller/follow_joint_trajectory/cancel
/gripper_controller/follow_joint_trajectory/feedback
/gripper_controller/follow_joint_trajectory/goal
/gripper_controller/follow_joint_trajectory/result
/gripper_controller/follow_joint_trajectory/status
/joint1_controller/command
/joint1_controller/command_duration
/joint1_controller/state
/joint2_controller/command
/joint2_controller/command_duration
/joint2_controller/state
/joint3_controller/command
/joint3_controller/command_duration
/joint3_controller/state
/joint4_controller/command
/joint4_controller/command_duration
/joint4_controller/state
/joint_states
/jointr_controller/state
/r_joint_controller/command
/r_joint_controller/command_duration
/r_joint_controller/state
/servo_control/set_servo_state
/servo_controllers/port_id_1/id_pos_dur
/servo_controllers/port_id_1/multi_id_pos_dur
/servo_controllers/port_id_1/servo_states
jetauto@jetauto-desktop:~$ ls /dev/ttyUSB*
/dev/ttyUSB0
jetauto@jetauto-desktop:~$ ls /dev/ttyACM*
ls: cannot access '/dev/ttyACM*': No such file or directory
jetauto@jetauto-desktop:~$ ls /dev/ttyACM*
ls: cannot access '/dev/ttyACM*': No such file or directory
jetauto@jetauto-desktop:~$ ls /dev/ttyACM*
ls: cannot access '/dev/ttyACM*': No such file or directory
jetauto@jetauto-desktop:~$ ls /dev/serial/by-id/
usb-1a86_USB_Serial-if00-port0
jetauto@jetauto-desktop:~$ find ~/ -maxdepth 3 -type d \( -iname "*arm*" -o -iname "*servo*" \) 2>/dev/null
/home/jetauto/.pycharm_helpers
/home/jetauto/.pycharm_helpers/pycharm_display
/home/jetauto/.pycharm_helpers/pycharm
/home/jetauto/.pycharm_helpers/pycharm/pycharm_commands
/home/jetauto/.pycharm_helpers/pycharm_matplotlib_backend
/home/jetauto/jetauto_third_party/Astra_OpenNI/Arm64
/home/jetauto/jetauto_software/servo_tool
/home/jetauto/jetauto_software/jetauto_arm_pc
/home/jetauto/jetauto_ws/logs/hiwonder_servo_msgs
/home/jetauto/jetauto_ws/logs/hiwonder_servo_controllers
/home/jetauto/jetauto_ws/logs/jetauto_arm_kinematics
/home/jetauto/jetauto_ws/logs/hiwonder_servo_driver
/home/jetauto/jetauto_ws/build/hiwonder_servo_msgs
/home/jetauto/jetauto_ws/build/hiwonder_servo_controllers
/home/jetauto/jetauto_ws/build/jetauto_arm_kinematics
/home/jetauto/jetauto_ws/build/hiwonder_servo_driver
jetauto@jetauto-desktop:~$ find ~/ -maxdepth 4 -type f \( -iname "*servo*.py" -o -iname "*arm*.launch" -o -iname "*arm*.yaml" \) 2>/dev/null
/home/jetauto/jetauto_software/servo_tool/BusServoControl.py
/home/jetauto/jetauto_software/servo_tool/BusServoCmd.py
/home/jetauto/jetauto_software/servo_tool/servo_controller.py
/home/jetauto/jetauto_software/jetauto_arm_pc/BusServoControl.py
/home/jetauto/jetauto_software/jetauto_arm_pc/BusServoCmd.py
/home/jetauto/jetauto_software/jetauto_arm_pc/servo_controller.py
jetauto@jetauto-desktop:~$ rospack list | grep -Ei "servo|arm|kinematic|hiwonder|jetauto"
astra_camera /home/jetauto/jetauto_ws/src/third_party/ros_astra_camera
astra_demo /home/jetauto/catkin_ws/src/astra_demo
cartographer /home/jetauto/jetauto_ws/src/third_party/cartographer
cartographer_ros /home/jetauto/jetauto_ws/src/third_party/cartographer_ros/cartographer_ros
cartographer_ros_msgs /home/jetauto/jetauto_ws/src/third_party/cartographer_ros/cartographer_ros_msgs
cartographer_rviz /home/jetauto/jetauto_ws/src/third_party/cartographer_ros/cartographer_rviz
cv_bridge /home/jetauto/jetauto_ws/src/third_party/vision_opencv/cv_bridge
depth_image_proc /home/jetauto/jetauto_ws/src/third_party/image_pipeline/depth_image_proc
exploration_msgs /home/jetauto/jetauto_ws/src/third_party/frontier_exploration/exploration_msgs
exploration_server /home/jetauto/jetauto_ws/src/third_party/frontier_exploration/exploration_server
explore_lite /home/jetauto/jetauto_ws/src/third_party/explore
frontier_exploration /home/jetauto/jetauto_ws/src/third_party/frontier_exploration/frontier_exploration
hiwonder_servo_controllers /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers
hiwonder_servo_driver /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver
hiwonder_servo_msgs /home/jetauto/jetauto_ws/src/jetauto_driverhiwonder_servo/hiwonder_servo_msgs
image_geometry /home/jetauto/jetauto_ws/src/third_party/vision_opencv/image_geometry
image_proc /home/jetauto/jetauto_ws/src/third_party/image_pipeline/image_proc
image_publisher /home/jetauto/jetauto_ws/src/third_party/image_pipeline/image_publisher
image_rotate /home/jetauto/jetauto_ws/src/third_party/image_pipeline/image_rotate
image_view /home/jetauto/jetauto_ws/src/third_party/image_pipeline/image_view
imu_calib /home/jetauto/jetauto_ws/src/third_party/imu_calib
jetauto_app /home/jetauto/jetauto_ws/src/jetauto_app
jetauto_arm_kinematics /home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_arm_kinematics
jetauto_bringup /home/jetauto/jetauto_ws/src/jetauto_bringup
jetauto_calibration /home/jetauto/jetauto_ws/src/jetauto_calibration
jetauto_controller /home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller
jetauto_description /home/jetauto/jetauto_ws/src/jetauto_simulations/jetauto_description
jetauto_example /home/jetauto/jetauto_ws/src/jetauto_example
jetauto_gazebo /home/jetauto/jetauto_ws/src/jetauto_simulationsjetauto_gazebo
jetauto_interfaces /home/jetauto/jetauto_ws/src/jetauto_interfaces
jetauto_moveit_config /home/jetauto/jetauto_ws/src/jetauto_simulations/jetauto_moveit_config
jetauto_multi /home/jetauto/jetauto_ws/src/jetauto_multi
jetauto_navigation /home/jetauto/jetauto_ws/src/jetauto_navigation
jetauto_peripherals /home/jetauto/jetauto_ws/src/jetauto_peripherals
jetauto_pointcloud_mapping /home/jetauto/catkin_ws/src/jetauto_pointcloud_mapping
jetauto_sdk /home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_sdk
jetauto_slam /home/jetauto/jetauto_ws/src/jetauto_slam
lidar_cloud /home/jetauto/jetauto_ws/src/lidar_cloud
moveit_kinematics /opt/ros/melodic/share/moveit_kinematics
mpu_6050_driver /home/jetauto/jetauto_ws/src/third_party/mpu_6050_driver
opencv_tests /home/jetauto/jetauto_ws/src/third_party/vision_opencv/opencv_tests
pointcloud_segmentation /home/jetauto/catkin_ws/src/pointcloud_segmentation
polygon_layer /home/jetauto/jetauto_ws/src/third_party/frontier_exploration/polygon_layer
rplidar_ros /home/jetauto/jetauto_ws/src/third_party/rplidar_ros
rrt_exploration /home/jetauto/jetauto_ws/src/third_party/rrt_exploration
rviz_plugin /home/jetauto/jetauto_ws/src/third_party/rviz_plugin
sparse_bundle_adjustment /home/jetauto/jetauto_ws/src/third_party/sparse_bundle_adjustment
stereo_image_proc /home/jetauto/jetauto_ws/src/third_party/image_pipeline/stereo_image_proc
trac_ik_kinematics_plugin /opt/ros/melodic/share/trac_ik_kinematics_plugin
virtual_wall /home/jetauto/jetauto_ws/src/third_party/virtual_wall
xf_mic_asr_offline /home/jetauto/jetauto_ws/src/xf_mic_asr_offline
ydlidar_ros_driver /home/jetauto/jetauto_ws/src/third_party/ydlidar_ros_driver
jetauto@jetauto-desktop:~$ rospack find jetauto_sdk
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_sdk
jetauto@jetauto-desktop:~$ rospack find hiwonder_interfaces
[rospack] Error: package 'hiwonder_interfaces' not found
jetauto@jetauto-desktop:~$ rosnode list | grep -Ei "servo|arm|kinematic|sdk"
/hiwonder_servo_manager
jetauto@jetauto-desktop:~$ rosnode info /jetauto_sdk
--------------------------------------------------------------------------------
Node [/jetauto_sdk]
Publications: None

Subscriptions: None

Services: None

cannot contact [/jetauto_sdk]: unknown node
jetauto@jetauto-desktop:~$ rosnode info /hiwonder_servo_manager
--------------------------------------------------------------------------------
Node [/hiwonder_servo_manager]
Publications:
 * /ActionGroupRunner/feedback [hiwonder_servo_msgs/ActionGroupRunnerActionFeedback]
 * /ActionGroupRunner/result [hiwonder_servo_msgs/ActionGroupRunnerActionResult]
 * /ActionGroupRunner/status [actionlib_msgs/GoalStatusArray]
 * /arm_controller/follow_joint_trajectory/feedback [control_msgs/FollowJointTrajectoryActionFeedback]
 * /arm_controller/follow_joint_trajectory/result [control_msgs/FollowJointTrajectoryActionResult]
 * /arm_controller/follow_joint_trajectory/status [actionlib_msgs/GoalStatusArray]
 * /arm_controller/state [control_msgs/FollowJointTrajectoryFeedback]
 * /gripper_controller/follow_joint_trajectory/feedback [control_msgs/FollowJointTrajectoryActionFeedback]
 * /gripper_controller/follow_joint_trajectory/result [control_msgs/FollowJointTrajectoryActionResult]
 * /gripper_controller/follow_joint_trajectory/status [actionlib_msgs/GoalStatusArray]
 * /gripper_controller/state [control_msgs/FollowJointTrajectoryFeedback]
 * /joint1_controller/state [hiwonder_servo_msgs/JointState]
 * /joint2_controller/state [hiwonder_servo_msgs/JointState]
 * /joint3_controller/state [hiwonder_servo_msgs/JointState]
 * /joint4_controller/state [hiwonder_servo_msgs/JointState]
 * /r_joint_controller/state [hiwonder_servo_msgs/JointState]
 * /rosout [rosgraph_msgs/Log]
 * /servo_controllers/port_id_1/servo_states [hiwonder_servo_msgs/ServoStateList]

Subscriptions:
 * /ActionGroupRunner/cancel [unknown type]
 * /ActionGroupRunner/goal [unknown type]
 * /arm_controller/command [unknown type]
 * /arm_controller/follow_joint_trajectory/cancel [unknown type]
 * /arm_controller/follow_joint_trajectory/goal [unknown type]
 * /gripper_controller/command [unknown type]
 * /gripper_controller/follow_joint_trajectory/cancel [unknown type]
 * /gripper_controller/follow_joint_trajectory/goal [unknown type]
 * /joint1_controller/command [unknown type]
 * /joint1_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /joint2_controller/command [unknown type]
 * /joint2_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /joint3_controller/command [unknown type]
 * /joint3_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /joint4_controller/command [unknown type]
 * /joint4_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /r_joint_controller/command [unknown type]
 * /r_joint_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /servo_control/set_servo_state [unknown type]
 * /servo_controllers/port_id_1/id_pos_dur [unknown type]
 * /servo_controllers/port_id_1/multi_id_pos_dur [hiwonder_servo_msgs/MultiRawIdPosDur]
 * /servo_controllers/port_id_1/servo_states [hiwonder_servo_msgs/ServoStateList]

Services:
 * /hiwonder_servo_manager/get_loggers
 * /hiwonder_servo_manager/set_logger_level
 * /servo_control/get_servo_state
 * /servo_control/set_read_timeout


contacting node http://localhost:36273/ ...
Pid: 8992
Connections:
 * topic: /rosout
    * to: /rosout
    * direction: outbound (32803 - 127.0.0.1:38908) [12]
    * transport: TCPROS
 * topic: /servo_controllers/port_id_1/servo_states
    * to: /hiwonder_servo_manager
    * direction: outbound (32803 - 127.0.0.1:39024) [29]
    * transport: TCPROS
 * topic: /r_joint_controller/state
    * to: /joint_states_publisher
    * direction: outbound (32803 - 127.0.0.1:38978) [21]
    * transport: TCPROS
 * topic: /joint4_controller/state
    * to: /joystick_control
    * direction: outbound (32803 - 127.0.0.1:39112) [32]
    * transport: TCPROS
 * topic: /joint4_controller/state
    * to: /joint_states_publisher
    * direction: outbound (32803 - 127.0.0.1:39114) [40]
    * transport: TCPROS
 * topic: /joint2_controller/state
    * to: /joint_states_publisher
    * direction: outbound (32803 - 127.0.0.1:39188) [41]
    * transport: TCPROS
 * topic: /joint2_controller/state
    * to: /joystick_control
    * direction: outbound (32803 - 127.0.0.1:39196) [49]
    * transport: TCPROS
 * topic: /joint1_controller/state
    * to: /joint_states_publisher
    * direction: outbound (32803 - 127.0.0.1:39198) [51]
    * transport: TCPROS
 * topic: /joint1_controller/state
    * to: /joystick_control
    * direction: outbound (32803 - 127.0.0.1:39204) [48]
    * transport: TCPROS
 * topic: /joint3_controller/state
    * to: /joint_states_publisher
    * direction: outbound (32803 - 127.0.0.1:39232) [54]
    * transport: TCPROS
 * topic: /joint3_controller/state
    * to: /joystick_control
    * direction: outbound (32803 - 127.0.0.1:39240) [59]
    * transport: TCPROS
 * topic: /servo_controllers/port_id_1/multi_id_pos_dur
    * to: /line_following (http://localhost:38915/)
    * direction: inbound
    * transport: TCPROS
 * topic: /servo_controllers/port_id_1/multi_id_pos_dur
    * to: /object_tracking (http://localhost:36947/)
    * direction: inbound
    * transport: TCPROS
 * topic: /r_joint_controller/command_duration
    * to: /joystick_control (http://localhost:45415/)
    * direction: inbound
    * transport: TCPROS
 * topic: /servo_controllers/port_id_1/servo_states
    * to: /hiwonder_servo_manager (http://localhost:36273/)
    * direction: inbound
    * transport: TCPROS
 * topic: /joint4_controller/command_duration
    * to: /joystick_control (http://localhost:45415/)
    * direction: inbound
    * transport: TCPROS
 * topic: /joint2_controller/command_duration
    * to: /joystick_control (http://localhost:45415/)
    * direction: inbound
    * transport: TCPROS
 * topic: /joint1_controller/command_duration
    * to: /joystick_control (http://localhost:45415/)
    * direction: inbound
    * transport: TCPROS
 * topic: /joint3_controller/command_duration
    * to: /joystick_control (http://localhost:45415/)
    * direction: inbound
    * transport: TCPROS

jetauto@jetauto-desktop:~$ rostopic info /servo_controllers/port_id_1/servo_states
Type: hiwonder_servo_msgs/ServoStateList

Publishers:
 * /hiwonder_servo_manager (http://localhost:36273/)

Subscribers:
 * /hiwonder_servo_manager (http://localhost:36273/)


jetauto@jetauto-desktop:~$ rostopic echo /servo_controllers/port_id_1/servo_states
servo_states:
  -
    timestamp: 1787048287.12
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.13
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.14
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.15
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.16
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048287.22
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.23
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.24
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.25
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.26
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048287.32
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.33
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.34
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.35
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.36
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048287.42
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.43
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.44
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.45
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.46
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048287.52
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.53
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.54
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.55
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.56
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048287.62
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.63
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.64
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.65
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.66
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048287.72
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.73
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.74
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.75
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.76
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048287.82
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.83
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.84
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.85
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.86
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048287.92
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.93
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.94
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.95
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048287.96
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048288.02
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.03
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.04
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.05
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.06
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048288.12
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.13
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.14
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.15
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.16
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048288.22
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.23
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.24
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.25
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.26
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048288.32
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.33
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.34
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.35
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.36
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048288.42
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.43
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.44
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.45
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.46
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048288.52
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.53
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.54
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.55
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.56
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048288.62
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.63
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.64
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.65
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.66
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048288.72
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.73
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.74
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.75
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.76
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048288.82
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.83
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.84
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.85
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.86
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048288.92
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.93
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.94
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.95
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048288.96
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048289.02
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.03
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.04
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.05
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.06
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048289.12
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.13
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.14
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.15
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.16
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048289.22
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.23
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.24
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.25
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.26
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048289.32
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.33
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.34
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.35
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.36
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048289.42
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.43
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.44
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.45
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.46
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
servo_states:
  -
    timestamp: 1787048289.52
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.53
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.54
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.55
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048289.56
    id: 5
    goal: 500
    position: 500
    error: 0
    voltage: 9000
---
^Cjetauto@jetauto-desktop:~$ rostopic echo /joint1_controller/stete
header:
  seq: 6706
  stamp:
    secs: 1787048343
    nsecs: 356421232
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6707
  stamp:
    secs: 1787048343
    nsecs: 456533670
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6708
  stamp:
    secs: 1787048343
    nsecs: 556492090
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6709
  stamp:
    secs: 1787048343
    nsecs: 656440734
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6710
  stamp:
    secs: 1787048343
    nsecs: 756407260
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6711
  stamp:
    secs: 1787048343
    nsecs: 856525659
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6712
  stamp:
    secs: 1787048343
    nsecs: 956485033
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6713
  stamp:
    secs: 1787048344
    nsecs:  59899091
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6714
  stamp:
    secs: 1787048344
    nsecs: 156450033
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6715
  stamp:
    secs: 1787048344
    nsecs: 256728410
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6716
  stamp:
    secs: 1787048344
    nsecs: 356501579
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6717
  stamp:
    secs: 1787048344
    nsecs: 456523656
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6718
  stamp:
    secs: 1787048344
    nsecs: 556571483
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6719
  stamp:
    secs: 1787048344
    nsecs: 656461000
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
header:
  seq: 6720
  stamp:
    secs: 1787048344
    nsecs: 756492614
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
^Cheader:
  seq: 6721
  stamp:
    secs: 1787048344
    nsecs: 856446743
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
jetauto@jetauto-desktop:~$ rostopic echo /joint2_controller/state
header:
  seq: 6968
  stamp:
    secs: 1787048369
    nsecs: 546355247
  frame_id: ''
name: "joint2"
servo_ids: [4]
servo_temps: [0]
goal_pos: -0.699527952267
current_pos: -0.699527952267
error: 0.0
velocity: 10.0
---
header:
  seq: 6969
  stamp:
    secs: 1787048369
    nsecs: 646368026
  frame_id: ''
name: "joint2"
servo_ids: [4]
servo_temps: [0]
goal_pos: -0.699527952267
current_pos: -0.699527952267
error: 0.0
velocity: 10.0
---
header:
  seq: 6970
  stamp:
    secs: 1787048369
    nsecs: 746321439
  frame_id: ''
name: "joint2"
servo_ids: [4]
servo_temps: [0]
goal_pos: -0.699527952267
current_pos: -0.699527952267
error: 0.0
velocity: 10.0
---
header:
  seq: 6971
  stamp:
    secs: 1787048369
    nsecs: 846285820
  frame_id: ''
name: "joint2"
servo_ids: [4]
servo_temps: [0]
goal_pos: -0.699527952267
current_pos: -0.699527952267
error: 0.0
velocity: 10.0
---
header:
  seq: 6972
  stamp:
    secs: 1787048369
    nsecs: 946287870
  frame_id: ''
name: "joint2"
servo_ids: [4]
servo_temps: [0]
goal_pos: -0.699527952267
current_pos: -0.699527952267
error: 0.0
velocity: 10.0
---
header:
  seq: 6973
  stamp:
    secs: 1787048370
    nsecs:  46521902
  frame_id: ''
name: "joint2"
servo_ids: [4]
servo_temps: [0]
goal_pos: -0.699527952267
current_pos: -0.699527952267
error: 0.0
velocity: 10.0
---
header:
  seq: 6974
  stamp:
    secs: 1787048370
    nsecs: 146295785
  frame_id: ''
name: "joint2"
servo_ids: [4]
servo_temps: [0]
goal_pos: -0.699527952267
current_pos: -0.699527952267
error: 0.0
velocity: 10.0
---
header:
  seq: 6975
  stamp:
    secs: 1787048370
    nsecs: 246442079
  frame_id: ''
name: "joint2"
servo_ids: [4]
servo_temps: [0]
goal_pos: -0.699527952267
current_pos: -0.699527952267
error: 0.0
velocity: 10.0
---
header:
  seq: 6976
  stamp:
    secs: 1787048370
    nsecs: 346468448
  frame_id: ''
name: "joint2"
servo_ids: [4]
servo_temps: [0]
goal_pos: -0.699527952267
current_pos: -0.699527952267
error: 0.0
velocity: 10.0
---
^Cjetauto@jetauto-desktop:~$ rostopic echo /joint3_controller/stete
header:
  seq: 7249
  stamp:
    secs: 1787048397
    nsecs: 736185312
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7250
  stamp:
    secs: 1787048397
    nsecs: 836118936
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7251
  stamp:
    secs: 1787048397
    nsecs: 936072587
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7252
  stamp:
    secs: 1787048398
    nsecs:  36337137
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7253
  stamp:
    secs: 1787048398
    nsecs: 136315822
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7254
  stamp:
    secs: 1787048398
    nsecs: 236362457
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7255
  stamp:
    secs: 1787048398
    nsecs: 336304187
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7256
  stamp:
    secs: 1787048398
    nsecs: 436178922
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7257
  stamp:
    secs: 1787048398
    nsecs: 536131858
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7258
  stamp:
    secs: 1787048398
    nsecs: 636314153
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7259
  stamp:
    secs: 1787048398
    nsecs: 736111402
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
header:
  seq: 7260
  stamp:
    secs: 1787048398
    nsecs: 836314916
  frame_id: ''
name: "joint3"
servo_ids: [3]
servo_temps: [0]
goal_pos: 1.91846588107
current_pos: 1.91846588107
error: 0.0
velocity: 10.0
---
^Cjetauto@jetauto-desktop:~$ rostopic echo /joint4_controller/stete
header:
  seq: 7568
  stamp:
    secs: 1787048429
    nsecs: 326615571
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7569
  stamp:
    secs: 1787048429
    nsecs: 426091194
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7570
  stamp:
    secs: 1787048429
    nsecs: 525979280
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7571
  stamp:
    secs: 1787048429
    nsecs: 625947952
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7572
  stamp:
    secs: 1787048429
    nsecs: 725998878
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7573
  stamp:
    secs: 1787048429
    nsecs: 826081275
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7574
  stamp:
    secs: 1787048429
    nsecs: 926061391
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7575
  stamp:
    secs: 1787048430
    nsecs:  26009082
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7576
  stamp:
    secs: 1787048430
    nsecs: 126113176
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7577
  stamp:
    secs: 1787048430
    nsecs: 226023197
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7578
  stamp:
    secs: 1787048430
    nsecs: 326122045
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7579
  stamp:
    secs: 1787048430
    nsecs: 426101446
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
header:
  seq: 7580
  stamp:
    secs: 1787048430
    nsecs: 526080846
  frame_id: ''
name: "joint4"
servo_ids: [2]
servo_temps: [0]
goal_pos: 1.22312671893
current_pos: 1.22312671893
error: 0.0
velocity: 10.0
---
^Cjetauto@jetauto-desktop:~$ find ~/jetauto_ws/src/jetauto_drive-type f | grep -Ei "servo|arm|controller"
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/srv/GetServoState.srv
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/srv/SetReadTimeout.srv
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/package.xml
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/CMakeLists.txt
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/msg/MultiRawIdPosDur.msg
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/msg/ServoState.msg
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/msg/SetServoState.msg
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/msg/ServoStateList.msg
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/msg/CommandDuration.msg
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/msg/JointState.msg
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/msg/CommandDurationList.msg
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/msg/RawIdPosDur.msg
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/action/ActionGroupRunner.action
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/joint_state_publisher.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/setup.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/launch/joint_states_publisher.launch
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/launch/controller_manager.launch
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/launch/start.launch
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/package.xml
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/config/hiwonder_servo_controller.yaml
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/CMakeLists.txt
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/action_group_runner.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/bus_servo_control.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/bus_servo_control.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_controller.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/joint_position_controller.cpython-36.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/action_group_runner.cpython-36.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/bus_servo_control.cpython-36.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/joint_controller.cpython-36.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/joint_trajectory_action_controller.cpython-36.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_trajectory_action_controller.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/setup.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/package.xml
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/CMakeLists.txt
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/__pycache__/hiwonderservo_serialproxy.cpython-36.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/__pycache__/hiwonderservo_const.cpython-36.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/__pycache__/hiwonderservo_io.cpython-36.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_const.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/scripts/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/scripts/jetauto_controller_main.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/scripts/odom_publisher.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/launch/jetauto_controller.launch
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/launch/odom_publish.launch
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/package.xml
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/config/calibrate_params.yaml
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/CMakeLists.txt
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/frames.pdf
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_controller/frames.gv
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_sdk/src/jetauto_sdk/hiwonder_servo_controller.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_sdk/src/jetauto_sdk/hiwonder_servo_cmd.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_sdk/src/jetauto_sdk/__pycache__/hiwonder_servo_controller.cpython-36.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_sdk/src/jetauto_sdk/__pycache__/hiwonder_servo_cmd.cpython-36.pyc
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_sdk/src/jetauto_sdk/pwm_servo.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_arm_kinematics/setup.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_arm_kinematics/package.xml
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_arm_kinematics/build/lib/kinematics/search_kinematics_solutions.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_arm_kinematics/build/lib/kinematics/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_arm_kinematics/CMakeLists.txt
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_arm_kinematics/src/search_kinematics_solutions.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_arm_kinematics/src/__init__.py
/home/jetauto/jetauto_ws/src/jetauto_driver/jetauto_arm_kinematics/src/kinematics.so
jetauto@jetauto-desktop:~$ grep -R "ttyUSB\|port_id\|servo_id\|baudrate\|baud_rate" \
> ~/jetauto_ws/src/jetauto_driver/hiwonder_servo \
> ~/jetauto_ws/src/jetauto_driver/jetauto_bringup \
> 2>/dev/null
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/msg/JointState.msg:int32[] servo_ids   # motor ids controlling this joint
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py:           port_id = str(serial['port_id'])
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py:           baud_rate = serial['baud_rate']
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py:                                       str(port_id),
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py:                                       baud_rate,
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py:            self.serial_proxies[port_id] = serial_proxy
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py:        port_id = str(ctl_params['port_id'])
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py:        if port_id in self.serial_proxies:
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py:            controller = JointPositionController(self.serial_proxies[port_i].servo_io, ctl_name, port_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py:                self.controllers_by_id[controller.servo_id] = controller
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/config/hiwonder_servo_controller.yaml:   port_id: 1
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/config/hiwonder_servo_controller.yaml:   port_id: 1
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/config/hiwonder_servo_controller.yaml:   port_id: 1
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/config/hiwonder_servo_controller.yaml:   port_id: 1
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/config/hiwonder_servo_controller.yaml:   port_id: 1
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/config/hiwonder_servo_controller.yaml:   port_id: 1
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/config/hiwonder_servo_controller.yaml:   baud_rate: 115200
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/bus_servo_control.pyc matches
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/bus_servo_control.py:    joints_pub = rospy.Publisher('/servo_controllers/port_id_1/multi_id_pos_dur', MultiRawIdPosDur, queue_size=1)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_controller.py:    def __init__(self, servo_io, controller_namespace,port_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_controller.py:        self.port_id = str(port_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_controller.py:        self.servo_states_sub = rospy.Subscriber('servo_controllers/port_id_%s/servo_states' % self.port_id, ServoStateList,
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/joint_position_controller.cpython-36.pyc matches
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/bus_servo_control.cpython-36.pyc matches
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/joint_controller.cpython-36.pyc matches
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/joint_trajectory_action_controller.cpython-36.pyc matches
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:    def __init__(self, servo_io, controller_namespace, port_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        JointController.__init__(self, servo_io, controller_namespace, port_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        self.port_id = str(port_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        self.servo_id = rospy.get_param(self.param_namespace + '/servo/id')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        self.joint_state = JointState(name=self.joint_name, servo_ids=[self.servo_id])
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        # if not self.servo_id in available_ids:
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        #     rospy.logwarn('Specified id: %d' % self.servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        # 'hiwonder_servo/%s/%d/radians_per_encoder_tick' % (self.port_namespace, self.servo_id))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        # 'hiwonder_servo/%s/%d/encoder_ticks_per_radian' % (self.port_namespace, self.servo_id))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        # 'hiwonder_servo/%s/%d/encoder_resolution' % (self.port_namespace, self.servo_id))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        # 'hiwonder_servo/%s/%d/radians_second_per_encoder_tick' % (self.port_namespace, self.servo_id))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        # rospy.get_param('hiwonder_servo/%s/%d/max_velocity' % (self.port_namespace, self.servo_id))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:            state = list(filter(lambda state: state.id == self.servo_id, state_list.servo_states))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        self.servo_io.set_position(self.servo_id, pos)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        self.servo_io.set_position(self.servo_id, int(pos), int(duration))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        self.servo_io.set_position(self.servo_id, int(pos), int(duration))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_position_controller.py:        self.servo_io.set_position(self.servo_id, pos, duration)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_trajectory_action_controller.py:            if c.port_id not in self.port_to_joints:
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_trajectory_action_controller.py:                self.port_to_joints[c.port_id] = []
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_trajectory_action_controller.py:            self.port_to_joints[c.port_id].append(c.joint_name)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_trajectory_action_controller.py:            if c.port_id in self.port_to_io:
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_trajectory_action_controller.py:            self.port_to_io[c.port_i] = c.servo_io
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_trajectory_action_controller.py:                    servo_id = self.joint_to_controller[joint].servo_id
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/joint_trajectory_action_controller.py:                    vals.append((servo_id, pos))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:                 port_id= 1,
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:                 baud_rate='115200',
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        self.port_id = str(port_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        self.baud_rate = baud_rate
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        self.min_servo_id = min_motor_id
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        self.max_servo_id = max_motor_id
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        self.servo_states_pub = rospy.Publisher('servo_controllers/port_id_{}/servo_states'.format(self.port_id),
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        self.servo_command_sub = rospy.Subscriber('servo_controllers/port_id_{}/id_pos_dur'.format(self.port_id),
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        self.servo_command_sub = rospy.Subscriber('servo_controllers/port_id_{}/multi_id_pos_dur'.format(self.port_id),
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            self.servo_io.set_servo_id(param[0], param[1])
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        servo_id = msg.id
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            if servo_id >= 0:
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:                result = self.servo_io.get_servo_id(servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:                result = self.servo_io.get_servo_id()
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            result = self.servo_io.get_servo_deviationservo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            result = self.servo_io.get_servo_range(servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            result = self.servo_io.get_servo_vin_rangeservo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            result = self.servo_io.get_servo_temp_range(servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            result = self.servo_io.get_servo_temp(servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            result = self.servo_io.get_servo_vin(servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            result = self.servo_io.get_servo_load_state(servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            self.servo_io = hiwonder_servo_io.HiwonderServoIO(self.port_name, self.baud_rate)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            '%s: Pinging motor IDs %d through %d...' % (self.port_id, self.min_servo_id, self.max_servo_id))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            for servo_id in range(self.min_servo_id, self.max_servo_id + 1):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:                result = self.servo_io.ping(servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:                    self.servos.append(servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            rospy.logfatal('port_id_%s: No motors found.' % self.port_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        status_str = 'port_id_%s: Found %d motors - ' % (self.port_id, len(self.servos))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:            for servo_id in self.servos:
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:                    state = self.servo_io.get_feedbackservo_id, self.fake_read)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:                    #print(servo_id, state['position'])
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/__pycache__/hiwonder_servo_serialproxy.cpython-36.pyc matches
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/__pycache__/hiwonder_servo_io.cpython-36.pyc matches
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def __init__(self, port, baudrate):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            self.ser = serial.Serial(port, baudrate, timeout=0.01)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            raise SerialOpenError(port, baudrate)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def __read_response(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            raise DroppedPacketError('Invalid response received from servo ' + str(servo_id) + ' ' + str(e))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            raise ChecksumError(servo_id, data, checksum)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def read(self, servo_id, cmd):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        checksum = 255 - ((servo_id + length + cmd) % 256)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        packet = [0x55, 0x55, servo_id, length, cmd, checksum]
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                    data = self.__read_response(servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def write(self, servo_id, cmd, params):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        """ Write the values from the "data" list to the servo with "servo_id"
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        checksum = 255 - ((servo_id + length + cmd + sum(params)) % 256)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        packet = [0x55, 0x55, servo_id, length, cmd]
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def ping(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        checksum = 255 - ((servo_id + length + HIWONDER_SERVO_ID_READ) % 256)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        packet = [0x55, 0x55, servo_id, length, HIWONDER_SERVO_ID_READ, checksum]
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                    response = self.__read_response(servo_id)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                    if response[5] == servo_id:
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_position(self, servo_id, fake_read=False):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            return self.servos[servo_id].goal
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            response = self.read(servo_id, HIWONDER_SERVO_POS_READ)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                self.exception_on_error(response[4], servo_id, 'fetching present position')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_voltage(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        response = self.read(servo_id, HIWONDER_SERVO_VIN_READ)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            self.exception_on_error(response[4], servo_id, 'fetching supplied voltage')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_feedback(self, servo_id, fake_read=False):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        position = self.get_position(servo_id, fake_read)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            goal = self.servos[servo_id].goal
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                    'id': servo_id,
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def set_servo_id(self, oldid, newid):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_servo_id(self, servo_id=None):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            if servo_id is None:  # 总线上只能有一个舵机
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                response = self.read(servo_id, HIWONDER_SERVO_ID_READ)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                self.exception_on_error(response[4], servo_id, 'fetching present position')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def set_position(self, servo_id, position, duration=None):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        # print("id:{}, pos:{}, duration:{}".format(servo_id, position, duration))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        servo = self.servos[servo_id]
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        self.write(servo_id, HIWONDER_SERVO_MOVE_TIME_WRITE, (loVal, hiVal, loTime, hiTime))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def stop(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        self.write(servo_id, HIWONDER_SERVO_MOVE_STOP, ())
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def set_servo_deviation(self, servo_id, dev=0):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        self.write(servo_id, HIWONDER_SERVO_ANGLE_OFFSET_ADJUST, (dev, ))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def save_servo_deviation(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        self.write(servo_id, HIWONDER_SERVO_ANGLE_OFFSET_WRITE, ())
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_servo_deviation(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            response = self.read(servo_id, HIWONDER_SERVO_ANGLE_OFFSET_READ)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                self.exception_on_error(response[4], servo_id, 'fetching present position')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def set_servo_range(self, servo_id, low, high):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        self.write(servo_id, HIWONDER_SERVO_ANGLE_LIMIT_WRITE, (loLow, hiLow, loHigh, hiHigh))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_servo_range(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            response = self.read(servo_id, HIWONDER_SERVO_ANGLE_LIMIT_READ)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                self.exception_on_error(response[4], servo_id, 'fetching present position')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def set_servo_vin_range(self, servo_id, low, high):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        self.write(servo_id, HIWONDER_SERVO_VIN_LIMIT_WRITE, (loLow, hiLow, loHigh, hiHigh))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_servo_vin_range(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            response = self.read(servo_id, HIWONDER_SERVO_VIN_LIMIT_READ)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                self.exception_on_error(response[4], servo_id, 'fetching present position')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def set_servo_temp_range(self, servo_id, m_temp):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        self.write(servo_id, HIWONDER_SERVO_TEMP_MAX_LIMIT_WRITE, (m_temp, ))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_servo_temp_range(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            response = self.read(servo_id, HIWONDER_SERVO_TEMP_MAX_LIMIT_READ)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                self.exception_on_error(response[4], servo_id, 'fetching present position')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_servo_temp(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            response = self.read(servo_id, HIWONDER_SERVO_TEMP_READ)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                self.exception_on_error(response[4], servo_id, 'fetching present position')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_servo_vin(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            response = self.read(servo_id, HIWONDER_SERVO_VIN_READ)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                self.exception_on_error(response[4], servo_id, 'fetching present position')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def reset(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        self.set_deviation(servo_id, 0)    # 清零偏差
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        self.write(servo_id, HIWONDER_SERVO_MOVE_TIME_WRITE, 500, 100)    # 中位
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def unload_servo(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        self.write(servo_id, HIWONDER_SERVO_LOAD_OR_UNLOAD_WRITE, (0, ))
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def get_servo_load_state(self, servo_id):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py            response = self.read(servo_id, HIWONDER_SERVO_LOAD_OR_UNLOAD_READ)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                self.exception_on_error(response[4], servo_id, 'fetching present position')
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def exception_on_error(self, error_code, servo_id, command_failed):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py        ex_message = '[servo #%d on %s@%sbps]: %s failed' % (servo_id, self.ser.port, self.ser.baudrate, command_failed)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py    def __init__(self, servo_id, response, checksum):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_io.py                       % (servo_id, response[-1], checksum)
jetauto@jetauto-desktop:~$ ls -l /dev/ttyUSB0
crw-rw-rw- 1 root dialout 188, 0 Aug 18 15:37 /dev/ttyUSB0
jetauto@jetauto-desktop:~$ ls -l /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0
lrwxrwxrwx 1 root root 13 Aug 18 14:42 /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 -> ../../ttyUSB0
jetauto@jetauto-desktop:~$ ls -l /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0
lrwxrwxrwx 1 root root 13 Aug 18 14:42 /dev/serial/by-id/usb-1a86_USB_Serial-if00-port0 -> ../../ttyUSB0
jetauto@jetauto-desktop:~$ groups
jetauto adm dialout cdrom sudo audio dip video plugdev i2c lpadmin gdm lightdm sambashare weston-launch gpio jtop
jetauto@jetauto-desktop:~$ rostopic type /joint1_controller/command
std_msgs/Float64
jetauto@jetauto-desktop:~$ rosmsg show $(rostopic type /joint1_controller/command)
float64 data

jetauto@jetauto-desktop:~$ rosparam get /joint1_controller
ERROR: Parameter [/joint1_controller] is not set
jetauto@jetauto-desktop:~$ rosparam get /joint2_controller
ERROR: Parameter [/joint2_controller] is not set
jetauto@jetauto-desktop:~$ rostopic info /joint1_controller/command
Type: std_msgs/Float64

Publishers: None

Subscribers:
 * /hiwonder_servo_manager (http://localhost:36273/)


jetauto@jetauto-desktop:~$ rostopic pub -1 /joint1_controller/command std_msgs/Float64 "data: 0.1"
publishing and latching message for 3.0 seconds
jetauto@jetauto-desktop:~$ rostopic echo -n 1 /joint1_controller/state
header:
  seq: 12068
  stamp:
    secs: 1787048879
    nsecs: 556596994
  frame_id: ''
name: "joint1"
servo_ids: [5]
servo_temps: [0]
goal_pos: 0.1005309632
current_pos: 0.1005309632
error: 0.0
velocity: 10.0
---
jetauto@jetauto-desktop:~$ rostopic echo -n 1 /servo_controllers/port_id_1/servo_states
servo_states:
  -
    timestamp: 1787048955.82
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048955.83
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048955.84
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048955.85
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048955.86
    id: 5
    goal: 476
    position: 476
    error: 0
    voltage: 9000
---
jetauto@jetauto-desktop:~$ rostopic pub -1 /joint1_controller/command std_msgs/Float64 "data: -0.1"
publishing and latching message for 3.0 seconds
jetauto@jetauto-desktop:~$ rostopic echo -n 1 /servo_controllers/port_id_1/servo_states
servo_states:
  -
    timestamp: 1787048973.32
    id: 1
    goal: 500
    position: 500
    error: 0
    voltage: 9000
  -
    timestamp: 1787048973.33
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787048973.34
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787048973.35
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787048973.36
    id: 5
    goal: 524
    position: 524
    error: 0
    voltage: 9000
---
jetauto@jetauto-desktop:~$ rosnode info /hiwonder_servo_manager | grep -A5 -B2 gripper
 * /arm_controller/follow_joint_trajectory/status [actionlib_msgs/GoalStatusArray]
 * /arm_controller/state [control_msgs/FollowJointTrajectoryFeedback]
 * /gripper_controller/follow_joint_trajectory/feedback [control_msgs/FollowJointTrajectoryActionFeedback]
 * /gripper_controller/follow_joint_trajectory/result [control_msgs/FollowJointTrajectoryActionResult]
 * /gripper_controller/follow_joint_trajectory/status [actionlib_msgs/GoalStatusArray]
 * /gripper_controller/state [control_msgs/FollowJointTrajectoryFeedback]
 * /joint1_controller/state [hiwonder_servo_msgs/JointState]
 * /joint2_controller/state [hiwonder_servo_msgs/JointState]
 * /joint3_controller/state [hiwonder_servo_msgs/JointState]
 * /joint4_controller/state [hiwonder_servo_msgs/JointState]
 * /r_joint_controller/state [hiwonder_servo_msgs/JointState]
--
 * /arm_controller/follow_joint_trajectory/cancel [unknown type]
 * /arm_controller/follow_joint_trajectory/goal [unknown type]
 * /gripper_controller/command [unknown type]
 * /gripper_controller/follow_joint_trajectory/cancel [unknown type]
 * /gripper_controller/follow_joint_trajectory/goal [unknown type]
 * /joint1_controller/command [unknown type]
 * /joint1_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /joint2_controller/command [unknown type]
 * /joint2_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /joint3_controller/command [unknown type]
jetauto@jetauto-desktop:~$ rostopic info /gripper_controller/follow_joint_trajectory/goal
Type: control_msgs/FollowJointTrajectoryActionGoal

Publishers: None

Subscribers:
 * /hiwonder_servo_manager (http://localhost:36273/)


jetauto@jetauto-desktop:~$ rostopic type /gripper_controller/command
trajectory_msgs/JointTrajectory
jetauto@jetauto-desktop:~$ rostopic info /r_joint_controller/command
Type: std_msgs/Float64

Publishers: None

Subscribers:
 * /hiwonder_servo_manager (http://localhost:36273/)


jetauto@jetauto-desktop:~$ cat ~/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/config/hiwonder_servo_controller.yaml
controllers:
  joint1_controller:
    type: JointPositionController
    joint_name: joint1
    joint_speed: 1.0
    port_id: 1
    servo:
      id: 5
      init: 500
      min: 1000
      max: 0

  joint2_controller:
    type: JointPositionController
    joint_name: joint2
    joint_speed: 1.0
    port_id: 1
    servo:
      id: 4
      init: 500
      min: 1000
      max: 0

  joint3_controller:
    type: JointPositionController
    joint_name: joint3
    joint_speed: 1.0
    port_id: 1
    servo:
      id: 3
      init: 500
      min: 1000
      max: 0

  joint4_controller:
    type: JointPositionController
    joint_name: joint4
    joint_speed: 1.0
    port_id: 1
    servo:
      id: 2
      init: 500
      min: 1000
      max: 0

  r_joint_controller:
    type: JointPositionController
    joint_name: r_joint
    joint_speed: 1.0
    port_id: 1
    servo:
      id: 1
      init: 500
      min: 1000
      max: 0

  arm_controller:
    type: JointTrajectoryActionController
    joint_trajectory_action_node:
      min_velocity: 0.1
      constraints:
        goal_time: 0.05
    joint_controllers:
      - "joint1_controller"
      - "joint2_controller"
      - "joint3_controller"
      - "joint4_controller"

  gripper_controller:
    type: JointTrajectoryActionController
    joint_trajectory_action_node:
      min_velocity: 0.1
      constraints:
        goal_time: 0.05
    joint_controllers:
      - "r_joint_controller"

serial_ports:
  - port_name: "/dev/ttyTHS1"
    port_id: 1
    baud_rate: 115200
    min_motor_id: 1
    max_motor_id: 5
    fake_read: true
    connected_ids: [ 1, 2, 3, 4, 5]
    update_rate: 10
jetauto@jetauto-desktop:~$ rostopic echo -n 1 /r_joint_controller/state
header:
  seq: 17714
  stamp:
    secs: 1787049443
    nsecs: 815720796
  frame_id: ''
name: "r_joint"
servo_ids: [1]
servo_temps: [0]
goal_pos: 0.0
current_pos: 0.0
error: 0.0
velocity: 10.0
---
jetauto@jetauto-desktop:~$ rostopic pub -1 /r_joint_controller/command std_msgs/Float64 "data: 0.1"
publishing and latching message for 3.0 seconds
jetauto@jetauto-desktop:~$ rostopic echo -n 1 /servo_controllers/port_id_1/servo_states
servo_states:
  -
    timestamp: 1787049464.82
    id: 1
    goal: 476
    position: 476
    error: 0
    voltage: 9000
  -
    timestamp: 1787049464.83
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787049464.84
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787049464.85
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787049464.86
    id: 5
    goal: 524
    position: 524
    error: 0
    voltage: 9000
---
jetauto@jetauto-desktop:~$ rostopic pub -1 /r_joint_controller/command std_msgs/Float64 "data: -0.1"
publishing and latching message for 3.0 seconds
jetauto@jetauto-desktop:~$ rostopic echo -n 1 /servo_controllers/port_id_1/servo_states
servo_states:
  -
    timestamp: 1787049480.52
    id: 1
    goal: 524
    position: 524
    error: 0
    voltage: 9000
  -
    timestamp: 1787049480.53
    id: 2
    goal: 208
    position: 208
    error: 0
    voltage: 9000
  -
    timestamp: 1787049480.54
    id: 3
    goal: 42
    position: 42
    error: 0
    voltage: 9000
  -
    timestamp: 1787049480.55
    id: 4
    goal: 667
    position: 667
    error: 0
    voltage: 9000
  -
    timestamp: 1787049480.56
    id: 5
    goal: 524
    position: 524
    error: 0
    voltage: 9000
---
jetauto@jetauto-desktop:~$ rosparam list | grep -E "joint[1-4]|r_joint|gripper"
/hiwonder_servo_manager/controllers/gripper_controller/joint_controllers
/hiwonder_servo_manager/controllers/gripper_controller/joint_trajectory_action_node/constraints/goal_time
/hiwonder_servo_manager/controllers/gripper_controller/joint_trajectory_action_node/min_velocity
/hiwonder_servo_manager/controllers/gripper_controller/type
/hiwonder_servo_manager/controllers/joint1_controller/joint_name
/hiwonder_servo_manager/controllers/joint1_controller/joint_speed
/hiwonder_servo_manager/controllers/joint1_controller/port_id
/hiwonder_servo_manager/controllers/joint1_controller/servo/id
/hiwonder_servo_manager/controllers/joint1_controller/servo/init
/hiwonder_servo_manager/controllers/joint1_controller/servo/max
/hiwonder_servo_manager/controllers/joint1_controller/servo/min
/hiwonder_servo_manager/controllers/joint1_controller/type
/hiwonder_servo_manager/controllers/joint2_controller/joint_name
/hiwonder_servo_manager/controllers/joint2_controller/joint_speed
/hiwonder_servo_manager/controllers/joint2_controller/port_id
/hiwonder_servo_manager/controllers/joint2_controller/servo/id
/hiwonder_servo_manager/controllers/joint2_controller/servo/init
/hiwonder_servo_manager/controllers/joint2_controller/servo/max
/hiwonder_servo_manager/controllers/joint2_controller/servo/min
/hiwonder_servo_manager/controllers/joint2_controller/type
/hiwonder_servo_manager/controllers/joint3_controller/joint_name
/hiwonder_servo_manager/controllers/joint3_controller/joint_speed
/hiwonder_servo_manager/controllers/joint3_controller/port_id
/hiwonder_servo_manager/controllers/joint3_controller/servo/id
/hiwonder_servo_manager/controllers/joint3_controller/servo/init
/hiwonder_servo_manager/controllers/joint3_controller/servo/max
/hiwonder_servo_manager/controllers/joint3_controller/servo/min
/hiwonder_servo_manager/controllers/joint3_controller/type
/hiwonder_servo_manager/controllers/joint4_controller/joint_name
/hiwonder_servo_manager/controllers/joint4_controller/joint_speed
/hiwonder_servo_manager/controllers/joint4_controller/port_id
/hiwonder_servo_manager/controllers/joint4_controller/servo/id
/hiwonder_servo_manager/controllers/joint4_controller/servo/init
/hiwonder_servo_manager/controllers/joint4_controller/servo/max
/hiwonder_servo_manager/controllers/joint4_controller/servo/min
/hiwonder_servo_manager/controllers/joint4_controller/type
/hiwonder_servo_manager/controllers/r_joint_controller/joint_name
/hiwonder_servo_manager/controllers/r_joint_controller/joint_speed
/hiwonder_servo_manager/controllers/r_joint_controller/port_id
/hiwonder_servo_manager/controllers/r_joint_controller/servo/id
/hiwonder_servo_manager/controllers/r_joint_controller/servo/init
/hiwonder_servo_manager/controllers/r_joint_controller/servo/max
/hiwonder_servo_manager/controllers/r_joint_controller/servo/min
/hiwonder_servo_manager/controllers/r_joint_controller/type
jetauto@jetauto-desktop:~$ rostopic echo -n 1 /r_joint_controller/state
header:
  seq: 18286
  stamp:
    secs: 1787049501
    nsecs:  15762805
  frame_id: ''
name: "r_joint"
servo_ids: [1]
servo_temps: [0]
goal_pos: -0.1005309632
current_pos: -0.1005309632
error: 0.0
velocity: 10.0
---
jetauto@jetauto-desktop:~$ rostopic echo -n 1 /r_joint_controller/state
header:
  seq: 18924
  stamp:
    secs: 1787049564
    nsecs: 816114902
  frame_id: ''
name: "r_joint"
servo_ids: [1]
servo_temps: [0]
goal_pos: -0.1005309632
current_pos: -0.1005309632
error: 0.0
velocity: 10.0
---
jetauto@jetauto-desktop:~$ rosparam get /hiwonder_servo_manager/serial_ports
- baud_rate: 115200
  connected_ids: [1, 2, 3, 4, 5]
  fake_read: true
  max_motor_id: 5
  min_motor_id: 1
  port_id: 1
  port_name: /dev/ttyTHS1
  update_rate: 10

jetauto@jetauto-desktop:~$ rosparam get /hiwonder_servo_manager/controllers/r_joint_controller
joint_name: r_joint
joint_speed: 1.0
port_id: 1
servo: {id: 1, init: 500, max: 0, min: 1000}
type: JointPositionController

jetauto@jetauto-desktop:~$ rosparam get /hiwonder_servo_manager/controllers/joint1_controller
joint_name: joint1
joint_speed: 1.0
port_id: 1
servo: {id: 5, init: 500, max: 0, min: 1000}
type: JointPositionController

jetauto@jetauto-desktop:~$ ls -l ~/jetauto/jetauto_software/servo_tool/
ls: cannot access '/home/jetauto/jetauto/jetauto_software/servo_tool/': No such file or directory
jetauto@jetauto-desktop:~$ sed -n '1,240p' ~/jetauto/jetauto_software/servo_tool/servo_controller.py
sed: can't read /home/jetauto/jetauto/jetauto_software/servo_tool/servo_controller.py: No such file or directory
jetauto@jetauto-desktop:~$ sed -n '1,240p' ~/jetauto/jetauto_software/servo_tool/BusServoControl.py
sed: can't read /home/jetauto/jetauto/jetauto_software/servo_tool/BusServoControl.py: No such file or directory
jetauto@jetauto-desktop:~$ ls -l /dev/ttyTHS1
crwxrwxrwx 1 root dialout 238, 1 Aug 18 16:13 /dev/ttyTHS1
jetauto@jetauto-desktop:~$ readlink -f /dev/ttyTHS1
/dev/ttyTHS1
jetauto@jetauto-desktop:~$ ls -l /dev/ttyTHS*
crwxrwxrwx 1 root dialout 238, 1 Aug 18 16:13 /dev/ttyTHS1
crw-rw---- 1 root dialout 238, 2 Aug 18 14:42 /dev/ttyTHS2
jetauto@jetauto-desktop:~$ ps aux | grep -E "hiwonder_servo|controller_manager" | grep -v grep
jetauto   8992  6.6  1.3 2445704 52808 ?       Ssl  15:37   2:23 python3 /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py __name:=hiwonder_servo_manager __log:=/home/jetauto/.ros/log/f5641a32-9ae4-11f1-a6eb-02428986abe0/hiwonder_servo_manager-3.log
jetauto   9005  3.5  1.0 859328 41348 ?        Ssl  15:37   1:17 python3 /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/joint_state_publisher.py __name:=joint_states_publisher __log:=/home/jetauto/.ros/log/f5641a32-9ae4-11f1-a6eb-02428986abe0/joint_states_publisher-4.log
jetauto@jetauto-desktop:~$ rosnode info /hiwonder_servo_manager
--------------------------------------------------------------------------------
Node [/hiwonder_servo_manager]
Publications:
 * /ActionGroupRunner/feedback [hiwonder_servo_msgs/ActionGroupRunnerActionFeedback]
 * /ActionGroupRunner/result [hiwonder_servo_msgs/ActionGroupRunnerActionResult]
 * /ActionGroupRunner/status [actionlib_msgs/GoalStatusArray]
 * /arm_controller/follow_joint_trajectory/feedback [control_msgs/FollowJointTrajectoryActionFeedback]
 * /arm_controller/follow_joint_trajectory/result [control_msgs/FollowJointTrajectoryActionResult]
 * /arm_controller/follow_joint_trajectory/status [actionlib_msgs/GoalStatusArray]
 * /arm_controller/state [control_msgs/FollowJointTrajectoryFeedback]
 * /gripper_controller/follow_joint_trajectory/feedback [control_msgs/FollowJointTrajectoryActionFeedback]
 * /gripper_controller/follow_joint_trajectory/result [control_msgs/FollowJointTrajectoryActionResult]
 * /gripper_controller/follow_joint_trajectory/status [actionlib_msgs/GoalStatusArray]
 * /gripper_controller/state [control_msgs/FollowJointTrajectoryFeedback]
 * /joint1_controller/state [hiwonder_servo_msgs/JointState]
 * /joint2_controller/state [hiwonder_servo_msgs/JointState]
 * /joint3_controller/state [hiwonder_servo_msgs/JointState]
 * /joint4_controller/state [hiwonder_servo_msgs/JointState]
 * /r_joint_controller/state [hiwonder_servo_msgs/JointState]
 * /rosout [rosgraph_msgs/Log]
 * /servo_controllers/port_id_1/servo_states [hiwonder_servo_msgs/ServoStateList]

Subscriptions:
 * /ActionGroupRunner/cancel [unknown type]
 * /ActionGroupRunner/goal [unknown type]
 * /arm_controller/command [unknown type]
 * /arm_controller/follow_joint_trajectory/cancel [unknown type]
 * /arm_controller/follow_joint_trajectory/goal [unknown type]
 * /gripper_controller/command [unknown type]
 * /gripper_controller/follow_joint_trajectory/cancel [unknown type]
 * /gripper_controller/follow_joint_trajectory/goal [unknown type]
 * /joint1_controller/command [unknown type]
 * /joint1_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /joint2_controller/command [unknown type]
 * /joint2_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /joint3_controller/command [unknown type]
 * /joint3_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /joint4_controller/command [unknown type]
 * /joint4_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /r_joint_controller/command [unknown type]
 * /r_joint_controller/command_duration [hiwonder_servo_msgs/CommandDuration]
 * /servo_control/set_servo_state [unknown type]
 * /servo_controllers/port_id_1/id_pos_dur [unknown type]
 * /servo_controllers/port_id_1/multi_id_pos_dur [hiwonder_servo_msgs/MultiRawIdPosDur]
 * /servo_controllers/port_id_1/servo_states [hiwonder_servo_msgs/ServoStateList]

Services:
 * /hiwonder_servo_manager/get_loggers
 * /hiwonder_servo_manager/set_logger_level
 * /servo_control/get_servo_state
 * /servo_control/set_read_timeout


contacting node http://localhost:36273/ ...
Pid: 8992
Connections:
 * topic: /rosout
    * to: /rosout
    * direction: outbound (32803 - 127.0.0.1:38908) [12]
    * transport: TCPROS
 * topic: /servo_controllers/port_id_1/servo_states
    * to: /hiwonder_servo_manager
    * direction: outbound (32803 - 127.0.0.1:39024) [29]
    * transport: TCPROS
 * topic: /r_joint_controller/state
    * to: /joint_states_publisher
    * direction: outbound (32803 - 127.0.0.1:38978) [21]
    * transport: TCPROS
 * topic: /joint4_controller/state
    * to: /joystick_control
    * direction: outbound (32803 - 127.0.0.1:39112) [32]
    * transport: TCPROS
 * topic: /joint4_controller/state
    * to: /joint_states_publisher
    * direction: outbound (32803 - 127.0.0.1:39114) [40]
    * transport: TCPROS
 * topic: /joint2_controller/state
    * to: /joint_states_publisher
    * direction: outbound (32803 - 127.0.0.1:39188) [41]
    * transport: TCPROS
 * topic: /joint2_controller/state
    * to: /joystick_control
    * direction: outbound (32803 - 127.0.0.1:39196) [49]
    * transport: TCPROS
 * topic: /joint1_controller/state
    * to: /joint_states_publisher
    * direction: outbound (32803 - 127.0.0.1:39198) [51]
    * transport: TCPROS
 * topic: /joint1_controller/state
    * to: /joystick_control
    * direction: outbound (32803 - 127.0.0.1:39204) [48]
    * transport: TCPROS
 * topic: /joint3_controller/state
    * to: /joint_states_publisher
    * direction: outbound (32803 - 127.0.0.1:39232) [54]
    * transport: TCPROS
 * topic: /joint3_controller/state
    * to: /joystick_control
    * direction: outbound (32803 - 127.0.0.1:39240) [59]
    * transport: TCPROS
 * topic: /servo_controllers/port_id_1/multi_id_pos_dur
    * to: /line_following (http://localhost:38915/)
    * direction: inbound
    * transport: TCPROS
 * topic: /servo_controllers/port_id_1/multi_id_pos_dur
    * to: /object_tracking (http://localhost:36947/)
    * direction: inbound
    * transport: TCPROS
 * topic: /r_joint_controller/command_duration
    * to: /joystick_control (http://localhost:45415/)
    * direction: inbound
    * transport: TCPROS
 * topic: /servo_controllers/port_id_1/servo_states
    * to: /hiwonder_servo_manager (http://localhost:36273/)
    * direction: inbound
    * transport: TCPROS
 * topic: /joint4_controller/command_duration
    * to: /joystick_control (http://localhost:45415/)
    * direction: inbound
    * transport: TCPROS
 * topic: /joint2_controller/command_duration
    * to: /joystick_control (http://localhost:45415/)
    * direction: inbound
    * transport: TCPROS
 * topic: /joint1_controller/command_duration
    * to: /joystick_control (http://localhost:45415/)
    * direction: inbound
    * transport: TCPROS
 * topic: /joint3_controller/command_duration
    * to: /joystick_control (http://localhost:45415/)
    * direction: inbound
    * transport: TCPROS

jetauto@jetauto-desktop:~$ ls -l ~/jetauto_software/servo_tool/
total 164
-rw-rw-r-- 1 jetauto jetauto  5564 Feb 23  2023 BusServoCmd.py
-rw-rw-r-- 1 jetauto jetauto  6288 Feb 23  2023 BusServoControl.py
-rw-rw-r-- 1 jetauto jetauto 23563 Feb 23  2023 main.py
drwxrwxr-x 2 jetauto jetauto  4096 Feb 23  2023 __pycache__
-rwxrwxr-x 1 jetauto jetauto    38 Feb 23  2023 qrc2py
drwxrwxr-x 2 jetauto jetauto  4096 Feb 23  2023 resources
-rw-rw-r-- 1 jetauto jetauto   480 Feb 23  2023 servo_controller.py
-rwxrwxr-x 1 jetauto jetauto   311 Feb 23  2023 servo_tool.desktop
-rwxrwxr-x 1 jetauto jetauto    95 Feb 23  2023 servo_tool.sh
-rwxrwxr-x 1 jetauto jetauto    22 Feb 23  2023 ui2py
-rw-rw-r-- 1 jetauto jetauto 26102 Feb 23  2023 ui.bk
-rw-rw-r-- 1 jetauto jetauto 29724 Feb 23  2023 ui.py
-rw-rw-r-- 1 jetauto jetauto 35276 Feb 23  2023 ui.ui
jetauto@jetauto-desktop:~$ sed -n '1,240p' ~/jetauto_software/servo_tool/servo_controller.py
from BusServoControl import *

def getServoPulse(servo_id):
    return getBusServoPulse(servo_id)

def getServoDeviation(servo_id):
    return getBusServoDeviation(servo_id)

def setServoPulse(servo_id, pulse, use_time):
    setBusServoPulse(servo_id, pulse, use_time)

def setServoDeviation(servo_id ,dev):
    setBusServoDeviation(servo_id, dev)

def saveServoDeviation(servo_id):
    saveBusServoDeviation(servo_id)

def unloadServo(servo_id):
    unloadBusServo(servo_id)
jetauto@jetauto-desktop:~$ sed -n '1,240p' ~/jetauto_software/servo_tool/BusServoControl.py
#!/usr/bin/env python3
import time
from BusServoCmd import *

time_out = 50

def setBusServoID(oldid, newid):
    """
    配置舵机servo_id号, 出厂默认为1
    :param oldid: 原来的servo_id， 出厂默认为1
    :param newid: 新的servo_id
    """
    serial_serro_wirte_cmd(oldid, LOBOT_SERVO_ID_WRITE, newid)

def getBusServoID(servo_id=None):
    """
    读取串口舵机servo_id
    :param servo_id: 默认为空
    :return: 返回舵机servo_id
    """
    count = 0
    while True:
        if servo_id is None:  # 总线上只能有一个舵机
            serial_servo_read_cmd(0xfe, LOBOT_SERVO_ID_READ)
        else:
            serial_servo_read_cmd(servo_id, LOBOT_SERVO_ID_READ)
        # 获取内容
        msg = serial_servo_get_rmsg(LOBOT_SERVO_ID_READ)
        count += 1
        if msg is not None:
            return msg
        elif count > time_out:
            return None

def setBusServoPulse(servo_id, pulse, use_time):
    """
    驱动串口舵机转到指定位置
    :param servo_id: 要驱动的舵机servo_id
    :pulse: 位置
    :use_time: 转动需要的时间
    """
    pulse = 0 if pulse < 0 else pulse
    pulse = 1000 if pulse > 1000 else pulse
    use_time = 0 if use_time < 0 else use_time
    use_time = 30000 if use_time > 30000 else use_time
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_MOVE_TIME_WRITE, pulse, use_time)

def stopBusServo(servo_id=None):
    '''
    停止舵机运行
    :param servo_id:
    :return:
    '''
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_MOVE_STOP)

def setBusServoDeviation(servo_id, d=0):
    """
    调整偏差
    :param servo_id: 舵机servo_id
    :param d:  偏差
    """
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_ANGLE_OFFSET_ADJUST, d)

def saveBusServoDeviation(servo_id):
    """
    配置偏差，掉电保护
    :param servo_id: 舵机servo_id
    """
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_ANGLE_OFFSET_WRITE)

def getBusServoDeviation(servo_id):
    '''
    读取偏差值
    :param servo_id: 舵机号
    :return:
    '''
    # 发送读取偏差指令
    count = 0
    while True:
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_ANGLE_OFFSET_READ)
        # 获取
        msg = serial_servo_get_rmsg(LOBOT_SERVO_ANGLE_OFFSET_READ)
        count += 1
        if msg is not None:
            return msg
        if count > time_out:
            return None

def setBusServoAngleLimit(servo_id, low, high):
    '''
    设置舵机转动范围
    :param servo_id:
    :param low:
    :param high:
    :return:
    '''
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_ANGLE_LIMIT_WRITE, low, high)

def getBusServoAngleLimit(servo_id):
    '''
    读取舵机转动范围
    :param servo_id:
    :return: 返回元祖 0： 低位  1： 高位
    '''
    count = 0
    while True:
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_ANGLE_LIMIT_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_ANGLE_LIMIT_READ)
        count += 1
        if msg is not None:
            return msg
        elif count > time_out:
            return None

def setBusServoVinLimit(servo_id, low, high):
    '''
    设置舵机电压范围
    :param servo_id:
    :param low:
    :param high:
    :return:
    '''
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_VIN_LIMIT_WRITE, low, high)

def getBusServoVinLimit(servo_id):
    '''
    读取舵机转动范围
    :param servo_id:
    :return: 返回元祖 0： 低位  1： 高位
    '''
    count = 0
    while True:
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_VIN_LIMIT_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_VIN_LIMIT_READ)
        count += 1
        if msg is not None:
            return msg
        elif count > time_out:
            return None

def setBusServoMaxTemp(servo_id, m_temp):
    '''
    设置舵机最高温度报警
    :param servo_id:
    :param m_temp:
    :return:
    '''
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_TEMP_MAX_LIMIT_WRITE, m_temp)

def getBusServoTempLimit(servo_id):
    '''
    读取舵机温度报警范围
    :param servo_id:
    :return:
    '''
    count = 0
    while True:
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_TEMP_MAX_LIMIT_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_TEMP_MAX_LIMIT_READ)
        count += 1
        if msg is not None:
            return msg
        elif count > time_out:
            return None

def getBusServoPulse(servo_id):
    '''
    读取舵机当前位置
    :param servo_id:
    :return:
    '''
    count = 0
    while True:
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_POS_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_POS_READ)
        count += 1
        if msg is not None:
            return msg
        elif count > time_out:
            return None

def getBusServoTemp(servo_id):
    '''
    读取舵机温度
    :param servo_id:
    :return:
    '''
    count = 0
    while True:
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_TEMP_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_TEMP_READ)
        count += 1
        if msg is not None:
            return msg
        elif count > time_out:
            return None

def getBusServoVin(servo_id):
    '''
    读取舵机电压
    :param servo_id:
    :return:
    '''
    count = 0
    while True:
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_VIN_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_VIN_READ)
        count += 1
        if msg is not None:
            return msg
        elif count > time_out:
            return None

def restBusServoPulse(oldid):
    # 舵机清零偏差和P值中位（500）
    serial_servo_set_deviation(oldid, 0)    # 清零偏差
    time.sleep(0.1)
    serial_serro_wirte_cmd(oldid, LOBOT_SERVO_MOVE_TIME_WRITE, 500, 100)    # 中位

def unloadBusServo(servo_id):
    # 掉电
    serial_serro_wirte_cmd(servo_id, LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE, 0)

def getBusServoLoadStatus(servo_id):
    # 读取是否掉电
    count = 0
    while True:
        serial_servo_read_cmd(servo_id, LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
        msg = serial_servo_get_rmsg(LOBOT_SERVO_LOAD_OR_UNLOAD_READ)
        count += 1
        if msg is not None:
            return msg
        elif count > time_out:
            return None
jetauto@jetauto-desktop:~$ sed -n '1,240p' ~/jetauto_software/servo_tool/BusServoCmd.py
#!/usr/bin/env python3
# encoding: utf-8
#幻尔科技总线舵机通信#
import sys
import time
import ctypes
import serial
sys.path.append('/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO')
import Jetson.GPIO as GPIO

LOBOT_SERVO_FRAME_HEADER         = 0x55
LOBOT_SERVO_MOVE_TIME_WRITE      = 1
LOBOT_SERVO_MOVE_TIME_READ       = 2
LOBOT_SERVO_MOVE_TIME_WAIT_WRITE = 7
LOBOT_SERVO_MOVE_TIME_WAIT_READ  = 8
LOBOT_SERVO_MOVE_START           = 11
LOBOT_SERVO_MOVE_STOP            = 12
LOBOT_SERVO_ID_WRITE             = 13
LOBOT_SERVO_ID_READ              = 14
LOBOT_SERVO_ANGLE_OFFSET_ADJUST  = 17
LOBOT_SERVO_ANGLE_OFFSET_WRITE   = 18
LOBOT_SERVO_ANGLE_OFFSET_READ    = 19
LOBOT_SERVO_ANGLE_LIMIT_WRITE    = 20
LOBOT_SERVO_ANGLE_LIMIT_READ     = 21
LOBOT_SERVO_VIN_LIMIT_WRITE      = 22
LOBOT_SERVO_VIN_LIMIT_READ       = 23
LOBOT_SERVO_TEMP_MAX_LIMIT_WRITE = 24
LOBOT_SERVO_TEMP_MAX_LIMIT_READ  = 25
LOBOT_SERVO_TEMP_READ            = 26
LOBOT_SERVO_VIN_READ             = 27
LOBOT_SERVO_POS_READ             = 28
LOBOT_SERVO_OR_MOTOR_MODE_WRITE  = 29
LOBOT_SERVO_OR_MOTOR_MODE_READ   = 30
LOBOT_SERVO_LOAD_OR_UNLOAD_WRITE = 31
LOBOT_SERVO_LOAD_OR_UNLOAD_READ  = 32
LOBOT_SERVO_LED_CTRL_WRITE       = 33
LOBOT_SERVO_LED_CTRL_READ        = 34
LOBOT_SERVO_LED_ERROR_WRITE      = 35
LOBOT_SERVO_LED_ERROR_READ       = 36

serialHandle = serial.Serial("/dev/ttyTHS1", 115200)  # 初始化串口， 波特率为115200

rx_pin = 17
tx_pin = 27

mode = GPIO.getmode()
if mode == 1 or mode is None:  # 是否已经设置引脚编码
    GPIO.setmode(GPIO.BCM)  # 设为BCM编码
GPIO.setwarnings(False)

def portInit():  # 配置用到的IO口
    GPIO.setup(rx_pin, GPIO.OUT)  # 配置RX_CON 即 GPIO17 为输出
    GPIO.output(rx_pin, 0)
    GPIO.setup(tx_pin, GPIO.OUT)  # 配置TX_CON 即 GPIO27 为输出
    GPIO.output(tx_pin, 1)

portInit()

def portWrite():  # 配置单线串口为输出
    GPIO.output(tx_pin, 1)  # 拉高TX_CON 即 GPIO27
    GPIO.output(rx_pin, 0)  # 拉低RX_CON 即 GPIO17

def portRead():  # 配置单线串口为输入
    GPIO.output(rx_pin, 1)  # 拉高RX_CON 即 GPIO17
    GPIO.output(tx_pin, 0)  # 拉低TX_CON 即 GPIO27

def portRest():
    time.sleep(0.1)
    serialHandle.close()
    GPIO.output(rx_pin, 1)
    GPIO.output(tx_pin, 1)
    serialHandle.open()
    time.sleep(0.1)

def checksum(buf):
    # 计算校验和
    sum = 0x00
    for b in buf:  # 求和
        sum += b
    sum = sum - 0x55 - 0x55  # 去掉命令开头的两个 0x55
    sum = ~sum  # 取反
    return sum & 0xff

def serial_serro_wirte_cmd(id=None, w_cmd=None, dat1=None, dat2=None):
    '''
    写指令
    :param id:
    :param w_cmd:
    :param dat1:
    :param dat2:
    :return:
    '''
    portWrite()
    buf = bytearray(b'\x55\x55')  # 帧头
    buf.append(id)
    # 指令长度
    if dat1 is None and dat2 is None:
        buf.append(3)
    elif dat1 is not None and dat2 is None:
        buf.append(4)
    elif dat1 is not None and dat2 is not None:
        buf.append(7)

    buf.append(w_cmd)  # 指令
    # 写数据
    if dat1 is None and dat2 is None:
        pass
    elif dat1 is not None and dat2 is None:
        buf.append(dat1 & 0xff)  # 偏差
    elif dat1 is not None and dat2 is not None:
        buf.extend([(0xff & dat1), (0xff & (dat1 >> 8))])  # 分低8位 高8位 放入缓存
        buf.extend([(0xff & dat2), (0xff & (dat2 >> 8))])  # 分低8位 高8位 放入缓存
    # 校验和
    buf.append(checksum(buf))
    # for i in buf:
    #     print('%x' %i)
    serialHandle.write(buf)  # 发送

def serial_servo_read_cmd(id=None, r_cmd=None):
    '''
    发送读取命令
    :param id:
    :param r_cmd:
    :param dat:
    :return:
    '''
    portWrite()
    buf = bytearray(b'\x55\x55')  # 帧头
    buf.append(id)
    buf.append(3)  # 指令长度
    buf.append(r_cmd)  # 指令
    buf.append(checksum(buf))  # 校验和
    serialHandle.write(buf)  # 发送
    time.sleep(0.00034)

def serial_servo_get_rmsg(cmd):
    '''
    # 获取指定读取命令的数据
    :param cmd: 读取命令
    :return: 数据
    '''
    serialHandle.flushInput()  # 清空接收缓存
    portRead()  # 将单线串口配置为输入
    time.sleep(0.005)  # 稍作延时，等待接收完毕
    count = serialHandle.inWaiting()    # 获取接收缓存中的字节数
    if count != 0:  # 如果接收到的数据不空
        recv_data = serialHandle.read(count)  # 读取接收到的数据
        # for i in recv_data:
        #     print('%#x' %ord(i))
        # 是否是读id指令
        try:
            if recv_data[0] == 0x55 and recv_data[1] == 0x55 and recv_data[4] == cmd:
                dat_len = recv_data[3]
                serialHandle.flushInput()  # 清空接收缓存
                if dat_len == 4:
                    # print ctypes.c_int8(ord(recv_data[5])).value    # 转换成有符号整型
                    return recv_data[5]
                elif dat_len == 5:
                    pos = 0xffff & (recv_data[5] | (0xff00 & (recv_data[6] << 8)))
                    return ctypes.c_int16(pos).value
                elif dat_len == 7:
                    pos1 = 0xffff & (recv_data[5] | (0xff00 & (recv_data[6] << 8)))
                    pos2 = 0xffff & (recv_data[7] | (0xff00 & (recv_data[8] << 8)))
                    return ctypes.c_int16(pos1).value, ctypes.c_int16(pos2).value
            else:
                return None
        except BaseException as e:
            print(e)
    else:
        serialHandle.flushInput()  # 清空接收缓存
        return None
jetauto@jetauto-desktop:~$ rosservice type /servo_control/get_servo_state
hiwonder_servo_msgs/GetServoState
jetauto@jetauto-desktop:~$ rossrv show $(rosservice type /servo_control/get_servo_state)
string cmd
int16 id
---
bool success
float32[] value

jetauto@jetauto-desktop:~$ rosservice type /servo_control/set_servo_state
Unknown service [/servo_control/set_servo_state]
jetauto@jetauto-desktop:~$ rosservice call /servo_control/get_servo_state "cmd: 'pos'
> id: 1"
success: True
value: []
jetauto@jetauto-desktop:~$ rosservice call /servo_control/get_servo_state "cmd: 'voltage'
> id: 1"
success: True
value: []
jetauto@jetauto-desktop:~$ rosservice call /servo_control/get_servo_state "cmd: 'temperature'
> id: 1"
success: True
value: []
jetauto@jetauto-desktop:~$ grep -R "GetServoState\|get_servo_state\|cmd ==" \
> ~/jetauto_ws/src/jetauto_driver/hiwonder_servo \
> 2>/dev/null
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_msgs/CMakeLists.txt:  GetServoState.srv
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/bus_servo_control.pyc matches
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/bus_servo_control.py:from hiwonder_servo_msgs.srv import GetServoState
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/bus_servo_control.py:            res = rospy.ServiceProxy('/servo_control/get_servo_state', GetServoState)('voltage', 5)
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/bus_servo_control.cpython-36.pyc matches
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:from hiwonder_servo_msgs.srv import GetServoState, SetReadTimeout
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        rospy.Service('servo_control/get_servo_state',GetServoState, self.get_servo_state)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        if cmd == 'id':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'deviation':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'save_deviation':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'pulse_range':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'voltage_range':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'temperature_range':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'unload':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:    def get_servo_state(self, msg):
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        if cmd == 'id':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'deviation':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'pulse_range':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'voltage_range':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'temperature_range':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'temperature':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'voltage':
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        elif cmd == 'load_state':
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/__pycache__/hiwonder_servo_serialproxy.cpython-36.pyc matches
jetauto@jetauto-desktop:~$ grep -R "get_servo_state" \
> ~/jetauto_ws/src/jetauto_driver/hiwonder_servo \
> 2>/dev/null
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/bus_servo_control.pyc matches
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/bus_servo_control.py:            res = rospy.ServiceProxy('/servo_control/get_servo_state', GetServoState)('voltage', 5)
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/src/hiwonder_servo_controllers/__pycache__/bus_servo_control.cpython-36.pyc matches
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:        rospy.Service('servo_control/get_servo_state', GetServoState, self.get_servo_state)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/hiwonder_servo_serialproxy.py:    def get_servo_state(self, msg):
Binary file /home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_driver/src/hiwonder_servo_driver/__pycache__/hiwonder_servo_serialproxy.cpython-36.pyc matches
jetauto@jetauto-desktop:~$ rosservice call /servo_control/get_servo_state "cmd: 'load_state'
> id: 1"
success: True
value: []
jetauto@jetauto-desktop:~$ rosservice call /servo_control/get_servo_state "cmd: 'voltage'
> id: 1"
success: True
value: []
jetauto@jetauto-desktop:~$ rosservice call /servo_control/get_servo_state "cmd: 'temperature'
> id: 1"
success: True
value: []
jetauto@jetauto-desktop:~$ rosnode list | grep hiwonder
/hiwonder_servo_manager
jetauto@jetauto-desktop:~$ rosnode kill /hiwonder_servo_manager
killing /hiwonder_servo_manager
killed
jetauto@jetauto-desktop:~$ cd ~/jetauto_software/servo_tool
jetauto@jetauto-desktop:~/jetauto_software/servo_tool$ python3 -c "from BusServoControl import getBusServoPulse; print(getBusServoPulse(1))"
None
jetauto@jetauto-desktop:~/jetauto_software/servo_tool$ python3 -c "from BusServoControl import getBusServoLoadStatus; print(getBusServoLoadStatus(1))"
None
jetauto@jetauto-desktop:~/jetauto_software/servo_tool$ python3 -c "from BusServoControl import getBusServoVin; print(getBusServoVin(1))"
None
jetauto@jetauto-desktop:~/jetauto_software/servo_tool$ cd ~/jetauto_software/servo_tool
jetauto@jetauto-desktop:~/jetauto_software/servo_tool$ python3 -c "from BusServoControl import getBusServoPulse; print(getBusServoPulse(5))"
522
jetauto@jetauto-desktop:~/jetauto_software/servo_tool$ python3 -c "from BusServoControl import getBusServoVin; print(getBusServoVin(5))"
11506
jetauto@jetauto-desktop:~/jetauto_software/servo_tool$ python3 -c "from BusServoControl import getBusServoPulse; print('ID1:', getBusServoPulse(1)); print('ID2:', getBusServoPulse(2)); print('ID3:', getBusServoPulse(3)); print('ID4:', getBusServoPulse(4)); print('ID5:', getBusServoPulse(5))"
ID1: None
ID2: None
ID3: None
ID4: None
ID5: 522
jetauto@jetauto-desktop:~/jetauto_software/servo_tool$ python3 -c "from BusServoControl import getBusServoVin; print(getBusServoVin(5))"
11473
jetauto@jetauto-desktop:~/jetauto_software/servo_tool$ grep -R "hiwonder_servo_manager" ~/jetauto_ws/src/jetauto_bringup ~/jetauto_ws/src/jetauto_driver -n 2>/dev/null | head -30
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/scripts/controller_manager.py:11:        rospy.init_node('hiwonder_servo_manager', anonymous=True)
/home/jetauto/jetauto_ws/src/jetauto_driver/hiwonder_servo/hiwonder_servo_controllers/launch/controller_manager.launch:3:    <node name="hiwonder_servo_manager" pkg="hiwonder_servo_controllers" type="controller_manager.py" required="true" output="screen">
jetauto@jetauto-desktop:~/jetauto_software/servo_tool$ sudo poweroff
Connection to 10.23.78.76 closed by remote host.
Connection to 10.23.78.76 closed.

```
