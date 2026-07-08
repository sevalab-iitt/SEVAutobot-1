# Wheel Telemetry: Actual Speed Verification

## 1. Purpose

The JetAuto Pro's built-in `/jetauto_controller` node does **not** publish real encoder feedback (verified via `rosnode info /jetauto_controller` — only `/rosout` is published). The existing `odom_publisher.py` node only estimates position by integrating *commanded* velocity (dead-reckoning), not real measured wheel motion.

To get genuine, hardware-measured wheel speed, a custom script was written that bypasses ROS entirely and reads raw encoder pulse counts directly over I2C from the motor driver board.

---

## 2. Background — What is Dead Reckoning?

Dead reckoning is a way of **estimating** position without directly measuring it — by calculating from a known starting point, a known speed, a known direction, and elapsed time, rather than checking the real world.

**Analogy:** Walking blindfolded in a hallway, being told "walk forward 1 step/second for 5 seconds, then turn right for 3 steps." You never look at where you actually end up — you just trust the instructions and calculate: "I should now be about 5 steps down, 3 steps right." That calculation is dead reckoning.

**In the existing code (`odom_publisher.py`):**
```python
self.x += math.cos(self.pose_yaw)*self.linear_x*self.dt - math.sin(self.pose_yaw)*self.linear_y*self.dt
self.y += math.sin(self.pose_yaw)*self.linear_x*self.dt + math.cos(self.pose_yaw)*self.linear_y*self.dt
self.yaw += self.angular_factor*self.angular_z*self.dt
```
This trusts the *commanded* speed and simply adds up small movements over time — it never checks a sensor to confirm the robot actually moved that far.

**Why this is risky:** if a wheel slips, stalls, hits an obstacle, or the robot is moved manually, dead reckoning has no way of knowing — it keeps calculating as if the command was followed exactly. These small errors **accumulate** over time, causing the estimated position to drift further and further from the true position the longer the robot runs.



---

## 3. How the Custom Script Works

The motor driver board (I2C address `0x34`) maintains a running pulse counter for each of the 4 wheels, incremented by physical encoder sensors on each motor shaft. The script:

1. Reads all 4 counters
2. Waits a fixed interval (0.2s)
3. Reads the counters again
4. Computes the *difference* in pulses over that time window
5. Converts pulses → wheel rotations → linear speed, using the robot's real chassis constants (from `jetauto_sdk/mecanum.py`):
   - Wheel diameter: 96.5 mm
   - Pulses per wheel revolution: 44 × 178 = 7832

---

## 4. Script — `actual_wheel_speed.py`

```python
#!/usr/bin/env python3
"""
JetAuto Pro - ACTUAL Wheel Speed Monitor
Reads real encoder pulse counts directly over I2C (bypassing ROS)
to compute true measured wheel speed - not commanded speed.

Based on constants from jetauto_sdk/mecanum.py and the I2C protocol
in jetauto_sdk/encoder_motor.py
"""

import time
import math
import smbus2
import struct

ENCODER_MOTOR_MODULE_ADDRESS = 0x34
I2C_PORT = 1
ENCODER_REG = 60  # base register, 4x int32 (16 bytes total)

# ---- Real constants confirmed from mecanum.py ----
WHEEL_DIAMETER_MM = 96.5
PULSES_PER_REV = 44 * 178   # 7832
WHEEL_CIRCUMFERENCE_MM = math.pi * WHEEL_DIAMETER_MM
WHEEL_RADIUS_M = (WHEEL_DIAMETER_MM / 1000.0) / 2.0

# Motor ID -> physical wheel position (from mecanum.py diagram)
WHEEL_NAMES = {
    0: "Front-Right (motor 1)",
    1: "Rear-Right  (motor 2)",
    2: "Front-Left  (motor 3)",
    3: "Rear-Left   (motor 4)",
}

POLL_INTERVAL = 0.2  # seconds between samples


def read_encoders(bus):
    data = bus.read_i2c_block_data(ENCODER_MOTOR_MODULE_ADDRESS, ENCODER_REG, 16)
    return list(struct.unpack('<iiii', bytes(data)))


def main():
    print("Reading real encoder feedback via I2C ... drive the robot now (Ctrl+C to stop)")
    with smbus2.SMBus(I2C_PORT) as bus:
        prev_counts = read_encoders(bus)
        prev_time = time.time()

        while True:
            time.sleep(POLL_INTERVAL)
            curr_counts = read_encoders(bus)
            curr_time = time.time()
            dt = curr_time - prev_time

            print("\n===== ACTUAL Wheel Speed (measured via encoders) =====")
            for i in range(4):
                delta_pulses = curr_counts[i] - prev_counts[i]
                revs_per_sec = (delta_pulses / PULSES_PER_REV) / dt
                speed_mm_s = revs_per_sec * WHEEL_CIRCUMFERENCE_MM
                speed_m_s = speed_mm_s / 1000.0
                angular_speed_rad_s = speed_m_s / WHEEL_RADIUS_M

                direction = "forward" if delta_pulses > 0 else ("reverse" if delta_pulses < 0 else "stopped")

                print(f"{WHEEL_NAMES[i]}: "
                      f"{speed_m_s:+.3f} m/s | "
                      f"{angular_speed_rad_s:+.3f} rad/s | "
                      f"{revs_per_sec*60:+.1f} RPM | "
                      f"{direction} | "
                      f"raw_ticks={curr_counts[i]}")

            prev_counts = curr_counts
            prev_time = curr_time


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped.")
    except Exception as e:
        print(f"Error: {e}")
```

---

## 5. How to Run

**1. Save the script** on the robot:
```bash
nano ~/actual_wheel_speed.py
```
(paste the code above, save with `Ctrl+O`, exit with `Ctrl+X`)

**2. Install the required dependency** (if not already present):
```bash
pip3 install smbus2
```

**3. Make it executable (optional):**
```bash
chmod +x ~/actual_wheel_speed.py
```

**4. Run it:**
```bash
python3 ~/actual_wheel_speed.py
```

**5. While it's running**, drive the robot using the app, joystick, or any control mode. Live wheel data prints continuously to the terminal.

Expected Output


<img width="500" height="300" alt="image" src="https://github.com/user-attachments/assets/56689804-b2a5-4ab5-bd9e-55fafc709a53" />

**6. Stop it** with `Ctrl+C` when done.

> **Note:** If you get a `PermissionError` or `OSError: [Errno 13]` on the I2C read, run with `sudo`:
> ```bash
> sudo python3 ~/actual_wheel_speed.py
> ```

---

## 7. Output Field Reference

| Field | Meaning |
|---|---|
| Wheel name | Physical wheel position (Front-Right, Rear-Right, Front-Left, Rear-Left), mapped from motor ID via `mecanum.py`'s wiring order |
| `m/s` | Linear surface speed — how fast the wheel's edge is moving across the ground |
| `rad/s` | Angular velocity — how fast the wheel is spinning, independent of wheel size |
| `RPM` | Same angular speed, in revolutions per minute (human-readable form) |
| `forward` / `reverse` / `stopped` | Rotation direction, derived from the sign of the pulse-count change |
| `raw_ticks` | Raw cumulative encoder pulse count at that instant (only the *difference* between two readings is meaningful) |

---

## 8. Known Limitation — Bus Contention

`/jetauto_controller` also communicates with I2C address `0x34` during normal operation. This script should be treated as a **diagnostic tool**, not run continuously alongside normal robot operation, to avoid potential I2C bus contention.

## 9. Known SDK Bug

The underlying SDK's single-motor `read_encoder(motor_id)` function only accepts `motor_id` values 1–3 due to a boundary condition (`0 < motor_id < 4`), meaning motor 4 can never be read individually through that path. This script avoids the issue entirely by always requesting all 4 encoder values at once (`motor_id=None`).

---

## 10. Compare & Contrast — Custom Script vs. Existing JetAuto Source Code

This section compares `actual_wheel_speed.py` against the three existing Hiwonder source files it draws from, clarifying what each one actually does and why a new script was necessary.

### `odom_publisher.py` (existing) vs. `actual_wheel_speed.py` (custom)

| | `odom_publisher.py` (existing) | `actual_wheel_speed.py` (custom) |
|---|---|---|
| **Data source** | Commanded `/jetauto_controller/cmd_vel` values | Real encoder pulse counts read directly over I2C |
| **Method** | Dead-reckoning — integrates commanded speed over time | Measures actual pulse count change between two hardware reads |
| **What it answers** | "Where should the robot be, if it did what it was told?" | "How fast is each wheel actually spinning, right now?" |
| **Accuracy over time** | Drifts — errors accumulate if wheels slip, stall, or are blocked | Stays accurate — every reading reflects real hardware state, no accumulation |
| **Runs via** | ROS node (`roslaunch jetauto_controller odom_publish.launch`) | Standalone Python, no ROS required |
| **Output** | Estimated robot pose (x, y, yaw) as one combined value | Per-wheel speed (m/s, rad/s, RPM) and direction, individually |

**Summary:** `odom_publisher.py` estimates the *robot's* overall position by trusting commands; our script measures *each wheel's* real motion by reading the sensor hardware directly. They answer different questions — one is a position estimate, the other is a speed verification tool.

### `mecanum.py` (existing) vs. `actual_wheel_speed.py` (custom)

| | `mecanum.py` (existing) | `actual_wheel_speed.py` (custom) |
|---|---|---|
| **Direction of conversion** | Speed → pulses (converts a desired mm/s into pulses/10ms to *send* to the motors) | Pulses → speed (converts real pulse count changes back into m/s, rad/s, RPM) |
| **Purpose** | Commands the robot on how fast to spin each wheel to achieve a desired overall motion | Reports how fast each wheel actually spun, after the fact |
| **Uses constants** | Defines the constants (wheel diameter 96.5mm, pulse_per_cycle 44×178, a=103, b=97) | Reuses the same wheel diameter and pulse-per-cycle constants |
| **Wheel mapping logic** | Reorders `[v1, v2, v3, v4]` into physical motor order via `[-v2, v3, v1, -v4]` | Uses this exact reordering pattern to label which array index is Front-Right, Rear-Right, etc. |

**Summary:** `mecanum.py` is the *outgoing* half of the system — turning a desired motion into wheel commands. Our script is the *incoming*, reverse half — turning real wheel behavior back into readable speed — using the same physical constants so the numbers are consistent with how the robot itself calculates motion.

### `encoder_motor.py` (existing) vs. `actual_wheel_speed.py` (custom)

| | `encoder_motor.py` (existing) | `actual_wheel_speed.py` (custom) |
|---|---|---|
| **Role** | Low-level driver — defines how to read/write the motor controller chip over I2C | Application script — uses that same I2C read pattern to build a live monitoring tool |
| **`read_encoder()` behavior** | Returns raw pulse counts, single snapshot only | Calls the equivalent read twice, computes the *difference* over time to derive speed |
| **Single-motor read** | Has a boundary bug — only accepts IDs 1–3, motor 4 can never be read alone | Avoids the bug entirely by always requesting all 4 motors at once |
| **Output** | Just numbers (raw ticks) — no interpretation | Fully interpreted: speed, direction, RPM, human-readable labels |
| **Intended use** | Building block, meant to be called by higher-level code | Complete standalone diagnostic tool |

**Summary:** `encoder_motor.py` provides the raw capability to talk to the hardware but does no interpretation and contains an unfixed access bug for one motor. Our script builds directly on top of it — same I2C read logic, but adds the "before vs. after" comparison needed to turn a single snapshot into a meaningful speed measurement, and works around the SDK's own limitation in the process.

### Overall Takeaway

None of the three existing files, individually or combined, produce real-time human-readable wheel speed:
- `odom_publisher.py` estimates position, not per-wheel speed, and isn't hardware-verified.
- `mecanum.py` only converts commands *into* motor instructions — it has no path back to real measured speed.
- `encoder_motor.py` can fetch raw pulse data but performs no timing, conversion, or interpretation, and has a bug that blocks reading motor 4 alone.

`actual_wheel_speed.py` was written specifically to fill this gap — combining the correct hardware constants from `mecanum.py`, the correct I2C access pattern from `encoder_motor.py`, and a genuine time-based speed calculation that none of the existing files perform, into one verifiable diagnostic tool.


