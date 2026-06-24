# JetAuto Pro — Driver Documentation

> How to Find, Access & Document Every Driver
> **ROS Melodic** · Workspace: `~/jetauto_ws` · Ubuntu 18.04

## Table of Contents
1. [What is a Driver in ROS?](#1-what-is-a-driver-in-ros)
2. [Step 1 — SSH Into the Robot](#2-step-1--ssh-into-the-robot)
3. [Step 2 — Find All Packages](#3-step-2--find-all-packages-driver-containers)
4. [Step 3 — Find All Driver Python Files](#4-step-3--find-all-driver-python-files)
5. [Step 4 — Find Each Specific Driver Path](#5-step-4--find-each-specific-driver-path)
6. [Step 5 — Read Each Driver File](#6-step-5--read-each-driver-file)
7. [Step 6 — Find Hardware Device Ports](#7-step-6--find-hardware-device-ports)
8. [Step 7 — Run the Auto-Scanner Script](#8-step-7--run-the-auto-scanner-script)
9. [Step 8 — Copy Report to Your Laptop](#9-step-8--copy-report-to-your-laptop)
10. [Step 9 — Fill This Table With Your Findings](#10-step-9--fill-this-table-with-your-findings)
11. [Quick Command Reference](#11-quick-command-reference)

---

## 1. What is a Driver in ROS?

In ROS, a **driver** is a Python or C++ node that:

- Talks directly to a hardware device (camera, LiDAR, motors, servos)
- Reads sensor data and publishes it to a ROS topic
- Receives ROS commands and sends them to the hardware

Every driver lives as a `.py` or `.cpp` file inside a ROS package under `~/jetauto_ws/src/`.

---

## 2. Step 1 — SSH Into the Robot

```bash
# From your laptop
ssh jetauto@192.168.0.114        
  password: hiwonder

# Source the workspace immediately
source ~/jetauto_ws/devel/setup.bash
```

---

## 3. Step 2 — Find All Packages (Driver Containers)

```bash
# List all packages in the workspace
ls ~/jetauto_ws/src/

# List ONLY directory names (clean output)
find ~/jetauto_ws/src/ -maxdepth 1 -type d | sort

# Find every package.xml (one per package)
find ~/jetauto_ws/src/ -name "package.xml" \
  | sed 's|/package.xml||' \
  | sed 's|.*/||' \
  | sort
```

> ## Verification:
> <img width="928" height="283" alt="image" src="https://github.com/user-attachments/assets/526eb275-a5e7-4268-9721-fcb1415f17cd" />


---

## 4. Step 3 — Find All Driver Python Files

```bash
# ALL Python files — full paths
find ~/jetauto_ws/src/ -name "*.py" | sort

# Count total
find ~/jetauto_ws/src/ -name "*.py" | wc -l

# ALL launch files ( it show how drivers are started)
find ~/jetauto_ws/src/ -name "*.launch" | sort
```
 ## Verification:
 <img width="607" height="230" alt="image" src="https://github.com/user-attachments/assets/024c17e8-530f-4f24-a06d-e1f17f0246e7" />

 <img width="624" height="137" alt="image" src="https://github.com/user-attachments/assets/1bfdab74-18c8-489d-b2f9-6b2161d3eaa2" />

 

---

## 5. Step 4 — Find Each Specific Driver Path

Run each command to find the exact file path of each driver:

### Camera Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "image_raw\|usb_cam\|VideoCapture" 2>/dev/null
```
## Verification:
<img width="656" height="176" alt="image" src="https://github.com/user-attachments/assets/618b106e-3589-479c-afd1-3cb17a1bfcb1" />

### LiDAR Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "LaserScan\|/scan\|ydlidar" 2>/dev/null
```

### Motor / Chassis Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "cmd_vel\|Twist\|motor" 2>/dev/null
```

### Servo / Arm Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "servo\|HTD\|bus_servo\|MultiRawIdPosDur" 2>/dev/null
```

### IMU Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "Imu\|imu\|accelerometer" 2>/dev/null
```

### Depth Camera Driver
```bash
find ~/jetauto_ws/src/ -name "*.py" \
  | xargs grep -l "depth\|PointCloud\|astra\|openni" 2>/dev/null
```

---

## 6. Step 5 — Read Each Driver File

Once you have the path from Step 4, read it:

```bash
# Read full file
cat ~/jetauto_ws/src/PACKAGE_NAME/scripts/DRIVER_FILE.py

# Read with line numbers
cat -n ~/jetauto_ws/src/PACKAGE_NAME/scripts/DRIVER_FILE.py

# Read only first 50 lines (see imports + node init)
head -50 ~/jetauto_ws/src/PACKAGE_NAME/scripts/DRIVER_FILE.py

# Search for subscriber/publisher lines inside the file
grep -n "Subscriber\|Publisher\|rospy.init" \
  ~/jetauto_ws/src/PACKAGE_NAME/scripts/DRIVER_FILE.py
```

> **Note — What to look for inside each driver**
>
> | Pattern | Meaning |
> |---|---|
> | `rospy.init_node(...)` | Node name |
> | `rospy.Subscriber(...)` | Topics it reads from |
> | `rospy.Publisher(...)` | Topics it publishes to |
> | `rospy.Rate(...)` | Publishing frequency |
> | `/dev/ttyUSB*` | Hardware port it uses |

---

## 7. Step 6 — Find Hardware Device Ports

```bash
# All connected USB serial ports
ls /dev/ttyUSB*
ls /dev/ttyACM*

# All cameras
ls /dev/video*

# See what is on each port (vendor/product ID)
dmesg | grep tty  | tail -20
dmesg | grep usb  | tail -20
dmesg | grep video| tail -10

# Detailed USB device list
lsusb

# Match port to device automatically
for port in /dev/ttyUSB*; do
  echo "Port: $port"
  udevadm info -a -n $port | grep -E "idVendor|idProduct|product" | head -4
  echo "---"
done
```

---

## 8. Step 7 — Run the Auto-Scanner Script

Save and run this script — it maps all drivers automatically:

```bash
nano ~/jetauto_ws/src/scan_drivers.py
```

Paste:

```python
#!/usr/bin/env python3
"""scan_drivers.py — Auto-documents all ROS drivers in jetauto_ws"""
import os, re

WS = os.path.expanduser("~/jetauto_ws/src")

SUB = r'rospy\.Subscriber\s*\(\s*["\']([^"\']+)["\']'
PUB = r'rospy\.Publisher\s*\(\s*["\']([^"\']+)["\']'
NOD = r'rospy\.init_node\s*\(\s*["\']([^"\']+)["\']'
RAT = r'rospy\.Rate\s*\(\s*([0-9.]+)\s*\)'
DEV = r'(/dev/tty\w+|/dev/video\w+)'

results = []
for root, dirs, files in os.walk(WS):
    dirs[:] = [d for d in dirs if d not in
               ('build','devel','__pycache__','.git')]
    for f in files:
        if not f.endswith('.py'): continue
        path = os.path.join(root, f)
        try:
            txt = open(path, errors='ignore').read()
        except: continue
        n = re.search(NOD, txt)
        if not n: continue
        results.append({
            'file':  os.path.relpath(path, WS),
            'node':  n.group(1),
            'subs':  list(dict.fromkeys(re.findall(SUB, txt))),
            'pubs':  list(dict.fromkeys(re.findall(PUB, txt))),
            'rates': list(dict.fromkeys(re.findall(RAT, txt))),
            'devs':  list(dict.fromkeys(re.findall(DEV, txt))),
        })

print("\n" + "="*65)
print("  JETAUTO DRIVER SCAN REPORT")
print("="*65)
for r in results:
    print(f"\nFILE  : {r['file']}")
    print(f"NODE  : {r['node']}")
    print(f"SUBS  : {r['subs']  or 'none'}")
    print(f"PUBS  : {r['pubs']  or 'none'}")
    print(f"RATE  : {r['rates'] or 'event-driven'} Hz")
    print(f"DEVICE: {r['devs']  or 'no /dev port'}")
    print("-"*65)

# Save to file
with open(os.path.expanduser("~/driver_report.txt"), "w") as f:
    for r in results:
        f.write(f"FILE  : {r['file']}\n")
        f.write(f"NODE  : {r['node']}\n")
        f.write(f"SUBS  : {r['subs']}\n")
        f.write(f"PUBS  : {r['pubs']}\n")
        f.write(f"RATE  : {r['rates']} Hz\n")
        f.write(f"DEVICE: {r['devs']}\n\n")
print("\nSaved to ~/driver_report.txt")
```

Run it:

```bash
python3 ~/jetauto_ws/src/scan_drivers.py

# View the saved report
cat ~/driver_report.txt
```

---

## 9. Step 8 — Copy Report to Your Laptop

```bash
# Run this on YOUR LAPTOP (not robot)
scp jetauto@192.168.1.xxx:~/driver_report.txt ./

# Now open driver_report.txt on your laptop
# Copy the content into your documentation
```

---

## 10. Step 9 — Fill This Table With Your Findings

After running Steps 4–7, fill in the actual paths from your robot:

| Driver | File Path |
|---|---|
| Camera | `jetauto_ws/src/______/scripts/_____.py` |
| LiDAR | `jetauto_ws/src/______/scripts/_____.py` |
| Motor Control | `jetauto_ws/src/______/scripts/_____.py` |
| Servo / Arm | `jetauto_ws/src/______/scripts/_____.py` |
| IMU | `jetauto_ws/src/______/scripts/_____.py` |
| Depth Camera | `jetauto_ws/src/______/scripts/_____.py` |

---

## 11. Quick Command Reference

| Goal | Command |
|---|---|
| List all packages | `ls ~/jetauto_ws/src/` |
| Find all .py files | `find ~/jetauto_ws/src/ -name "*.py" \| sort` |
| Find camera driver | `grep -rl "image_raw" ~/jetauto_ws/src/` |
| Find LiDAR driver | `grep -rl "LaserScan" ~/jetauto_ws/src/` |
| Find motor driver | `grep -rl "cmd_vel" ~/jetauto_ws/src/` |
| Find servo driver | `grep -rl "servo" ~/jetauto_ws/src/` |
| Read a driver file | `cat -n PATH/driver.py` |
| Find USB ports | `ls /dev/ttyUSB* /dev/video*` |
| Run auto-scanner | `python3 ~/jetauto_ws/src/scan_drivers.py` |
| Copy report to laptop | `scp jetauto@IP:~/driver_report.txt ./` |

> ⚠️ **Warning — Before running any command**
> Always run `source ~/jetauto_ws/devel/setup.bash` in every new terminal, otherwise ROS commands will not be found.
