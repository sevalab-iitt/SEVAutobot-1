#  RPLIDAR
 
---

## Part 1 — The Crash Bug (`*** buffer overflow detected ***`)

### Symptom
```bash
roslaunch rplidar_ros rplidar.launch
```
caused an infinite crash-restart loop:
```
*** buffer overflow detected ***: rplidarNode terminated
[rplidarNode-1] process has died [pid ..., exit code -6, ...]
[rplidarNode-1] restarting process
```
Crashed immediately after printing `SDK Version:2.0.0`, before publishing any `/scan` data. `respawn="true"` in the launch file caused endless restarts, flooding the terminal.

### Root Cause
`*** buffer overflow detected ***` is glibc's stack-protector (`fortify_source`) catching a stack-smashing bug in the compiled `rplidarNode` binary, triggered specifically by `angle_compensate`:

- Lidar auto-selected a **high-sample-rate scan mode** ("Sensitivity", 8 kHz).
- `angle_compensate` in `rplidar_ros` uses a **fixed-size stack buffer** to build the angle-compensated scan.
- At 8 kHz sample rate, more samples per revolution are produced than that buffer was sized for → stack overflow → glibc aborts the process (`SIGABRT`, exit code `-6`).

**Confirmed by:** running the node directly via `rosrun rplidar_ros rplidarNode` (bypassing the launch file's `angle_compensate=true` param) — it started cleanly, no crash. This proved the hardware/serial connection was fine and the bug was purely software-side.

### The Fix

**File:** `~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch`

Changed:
```xml
<param name="angle_compensate" type="bool" value="true"/>
```
to:
```xml
<param name="angle_compensate" type="bool" value="false"/>
```

> Note: `angle_compensate` is hardcoded via `<param>` with no `<arg>` wrapper, so passing `angle_compensate:=false` on the command line does **nothing**. The XML must be edited directly.

**Commands used:**
```bash
# Backup first
cp ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch \
   ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch.bak

# Edit just the one line
sed -i 's/name="angle_compensate" type="bool" value="true"/name="angle_compensate" type="bool" value="false"/' \
  ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch

# Confirm only that line changed
diff ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch.bak \
     ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch
```

### Final working launch file
```xml
<launch>
  <node
      name="rplidarNode"
      pkg="rplidar_ros"
      type="rplidarNode"
      output="screen"
      respawn="true">
    <param name="serial_port" type="string" value="/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0"/>
    <param name="serial_baudrate" type="int" value="115200"/>
    <!-- For A3:
    <param name="serial_baudrate" type="int" value="256000"/>
    -->
    <param name="frame_id" type="string" value="laser"/>
    <param name="inverted" type="bool" value="false"/>
    <param name="angle_compensate" type="bool" value="false"/>
  </node>
</launch>
```

**Verify:** relaunch and confirm the SUMMARY block prints `angle_compensate: False`, with no `*** buffer overflow detected ***`.

---

## Part 2 — Understanding the `/scan` Topic

Message type: `sensor_msgs/LaserScan`

```
Header header            # timestamp + frame_id ("laser")

float32 angle_min        # start angle (radians)
float32 angle_max        # end angle (radians)
float32 angle_increment  # angular step between measurements (radians)

float32 time_increment   # time between measurements (sec)
float32 scan_time        # time between full scans (sec)

float32 range_min        # min valid range (m)
float32 range_max        # max valid range (m)

float32[] ranges         # distance per angle step (m)
float32[] intensities    # signal strength (often unused on RPLIDAR)
```

To compute the angle for `ranges[i]`:
```
angle = angle_min + i * angle_increment
```
Invalid readings (`0.0`, `inf`, `nan`) should be filtered before use.

---

## Part 3 — Point Cloud Conversion & Saving

### Convert LaserScan → PointCloud2
Requires `laser_geometry`:
```bash
sudo apt install ros-melodic-laser-geometry
```

Create `~/scan_to_cloud.py` (via `nano`, not pasted into bash directly):
```python
#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan, PointCloud2
import laser_geometry.laser_geometry as lg

projector = lg.LaserProjection()
pub = rospy.Publisher('/cloud', PointCloud2, queue_size=1)

def callback(scan_msg):
    cloud = projector.projectLaser(scan_msg)
    pub.publish(cloud)

rospy.init_node('scan_to_cloud')
rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
```
```bash
chmod +x ~/scan_to_cloud.py
python ~/scan_to_cloud.py
```

### Save to `.pcd` files
```bash
sudo apt install ros-melodic-pcl-ros
rosrun pcl_ros pointcloud_to_pcd input:=/cloud
```
Writes one timestamped `.pcd` file per message received (e.g. `1782994466046738.pcd`) into the current directory. **Ctrl+C once you have enough** — it writes a new file almost every scan cycle.

### Inspect saved files
```bash
ls -lh *.pcd
ls *.pcd | wc -l
head -15 <file>.pcd     # view text header, confirms valid data
```

### View `.pcd` files (needs a display, or `ssh -X`)
```bash
sudo apt install pcl-tools
pcl_viewer <file>.pcd
```
Or republish into ROS/RViz:
```bash
rosrun pcl_ros pcd_to_pointcloud <file>.pcd 0.1
```

### Merge multiple files into one cloud
```bash
pcl_concatenate_points_pcd *.pcd
pcl_viewer output.pcd
```
>   If the lidar was stationary, this just overlays near-identical scans — it does not build a bigger map. Real map-building needs the robot to move + odometry data (SLAM).

### Cleanup extra files
```bash
ls *.pcd | sort | tail -n +6 | xargs rm   # keeps first 5, deletes rest
```

---

## Part 4 — Autostart on Boot (systemd)

### Discovery: JetAuto already has an autostart mechanism
```bash
systemctl list-units --type=service --all | grep -i ros
# roscore.service — always running

find ~/jetauto_ws -iname "*.service"
# jupyter.service, start_app_node.service, clear_log.service,
# fan_control.service, expand_rootfs.service, voltage_detect.service
```

`start_app_node.service` is JetAuto's official master autostart entry point:
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
>   `StandardOutput=null` / `StandardError=null` means crashes are **silent** in `systemctl status` — use `journalctl -u start_app_node.service` to see real errors.

### Managing this service
```bash
sudo systemctl status start_app_node.service     # check state
sudo systemctl is-enabled start_app_node.service # confirm boot-persistence
sudo systemctl enable start_app_node.service      # enable permanently
sudo systemctl start start_app_node.service       # start now
sudo systemctl stop start_app_node.service        # stop now (temporary)
sudo systemctl disable start_app_node.service     # disable permanently
sudo systemctl restart start_app_node.service     # restart
journalctl -u start_app_node.service --no-pager | tail -100   # view real logs
```

### Problem found: lidar was missing from bringup.launch
`bringup.launch` (`~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch`) brings up the chassis controller, servos, cameras, app communication (`rosbridge`), and joystick — but had **no include for `rplidar_ros`**. This is why `/rplidarNode` never appeared in `rosnode list`, even though `/lidar_app` (a higher-level app-control node) was running and waiting for `/scan` data that never came.

### The fix: add lidar include to bringup.launch

Backup first:
```bash
cp ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch \
   ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch.bak
```

Edit `~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch` and add, near the chassis/servo includes:
```xml
<!--激光雷达驱动(lidar driver)-->
<include file="$(find rplidar_ros)/launch/rplidar.launch"/>
```

Restart the service to apply:
```bash
sudo systemctl restart start_app_node.service
sleep 8
rosnode list | grep -i rplidar
rostopic list | grep -i scan
```

Since this include points to the same `rplidar.launch` fixed in Part 1 (`angle_compensate=false`), the crash fix automatically carries over.

**Full reboot test (final proof):**
```bash
sudo reboot
# after reboot:
rosnode list | grep -i rplidar
```

---

## Part 5 — Duplicate Process Conflict ("no new messages")

### Symptom
```bash
rostopic echo /scan
subscribed to [/scan]
no new messages
no new messages
...
```
`/scan` topic existed (registered), but nothing was actually publishing to it.

### Root cause
**Two separate `roslaunch rplidar_ros rplidar.launch` processes were running simultaneously** — one from the systemd bringup service (after adding the include), and a leftover manual one from earlier testing that was never fully killed. Both fought over the same `/dev/ttyUSB0` serial port. Symptoms in `ps aux`:
```
roslaunch rplidar_ros rplidar.launch     (older PID)
roslaunch rplidar_ros rplidar.launch     (newer PID)
[rplidarNode] <defunct>                   ← zombie process
rplidarNode-1.log  / rplidarNode-2.log    ← two competing node instances
```
This also caused `start_app_node.service` to exit with `code=1/FAILURE` in the journal, due to "new node registered with same name" conflicts cascading through bringup.

### The fix
```bash
# 1. Stop the service so it stops respawning during cleanup
sudo systemctl stop start_app_node.service

# 2. Kill every lidar-related process, including zombie parents
pkill -9 -f rplidarNode
pkill -9 -f "roslaunch rplidar_ros"
ps aux | grep -i rplidar        # confirm clean (only the grep line itself)

# 3. Check no manual terminal is still running roslaunch (Ctrl+C any that are)

# 4. Restart the bringup service fresh
sudo systemctl start start_app_node.service
sleep 8

# 5. Confirm single clean process + real data
ps aux | grep -i rplidar        # should show exactly ONE rplidarNode
rosnode list | grep rplidar
rostopic hz /scan                # should show steady ~10 Hz
```

**Lesson:** always fully kill old manual test sessions (`pkill -9 -f rplidarNode; pkill -9 -f roslaunch`) before restarting the systemd service, to avoid two instances racing for the same serial port.

---

## Part 6 — Accessing the Live Feed (Terminal Only, No Code)

Once `rostopic hz /scan` shows a steady rate, use any of these — no scripting required:

```bash
# 1. See raw data scrolling live
rostopic echo /scan

# 2. See one snapshot only
rostopic echo /scan -n 1

# 3. Check it's alive + publish rate
rostopic hz /scan

# 4. See topic info (type, publishers, subscribers) without the data
rostopic info /scan

# 5. See it visually (most useful — an actual live picture)
rosrun rviz rviz
# then in RViz: Fixed Frame -> "laser", Add -> By topic -> /scan -> LaserScan
```

### When you'd need code instead
The `lidar_listener.py` style script (subscribing in Python) is only needed if you want the robot to **act** on the data automatically — e.g. stop before hitting a wall, trigger an alert, log to a file continuously. For just watching/checking the feed, the terminal commands above are sufficient.

```python
#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan

def callback(scan_msg):
    ranges = scan_msg.ranges
    valid = [r for r in ranges if r > 0.0]
    if valid:
        rospy.loginfo("Closest obstacle: %.2f m" % min(valid))

rospy.init_node('lidar_listener')
rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
```
| Line | Purpose |
|---|---|
| `#!/usr/bin/env python` | Lets the file run directly (`./script.py`) with the right interpreter |
| `import rospy` | ROS's Python client library — talks to ROS |
| `from sensor_msgs.msg import LaserScan` | Import the message type so Python understands the data structure |
| `def callback(...)` | Function ROS calls automatically on every new `/scan` message |
| `scan_msg.ranges` | Pulls out the distance array from that message |
| `[r for r in ranges if r > 0.0]` | Filters out invalid readings (`0.0`/`inf`/`nan`) |
| `rospy.loginfo(...)` | ROS's version of `print`, tagged with node name/timestamp |
| `rospy.init_node(...)` | Registers this script as a real ROS node |
| `rospy.Subscriber(...)` | Sets up the actual subscription + callback binding |
| `rospy.spin()` | Keeps the script alive listening forever (Ctrl+C to stop) — without it, the script exits instantly and never receives anything |

---

## Quick Reference — Everything in Order

```bash
# === ONE-TIME FIXES (already applied) ===

# Fix 1: disable angle_compensate to stop the buffer overflow crash
cp ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch{,.bak}
sed -i 's/angle_compensate" type="bool" value="true"/angle_compensate" type="bool" value="false"/' \
  ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch

# Fix 2: add lidar to the auto-start bringup chain
cp ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch{,.bak}
# manually add inside <launch>: <include file="$(find rplidar_ros)/launch/rplidar.launch"/>

sudo systemctl enable start_app_node.service     # ensure it persists on reboot
sudo systemctl restart start_app_node.service

# === EVERY-TIME SANITY CHECK ===
ps aux | grep -i rplidar        # exactly ONE rplidarNode process, no zombies
rosnode list | grep rplidar
rostopic hz /scan                # confirm ~10 Hz

# === VIEW THE LIVE FEED ===
rostopic echo /scan              # raw text
rosrun rviz rviz                 # visual (Fixed Frame: laser, Add -> /scan -> LaserScan)

# === SAVE AS POINT CLOUD (optional) ===
python ~/scan_to_cloud.py &
rosrun pcl_ros pointcloud_to_pcd input:=/cloud
# Ctrl+C after a few files
pcl_viewer <file>.pcd
```

---

## Troubleshooting Checklist (if it breaks again)

1. **Buffer overflow crash returns** → check `angle_compensate` is still `false` in `rplidar.launch` (a package reinstall/update could overwrite it — the `.bak` file has the working version).
2. **`/rplidarNode` missing from `rosnode list`** → check `bringup.launch` still has the `rplidar_ros` include (same risk as above).
3. **`/scan` exists but "no new messages"** → check for duplicate processes: `ps aux | grep -i rplidar`. Kill all with `pkill -9 -f rplidarNode; pkill -9 -f roslaunch`, then `sudo systemctl restart start_app_node.service`.
4. **Service crashes silently** → `journalctl -u start_app_node.service --no-pager | tail -100` (systemd status alone won't show it, since output is redirected to null).
5. **Serial port conflict** → `sudo lsof /dev/ttyUSB0` to check nothing else is holding it.
