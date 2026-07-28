# 🤖 The JetAuto Chronicles: A SLAM Debugging Story (Gmapping)

> **Platform:** Jetson Nano · Ubuntu 18.04 · ROS Melodic · JetAuto Pro · G4 LiDAR · Astra Pro Plus
>
> **Status:** ✅ Resolved — SLAM is alive and mapping!

This is the story of how a stubborn JetAuto Pro robot went from "nothing works" to confidently drawing maps of its surroundings in RViz. It took patience, a lot of `grep`, and a healthy dose of "wait, WHY are there two nodes with the same name?!" — but we got there.

---

## 🎬 Session 1: "Why Won't You Just Boot Properly?"

Every good debugging story starts with a simple question: *does the startup even work?*

### Step 1 — Checking the Autostart Service

First things first, I needed to know what actually happens when this robot powers on.

```bash
systemctl cat start_app_node.service
```

Turns out, the boot sequence looked clean on paper:

```text
source_env.bash
    ↓
roslaunch jetauto_bringup bringup.launch
```

Confirmed with:

```bash
sudo grep "^ExecStart" /etc/systemd/system/start_app_node.service
```

```text
ExecStart=/home/jetauto/jetauto_ws/src/jetauto_bringup/scripts/source_env.bash roslaunch jetauto_bringup bringup.launch
```

✅ **Verdict:** The startup service itself was innocent. Time to look deeper.

<img width="933" height="510" alt="Startup service inspection" src="https://github.com/user-attachments/assets/c0291633-07cb-4b46-b603-e9a4ebdcf1c9" />

---

## 🔍 Step 2 — Peeking Inside `bringup.launch`

This is where things got interesting.

```bash
sed -n '1,200p' ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch
```

Buried in the file was this line:

```xml
<include file="$(find rplidar_ros)/launch/rplidar.launch"/>
```

But that's not what JetAuto is *supposed* to use. It should be calling its own dedicated LiDAR wrapper:

```xml
<include file="$(find jetauto_peripherals)/launch/lidar.launch"/>
```

💡 **Why this matters:** JetAuto's wrapper handles multiple LiDAR types intelligently. Going straight to the generic RPLiDAR package skips all of that logic.

### The Fix

```bash
# Edited: ~/jetauto_ws/src/jetauto_bringup/launch/bringup.launch
# Changed the include to use jetauto_peripherals/launch/lidar.launch
```

```bash
sudo systemctl restart start_app_node.service
```

<img width="1297" height="267" alt="bringup.launch edit" src="https://github.com/user-attachments/assets/0c9eeeb1-ec65-4452-9f12-a9e569110597" />

---

## 📡 Step 3 — "The Scan Topic Exists... But Something's Off"

```bash
rostopic list | grep scan
```

```text
/scan
```

Great, `/scan` was there. But then:

```bash
rostopic info /scan
```

```text
Publisher:
/rplidarNode
```

Wait — `/rplidarNode`? That name felt suspicious, like there was a ghost driver running somewhere it shouldn't be.

<img width="761" height="276" alt="rostopic info scan output" src="https://github.com/user-attachments/assets/9a8ee427-6ef7-4905-ab22-a8469e936e12" />

---

## 💥 Step 4 — The Crash That Cracked the Case

Time to stop letting systemd hide the logs. Manual launch time.

```bash
sudo systemctl stop start_app_node.service

source ~/jetauto_ws/src/jetauto_bringup/scripts/source_env.bash
roslaunch jetauto_bringup bringup.launch
```

And there it was — the smoking gun:

```text
RLException:
multiple nodes named
/ydlidar_lidar_g4_publisher
```

😤 **Finally!** A real, concrete error. The robot was trying to launch the *same LiDAR node twice*.

<img width="927" height="646" alt="RLException duplicate node error" src="https://github.com/user-attachments/assets/9fc90581-ba2a-4ade-975d-1098e4d630d8" />

---

## 🕵️ Step 5 — Hunting Down the Duplicate

```bash
grep -R "ydlidar_lidar_g4_publisher" ~/jetauto_ws/src -n
```

Only **one** definition existed:

```text
jetauto_peripherals/launch/include/ydlidar.launch
```

So if there's only one definition... something was *including* it more than once.

```bash
grep -R "ydlidar.launch" ~/jetauto_ws/src -n
```

---

## 🧩 Step 6 — Tracing Every Path to `lidar.launch`

```bash
grep -R "launch/lidar.launch" ~/jetauto_ws/src -n
```

The results painted a busy picture — `lidar.launch` was being pulled in from multiple places:

- `bringup.launch`
- `jetauto_slam/include/jetauto_robot.launch`
- `jetauto_app/lidar_app.launch`
- voice control packages
- example packages

And the biggest clue of all: `start_app.launch` was quietly including:

```xml
<include file="$(find jetauto_app)/launch/lidar_app.launch"/>
```

### 🧠 The Hypothesis

```text
bringup.launch → lidar.launch → ydlidar.launch
            AND
start_app.launch → lidar_app.launch → lidar.launch → ydlidar.launch
```

Two separate paths, both trying to spin up a node called `ydlidar_lidar_g4_publisher`. No wonder ROS was throwing a tantrum.

```text
$ grep -R "ydlidar_lidar_g4_publisher" ~/jetauto_ws/src -n
.../include/ydlidar.launch:8: <node name="ydlidar_lidar_g4_publisher" pkg="ydlidar_ros_driver" .../>

$ grep -R "launch/lidar.launch" ~/jetauto_ws/src -n
.../jetauto_slam/launch/include/jetauto_robot.launch:83
.../jetauto_bringup/launch/bringup.launch:25
.../jetauto_app/launch/lidar_app.launch
.../xf_mic_asr_offline/launch/voice_control_move.launch:5
.../jetauto_example/scripts/line_follow_clean/line_follow_clean_node.launch:4

$ sed -n '1,200p' ~/jetauto_ws/src/jetauto_app/launch/start_app.launch
<launch>
    <include file="$(find jetauto_app)/launch/lidar_app.launch"/>
    <include file="$(find jetauto_app)/launch/line_following.launch"/>
    <include file="$(find jetauto_app)/launch/object_tracking.launch"/>
    <include file="$(find jetauto_app)/launch/ar_app.launch"/>
    <include file="$(find jetauto_app)/launch/patrol.launch"/>
</launch>
```

**Confirmed.** `lidar_app.launch` was the culprit — a second, redundant LiDAR launch fighting for the same node name.

### 📝 Lessons from Session 1

1. When systemd hides your logs, launch manually — you'll see the truth.
2. A duplicate node name almost always means a launch file is being included twice, somewhere.
3. Search *before* you edit. Know the whole tree before you cut a branch.

<img width="948" height="612" alt="Debugging session screenshot" src="https://github.com/user-attachments/assets/2bfd98c5-f8fa-4a2f-a303-0b1d3af14881" />
<img width="1058" height="738" alt="Debugging session screenshot" src="https://github.com/user-attachments/assets/99b634c2-b2b8-4227-8f6c-7a01889060d3" />
<img width="1047" height="256" alt="Debugging session screenshot" src="https://github.com/user-attachments/assets/4a1d6e48-40f7-41d0-a609-3d83a5687141" />

---

## 🗺️ Part 3: The SLAM & RPLIDAR Migration Saga

With the duplicate-node ghost exorcised, it was time for the real mission: **get 2D Gmapping working with the onboard LiDAR.**

At first, nothing cooperated:

- ❌ No `/scan` topic
- ❌ No odometry
- ❌ Wrong LiDAR driver launching
- ❌ Broken environment configuration
- ❌ Wrong serial device path

By the end of this chapter, though, every single one of those turned green. Here's how it happened.

---

## 🔦 Step 1 — Is the Hardware Even Okay?

Before blaming any code, I tested the LiDAR completely on its own, bypassing all the JetAuto wrapper logic.

```bash
roslaunch rplidar_ros rplidar.launch
```

```text
RPLIDAR S/N
Firmware 1.29
Hardware Rev 7
Health OK
```

```bash
rostopic list | grep scan
```

```text
/scan
```

```bash
rostopic hz /scan
```

```text
~14 Hz
```

🎉 The hardware was **perfectly healthy**. So the problem lived in software, not silicon. That was actually a relief — hardware failures are a much worse day.

---

## ⚖️ Step 2 — Two Drivers, One Robot

A quick look at the workspace showed *both* LiDAR driver packages sitting side by side:

```text
third_party/
    rplidar_ros/
    ydlidar_ros_driver/
```

Which raised the obvious question: which one is actually supposed to run?

---

## 🎯 Step 3 — Finding Where the Driver Gets Chosen

```bash
grep -R "ydlidar_lidar_g4_publisher" ~/jetauto_ws/src -n
grep -R "rplidar.launch" ~/jetauto_ws/src -n
```

Inside `jetauto_peripherals/launch/lidar.launch`, the logic was actually quite elegant:

```text
if lidar_type == "A1"  → rplidar.launch
if lidar_type == "A2"  → rplidar.launch
if lidar_type == "G4"  → ydlidar.launch
```

So the *system* already knew how to support both LiDARs. It was simply being told to pick the **wrong one**.

---

## 🧵 Step 4 — Following the Thread of `lidar_type`

```bash
grep -R "lidar_type" ~/jetauto_ws/src -n
```

```xml
<arg name="lidar_type" default="$(env LIDAR_TYPE)"/>
```

Ahh — so `lidar_type` wasn't hardcoded at all. It came from an **environment variable**. Time to check it.

```bash
echo $LIDAR_TYPE
```

```text
G4
```

😳 There it was. The system genuinely believed this robot had a **G4 YDLIDAR** — but it actually had an **RPLIDAR**.

---

## 📁 Step 5 — Finding Where That Variable Lived

```bash
grep -R "export LIDAR_TYPE" /home/jetauto -n
```

```text
~/.typerc
```

```bash
export LIDAR_TYPE=G4
```

Interestingly, an older backup file `.bktyperc` still had:

```bash
export LIDAR_TYPE=A1
```

A little archaeological proof that this robot originally shipped configured for an **A1 RPLIDAR** — somewhere along the way, that got overwritten.

---

## 🛠️ Step 6 — Fixing the Environment Variable

```bash
nano ~/.typerc
```

Changed:

```bash
export LIDAR_TYPE=G4
```

to:

```bash
export LIDAR_TYPE=A1
```

```bash
source ~/.typerc
echo $LIDAR_TYPE
```

```text
A1
```

No launch files touched. Just one honest configuration value, corrected — and the existing logic did the rest.

---

## 🔌 Step 7 — The Serial Port Mystery

```bash
cat jetauto_peripherals/launch/include/rplidar.launch
```

```xml
serial_port="/dev/lidar"
```

```bash
ls -l /dev/lidar
```

```text
No such file
```

```bash
ls -l /dev/ttyUSB0
```

```text
Device exists
```

So `/dev/lidar` was a symlink that simply never got created (no udev rule for it). The real hardware was sitting at `/dev/ttyUSB0` the whole time.

### The Fix

```xml
<!-- Before -->
<param name="serial_port" value="/dev/lidar"/>

<!-- After -->
<param name="serial_port" value="/dev/ttyUSB0"/>
```

---

## 🧹 Housekeeping: Earlier Fixes Along the Way

A few smaller changes had already happened earlier in the debugging journey and deserve a mention:

- **Disabled auto-startup** temporarily, so nothing unexpected launched mid-debug.
- **Removed the duplicate LiDAR include** inside `lidar_app.launch`, stopping two drivers from fighting over the same serial port.
- **Updated the YDLIDAR launch file** from `/dev/lidar` to `/dev/ttyUSB0` — though this later became irrelevant once RPLIDAR took over.

---

## 🎉 The Payoff: SLAM Actually Works!

```bash
roslaunch jetauto_slam slam.launch
```

```text
RPLIDAR S/N
Firmware 1.29
Hardware Rev 7
Health OK

Initialization complete
Registering First Scan
Registering Scans: Done
```

And the node list now proudly showed `rplidarNode` instead of the old `ydlidar_lidar_g4_publisher`. 🥳

### Topics Now Publishing

```text
/jetauto_1/scan
/jetauto_1/scan_raw
/jetauto_1/odom
/jetauto_1/map
/map_metadata
```

LiDAR ✅ · Odometry ✅ · Gmapping ✅ — all green.

---

## 🏷️ Why `/jetauto_1/...` Instead of Plain `/scan`?

JetAuto namespaces everything under `/jetauto_1/` so that multiple robots can share one ROS Master without their topics colliding. So:

```text
/scan  →  /jetauto_1/scan
/odom  →  /jetauto_1/odom
```

Small detail, but it explains a lot of confusion later.

---

## ⏳ Why `map_saver` Hung Forever

```bash
rosrun map_server map_saver -f my_map
```

This command waited... and waited... and waited. Why? Because it subscribes to `/map` by default — but JetAuto publishes to `/jetauto_1/map`. Classic namespace trap.

### The Correct Command

```bash
rosrun map_server map_saver \
  map:=/jetauto_1/map \
  -f my_map
```

This produced two files:

```text
my_map.pgm   →  the occupancy grid image (walls, free space, unknown space)
my_map.yaml  →  resolution, origin, thresholds, image name
```

### Viewing the Map

```bash
eog my_map.pgm
# or
xdg-open my_map.pgm
```

---

## ⚠️ One Small Loose End

```text
usb_cam tries to open /dev/usb_cam — which doesn't exist.
Result: "Cannot identify /dev/usb_cam"
```

The good news? The camera isn't needed for 2D Gmapping, so SLAM runs perfectly fine despite this error. A problem for another day.

---

## 🏗️ Final Architecture

```text
                Wheel Encoder
                     │
                     ▼
          jetauto_odom_publisher
                     │
                     ▼
             /jetauto_1/odom_raw
                     │
                     ▼
             ekf_localization
                     │
                     ▼
              /jetauto_1/odom
                     │
                     │
                     ▼
                 Gmapping
                 ▲       ▲
                 │       │
        /jetauto_1/scan  │
                 ▲        │
                 │        │
            RPLIDAR Node
                 │
                 ▼
            /dev/ttyUSB0
```

---

## 📚 Lessons Learned (The Hard-Won Kind)

1. **Verify hardware independently** before ever touching software — it saves you from chasing ghosts.
2. **Never assume launch files are broken.** Often the logic is fine; the *inputs* are wrong.
3. **Trace every configuration variable back to its source.** Environment variables are sneaky.
4. **One overwritten variable can change everything.** `LIDAR_TYPE=G4` silently broke a robot that had an RPLIDAR.
5. **ROS namespaces change topic names** — always double-check before assuming a topic doesn't exist.
6. **`/jetauto_1/map` is not `/map`.** Small prefix, big difference.
7. **Fix configuration, not code**, whenever possible — it's safer and more maintainable.
8. **Debug one layer at a time:**

```text
Hardware → Driver → Topics → TF → Odometry → SLAM → Mapping
```

---

## ✅ Final Status Report

| Component         | Status                              |
|--------------------|--------------------------------------|
| RPLIDAR            | ✅ Working                            |
| Driver Selection   | ✅ Fixed                              |
| Serial Port        | ✅ Fixed                              |
| `/scan`            | ✅ Publishing                         |
| `/odom`            | ✅ Publishing                         |
| EKF                | ✅ Running                            |
| Gmapping           | ✅ Running                            |
| Map Generation     | ✅ Working                            |
| Map Saving         | ✅ Ready (via `/jetauto_1/map`)       |
| USB Camera         | ⚠️ Minor unresolved issue (non-blocking) |

---

## 🚀 What's Next

With SLAM finally cooperating, the road ahead looks like:

- 🧭 Building a full room map from start to finish
- 💾 Saving the occupancy grid for reuse
- 🗺️ Loading the saved map with `map_server`
- 📍 Adding localization via AMCL
- 🛞 Moving on to full autonomous navigation
- 🧠 Implementing path planning

*To be continued...*
