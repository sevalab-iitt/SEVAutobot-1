# Network Configuration & Remote Access

> How this JetAuto Pro unit is networked, how to connect to it, and how to verify each piece is working before you start debugging ROS nodes.

---

## Table of Contents

- [Network Identity — This Unit](#-network-identity--this-unit)
- [1. Checking the Robot's IP Address](#1-checking-the-robots-ip-address)
- [2. Checking Hostname](#2-checking-hostname)
- [3. Checking ROS_HOSTNAME and ROS_MASTER_URI](#3-checking-ros_hostname-and-ros_master_uri)
- [4. SSH Setup & Key Commands](#4-ssh-setup--key-commands)
- [5. NoMachine Setup & Key Commands](#5-nomachine-setup--key-commands)
- [6. Verifying the Robot Is Reachable](#6-verifying-the-robot-is-reachable)
- [7. Setting Up a Second Machine for RViz](#7-setting-up-a-second-machine-for-rviz)
- [8. Wi-Fi Card Check (M.2 Key E)](#8-wi-fi-card-check-m2-key-e)
- [Common Network Failures](#-common-network-failures)

---

## Network Identity — This Unit

| Item | Value |
|---|---|
| IP address | `192.168.0.114` |
| Hostname | `jetauto-desktop` |
| `ROS_MASTER_URI` | `http://192.168.0.114:11311` |
| `ROS_HOSTNAME` | `192.168.0.114` |
| System username | `jetauto` |
| Default SSH password | `hiwonder` *(unless changed)* |
| Network mode | Standalone — `roscore` runs locally, robot does not depend on any other machine |

---

## 1. Checking the Robot's IP Address

```bash
hostname -I
```

**Expected result:** A single IPv4 address printed, e.g. `192.168.0.114`.

**Confirms:** The robot has successfully obtained an IP address on the local network (via DHCP or static config).

**If it fails / prints nothing:**
- Check the Wi-Fi card is seated in the M.2 Key E slot (Section 8), or that an Ethernet cable is connected.
- Run `nmcli device status` to see if any interface shows `connected`.
- Check the router's DHCP client list to confirm the robot registered.

---

## 2. Checking Hostname

```bash
hostname
```

**Expected result:** `jetauto-desktop`
<img width="300" height="70" alt="{AB6403E7-8CDA-4102-8176-C26746457ACB}" src="https://github.com/user-attachments/assets/3945287a-8029-47c9-a5c7-dd6007fc16c2" />


**Confirms:** The system hostname matches what's expected by any hardcoded scripts, systemd services, or documentation.

**If it fails:** If a different hostname appears, either the factory image was re-flashed with different settings, or `/etc/hostname` was edited. Update your own scripts/docs to match the actual value rather than assuming `jetauto-desktop`.

---

## 3. Checking ROS_HOSTNAME and ROS_MASTER_URI

```bash
echo $ROS_HOSTNAME
echo $ROS_MASTER_URI
```

**Expected result:**
<img width="400" height="90" alt="{E714515B-A6DB-4544-B1F0-DDAFD439D9EA}" src="https://github.com/user-attachments/assets/8cbfbe41-86c1-4bbe-a90b-471da831fff9" />



**Confirms:** These environment variables (normally set in `~/.bashrc`) point ROS tools to the robot's own locally-running ROS Master — a standalone configuration where the robot doesn't depend on any external machine.

**If it fails / values are empty or different:**
- Check `~/.bashrc` for the lines exporting these variables — they may have been removed or point somewhere else.
- If you're inside an SSH session and see nothing, you may be in a shell that didn't source `.bashrc` — try `source ~/.bashrc` manually.

---

## 4. SSH Setup & Key Commands

**What it is:** SSH (Secure Shell) gives you a command-line session on the robot over the network, from your laptop, without needing a monitor/keyboard plugged into the Jetson itself. It's the fastest way to run and debug ROS commands on this robot.

### Checking SSH is installed and running (on the robot)

```bash
sudo systemctl status ssh
```

**Expected result:** `active (running)` in green.
<img width="900" height="400" alt="{D3E2518B-5A79-4110-B3D0-1D3B6344EEC5}" src="https://github.com/user-attachments/assets/0fa44b15-4a35-4207-b3f2-cc9a99f14812" />


**If not installed:**
```bash
sudo apt update
sudo apt install openssh-server -y
sudo systemctl enable ssh
sudo systemctl start ssh
```

### Connecting from your laptop

```bash
ssh jetauto@192.168.0.114
```
The ip address is first checked and accordingly put after @.
Enter the password when prompted (`hiwonder` by default).


**✅ Confirms:** You are now running commands directly on the robot, not on your laptop — this distinction matters for every subsequent chapter in this documentation.

**If it fails:**
- `Connection refused` / `No route to host` → robot isn't reachable at that IP; re-check Section 1.
- `Connection timed out` → laptop and robot are likely on different networks/subnets (e.g. laptop on 5 GHz guest Wi-Fi, robot on 2.4 GHz main network).
- Password rejected → password may have been changed from the factory default; check with whoever last configured the unit.

### Useful day-to-day SSH commands

| Command | What it does |
|---|---|
| `ssh jetauto@192.168.0.114` | Connect to the robot |
| `exit` | Close the SSH session, return to your laptop's shell |
| `ssh-keygen -t ed25519` | Generate an SSH key pair on your laptop (for passwordless login) |
| `ssh-copy-id jetauto@192.168.0.114` | Copy your public key to the robot so you don't need to type the password every time |
| `scp file.py jetauto@192.168.0.114:~/jetauto_ws/src/` | Copy a file from your laptop to the robot |
| `scp jetauto@192.168.0.114:~/map.pgm .` | Copy a file *from* the robot to your laptop |
| `ssh jetauto@192.168.0.114 "rostopic list"` | Run a single remote command without opening a full session |
| `sudo systemctl restart ssh` | Restart the SSH service on the robot (if connections start failing) |

**Tip:** Once `ssh-copy-id` is done, connecting no longer prompts for the `hiwonder` password — useful since you'll be typing `ssh jetauto@192.168.0.114` dozens of times a day while developing.

---

## 5. NoMachine Setup & Key Commands

**What it is:** NoMachine gives you the robot's **full graphical desktop** remotely — useful for RViz, the file manager, or anything that isn't comfortable purely from a terminal (e.g., visually inspecting a LIDAR scan or camera feed live).

### Checking NoMachine service status (on the robot)

```bash
sudo systemctl status nxserver
```

**Expected result:** Service listed as running, and it prints the NoMachine version.

<img width="900" height="500" alt="{B805D914-7F4C-4CD7-BAC8-3C746A2D4882}" src="https://github.com/user-attachments/assets/b62ff317-2ea2-4544-a990-4f112fe5f15d" />


### Starting / restarting the NoMachine server (on the robot)

```bash
sudo /etc/NX/nxserver --startup    # ensure it's set to start on boot
sudo /etc/NX/nxserver --restart    # restart the server if a connection is stuck
sudo /etc/NX/nxserver --status     # check current status
```

### Connecting from your laptop

**Download the NoMachine required for the laptop**

[NoMachine](https://drive.google.com/drive/folders/1rNafJCELxP4iADF-lW4vfBlmc6uI0JtW)

1. Open the **NoMachine client** app (not a terminal command — this is the GUI app installed on your laptop).
2. Enter `192.168.0.114` as the host. (keep the IP address of the robot at the time of using)
3. Log in with the `jetauto` username and password. Username is : jetauto, password is : hiwonder.

**Expected result:** The robot's Ubuntu desktop opens in a window, exactly as if you had a monitor plugged directly into the Jetson.

**Confirms:** Graphical tools (RViz, rqt_image_view) can be used without needing a second machine's ROS environment configured (see Section 7 for the alternative).

### Useful commands once inside a NoMachine session

| Command | What it does |
|---|---|
| `sudo /etc/NX/nxserver --restart` | Restart NoMachine if the session freezes |
| `sudo /etc/NX/nxserver --list` | List currently active NoMachine sessions |
| `sudo /etc/NX/nxserver --stop` | Stop the server (e.g., before rebooting) |
| `xrandr` | Check the virtual display resolution NoMachine is using |

**Tip:** RViz is much smoother run *directly* inside a NoMachine session on the robot than piped over `ROS_MASTER_URI` to your laptop (Section 7) — no network topic-streaming overhead, since it's rendering locally on the robot's own GPU.

**If NoMachine won't connect:**
- Confirm the robot is reachable at all first: `ping 192.168.0.114` from your laptop.
- Check the server is actually running: `sudo /etc/NX/nxserver --status`.
- Only one NoMachine session can usually be *active* (not just connected) at a time — if you were disconnected uncleanly, use `sudo /etc/NX/nxserver --restart` on the robot to clear a stuck session (you'll need SSH access to do this if the graphical client itself is unreachable).

---

## 6. Verifying the Robot Is Reachable

```bash
ping 192.168.0.114
```
*(Run this from your laptop, not the robot.)*

**Expected result:** Continuous replies with low latency (typically <5 ms on a local network).

**Confirms:** Basic network-layer connectivity exists between your laptop and the robot, independent of SSH or ROS.

**If it fails:** `Request timeout` / `Destination host unreachable` → laptop and robot are not on the same network/subnet, or the robot hasn't finished booting (allow 30–60 seconds after power-on).

---

## 7. Setting Up a Second Machine for RViz

To visualize topics (LIDAR scans, camera feeds) live on a laptop instead of the robot's own display:

**On your laptop's terminal:**
```bash
export ROS_MASTER_URI=http://192.168.0.114:11311
export ROS_HOSTNAME=<your laptop's own IP address>
rviz
```

**Expected result:** RViz opens on the laptop and can subscribe to topics like `/scan` or `/camera/rgb/image_raw` published by the robot.

**Confirms:** The laptop is correctly pointed at the robot's ROS Master rather than trying to run its own separate one.

**If it fails / topics don't appear:**
- Both machines must be on the **same local network** — this will not work across different Wi-Fi networks or over the internet without a VPN.
- Do **not** run `roscore` on the laptop — that creates a second, disconnected ROS system that has no way of seeing the robot's topics.
- Run `rostopic list` on the laptop first — if it's empty, the `ROS_MASTER_URI` value likely doesn't match the robot's exactly.

---

## 8. Wi-Fi Card Check (M.2 Key E)

```bash
lspci | grep -i network
```
or
```bash
nmcli device status
```

**Expected result:** A wireless network adapter listed (exact chip name varies by which M.2 card is installed).

**Confirms:** The Jetson Nano's M.2 Key E slot has a Wi-Fi card correctly seated and recognized by the OS — the Jetson Nano module itself has no built-in wireless networking, so this card is required for Wi-Fi.

**If it fails / nothing listed:** Card may be loose in the M.2 slot (power off before reseating), or missing entirely — fall back to a wired Ethernet connection via the Gigabit Ethernet port.

---

## Common Network Failures

| Symptom | Likely Cause | Fix |
|---|---|---|
| Can't SSH in | Robot not on same subnet | Check router's connected-devices list for the robot's actual IP |
| SSH works, but `rostopic list` is empty | `roscore` not running yet | Run `roscore` on the robot first (Chapter: ROS Basics) |
| RViz on laptop shows nothing | `ROS_MASTER_URI` mismatch | Re-export the exact URI on the laptop, `echo` to confirm |
| Robot's IP changed after reboot | DHCP reassigned a new address | Consider setting a static IP/DHCP reservation on your router |
| Wi-Fi drops intermittently | M.2 card loose or weak signal | Reseat card; move router closer for testing |
| NoMachine session frozen/stuck | Previous session disconnected uncleanly | SSH in and run `sudo /etc/NX/nxserver --restart` |

---

