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

---

## ROS Master

```bash
echo $ROS_MASTER_URI
```

Example:

```text
http://192.168.0.114:11311
```

---

## Connected USB Devices

```bash
lsusb
```

Useful for checking:

* Astra Camera
* USB Serial Devices
* Additional Peripherals

---

## Available ROS Packages

```bash
rospack list
```

Displays all installed ROS packages in the workspace.

