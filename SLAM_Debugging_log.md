# JetAuto Pro - SLAM & Navigation Debugging Log

> Status: In Progress
>
> Platform:
> - Jetson Nano
> - Ubuntu 18.04
> - ROS Melodic
> - JetAuto Pro
> - G4 LiDAR
> - Astra Pro Plus

---

# Session 1

## Objective

Restore the complete JetAuto software stack so that:

- Bringup starts correctly
- LiDAR works
- Odom is published
- SLAM runs
- Navigation works
- No duplicate nodes or launch conflicts remain

---

# Step 1 - Verify Startup Service

### Command

```bash
systemctl cat start_app_node.service
```

### Result

Autostart service launches:

```text
source_env.bash
↓
roslaunch jetauto_bringup bringup.launch
```

Verified with:

```bash
sudo grep "^ExecStart" /etc/systemd/system/start_app_node.service
```

Output:

```text
ExecStart=/home/jetauto/jetauto_ws/src/jetauto_bringup/scripts/source_env.bash roslaunch jetauto_bringup bringup.launch
```

## Conclusion

Startup service is correct.

---

# Screenshot

<img width="933" height="510" alt="image" src="https://github.com/user-attachments/assets/c0291633-07cb-4b46-b603-e9a4ebdcf1c9" />


---

# Step 2 - Inspect bringup.launch

Command

```bash
sed -n '1,200p' ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch
```

Observation

The launch file contained:

```xml
<include file="$(find rplidar_ros)/launch/rplidar.launch"/>
```

Expected:

```xml
<include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
```

Reason:

JetAuto expects its own LiDAR wrapper instead of directly launching the generic RPLiDAR package.

---

# Fix Applied

Edited:

```text
~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch
```

Changed:

```xml
<include file="$(find rplidar_ros)/launch/rplidar.launch"/>
```

↓

```xml
<include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
```

Restarted:

```bash
sudo systemctl restart start_app_node.service
```

---

# Screenshot

```
jetauto@jetauto-desktop:~$ sed -n '1,200p' ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch
<?xml version="1.0"?>
<!--此launch文件被设定为自启动，自启文件路径:/etc/systemd/system/start_app_node.service 方式systemd，(this launch file is set as auto-start. The path of the auto-start file is /etc/systemd/system/start_app_node.service  method:systemd)
关闭自启（重启后失效）：sudo systemctl stop start_app_node.service(close auto-start(invalid after reboot)：sudo systemctl stop start_app_node.service)
开启自启（重启后失效）：sudo systemctl start start_app_node.service(enable auto-start(invalid after reboot): sudo systemctl start start_app_node.service)
永久关闭自启（重启依旧生效）：sudo systemctl disable start_app_node.service(close auto-start permanently(still valid after reboot)：sudo systemctl disable start_app_node.service)
永久开启自启（重启依旧生效）：sudo systemctl enable start_app_node.service(enable auto-start permanently(still valid after reboot):sudo systemctl enable start_app_node.service)
重启自启：sudo systemctl restart start_app_node.service(restart auto-start:sudo systemctl restart start_app_node.service)
查看自启：sudo systemctl status start_app_node.service(check auto-start: sudo systemctl status start_app_node.service)
-->
<launch>
    <!--自定义usb摄像头名称(custom usb camera name)-->
    <arg name="usb_cam_name"        default="usb_cam"/>
    <!--自定义深度摄像头名称(custom depth camera name)-->
    <arg name="depth_camera_name"   default="astra_cam"/>
    <!--自定义深度摄像头rgb话题名称(custom depth camera rgb topic name)-->
    <arg name="image_topic"         default="image_raw"/>
    <!--获取当前设备类型, 具体类型在~/.typerc里定义(Acquire the type of the current device. The specific type is defined by ~/.typerc)-->
    <arg name="machine_type"        default="$(env MACHINE_TYPE)"/>
    <arg name="depth_camera_type"   default="$(env DEPTH_CAMERA_TYPE)"/>

    <!--底盘驱动(chassis driver)-->
    <include file="$(find jetauto_controller)/launch/jetauto_controller.launch"/>

     <!--激光雷达驱动(lidar driver)-->
    <include file="$(find rplidar_ros)/launch/rplidar.launch"/>  

     <!--舵机驱动(servo driver)-->
    <include file="$(find hiwonder_servo_controllers)/launch/start.launch"/>

    <!--姿态(Pose)-->
    <node name="init_pose" pkg="jetauto_slam" type="init_pose.py" output="screen"/>

    <!--usb摄像头，只有设备为JetAutoPro时才开启(usb camera. Only when the device is JetAutoPro, the camera will be start)-->
    <include if="$(eval machine_type == 'JetAutoPro')" file="$(find jetauto_peripherals)/launch/usb_cam.launch">
        <arg name="usb_cam_name" value="$(arg usb_cam_name)"/>
    </include>

    <!--深度摄像头(depth camera)-->
    <include file="$(find jetauto_peripherals)/launch/astrapro.launch">
        <arg name="depth_camera_name" value="$(arg depth_camera_name)"/>
        <arg name="image_topic" value="$(arg image_topic)"/>
    </include>

    <!--app画面传输(app image transimission)-->
    <node if="$(eval depth_camera_type != '')" name="web_video_server" pkg="web_video_server" respawn="true" respawn_delay="2"  type="web_video_server" output="screen"/>

    <!--app通信(app communication)-->
    <include file="$(find jetauto_bringup)/launch/rosbridge.launch"/>

    <!--app功能(app function)-->
    <include file="$(find jetauto_app)/launch/start_app.launch"/>

    <!--手柄控制(handle control)-->
    <include file="$(find jetauto_peripherals)/launch/joystick_control.launch"/>

    <!--开机自检(Power on self test)-->
    <node name="startup_check" pkg="jetauto_bringup" type="startup_check.py" output="screen"/>
</launch>
```
<img width="1297" height="267" alt="image" src="https://github.com/user-attachments/assets/0c9eeeb1-ec65-4452-9f12-a9e569110597" />

---

# Step 3 - Verify LiDAR

Command

```bash
rostopic list | grep scan
```

Output

```text
/scan
```

Command

```bash
rostopic info /scan
```

Output

```text
Publisher:
/rplidarNode
```

Observation

Publisher still appeared as:

```text
/rplidarNode
```

This suggested either:

- lidar.launch internally starts the same driver

or

- another launch file also starts the LiDAR.

---

# Screenshot

<img width="761" height="276" alt="image" src="https://github.com/user-attachments/assets/9a8ee427-6ef7-4905-ab22-a8469e936e12" />


---

# Step 4 - Launch bringup Manually

Stopped systemd:

```bash
sudo systemctl stop start_app_node.service
```

Started manually:

```bash
source ~/jetauto_ws/src/jetauto_bringup/scripts/source_env.bash

roslaunch jetauto_bringup bringup.launch
```

Result

```text
RLException:

multiple nodes named

/ydlidar_lidar_g4_publisher
```

This was the first concrete failure explaining why bringup was exiting.

---

# Screenshot

<img width="927" height="646" alt="image" src="https://github.com/user-attachments/assets/9fc90581-ba2a-4ade-975d-1098e4d630d8" />


---

# Step 5 - Search for Duplicate LiDAR Launches

Commands

```bash
grep -R "ydlidar_lidar_g4_publisher" ~/jetauto_ws/src -n
```

```bash
grep -R "ydlidar.launch" ~/jetauto_ws/src -n
```

Result

Only one node definition exists:

```text
jetauto_peripherals/launch/include/ydlidar.launch
```

Meaning:

The same launch file is being included multiple times.

---

# Step 6 - Search Who Includes lidar.launch

Command

```bash
grep -R "launch/lidar.launch" ~/jetauto_ws/src -n
```

Result

Found:

- bringup.launch
- jetauto_slam/include/jetauto_robot.launch
- jetauto_app/lidar_app.launch
- voice_control
- example packages

Important finding:

```text
start_app.launch
```

contains

```xml
<include file="$(find jetauto_app)/launch/lidar_app.launch"/>
```

This is currently the strongest candidate for the duplicate launch.

---

# Current Hypothesis

bringup.launch

↓

lidar.launch

↓

ydlidar.launch

AND

start_app.launch

↓

lidar_app.launch

↓

lidar.launch

↓

ydlidar.launch

Result:

Two nodes named

```text
ydlidar_lidar_g4_publisher
```

are launched simultaneously.

Status:

Not yet confirmed.

---

# Next Step

Inspect

```text
jetauto_app/launch/lidar_app.launch
```

Determine whether it launches

```text
jetauto_peripherals/lidar.launch
```

If confirmed:

Remove the duplicate launch and verify that bringup starts successfully.

```
jetauto@jetauto-desktop:~$ grep -R "ydlidar_lidar_g4_publisher" ~/jetauto_ws/src -n
/home/jetauto/jetauto_ws/src/jetauto_peripherals/launch/include/ydlidar.launch:8:    <node name="ydlidar_lidar_g4_publisher"  pkg="ydlidar_ros_driver"  type="ydlidar_ros_driver_node" output="screen" respawn="false" >
jetauto@jetauto-desktop:~$ grep -R "ydlidar.launch" ~/jetauto_ws/src -n
/home/jetauto/jetauto_ws/src/jetauto_peripherals/launch/lidar.launch:29:    <include if="$(eval lidar_type == 'G4')" file="$(find jetauto_peripherals)/launch/include/ydlidar.launch">
jetauto@jetauto-desktop:~$ grep -R "launch/lidar.launch" ~/jetauto_ws/src -n
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/jetauto_robot.launch:83:            <include unless="$(arg use_depth_camera)" file="$(find jetauto_peripherals)/launch/lidar.launch">
/home/jetauto/jetauto_ws/src/jetauto_bringup/launch/bringup.launch:25:    <include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
/home/jetauto/jetauto_ws/src/jetauto_app/launch/lidar_app.launc    <include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
/home/jetauto/jetauto_ws/src/third_party/ydlidar_ros_driver/launch/lidar_view.launch:2:  <include file="$(find ydlidar_ros_driver)/launch/lidar.launch" />
/home/jetauto/jetauto_ws/src/xf_mic_asr_offline/launch/voice_control_move.launch:5:    <include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
/home/jetauto/jetauto_ws/src/jetauto_example/scripts/line_follow_clean/line_follow_clean_node.launch:4:    <include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
jetauto@jetauto-desktop:~$ grep -R "jetauto_peripherals.*lidar.launch" ~/jetauto_ws/src -n
/home/jetauto/jetauto_ws/src/jetauto_peripherals/launch/lidar.launch:12:    <include if="$(eval lidar_type == 'A1')" file="$(find jetauto_peripherals)/launch/include/rplidar.launch">
/home/jetauto/jetauto_ws/src/jetauto_peripherals/launch/lidar.launch:18:    <include if="$(eval lidar_type == 'A2')" file="$(find jetauto_peripherals)/launch/include/rplidar.launch">
/home/jetauto/jetauto_ws/src/jetauto_peripherals/launch/lidar.launch:29:    <include if="$(eval lidar_type == 'G4')" file="$(find jetauto_peripherals)/launch/include/ydlidar.launch">
/home/jetauto/jetauto_ws/src/jetauto_slam/launch/include/jetauto_robot.launch:83:            <include unless="$(arg use_depth_camera)" file="$(find jetauto_peripherals)/launch/lidar.launch">
/home/jetauto/jetauto_ws/src/jetauto_bringup/launch/bringup.launch:25:    <include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
/home/jetauto/jetauto_ws/src/jetauto_app/launch/lidar_app.launc    <include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
/home/jetauto/jetauto_ws/src/xf_mic_asr_offline/launch/voice_control_move.launch:5:    <include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
/home/jetauto/jetauto_ws/src/jetauto_example/scripts/line_follow_clean/line_follow_clean_node.launch:4:    <include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
jetauto@jetauto-desktop:~$ sed -n '1,200p' ~/jetauto_ws/src/jetauto_app/launch/start_app.launch
<?xml version="1.0"?>
<launch>
    <!--启动app节点(start app node)-->
    <include file="$(find jetauto_app)/launch/lidar_app.launch"/>
    <include file="$(find jetauto_app)/launch/line_following.launch"/>
    <include file="$(find jetauto_app)/launch/object_tracking.launch"/>
    <include file="$(find jetauto_app)/launch/ar_app.launch"/>
    <include file="$(find jetauto_app)/launch/patrol.launch"/>
</launch>
jetauto@jetauto-desktop:~$ grep -R "lidar_app.launch" ~/jetauto_ws/src/jetauto_app -n
/home/jetauto/jetauto_ws/src/jetauto_app/launch/start_app.launc    <include file="$(find jetauto_app)/launch/lidar_app.launch"/>
```
---

# Lessons Learned

- Always run bringup manually when systemd suppresses logs.
- Duplicate ROS node names indicate the same launch file is started twice.
- Search launch inclusions before editing node definitions.
