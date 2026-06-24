# Hardware Specifications

## System Information

| Item             | Expected Value     | Verification Command |
| ---------------- | ------------------ | -------------------- |
| Operating System | Ubuntu 18.04.6 LTS | `lsb_release -a`     |
| ROS Version      | Melodic            | `rosversion -d`      |
| Kernel Version   | 4.9.x-tegra        | `uname -r`           |
| Hostname         | jetauto-desktop    | `hostname`           |
| Username         | jetauto            | `whoami`             |
| Architecture     | aarch64            | `uname -m`           |

---

## Compute Module

| Item            | Expected Value     | Verification Command          |
| --------------- | ------------------ | ----------------------------- |
| Board           | NVIDIA Jetson Nano | `cat /proc/device-tree/model` |
| CPU Cores       | 4                  | `nproc`                       |
| CPU Information | Cortex-A57         | `lscpu`                       |
| RAM             | 4 GB               | `free -h`                     |
| GPU             | Maxwell GPU        | `tegrastats`                  |

---

## ROS Workspace

| Item          | Expected Value | Verification Command     |
| ------------- | -------------- | ------------------------ |
| Workspace     | jetauto_ws     | `echo $ROS_PACKAGE_PATH` |
| Source Folder | jetauto_ws/src | `ls ~/jetauto_ws/src`    |

---

## Quick System Summary

To display a quick overview of the system:

```bash
neofetch
```

Example information displayed:

* OS Version
* Kernel Version
* CPU
* Memory Usage
* Hostname
* Architecture
<img width="500" height="200" alt="{FB2C0276-7C35-4B46-8BB0-360B57E9A852}" src="https://github.com/user-attachments/assets/19779d6b-9bd8-4504-80fc-88c559ba4de0" />

---

## Network Information

```bash
hostname -I
```

Displays the robot IP address.

Example:

```text
192.168.0.114
```
<img width="485" height="110" alt="{84D6DC13-35C3-49A7-B32D-3A5905972F22}" src="https://github.com/user-attachments/assets/82074a02-1f26-4619-840b-34b820391715" />

---

## ROS Master

```bash
echo $ROS_MASTER_URI
```

Example:

```text
http://192.168.0.114:11311
```
<img width="574" height="91" alt="{3F90C176-2185-42B5-BBA5-A457C869EC5B}" src="https://github.com/user-attachments/assets/3798383f-5044-4364-9605-75dffbacc9de" />

---

## Connected USB Devices

```bash
lsusb
```

Useful for checking:

* Astra Camera
* USB Serial Devices
* Additional Peripherals

<img width="737" height="348" alt="{28EB027D-8A23-4D6A-B6C8-62D72DC30C3C}" src="https://github.com/user-attachments/assets/e9d601c5-cc71-43b1-bf15-eadc2f574052" />

---

## Available ROS Packages

```bash
rospack list
```

Displays all installed ROS packages in the workspace.
<img width="1140" height="804" alt="{04888900-312D-4D2F-8C33-805734AFB13D}" src="https://github.com/user-attachments/assets/2fa39fa4-cd46-4036-a7d1-af51e0305c51" />

