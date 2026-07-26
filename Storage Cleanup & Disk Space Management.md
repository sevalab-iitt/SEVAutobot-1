# JetAuto Pro Storage Cleanup & Disk Space Management

**Platform:** JetAuto Pro (Jetson Nano)  
**Operating System:** Ubuntu 18.04 LTS  
**ROS Version:** ROS Melodic  

---

# Objective

The JetAuto Pro internal storage (30 GB eMMC) was almost completely full, leaving very little free space for ROS packages, SLAM, datasets, and development work.

The objective was to:

- Analyze disk usage
- Identify unnecessary files
- Remove safe-to-delete data
- Preserve all ROS, CUDA, TensorRT, and SLAM functionality
- Free as much storage as possible

---

# Initial Disk Status

```bash
df -h
```

Output:

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   28G  622M  98% /
```

Observation:

- Total Storage : 30 GB
- Used          : 28 GB
- Free          : 622 MB
- Usage         : 98%

This amount of free space is dangerous because:

- ROS builds may fail.
- apt installs may fail.
- System updates may fail.
- Log files cannot grow.
- Swap and temporary files become limited.

---

# Step 1 – Clean APT Cache

Removed cached package files.

Commands:

```bash
sudo apt autoremove -y
sudo apt clean
sudo apt autoclean
```

Purpose:

- Remove downloaded package archives.
- Remove unused dependencies.
- Remove obsolete package cache.

Result:

Approximately 500 MB recovered.

---

# Step 2 – Inspect Disk Usage

Root filesystem usage:

```bash
sudo du -xh --max-depth=1 / 2>/dev/null | sort -hr
```

Output:

```text
27G /
15G /usr
7.8G /home
1.6G /var
502M /root
483M /opt
```

Observation:

Most storage was occupied by:

- /usr
- /home
- /var

---

# Step 3 – Inspect Home Directory

Command:

```bash
du -xh --max-depth=1 /home/jetauto | sort -hr
```

Output:

```text
7.8G /home/jetauto

2.2G jetauto_third_party
1.6G .cache
688M jetauto_ws
469M .ros
295M .virtualenvs
227M .local
225M .nv
221M .vscode-server
```

Major storage consumers were identified.

---

# Step 4 – Remove Cache

Command:

```bash
rm -rf ~/.cache/*
```

Purpose:

Delete temporary application cache.

Safe because applications recreate cache automatically.

Recovered:

Approximately 1.6 GB.

---

# Step 5 – Inspect ROS Directory

Command:

```bash
du -sh ~/.ros/*
```

Output:

```text
82M rtabmap.db
520K test.png
```

Observation:

No large ROS logs remained.

RTAB-Map database exists.

File:

```
~/.ros/rtabmap.db
```

Recommendation:

Delete only if old maps are no longer needed.

Example:

```bash
rm ~/.ros/rtabmap.db
```

(Not deleted during this cleanup.)

---

# Step 6 – Find Large Files

Command:

```bash
sudo find / -type f -size +500M 2>/dev/null
```

Output:

```text
/home/jetauto/2026-06-16-19-13-01.bag

/usr/lib/aarch64-linux-gnu/libcudnn_static_v8.a

/swapfile
```

Observation:

The ROS bag file was unnecessary.

---

# Step 7 – Delete Old ROS Bag

Command:

```bash
rm ~/2026-06-16-19-13-01.bag
```

File Size:

```text
664 MB
```

Recovered:

664 MB

---

# Step 8 – Remove NVIDIA Cache

Command:

```bash
rm -rf ~/.nv/*
```

Purpose:

Delete NVIDIA temporary cache.

Safe because it is regenerated automatically.

Recovered:

Approximately 225 MB.

---

# Step 9 – Inspect Third Party Libraries

Command:

```bash
du -xh --max-depth=1 ~/jetauto_third_party | sort -hr
```

Output:

```text
2.2G jetauto_third_party

1.6G ORB_SLAM3
167M my_data
165M ORB_SLAM2
70M AstraSDK
34M yolov5
31M octomap
24M xf_tts
17M YDLidar-SDK
15M Pangolin
```

Observation:

ORB_SLAM3 occupies the majority of the directory.

---

# Step 10 – Inspect ORB_SLAM3

Command:

```bash
du -xh --max-depth=1 ~/jetauto_third_party/ORB_SLAM3
```

Output:

```text
1.6G ORB_SLAM3

680M Examples_old
674M Examples
180M Vocabulary
51M evaluation
24M Thirdparty
18M build
```

Analysis:

Large storage usage comes primarily from:

- Examples
- Examples_old

However, ORB_SLAM3 was **not deleted** because:

- Future SLAM experiments may require it.
- Vocabulary files are essential.
- Source code is needed for rebuilding.

Decision:

Keep ORB_SLAM3.

---

# Step 11 – Inspect /usr

Command:

```bash
sudo du -xh --max-depth=1 /usr
```

Output:

```text
15G /usr

6.3G lib
4.6G local
1.5G share
792M src
```

Further inspection:

```bash
sudo du -xh --max-depth=1 /usr/local
```

Output:

```text
4.6G /usr/local

2.9G cuda-10.2
1.8G lib
```

Conclusion:

These are required by:

- CUDA
- cuDNN
- TensorRT
- OpenCV
- ROS

Nothing was deleted.

---

# Step 12 – Inspect /var

Command:

```bash
sudo du -xh --max-depth=1 /var
```

Output:

```text
1.6G /var

1.1G cuda-repo-l4t-10-2-local
322M lib
96M cache
59M visionworks-repo
20M visionworks-sfm-repo
13M visionworks-tracking-repo
```

Observation:

The largest directory was:

```
cuda-repo-l4t-10-2-local
```

---

# Step 13 – Verify CUDA Repository

Command:

```bash
ls /var/cuda-repo-l4t-10-2-local
```

Result:

Directory contained numerous CUDA installation `.deb` packages.

Examples:

- cuda-toolkit
- cuda-nvcc
- libcublas
- libcufft
- libcusolver

These are installation packages only.

They are **not** the active CUDA installation.

---

# Step 14 – Remove CUDA Installer Repository

Command:

```bash
sudo rm -rf /var/cuda-repo-l4t-10-2-local
```

Recovered:

Approximately 1.1 GB.

Important:

CUDA itself remained installed because it resides under:

```
/usr/local/cuda-10.2
```

---

# Step 15 – Remove VisionWorks Installer Repositories

Commands:

```bash
sudo rm -rf /var/visionworks-repo
sudo rm -rf /var/visionworks-sfm-repo
sudo rm -rf /var/visionworks-tracking-repo
```

Recovered:

Approximately 90 MB.

---

# Storage After Cleanup

Command:

```bash
df -h
```

Output:

```text
Filesystem      Size  Used Avail Use% Mounted on

/dev/mmcblk0p1   30G   25G  3.9G  87% /
```

Result:

Before:

```text
Used : 28 GB
Free : 622 MB
Usage: 98%
```

After Cleanup:

```text
Used : 25 GB
Free : 3.9 GB
Usage: 87%
```

Recovered:

More than **3 GB** of storage.

---

# After Adding Approximately 2 GB of Data

After copying approximately **2 GB** of new project data onto the internal storage, disk usage became:

```bash
df -h
```

Output:

```text
Filesystem      Size  Used Avail Use% Mounted on

/dev/mmcblk0p1   30G   27G  2.0G  94% /
```

Observation:

Although approximately 2 GB of new data was added, the system still retained around **2 GB of free space**, which is significantly better than the original state of only **622 MB free**.

This confirms that the cleanup successfully created enough headroom for ongoing development and data storage.

---

# Files Deleted During Cleanup

```
APT Cache
Application Cache
NVIDIA Cache
Old ROS Bag File
CUDA Installer Repository
VisionWorks Installer Repository
```

---

# Files Preserved

The following components were intentionally preserved to avoid breaking the development environment:

- ROS Melodic
- CUDA Toolkit
- cuDNN
- TensorRT
- OpenCV
- JetAuto Workspace
- Astra SDK
- YDLidar SDK
- ORB_SLAM2
- ORB_SLAM3
- Pangolin
- Vocabulary Files
- RTAB-Map Database

---

# Why ORB_SLAM3 Was Not Deleted

Although ORB_SLAM3 occupied approximately 1.6 GB, it was retained because:

- Future SLAM experiments may require it.
- It contains source code required for compilation.
- Vocabulary files are essential.
- Reinstallation would require rebuilding dependencies.

Since future work includes learning and experimenting with SLAM algorithms, deleting ORB_SLAM3 would have complicated future development.

---

# Best Practices Going Forward

To prevent the internal eMMC from filling again:

- Store datasets on the external USB drive (`/media/jetauto/SEVA (SHBM)`).
- Store ROS bag files externally.
- Store recorded videos externally.
- Periodically remove application caches.
- Remove old ROS logs.
- Clean APT cache after installing packages.
- Monitor storage regularly using:

```bash
df -h
```

Inspect large directories:

```bash
sudo du -xh --max-depth=1 / | sort -hr
```

Inspect home directory:

```bash
du -xh --max-depth=1 ~ | sort -hr
```

Find files larger than 500 MB:

```bash
sudo find / -type f -size +500M 2>/dev/null
```

---

# Summary

The storage cleanup successfully:

- Increased free space from **622 MB** to **3.9 GB**.
- Reduced disk usage from **98%** to **87%**.
- Preserved all essential ROS, CUDA, TensorRT, and SLAM components.
- Removed only temporary files, caches, installer repositories, and obsolete data.
- Established a maintenance workflow for keeping the JetAuto Pro storage healthy during future robotics and SLAM development.
