# Obstacle Avoidance (LiDAR-based)

Basic autonomous obstacle avoidance for JetAuto Pro using an RPLiDAR A1. The robot
drives forward, detects obstacles using 3 LiDAR sectors (front / left / right),
and turns or reverses to avoid them — all in a single `roslaunch` command.

## Idea

A simple reactive state machine, no mapping or SLAM involved:

1. **FORWARD** — drive ahead while the front sector is clear.
2. Obstacle detected in front → stop, compare left vs. right sector clearance,
   and turn toward whichever side is more open (**AVOID_TURN**).
3. If front, left, **and** right are all blocked at once (boxed in) → reverse
   for a short time first (**REVERSE**), then turn.
4. Repeat. The robot has no fixed path — it wanders the room avoiding whatever
   it detects.

## Hardware-specific note: angle convention

This robot's LiDAR angle convention is **not** the usual 0°-forward layout:

| Direction | Angle |
|---|---|
| Front | +180° / -180° |
| Back  | 0° |
| Left  | -90° |
| Right | +90° |

All sector logic in the script is built around this convention. If you reuse
this code on a different robot, re-check your LiDAR's actual front angle first.

## Files

| File | Purpose |
|---|---|
| [`lidar_basic_obstacle_avoidance.py`](./lidar_basic_obstacle_avoidance.py) | The obstacle avoidance node |
| [`lidar_basic_obstacle_avoidance.launch`](./lidar_basic_obstacle_avoidance.launch) | Brings up controller + LiDAR + tf + the node in one command |

**On the robot**, these two files live at:
```
~/jetauto_ws/src/jetauto_peripherals/scripts/lidar_basic_obstacle_avoidance.py
~/jetauto_ws/src/jetauto_peripherals/launch/lidar_basic_obstacle_avoidance.launch
```

## Key settings

| Parameter | Value | Meaning |
|---|---|---|
| `LIN_VEL` | 0.20 m/s | forward / reverse speed |
| `ANG_VEL` | 0.60 rad/s | turning speed |
| `FRONT_STOP_DIST` | 0.50 m | obstacle distance in front that triggers avoidance |
| `BOXED_IN_DIST` | 0.40 m | if front+left+right are all closer than this → reverse instead of turning |
| `REVERSE_TIME` | 0.8 s | how long to reverse when boxed in |
| `TURN_TIME` | 0.7 s | fixed turn duration (~24° at current `ANG_VEL`) |
| `SECTOR_HALF_WIDTH` | 30° | each of front/left/right is a 60°-wide cone |
| `RATE_HZ` | 10 Hz | control loop rate |


## Running it

```bash
cd ~/jetauto_ws
source devel/setup.bash
roslaunch jetauto_peripherals lidar_basic_obstacle_avoidance.launch
```

This single command starts the motor controller, the LiDAR driver, the
`map -> lidar_frame` static transform, and the avoidance node together.

To stop, `Ctrl+C` the terminal running `roslaunch` — the node force-publishes
zero velocity on shutdown so the robot reliably stops moving.

## Current limitations

- Turning is **time-based, not angle-based** — there's no IMU/odometry
  feedback, so the `~X deg` turn estimate is theoretical and will drift with
  wheel slip and battery voltage.
- Only front/left/right sectors are checked (60° cones each); back is not
  monitored.
- No mapping/memory of the room — the robot can revisit the same area
  repeatedly.