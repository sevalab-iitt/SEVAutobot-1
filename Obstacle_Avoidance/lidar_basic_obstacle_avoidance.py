#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
auto_explore.py
Autonomous obstacle-avoidance driving for JetAuto Pro using RPLiDAR A1.

CONTROL (SSH-friendly - works identically over SSH or on the robot's
own screen, no keyboard/TTY capture needed):

    Pause the robot:
        rostopic pub /auto_explore/pause std_msgs/Bool "data: true"

    Resume the robot:
        rostopic pub /auto_explore/pause std_msgs/Bool "data: false"

    (You can run these from ANY terminal that has the workspace
     sourced - local terminal on the robot's screen, or SSH session
     from another machine. No xterm, no raw keyboard mode required.)

Why this approach instead of a keyboard key press:
    roslaunch nodes don't have a real terminal/TTY attached to them,
    so raw keyboard reading (like the old spacebar approach) only
    works if you manually run the script in its own terminal window
    with a real keyboard focus - which breaks over SSH and complicates
    the single-launch-file goal. Publishing a ROS topic instead works
    the same way regardless of how/where you're connected.

------------------------------------------------------------------
ANGLE CONVENTION on THIS robot (as measured by you, not the usual
0-degree-forward convention):
    front = +180 / -180 deg
    back  =    0 deg
    left  =  -90 deg
    right =  +90 deg
------------------------------------------------------------------

HOW THE OBSTACLE AVOIDANCE DECISION WORKS (state machine):

  FORWARD:
    - Drive straight at LIN_VEL as long as the FRONT sector's closest
      obstacle is farther than FRONT_STOP_DIST.
    - The instant the front sector's closest point drops to
      <= FRONT_STOP_DIST, stop and decide what to do next:
        * If front AND left AND right are ALL closer than
          BOXED_IN_DIST -> robot is boxed in on 3 sides -> go to REVERSE.
        * Otherwise -> compare left_min vs right_min and turn toward
          whichever side has MORE open space -> go to AVOID_TURN.

  AVOID_TURN:
    - Rotate in place at ANG_VEL toward the more-open side.
    - Keeps turning until EITHER:
        a) TURN_TIME seconds have elapsed, OR
        b) the front sector clears past FRONT_STOP_DIST * 1.3 early
           (so it doesn't over-rotate more than necessary once a path
           opens up)
    - Then returns to FORWARD.

  REVERSE:
    - Drives straight backward at LIN_VEL for REVERSE_TIME seconds
      (to get away from all 3 blocked sectors).
    - Then picks a turn direction (same left-vs-right comparison) and
      goes to AVOID_TURN to reorient before trying FORWARD again.

  PAUSED (via /auto_explore/pause topic):
    - Overrides all of the above. Publishes (0,0) continuously.
    - State machine is reset to FORWARD so that resuming always
      starts clean instead of mid-turn/mid-reverse.

------------------------------------------------------------------
ALL TUNABLE THRESHOLDS / PARAMETERS (see block below for values + meaning):

  LIN_VEL           - forward/backward driving speed (m/s)
  ANG_VEL           - in-place turning speed (rad/s)
  FRONT_STOP_DIST   - obstacle distance (m) in FRONT sector that
                       triggers stop-and-avoid
  BOXED_IN_DIST     - distance (m) below which front/left/right are
                       all considered "blocked" -> triggers REVERSE
                       instead of just turning
  MIN_LIDAR_LIMIT   - minimum valid range filter; set to 0.0 (only
                       drops literal invalid/zero readings, does NOT
                       ignore close-range real obstacles)
  REVERSE_TIME      - how long (seconds) to reverse when boxed in
  TURN_TIME         - fixed duration (seconds) of an avoidance turn
                       burst (hardcoded, not randomized - see notes
                       from our discussion: predictable/tunable
                       behavior was preferred over randomness here)
  RATE_HZ           - control loop frequency (Hz)
  FRONT_CENTER /
  LEFT_CENTER /
  RIGHT_CENTER      - center angle (deg) of each sector, matching
                       YOUR robot's measured convention (see above)
  SECTOR_HALF_WIDTH - each sector is this many degrees wide on EACH
                       side of its center (so total cone width =
                       2 * SECTOR_HALF_WIDTH) -> currently 60 deg
                       total per sector (30 deg either side)

Publishes: jetauto_controller/cmd_vel (geometry_msgs/Twist)
Subscribes:
    /scan (sensor_msgs/LaserScan)   -- RAW scan, full 360 deg
    /auto_explore/pause (std_msgs/Bool) -- true = pause, false = resume
"""

import math
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

# =================== TUNABLE PARAMETERS ===================
LIN_VEL          = 0.20    # m/s   - forward & reverse speed
ANG_VEL          = 0.60    # rad/s - in-place turning speed

FRONT_STOP_DIST  = 0.50    # m - stop & avoid if front obstacle closer than this
BOXED_IN_DIST    = 0.40    # m - if front+left+right ALL closer than this -> reverse

MIN_LIDAR_LIMIT  = 0.0     # m - disabled: no min-range filtering (sectors only
                            #     cover front/left/right cones, so LiDAR self-
                            #     detection from chassis/mount isn't a concern)

REVERSE_TIME     = 0.8     # sec - how long to reverse when boxed in
TURN_TIME        = 0.7     # sec - fixed avoidance-turn burst duration
                            #     (~0.7s * 0.6 rad/s ~= 24 deg turn, tune as needed)

RATE_HZ          = 10      # Hz  - control loop rate

# Sector centers (deg), using THIS robot's measured angle convention
FRONT_CENTER = 180.0
LEFT_CENTER  = -90.0
RIGHT_CENTER = 90.0
SECTOR_HALF_WIDTH = 30.0   # deg - each sector spans +/- this much around its center

# Shutdown behavior
SHUTDOWN_STOP_REPEATS = 6      # how many times to (re)publish zero-twist on exit
SHUTDOWN_STOP_INTERVAL = 0.05  # seconds between those repeats
# ============================================================


def normalize_deg(a):
    """Normalize an angle in degrees to (-180, 180]."""
    while a > 180.0:
        a -= 360.0
    while a <= -180.0:
        a += 360.0
    return a


def angular_distance(a, b):
    """Smallest absolute difference between two angles in degrees."""
    return abs(normalize_deg(a - b))


class AutoExplorer(object):
    def __init__(self):
        rospy.init_node('lidar_basic_obstacle_avoidance')

        self.pub = rospy.Publisher('jetauto_controller/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber('/scan', LaserScan, self.scan_cb, queue_size=1)
        rospy.Subscriber('/auto_explore/pause', Bool, self.pause_cb, queue_size=1)

        self.front_min = float('inf')
        self.left_min = float('inf')
        self.right_min = float('inf')
        self.scan_ready = False

        # avoidance state: 'FORWARD', 'AVOID_TURN', 'REVERSE'
        self.state = 'FORWARD'
        self.state_until = rospy.get_time()
        self.turn_dir = 1.0  # +1 = turn toward left, -1 = turn toward right

        self.paused = False  # controlled via /auto_explore/pause topic

        self.rate = rospy.Rate(RATE_HZ)

        # make sure the robot is stopped no matter how the node exits
        rospy.on_shutdown(self.shutdown_hook)

    # ---------------- Pause/Resume handling (SSH-friendly) ----------------
    def pause_cb(self, msg):
        was_paused = self.paused
        self.paused = msg.data
        if self.paused != was_paused:
            if self.paused:
                rospy.loginfo("[PAUSE] Received pause command -> robot stopped.")
            else:
                rospy.loginfo("[RESUME] Received resume command -> auto avoidance active.")
            # reset state machine so resuming always starts clean
            self.state = 'FORWARD'
            self.publish_twist(0.0, 0.0)

    # ---------------- LiDAR handling ----------------
    def scan_cb(self, msg):
        front_vals, left_vals, right_vals = [], [], []

        for i, r in enumerate(msg.ranges):
            if r <= MIN_LIDAR_LIMIT or r > msg.range_max or math.isinf(r) or math.isnan(r):
                # r <= 0 means "invalid/no return" from the LiDAR, not a real
                # obstacle - must still be dropped or it reads as 0m obstacle
                continue

            angle_rad = msg.angle_min + i * msg.angle_increment
            angle_deg = normalize_deg(math.degrees(angle_rad))

            if angular_distance(angle_deg, FRONT_CENTER) <= SECTOR_HALF_WIDTH:
                front_vals.append(r)
            elif angular_distance(angle_deg, LEFT_CENTER) <= SECTOR_HALF_WIDTH:
                left_vals.append(r)
            elif angular_distance(angle_deg, RIGHT_CENTER) <= SECTOR_HALF_WIDTH:
                right_vals.append(r)

        self.front_min = min(front_vals) if front_vals else float('inf')
        self.left_min = min(left_vals) if left_vals else float('inf')
        self.right_min = min(right_vals) if right_vals else float('inf')
        self.scan_ready = True

    # ---------------- Motion helpers ----------------
    def publish_twist(self, lin, ang):
        t = Twist()
        t.linear.x = lin
        t.angular.z = ang
        self.pub.publish(t)

    def pick_turn_direction(self):
        """Turn toward whichever side currently has more clearance."""
        if self.left_min > self.right_min:
            return 1.0   # turn left
        else:
            return -1.0  # turn right

    def shutdown_hook(self):
        """Guarantees the robot actually stops, even on Ctrl+C or roslaunch
        shutdown. A single publish right at shutdown can be dropped because
        ROS tears down publisher connections almost immediately after
        rospy.is_shutdown() becomes True - so we publish zero-twist several
        times with short delays to make sure it's received."""
        rospy.loginfo("Shutting down - forcing robot to stop.")
        for _ in range(SHUTDOWN_STOP_REPEATS):
            self.publish_twist(0.0, 0.0)
            rospy.sleep(SHUTDOWN_STOP_INTERVAL)

    # ---------------- Main loop ----------------
    def run(self):
        rospy.loginfo("Waiting for first /scan message...")
        while not rospy.is_shutdown() and not self.scan_ready:
            self.rate.sleep()

        rospy.loginfo("Scan received. Starting autonomous exploration.")
        rospy.loginfo("To pause:  rostopic pub /auto_explore/pause std_msgs/Bool \"data: true\"")
        rospy.loginfo("To resume: rostopic pub /auto_explore/pause std_msgs/Bool \"data: false\"")

        while not rospy.is_shutdown():
            if self.paused:
                self.publish_twist(0.0, 0.0)
                self.rate.sleep()
                continue

            now = rospy.get_time()

            if self.state == 'FORWARD':
                if self.front_min <= FRONT_STOP_DIST:
                    detect_time = now  # moment obstacle was detected

                    boxed_in = (self.front_min <= BOXED_IN_DIST and
                                self.left_min <= BOXED_IN_DIST and
                                self.right_min <= BOXED_IN_DIST)
                    if boxed_in:
                        self.state = 'REVERSE'
                        self.state_until = now + REVERSE_TIME
                        decision_ms = (rospy.get_time() - detect_time) * 1000.0
                        rospy.logwarn(
                            "[OBSTACLE] Boxed in (F:%.2fm L:%.2fm R:%.2fm) | "
                            "decision made in %.1f ms -> REVERSE for %.1fs",
                            self.front_min, self.left_min, self.right_min,
                            decision_ms, REVERSE_TIME)
                    else:
                        self.turn_dir = self.pick_turn_direction()
                        self.state = 'AVOID_TURN'
                        self.state_until = now + TURN_TIME
                        decision_ms = (rospy.get_time() - detect_time) * 1000.0
                        est_deg = math.degrees(ANG_VEL * TURN_TIME)
                        rospy.logwarn(
                            "[OBSTACLE] Front %.2fm (L:%.2fm R:%.2fm) | "
                            "decision made in %.1f ms -> TURN %s for %.2fs "
                            "(~%.1f deg)",
                            self.front_min, self.left_min, self.right_min,
                            decision_ms,
                            "LEFT" if self.turn_dir > 0 else "RIGHT",
                            TURN_TIME, est_deg)
                    self.publish_twist(0.0, 0.0)
                else:
                    self.publish_twist(LIN_VEL, 0.0)

            elif self.state == 'AVOID_TURN':
                self.publish_twist(0.0, self.turn_dir * ANG_VEL)
                if now >= self.state_until or self.front_min > FRONT_STOP_DIST * 1.3:
                    self.state = 'FORWARD'
                    self.publish_twist(0.0, 0.0)

            elif self.state == 'REVERSE':
                self.publish_twist(-LIN_VEL, 0.0)
                if now >= self.state_until:
                    self.turn_dir = self.pick_turn_direction()
                    est_deg = math.degrees(ANG_VEL * TURN_TIME)
                    self.state = 'AVOID_TURN'
                    self.state_until = now + TURN_TIME
                    rospy.loginfo(
                        "[REVERSE DONE] Now turning %s for %.2fs (~%.1f deg)",
                        "LEFT" if self.turn_dir > 0 else "RIGHT",
                        TURN_TIME, est_deg)
                    self.publish_twist(0.0, 0.0)

            self.rate.sleep()

        # main loop exited -> shutdown_hook will force-stop the robot


if __name__ == '__main__':
    try:
        AutoExplorer().run()
    except rospy.ROSInterruptException:
        pass