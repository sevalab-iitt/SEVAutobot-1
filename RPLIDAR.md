# RPLIDAR (JetAuto) — Crash Fix, Scan Feed, and Point Cloud Workflow

**Platform:** JetAuto (Jetson-based), ROS Melodic
**Lidar:** RPLIDAR (CH340 USB-serial bridge), S/N `D9ACED95C4E493CAA5E69EF0487C4B6E`, Firmware 1.29, Hardware Rev 7
**Serial baud rate:** 115200

---

## 1. The Problem

Running:
```bash
roslaunch rplidar_ros rplidar.launch
```
caused an infinite crash-restart loop:
```
*** buffer overflow detected ***: rplidarNode terminated
[rplidarNode-1] process has died [pid ..., exit code -6, ...]
[rplidarNode-1] restarting process
```
The node crashed immediately after printing `SDK Version:2.0.0`, before it could publish any `/scan` data. `respawn="true"` in the launch file caused it to restart endlessly, flooding the terminal.

### Root Cause

`*** buffer overflow detected ***` is glibc's stack-protector (`fortify_source`) catching a stack-smashing bug inside the `rplidarNode` binary. It was triggered by the `angle_compensate` feature:

- The lidar auto-selected a **high-sample-rate scan mode** ("Sensitivity", 8 kHz).
- `angle_compensate` in `rplidar_ros` uses a **fixed-size stack buffer** to build the angle-compensated scan.
- At 8 kHz sample rate, more samples per revolution are produced than that buffer was sized for → stack overflow → glibc aborts the process (`SIGABRT`, exit code `-6`).

Confirmed by running the node directly with `rosrun` (bypassing the launch file's `angle_compensate=true` param) — it started cleanly with no crash, proving the hardware/serial connection was fine and the bug was software-side.

---

## 2. The Fix

**File:** `~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch`

Changed:
```xml
<param name="angle_compensate" type="bool" value="true"/>
```
to:
```xml
<param name="angle_compensate" type="bool" value="false"/>
```

This is a **permanent fix** — it edits the launch file on disk, not a runtime argument, so it persists across reboots and future `roslaunch` calls. No rebuild needed since it's an XML param, not compiled code.

> 

### Applying the fix safely

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

### Cleaning up stuck/duplicate processes (do this before every relaunch during debugging)

```bash
pkill -9 -f rplidarNode
pkill -9 -f roslaunch
ps aux | grep -i rplidar   # should return nothing relevant
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

**Verify the fix:** relaunch and check the SUMMARY block prints `angle_compensate: False`, and no `*** buffer overflow detected ***` appears.

---

## 3. Understanding the `/scan` Topic

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

### Useful commands

```bash
rostopic echo /scan -n 1     # print one full scan message
rostopic echo /scan          # continuous stream
rostopic hz /scan             # confirm publish rate (~10 Hz)
```

### Visualize in RViz

```bash
rosrun rviz rviz
```
- Set **Fixed Frame** → `laser`
- **Add** → **By topic** → `/scan` → **LaserScan**

### Minimal Python subscriber example

```python
#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan

def callback(scan_msg):
    ranges = scan_msg.ranges
    closest = min(r for r in ranges if r > 0.0)
    rospy.loginfo("Closest obstacle: %.2f m" % closest)

rospy.init_node('lidar_listener')
rospy.Subscriber('/scan', LaserScan, callback)
rospy.spin()
```

---

## 4. Converting LaserScan → PointCloud2

Requires `laser_geometry`:
```bash
sudo apt install ros-melodic-laser-geometry
python -c "import laser_geometry"   # verify it's importable
```

**Create the converter script** (use `nano`, don't paste into bash directly):
```bash
nano ~/scan_to_cloud.py
```
Paste:
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
Save (`Ctrl+O`, `Enter`), exit (`Ctrl+X`), then:
```bash
chmod +x ~/scan_to_cloud.py
python ~/scan_to_cloud.py
```
Confirm it's publishing:
```bash
rostopic echo /cloud -n 1
```

---

## 5. Saving Point Cloud Data to `.pcd` Files

```bash
sudo apt install ros-melodic-pcl-ros
rosrun pcl_ros pointcloud_to_pcd input:=/cloud
```
This writes one timestamped `.pcd` file per received message (e.g. `1782994466046738.pcd`) into the current directory. **Press `Ctrl+C` once you have enough** — otherwise it keeps writing a new file roughly every scan cycle (this is why hundreds of near-identical files can accumulate quickly).

### Alternative: record raw data instead (for later conversion/replay)
```bash
rosbag record /scan
```

---

## 6. Finding and Inspecting Saved `.pcd` Files

```bash
ls -lh *.pcd                 # list files in current dir
ls *.pcd | wc -l              # count them
head -15 <file>.pcd           # view the text header (confirms valid data)
```

Typical header:
```
# .PCD v0.7 - Point Cloud Data file format
VERSION 0.7
FIELDS x y z
SIZE 4 4 4
TYPE F F F
COUNT 1 1 1
WIDTH ...
HEIGHT 1
POINTS ...
DATA ascii
```

---

## 7. Viewing `.pcd` Files

### Requires a display (local monitor or `ssh -X`)

Install:
```bash
sudo apt install pcl-tools
```

**View a single file:**
```bash
pcl_viewer <file>.pcd
```
Left-click drag = rotate, scroll = zoom, `r` = reset view.

**Republish a saved file back into ROS / RViz:**
```bash
rosrun pcl_ros pcd_to_pointcloud <file>.pcd 0.1
```
Then in RViz: **Add** → **By topic** → `/cloud_pcd` → **PointCloud2**.

### No display available (headless/SSH without X forwarding)
Use `head -15 <file>.pcd` to confirm valid point data as text, or copy the file to a desktop machine and open it in **CloudCompare**.

---

## 8. Working with Multiple `.pcd` Files

**Merge all files into one combined cloud:**
```bash
cd ~
pcl_concatenate_points_pcd *.pcd
pcl_viewer output.pcd
```
 

**Keep only the first N files, delete the rest:**
```bash
cd ~
ls *.pcd | sort | tail -n +6 | xargs rm   # keeps first 5, deletes rest
```

**Quick sequential preview (needs display):**
```bash
for f in *.pcd; do
  echo "Showing $f"
  timeout 1 pcl_viewer "$f"
done
```

---

## Quick Reference — Full Session Command Order

```bash
# 1. One-time fix
cp ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch \
   ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch.bak
sed -i 's/name="angle_compensate" type="bool" value="true"/name="angle_compensate" type="bool" value="false"/' \
  ~/jetauto_ws/src/third_party/rplidar_ros/launch/rplidar.launch

# 2. Clean processes, then launch
pkill -9 -f rplidarNode; pkill -9 -f roslaunch
roslaunch rplidar_ros rplidar.launch

# 3. (new terminal) Check scan data
rostopic echo /scan -n 1

# 4. Convert to point cloud
python ~/scan_to_cloud.py &

# 5. (another terminal) Save to .pcd
rosrun pcl_ros pointcloud_to_pcd input:=/cloud
# Ctrl+C after a few files

# 6. View
pcl_viewer <file>.pcd
```
