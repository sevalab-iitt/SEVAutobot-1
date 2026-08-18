# Wi-Fi Configuration (Verified for This Unit)

> This robot's Wi-Fi card is controlled by **Hiwonder's own `hw_wifi` toolbox**. Hiwonder's own service (`hw_wifi.service`) handles switching the card between Access Point and Station modes. 

---

## 📑 Table of Contents

- [How This Robot's Wi-Fi Actually Works](#-how-this-robots-wi-fi-actually-works)
- [1. Checking Current Wi-Fi Status](#1-checking-current-wi-fi-status)
- [2. Confirming the Card's Current Mode](#2-confirming-the-cards-current-mode)
- [3. Locating the Wi-Fi Toolbox](#3-locating-the-wi-fi-toolbox)
- [4. Understanding the Config File](#4-understanding-the-config-file)
- [5. Switching to Station (Client) Mode](#5-switching-to-station-client-mode)
- [6. Applying the Change](#6-applying-the-change)
- [Issues Hit During This Session](#-issues-hit-during-this-session)

---

## How This Robot's Wi-Fi Actually Works

The card supports two mutually-exclusive modes, controlled entirely by one config file:

| Mode | Value | What it does |
|---|---|---|
| **AP (Access Point)** | `HW_WIFI_MODE = 1` | Robot broadcasts its **own** Wi-Fi hotspot (e.g. `HW-Robot1`) for a phone/laptop to connect directly to — this is what the WonderAi mobile app relies on for control |
| **STA (Station / client)** | `HW_WIFI_MODE = 2` | Robot connects **to** an existing Wi-Fi network (your router), like a normal device — this is what's needed for SSH, `ROS_MASTER_URI` on your LAN, and everything documented in the Network Configuration chapter |

**Important for later:** The AP-mode SSID **must start with `HW-`** 

---

## 1. Checking Current Wi-Fi Status

```bash
nmcli device
```

**What you saw:**
<img width="400" height="200" alt="{34A0D428-F008-4842-A065-B536E93DE185}" src="https://github.com/user-attachments/assets/8d88fbf1-12f6-4af1-bc38-b37c98d6b154" />


**Confirms:** `wlan0` exists and the driver is loaded, but NetworkManager has no control over it — the `unmanaged` state is the tell. Anything you try via `nmcli device wifi connect` on this specific device will silently do nothing useful.

---

## 2. Confirming the Card's Current Mode

```bash
nmcli device wifi list
```
**Result:** 
<img width="400" height="65" alt="{16C4BC4C-EE7E-4ECD-A04B-928E8F899342}" src="https://github.com/user-attachments/assets/0e896a41-8e9f-4c41-8941-31d62b962798" />

Empty — no networks listed. This alone looks like a broken scan, but the real reason shows up in the next command.

```bash
iwconfig
```
**Relevant output:**
<img width="600" height="400" alt="{EEDDA488-7720-4BB7-B621-8637025D881B}" src="https://github.com/user-attachments/assets/b949aef2-71e4-4e44-8ec8-11c8b53a0734" />


---

## 3. Locating the Wi-Fi Toolbox

```bash
cd ~/hiwonder-toolbox
ls
```

**Result:**
<img width="700" height="100" alt="{5A1B8F1E-F3E0-4085-8A6F-1D85464E61FA}" src="https://github.com/user-attachments/assets/a5b7438a-f492-4640-b3f3-9ca34e0ddf0b" />


**Confirms:** `hiwonder_wifi_conf.py` is the config file, `hw_wifi.py` is the script that reads it and actually configures the radio, and `hw_wifi.service` is the systemd unit that runs it — restarting that service is how a config change takes effect without a full reboot.

---

## 4. Understanding the Config File

```bash
sudo nano hiwonder_wifi_conf.py
```

**Contents (as found on this unit):**
```python
#!/usr/bin/python3
#coding:utf8

HW_WIFI_MODE = 1                    # wifi's working mode: 1 = AP mode, 2 = STA mode
HW_WIFI_AP_SSID = 'HW-Robot1'       # AP mode SSID — must start with "HW-", or the app can't find it
HW_WIFI_AP_PASSWORD = 'hiwonder'    # AP mode Wi-Fi password
HW_WIFI_STA_SSID = 'Hiwonder'       # STA mode — SSID of the network to connect to
HW_WIFI_STA_PASSWORD = 'hiwonder'   # STA mode — password of that network
```

| Field | Purpose |
|---|---|
| `HW_WIFI_MODE` | `1` = AP (robot is the hotspot), `2` = STA (robot joins your network) |
| `HW_WIFI_AP_SSID` / `HW_WIFI_AP_PASSWORD` | Only used when `HW_WIFI_MODE = 1` |
| `HW_WIFI_STA_SSID` / `HW_WIFI_STA_PASSWORD` | Only used when `HW_WIFI_MODE = 2` — set these to your actual router's network |

---

## 5. Switching to Station (Client) Mode

Edit the four relevant lines:

```python
HW_WIFI_MODE = 2
HW_WIFI_STA_SSID = 'YOUR_ROUTER_SSID'
HW_WIFI_STA_PASSWORD = 'YOUR_ROUTER_PASSWORD'
```
**Result**

<img width="700" height="250" alt="{198CB9D6-FB89-4F74-8E59-24135A35315D}" src="https://github.com/user-attachments/assets/5b67b55a-2c20-4bc4-b414-da89f22b89a4" />


Save with `Ctrl+O`, `Enter`, then exit with `Ctrl+X` (standard `nano` save/exit).

**Verify the save worked:**
```bash
cat ~/hiwonder-toolbox/hiwonder_wifi_conf.py
```
**Result**

<img width="700" height="230" alt="{029C1EFE-5D88-4D4D-BE88-6771C95FCE6A}" src="https://github.com/user-attachments/assets/59442133-4954-49c5-a6d2-df482232563d" />


Confirm `HW_WIFI_MODE = 2` and the correct SSID/password are actually written to disk before moving on — don't assume the edit saved correctly.

---

## 6. Applying the Change

```bash
sudo systemctl restart hw_wifi.service
```
It will restart the wifi service.

---


## Issues Hit During This Session

| Symptom | What it means | Fix |
|---|---|---|
| `nmcli device wifi connect` does nothing | `wlan0` is `unmanaged` by NetworkManager on this robot | Use the `hiwonder_wifi_conf.py` + `hw_wifi.service` method above instead |
| `nmcli device wifi list` returns empty | Card is in AP (`Mode:Master`), not scanning as a client | Confirmed via `iwconfig`; switch to STA mode via the config file |
| `sudo: systemctl: command not found` | Terminal line-wrap / mistyped command, not a real missing binary | Retype the command cleanly |
| IP still shows `192.168.149.x` after restart | Radio hasn't fully re-associated with the new network yet | `sudo reboot`, then re-check IP |
| `roscore`/`rosmaster` fails with `Address already in use` (Errno 98) | A `rosmaster` process is **already running** (confirmed via `ps aux \| grep rosmaster`) — likely auto-started at boot | Don't run `roscore` manually if one's already up; check first with `ps aux \| grep rosmaster`, and if you do need to restart it, kill the existing process first: `kill <PID>` |

---

