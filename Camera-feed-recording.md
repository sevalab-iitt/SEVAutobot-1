# Camera Feed — Recording, Playback & Troubleshooting

> Capturing, recording, and replaying the live camera feed on JetAuto Pro via ROS1 — independent of Hiwonder's pre-built application. Covers verifying camera nodes, viewing the live feed, recording to a `.bag` file, managing storage, replaying footage, resolving the live-vs-recorded flicker conflict, and exporting to video.

---

## Table of Contents

- [0. Prerequisite — Starting the Camera Driver](#0-prerequisite--starting-the-camera-driver)
- [1. Viewing the Live Camera Feed](#1-viewing-the-live-camera-feed)
- [2. Recording the Camera Feed](#2-recording-the-camera-feed)
- [3. Playing Back Recorded Footage](#3-playing-back-recorded-footage)
- [4. Live vs. Recorded Feed Conflict](#4-live-vs-recorded-feed-conflict)
- [5. Inspecting Nodes and Topics](#5-inspecting-nodes-and-topics)
- [6. Exporting a Recording to Video](#6-exporting-a-recording-to-video)
- [Troubleshooting](#-troubleshooting)

---

## 0. Prerequisite — Starting the Camera Driver

Everything below assumes the Astra camera driver is already publishing. Checking the rosnode list.
<img width="641" height="584" alt="{633683FE-7AB1-43DB-99E0-DFB68F461ECB}" src="https://github.com/user-attachments/assets/2b85e0b7-3e67-4afd-93a6-493b3fbb8fc5" />

If it isn't then in jetauto_ws/src there is jetauto_peripherals in that from launch file we have to launch the astra cam.

```bash
roslaunch astra_camera astra.launch
```

**Expected result:** Device-detection messages ending with the camera's serial number and resolution. The IR projector (faint reddish glow near one of the three lenses) turns on.

**Confirms:** The `astra_camera` driver has claimed the USB device and is publishing image topics. Leave this terminal open — closing it (`Ctrl+C`) stops the driver and every step below.

> **Topic/node naming note:** This robot's driver may expose topics under `/camera/...` (e.g. `/camera/rgb/image_raw`) **or** `/astra_cam/...` (e.g. `/astra_cam/rgb/image_raw`) depending on the exact launch file and namespace used. Don't assume either — always confirm the real topic name with `rostopic list` (Section 5) before recording, and substitute it consistently through the rest of this chapter.

---

## 1. Viewing the Live Camera Feed

```bash
rosnode list
```

<img width="641" height="584" alt="{633683FE-7AB1-43DB-99E0-DFB68F461ECB}" src="https://github.com/user-attachments/assets/48f43601-8e9b-42a5-875a-30136b2f1e23" />


**Expected result:** Camera driver nodes appear — typically `astra_cam` (Astra depth camera) and/or `usb_cam` (standard USB camera), alongside the usual base and sensor nodes.

**Confirms:** The camera driver is running and registered with the ROS Master.

```bash
rqt_image_view
```

Select the live image topic (e.g. `/astra_cam/rgb/image_raw` or `/camera/rgb/image_raw`) from the dropdown at the top of the window.

**Expected result:** A live video feed updating in real time.

<img width="1920" height="990" alt="{DA73471F-7F29-4025-A663-494437EC9335}" src="https://github.com/user-attachments/assets/5bb3d3f5-1552-4b2b-ae34-66489652e3d5" />


**If no topics appear in the dropdown:** The camera driver node hasn't started. Re-check with `rosnode list`, and if it's missing, go back to Section 0.

---

## 2. Recording the Camera Feed

Once the live feed is confirmed:

```bash
rosbag record /astra_cam/rgb/image_raw
```

**Expected result:** Terminal prints `Recording...`, and a `.bag` file is saved in the current directory, named by timestamp (e.g. `2026-07-02-14-30-00.bag`).

<img width="737" height="54" alt="{BB22E255-C5AE-44D0-A9A7-36FD32C84687}" src="https://github.com/user-attachments/assets/039e0282-c06b-45a1-8636-f983fc9f38f6" />




Stop with:
```bash
Ctrl + C
```

**Name the file explicitly and store it in your workspace**, rather than relying on the default timestamp name and wherever the terminal happens to be `cd`'d into:

```bash
rosbag record -O ~/jetauto_ws/recordings/camera_test.bag /camera/rgb/image_raw
```

(Create the folder first with `mkdir -p ~/jetauto_ws/recordings` if it doesn't exist.)

**Compress while recording.** This robot has **no onboard eMMC** and records to a microSD card (see Hardware Specifications, Section 4.6), where write speed is a real bottleneck for image-heavy topics. Compressing at record time reduces both file size and write load:

```bash
rosbag record --lz4 -O ~/jetauto_ws/recordings/camera_test.bag /camera/rgb/image_raw
```
But if asked for the raw image feed then avoid compression.

### Managing Storage

```bash
df -h
```
**Expected result:** Disk usage table. Check available space before and after recording — camera topics fill storage fast.


<img width="499" height="222" alt="{6B16814C-7FC8-43FD-87EE-4C736CD16E0D}" src="https://github.com/user-attachments/assets/e035114a-f315-4da6-ae48-81725c2374cd" />


```bash
rm filename.bag
```
Deletes a specific recording. Replace `filename` with the actual file name.

```bash
ls -lh *.bag
```
Lists saved `.bag` files with sizes, confirming a recording saved successfully.

<img width="717" height="110" alt="{34017FDA-7A67-4B0C-A278-C2688F8BC2D7}" src="https://github.com/user-attachments/assets/95b62f26-668b-489d-b853-9263b0592e5b" />

---

## 3. Playing Back Recorded Footage

Requires **three terminals** running in parallel (three separate SSH sessions, or a terminal multiplexer like `tmux`/`Terminator`).

| Terminal | Command | Purpose |
|---|---|---|
| 1 | `roscore` | ROS Master — only needed if one isn't already running; check first with `rostopic list` |
| 2 | `rosbag play filename.bag` | Plays back the recorded topic(s) |
| 3 | `rqt_image_view` | Select the corresponding image topic to view the replayed stream |

**Before running `roscore` manually:** This robot normally starts `roscore` automatically at boot as a standalone ROS Master (see Network Configuration, Section 3). Running a second `roscore` while one is already active fails with `socket.error: [Errno 98] Address already in use`. Check first:
```bash
ps aux | grep rosmaster
```
If a `rosmaster` process is already listed, skip straight to Terminal 2 — don't start a new `roscore`.

---

## 4. Live vs. Recorded Feed Conflict

If the image flickers between live and recorded data during playback, it's because the live driver nodes are still publishing to the same topic the bag file is replaying to — both sources are competing.

### 4.1 Identify the Camera Nodes

```bash
rosnode list
```

Typical live camera nodes:
- `/astra_cam/astraplus`
- `/astra_cam/driver`
- `/astra_cam/astra_cam_nodelet_manager`

### 4.2 Stop the Live Camera Nodes

```bash
rosnode kill /astra_cam/astraplus
rosnode kill /astra_cam/driver
rosnode kill /astra_cam/astra_cam_nodelet_manager
```

**Confirms:** Run `rosnode list` again — the three nodes should no longer appear. Now `rosbag play filename.bag` + `rqt_image_view` will play back cleanly without flicker.

**If `rosnode kill` has no effect:** Some nodes auto-restart if managed by a launch file or supervisor process. Stop the parent launch process instead (`Ctrl+C` in the terminal that ran `roslaunch astra_camera astra.launch`), rather than killing the individual node.

---

## 5. Inspecting Nodes and Topics

| Command | What it does |
|---|---|
| `rosnode info /astra_cam/driver` | Shows a node's published/subscribed topics and offered services — useful for confirming the exact image topic a node publishes |
| `rostopic list` | Lists all active topics, independent of which node owns them — the reliable way to resolve the `/camera/...` vs `/astra_cam/...` naming question from Section 0 |
| `rostopic hz /astra_cam/rgb/image_raw` | Publishing rate (fps) of a topic — check this is a sane rate (typically ~30 fps for RGB) before recording |
| `rosbag info filename.bag` | Duration, size, topics, and message counts in a recorded bag — verify a recording before playback |

---

## 6. Exporting a Recording to Video

Convert a `.bag` file to `.mp4` for sharing or review outside ROS.

**Terminal A** — play the bag:
```bash
rosbag play filename.bag
```

**Terminal B** — extract frames while it plays:
```bash
rosrun image_view extract_images _sec_per_frame:=0.1 image:=/astra_cam/rgb/image_raw
```

**Then compile the extracted frames into video:**
```bash
ffmpeg -framerate 30 -i frame%04d.jpg -c:v libx264 output.mp4
```

**Timing matters:** `extract_images` subscribes to the *live* topic being replayed, so it must run **while** `rosbag play` is actively running in another terminal — not before or after.

** Missing from the original procedure — checking `ffmpeg` is installed** before relying on this step:
```bash
ffmpeg -version
```
**If not found:**
```bash
sudo apt update
sudo apt install ffmpeg -y
```

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| No image in `rqt_image_view` | Wrong topic selected, or driver not active | Confirm with `rosnode list`; relaunch driver (Section 0) if missing |
| Recording stops immediately / file is 0 KB | Topic name doesn't match an active topic | Check exact name with `rostopic list` before recording |
| Low disk space during recording | microSD card filling up (no eMMC on this board) | `df -h` before recording; use `--lz4` compression; offload old `.bag` files to a USB drive |
| Playback flickers between live and recorded | Live driver nodes still publishing to the same topic | Kill live nodes first (Section 4.2) |
| `roscore` fails: `Address already in use` | A `rosmaster` is already running (likely autostarted at boot) | Check with `ps aux \| grep rosmaster` before starting a new one |
| `rosnode kill` has no effect | Node is managed by a launch file / supervisor and auto-restarts | Stop the parent `roslaunch` process instead |
| `extract_images` produces nothing | Bag isn't actively playing at the same time | Run `rosbag play` in a separate terminal *first*, then start extraction |

---

