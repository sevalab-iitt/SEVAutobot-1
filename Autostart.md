#  Auto-Starting ALL ROS Nodes on Boot

**Goal:** Make every JetAuto ROS node (lidar, cameras, controller, servos, app communication, joystick, etc.) come up automatically on boot, without manually running any `roslaunch` command.

**Platform:** JetAuto (Jetson-based), ROS Melodic

---

## 1. The Short Answer

JetAuto already has a full autostart system built in — you don't need to create anything new. It's called **`start_app_node.service`**, and it launches **one master file** that in turn launches everything else:

```
start_app_node.service
        │
        ▼
roslaunch jetauto_bringup bringup.launch
        │
        ├── jetauto_controller.launch      (chassis driver)
        ├── hiwonder_servo_controllers     (servo driver)
        ├── init_pose.py                   (pose)
        ├── usb_cam.launch                 (USB camera, JetAutoPro only)
        ├── astrapro.launch                (depth camera)
        ├── web_video_server                (video streaming to app)
        ├── rosbridge.launch                (app communication)
        ├── start_app.launch                (app functions)
        ├── joystick_control.launch         (handle/joystick control)
        └── startup_check.py                (power-on self test)
```

So "autostart all nodes" = **make sure `start_app_node.service` is enabled, and make sure every node you want is included inside `bringup.launch`.** That's the entire mechanism — one service, one launch file, many includes.

---

## 2. Locate and Inspect the Service

```bash
find ~/jetauto_ws -iname "*.service"
```
Typical output:
```
/home/jetauto/jetauto_ws/src/jetauto_bringup/service/jupyter.service
/home/jetauto/jetauto_ws/src/jetauto_bringup/service/start_app_node.service   <-- this one
/home/jetauto/jetauto_ws/src/jetauto_bringup/service/clear_log.service
/home/jetauto/jetauto_ws/src/jetauto_bringup/service/fan_control.service
/home/jetauto/jetauto_ws/src/jetauto_bringup/service/expand_rootfs.service
/home/jetauto/jetauto_ws/src/jetauto_bringup/service/voltage_detect.service
```

View the actual installed service file:
```bash
cat /etc/systemd/system/start_app_node.service
```
```ini
[Unit]
Description=start node
After=NetworkManager.service time-sync.target
[Service]
Type=simple
User=jetauto
Restart=always
RestartSec=30
KillMode=mixed
ExecStart=/home/jetauto/jetauto_ws/src/jetauto_bringup/scripts/source_env.bash roslaunch jetauto_bringup bringup.launch
StandardOutput=null
StandardError=null
[Install]
WantedBy=multi-user.target
```

>  **Important:** `StandardOutput=null` / `StandardError=null` means crashes are **silent** in `systemctl status`. Always check real errors with:
> ```bash
> journalctl -u start_app_node.service --no-pager | tail -100
> ```

---

## 3. Managing the Service (applies to ALL nodes at once)

```bash
sudo systemctl status start_app_node.service       # current state
systemctl is-enabled start_app_node.service        # confirm boot-persistence
sudo systemctl enable start_app_node.service        # enable permanently (survives reboot)
sudo systemctl disable start_app_node.service       # disable permanently (survives reboot)
sudo systemctl start start_app_node.service         # start now
sudo systemctl stop start_app_node.service          # stop now
sudo systemctl restart start_app_node.service       # restart (apply any launch file changes)
journalctl -u start_app_node.service --no-pager | tail -100   # real logs/errors
```

Since **all** nodes are children of this one service, enabling/starting/stopping it controls the entire robot stack at once — you don't manage nodes individually at the systemd level.

---

## 4. Inspect What's Currently Included

```bash
find ~/jetauto_ws -iname "bringup.launch"
cat ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch
```

Full reference content of a typical `bringup.launch`:
```xml
<launch>
    <arg name="usb_cam_name"        default="usb_cam"/>
    <arg name="depth_camera_name"   default="astra_cam"/>
    <arg name="image_topic"         default="image_raw"/>
    <arg name="machine_type"        default="$(env MACHINE_TYPE)"/>
    <arg name="depth_camera_type"   default="$(env DEPTH_CAMERA_TYPE)"/>

    <!--底盘驱动(chassis driver)-->
    <include file="$(find jetauto_controller)/launch/jetauto_controller.launch"/>
    <!--舵机驱动(servo driver)-->
    <include file="$(find hiwonder_servo_controllers)/launch/start.launch"/>
    <!--姿态(Pose)-->
    <node name="init_pose" pkg="jetauto_slam" type="init_pose.py" output="screen"/>
    <!--usb摄像头(usb camera, JetAutoPro only)-->
    <include if="$(eval machine_type == 'JetAutoPro')" file="$(find jetauto_peripherals)/launch/usb_cam.launch">
        <arg name="usb_cam_name" value="$(arg usb_cam_name)"/>
    </include>
    <!--深度摄像头(depth camera)-->
    <include file="$(find jetauto_peripherals)/launch/astrapro.launch">
        <arg name="depth_camera_name" value="$(arg depth_camera_name)"/>
        <arg name="image_topic" value="$(arg image_topic)"/>
    </include>
    <!--app画面传输(app image transmission)-->
    <node if="$(eval depth_camera_type != '')" name="web_video_server" pkg="web_video_server" respawn="true" respawn_delay="2" type="web_video_server" output="screen"/>
    <!--app通信(app communication)-->
    <include file="$(find jetauto_bringup)/launch/rosbridge.launch"/>
    <!--app功能(app function)-->
    <include file="$(find jetauto_app)/launch/start_app.launch"/>
    <!--手柄控制(handle control)-->
    <include file="$(find jetauto_peripherals)/launch/joystick_control.launch"/>
    <!--开机自检(power-on self test)-->
    <node name="startup_check" pkg="jetauto_bringup" type="startup_check.py" output="screen"/>
</launch>
```

**Anything NOT listed here will not auto-start.** For example, the lidar driver (`rplidar_ros`) was missing entirely by default — meaning it never auto-started even though a higher-level app node (`/lidar_app`) was present and waiting for it.

---

## 5. Adding Any Node to Autostart

The pattern is always the same: add an `<include>` (for a launch file) or a `<node>` (for a single node) inside `bringup.launch`.

### Step 1: Back up first
```bash
cp ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch \
   ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch.bak
```

### Step 2: Edit the file
```bash
nano ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch
```

**To include an entire launch file** (most common — e.g. lidar):
```xml
<include file="$(find rplidar_ros)/launch/rplidar.launch"/>
```

**To include a single node directly** (used for things like `init_pose.py`, `startup_check.py`):
```xml
<node name="my_node_name" pkg="my_package" type="my_script.py" output="screen"/>
```

**Example — adding the lidar** (real fix applied on this robot):
```xml
<!--底盘驱动(chassis driver)-->
<include file="$(find jetauto_controller)/launch/jetauto_controller.launch"/>
<!--舵机驱动(servo driver)-->
<include file="$(find hiwonder_servo_controllers)/launch/start.launch"/>
<!--激光雷达驱动(lidar driver)-->
<include file="$(find rplidar_ros)/launch/rplidar.launch"/>
```

Save (`Ctrl+O`, `Enter`) and exit (`Ctrl+X`).

### Step 3: Ensure the service is enabled
```bash
sudo systemctl enable start_app_node.service
```

### Step 4: Restart the service to apply changes
```bash
sudo systemctl restart start_app_node.service
sleep 8
```

### Step 5: Confirm every expected node is running
```bash
rosnode list
```
Compare against what you expect — chassis, servos, cameras, lidar, app nodes, joystick, etc.

### Step 6: Full reboot test (final proof)
```bash
sudo reboot
```
After reboot, without touching anything:
```bash
rosnode list
```

---

## 6. Full Expected Node List (once everything is included)

```
/ar_app
/astra_cam/astra_cam_nodelet_manager
/astra_cam/depth_registered_hw_metric_rect
/astra_cam/depth_registered_metric
/astra_cam/depth_registered_rectify_depth
/astra_cam/points_xyzrgb_hw_registered
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
/rplidarNode          <-- added via the fix in Section 5
/usb_cam
/web_video_server
```

If any of these are missing after a reboot, check:
1. Is it included in `bringup.launch`? (`cat bringup.launch | grep -i <package_name>`)
2. Is the parent service actually running? (`systemctl status start_app_node.service`)
3. Did it crash silently? (`journalctl -u start_app_node.service --no-pager | tail -100`)

---

## 7. Common Pitfall — Duplicate Processes

If a node's topic exists (e.g. `/scan`) but shows "no new messages," check for **duplicate instances fighting over a shared resource** (serial port, camera device, etc.) — usually caused by a leftover manual test session running alongside the systemd-launched one.

### Detect it
```bash
ps aux | grep -i <node_or_package_name>
```
Look for more than one matching `roslaunch`/node process, or `<defunct>` (zombie) entries.

### Fix it
```bash
# 1. Stop the service so it stops respawning during cleanup
sudo systemctl stop start_app_node.service

# 2. Kill every related process
pkill -9 -f <node_name>
pkill -9 -f "roslaunch <package_name>"
ps aux | grep -i <node_name>        # should show nothing but the grep itself

# 3. Close any other terminal still manually running roslaunch for that node

# 4. Restart the service cleanly
sudo systemctl start start_app_node.service
sleep 8

# 5. Confirm exactly ONE process and real data
ps aux | grep -i <node_name>
rostopic hz <relevant_topic>
```

**Rule of thumb:** never leave a manually-launched node/launch file running in a spare terminal while also relying on the systemd service — always fully kill manual test sessions before restarting/enabling the service.

---

## 8. Quick Reference

```bash
# One-time setup for any new node
cp ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch{,.bak}
nano ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch
# add: <include file="$(find <package>)/launch/<file>.launch"/>  inside <launch>

sudo systemctl enable start_app_node.service
sudo systemctl restart start_app_node.service

# Verify after every reboot
rosnode list

# If something's wrong
journalctl -u start_app_node.service --no-pager | tail -100
ps aux | grep -i <node_name>
```

---

## 9. Troubleshooting Checklist

| Symptom | Likely Cause | Fix |
|---|---|---|
| A node is missing from `rosnode list` after reboot | Not included in `bringup.launch`, or service not enabled | Check `bringup.launch` includes; `systemctl is-enabled start_app_node.service` |
| Node crashes right after boot | Check hidden logs | `journalctl -u start_app_node.service --no-pager \| tail -100` (systemd status hides it) |
| A topic exists but "no new messages" | Duplicate processes competing for the same hardware/port | `pkill -9 -f <node_name>`, then restart the service |
| `systemctl status` shows nothing useful | Service redirects stdout/stderr to null | Use `journalctl` instead |
| Service exits with `code=exited, status=1/FAILURE` | Usually a node-name conflict from duplicate launches | Kill all duplicates, restart service fresh |
| Everything stops working after an update | An update package may have overwritten `bringup.launch` or a node's launch file | Restore from your `.bak` copies |
