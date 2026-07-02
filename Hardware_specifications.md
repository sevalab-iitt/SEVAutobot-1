# 🔧 Hardware Specifications

> Complete hardware reference for the **Hiwonder JetAuto Pro** — compute module, sensors, chassis, arm, and power system. Use this page to look up exact specs before writing or debugging code for any subsystem.

---

## 📑 Table of Contents

- [System Identity](#-system-identity)
- [1. Compute Module — NVIDIA Jetson Nano](#1-compute-module--nvidia-jetson-nano)
- [2. LIDAR — A1 vs G4](#2-lidar--a1-vs-g4)
  - [2.1 SLAMTEC RPLiDAR A1](#21-slamtec-rplidar-a1)
  - [2.2 EAI / YDLiDAR G4](#22-eai--ydlidar-g4)
  - [2.3 A1 vs G4 — Quick Comparison](#23-a1-vs-g4--quick-comparison)
- [3. Depth Camera — Orbbec Astra Pro Plus](#3-depth-camera--orbbec-astra-pro-plus)
- [4. Chassis & Drive System](#4-chassis--drive-system)
- [5. Robotic Arm](#5-robotic-arm)
- [6. Control Electronics — Expansion Board](#6-control-electronics--expansion-board)
- [7. Power System](#7-power-system)
- [📋 Quick-Reference Summary Table](#-quick-reference-summary-table)

---

## 🆔 System Identity

| Item | Value |
|---|---|
| Robot platform | JetAuto Pro (mecanum-wheel chassis + 6DOF arm) |
| Controller board | NVIDIA Jetson Nano Developer Kit |
| Operating system | Ubuntu 18.04.6 LTS, aarch64 |
| ROS version | ROS1 Melodic Morenia |
| System username | `jetauto` |
| Home directory | `/home/jetauto` |
| ROS workspace | `~/jetauto_ws` ⚠️ *(not `catkin_ws`, despite what generic tutorials assume)* |
| Hostname | `jetauto-desktop` |
| Robot IP address | `192.168.0.114` |
| `ROS_MASTER_URI` | `http://192.168.0.114:11311` |

> ⚠️ **Note:** This is a Jetson Nano (ROS1) build. If your unit is actually the **Jetson Orin Nano running ROS2**, the compute specs and low-level interfaces below will differ — confirm with `uname -a` and `rosversion -d` first.

---

## 1. Compute Module — NVIDIA Jetson Nano

| Component | Specification |
|---|---|
| SoC | NVIDIA Tegra X1 (model T210) |
| CPU | Quad-core ARM Cortex-A57 @ up to 1.43 GHz |
| GPU | 128-core NVIDIA Maxwell architecture |
| GPU compute throughput | 472 GFLOPS (FP16), peak theoretical |
| System memory | 4 GB 64-bit LPDDR4, 25.6 GB/s bandwidth (shared CPU/GPU) |
| Storage | microSD card slot — **no onboard eMMC** |
| Video encode | 4K@30fps, or 4× 1080p30, or 9× 720p30 (H.264/H.265) |
| Video decode | 4K@60fps, or 2× 4K30, or 8× 1080p30 (H.264/H.265) |
| Camera interface | 2-lane MIPI CSI-2 *(unused — the Astra Pro Plus connects via USB instead)* |
| Display output | HDMI 2.0, eDP 1.4 |
| USB | 4× USB 3.0 Type-A, 1× USB 2.0 Micro-B (power/device mode) |
| Networking | Gigabit Ethernet; M.2 Key E slot for optional Wi-Fi card |
| Low-level I/O | 40-pin header — GPIO, I2C, I2S, SPI, UART |
| Carrier board size | 100 mm × 80 mm × 29 mm |

**💡 Why it matters:** With only 128 CUDA cores and 4 GB shared RAM, this board favors lightweight detection models (MobileNet-SSD, YOLOv3/v4-tiny) converted with **TensorRT** rather than large, unoptimized networks.

---

## 2. LIDAR — A1 vs G4

JetAuto Pro ships with **one of two interchangeable LIDAR units** — check which one is physically fitted on your unit before trusting topic-level assumptions.

### 2.1 SLAMTEC RPLiDAR A1

| Parameter | Specification |
|---|---|
| Ranging principle | Laser triangulation |
| Laser safety | Infrared, Class 1 (<5 mW) |
| Distance range | 0.15 m – 12 m |
| Angular range | 360° |
| Sample rate | ~8,000 readings/second |
| Scan rate | 5.5 Hz typical (adjustable 1–10 Hz) |
| Angular resolution | ≤1° (~1,450 points/rotation) |
| Distance resolution | <0.5 mm |
| Communication | 3.3 V TTL UART → USB (via onboard adapter) |
| Power supply | 5 V |
| Dimensions / weight | ~98.5 × 70 × 60 mm, ~170 g |

**ROS integration:** Package `rplidar_ros` → topic `/scan` → message type `sensor_msgs/LaserScan`.

**⚠️ Caveat:** Degrades on highly reflective, transparent, or very dark matte surfaces; can saturate in strong direct sunlight.

### 2.2 EAI / YDLiDAR G4

| Parameter | Specification |
|---|---|
| Ranging principle | Laser triangulation |
| Laser safety | Infrared, FDA Class I eye-safe |
| Laser wavelength | ~792 nm |
| Laser power | ~3.5 mW average (6 mW max) |
| Distance range | 0.12 m – 16 m *(actual max depends on reflectivity and configured ranging frequency — 16 m is rated at 80% reflectivity)* |
| Angular range | 360° |
| Ranging frequency | Up to 9,000 Hz |
| Motor / scan rate | 5–12 Hz (default 7 Hz), software-adjustable |
| Angular resolution | ~0.2°–0.48° depending on motor speed |
| Systematic error | ~2 cm (range ≤1 m); ~2.0% relative error (1–8 m) |
| Communication | 3.3 V UART, 230,400 bps, via PH2.0-5P connector |
| Power supply | 5 V (4.8–5.2 V), ~350–500 mA working current |
| Weight | ~214 g |
| Operating temperature | 0 °C – 50 °C |

**ROS integration:** Typically driven by the `ydlidar_ros` / `ydlidar_ros2_driver` package → topic `/scan` → `sensor_msgs/LaserScan` (same message type as the A1, so downstream nodes don't need to change).

**⚠️ Caveat:** Longer range and higher sample rate than the A1, but also higher startup current draw (~1 A) — worth accounting for in power budgeting if running alongside a GPU-heavy detection node.

### 2.3 A1 vs G4 — Quick Comparison

| Spec | RPLiDAR A1 | YDLiDAR G4 |
|---|---|---|
| Max range | 12 m | 16 m |
| Sample rate | 8,000 Hz | 9,000 Hz |
| Scan rate | 5.5–10 Hz | 5–12 Hz |
| Weight | ~170 g | ~214 g |
| Interface | UART → USB adapter | UART (PH2.0-5P) |
| Typical use case | Lower-cost, compact indoor SLAM | Longer-range, slightly higher-precision mapping |

---

## 3. Depth Camera — Orbbec Astra Pro Plus

| Parameter | Specification |
|---|---|
| Sensing technology | Structured IR light (~850 nm, ~40,000-dot pattern) |
| Depth resolution | 640×480 (VGA) @ up to 30 fps |
| Depth range | 0.6 m – 8 m |
| Depth field of view | 58.4° (H) × 45.5° (V) |
| Depth precision | ±1–3 mm at 1 m |
| RGB resolution | Up to 1280×960 @ 30 fps (some variants: 1920×1080) |
| RGB field of view | 66.1° (H) × 40.2° (V) |
| Interface | USB 2.0 Type-A (single cable, power + data) |
| Power consumption | <2.4 W average, USB-powered |
| Software support | Astra SDK, OpenNI2; RGB stream is UVC-compliant |
| OS support | Windows, Linux, macOS, Android |
| Operating environment | 10–40 °C, 10–85% RH (indoor use) |

**ROS integration:** Package `astra_camera` → `/camera/rgb/image_raw`, `/camera/depth/image_raw`, `/camera/depth_registered/points`.

**💡 Practical constraints:**
- Running RGB (1280×960) + depth (640×480) simultaneously at 30 fps approaches the **USB 2.0 480 Mbps ceiling**.
- RGB and depth sensors have different fields of view — needs calibration-based alignment, not naive pixel matching.
- Objects **closer than 0.6 m** won't produce reliable depth data.

---

## 4. Chassis & Drive System

| Parameter | Specification |
|---|---|
| Wheel configuration | 4× independently-driven mecanum wheels |
| Drive motors | DC geared motors with magnetic encoders |
| Suspension | Pendulum-style, keeps all wheels evenly loaded |
| Motion modes | Forward/backward, strafe, diagonal, in-place rotation, and combinations |

**💡 Why mecanum wheels matter:** True omnidirectional motion — the robot can strafe sideways without turning — but this requires mecanum-specific inverse kinematics rather than simple left/right wheel-speed math.

---

## 5. Robotic Arm

| Parameter | Specification |
|---|---|
| Degrees of freedom | 6 DOF |
| End-effector | Gripper with its own dedicated close-range camera |
| Control | Serial bus servos, each with its own addressable ID |

**💡 Why 6 DOF matters:** 3 DOF position the gripper anywhere in 3D space; the other 3 DOF orient it at any angle — together they let the arm approach an object from an arbitrary angle, not just straight-on.

---

## 6. Control Electronics — Expansion Board

| Feature | Specification |
|---|---|
| Built-in IMU | Yes — orientation & angular velocity for odometry |
| Motor output | PWM (pulse-width modulation) for drive motors |
| Servo bus | 9-channel serial bus for arm servos |
| GPIO ports | 2 |
| I2C interfaces | 2 |
| Extras | 2 physical buttons, 1 LED, 1 buzzer |
| Link to Jetson | Simple serial connection (wrapped into ROS messages/services by a driver node) |

**💡 Why two controllers:** Linux on the Jetson can't guarantee microsecond-level timing (its scheduler can always be interrupted). A dedicated microcontroller running nothing else can — critical for smooth motor PWM and accurate encoder counting.

---

## 7. Power System

| Parameter | Specification |
|---|---|
| Battery | 11.1 V, 6000 mAh Li-ion/Li-Po (3-cell), built into chassis |
| Capacity | ≈66.6 Wh (11.1 V × 6 Ah) |
| Distribution | Regulator stage → steady 5 V to Jetson (via barrel jack); motors/servo bus powered separately at their own voltages |

**⚠️ Caution:** Sustained GPU-heavy workloads (e.g., continuous object detection) draw more current, shortening runtime and raising chip temperature. Monitor with `tegrastats` during long test sessions.

---

## 📋 Quick-Reference Summary Table

| Subsystem | Key Specification |
|---|---|
| **Compute SoC** | Tegra X1: quad-core Cortex-A57 @ 1.43 GHz + 128-core Maxwell GPU (472 GFLOPS FP16) |
| **Memory** | 4 GB LPDDR4, 25.6 GB/s, shared CPU/GPU |
| **Storage** | microSD card (no onboard eMMC) |
| **OS / Kernel** | Ubuntu 18.04.6 LTS aarch64; Linux 4.9.299-tegra |
| **Middleware** | ROS1 Melodic Morenia, Python 2.7 default |
| **LIDAR** | RPLiDAR A1 (0.15–12 m, 8,000 Hz) *or* YDLiDAR G4 (0.12–16 m, 9,000 Hz) |
| **Depth camera** | Astra Pro Plus — 640×480 depth @30fps, up to 1280×960 RGB @30fps, 0.6–8 m, USB 2.0 |
| **Drive** | 4× mecanum wheels, encoder-equipped DC motors, pendulum suspension |
| **Manipulation** | 6DOF vision-guided arm with end-effector camera |
| **Low-level control** | Expansion board: IMU, motor PWM, 9-channel servo bus, 2× GPIO, 2× I2C |
| **Power** | 11.1 V, 6000 mAh Li-ion battery (~66.6 Wh) |
| **Network** | Standalone ROS master @ `192.168.0.114:11311`, hostname `jetauto-desktop` |
| **System user** | `jetauto` (home: `/home/jetauto`, workspace: `~/jetauto_ws`) |
