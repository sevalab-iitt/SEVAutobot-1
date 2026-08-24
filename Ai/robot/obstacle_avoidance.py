# LiDAR safety + avoidance

# nano ~/catkin_ws/src/jetauto_llm/scripts/robot/obstacle_avoidance.py

# -*- coding: utf-8 -*-

"""
STAGE 6 - LiDAR OBSTACLE AVOIDANCE

Purpose:
    Provides LiDAR-based safety for the robot.

Responsibilities:
    - Subscribe to /scan
    - Read front, left and right distances
    - Detect obstacles
    - Prevent forward movement into an obstacle
    - Provide safety information to the main LLM orchestrator

Python:
    Python 2 compatible
"""

import math
import rospy
from sensor_msgs.msg import LaserScan


class ObstacleAvoidance(object):

    # ============================================================
    # STAGE 6 CONFIGURATION
    # ============================================================

    FRONT_SAFE_DISTANCE = 0.35
    SIDE_SAFE_DISTANCE = 0.25

    def __init__(self):

        self.front_distance = None
        self.left_distance = None
        self.right_distance = None

        self.scan_received = False

        self.scan_sub = rospy.Subscriber(
            '/scan',
            LaserScan,
            self.scan_callback,
            queue_size=1
        )

        rospy.loginfo("ObstacleAvoidance initialized")

    # ============================================================
    # STAGE 6 - LIDAR CALLBACK
    # ============================================================

    def scan_callback(self, msg):

        self.front_distance = self.get_sector_distance(
            msg,
            -15.0,
            15.0
        )

        self.left_distance = self.get_sector_distance(
            msg,
            60.0,
            120.0
        )

        self.right_distance = self.get_sector_distance(
            msg,
            -120.0,
            -60.0
        )

        self.scan_received = True

    # ============================================================
    # STAGE 6 - SECTOR DISTANCE
    # ============================================================

    def get_sector_distance(self, scan, min_angle_deg, max_angle_deg):

        values = []

        angle = scan.angle_min
        angle_increment = scan.angle_increment

        for distance in scan.ranges:

            angle_deg = math.degrees(angle)

            if min_angle_deg <= angle_deg <= max_angle_deg:

                if (
                    not math.isnan(distance)
                    and not math.isinf(distance)
                    and distance > scan.range_min
                    and distance < scan.range_max
                ):
                    values.append(distance)

            angle += angle_increment

        if not values:
            return None

        return min(values)

    # ============================================================
    # STAGE 6 - VALIDITY
    # ============================================================

    def has_valid_scan(self):

        return self.scan_received

    def has_front_distance(self):

        return self.front_distance is not None

    # ============================================================
    # STAGE 6 - SAFETY CHECK
    # ============================================================

    def is_safe_forward(self):

        if self.front_distance is None:
            return False

        return self.front_distance > self.FRONT_SAFE_DISTANCE

    # ============================================================
    # STAGE 6 - OBSTACLE CHECK
    # ============================================================

    def obstacle_ahead(self):

        if self.front_distance is None:
            return True

        return self.front_distance <= self.FRONT_SAFE_DISTANCE

    # ============================================================
    # STAGE 6 - SIDE INFORMATION
    # ============================================================

    def is_left_clear(self):

        if self.left_distance is None:
            return False

        return self.left_distance > self.SIDE_SAFE_DISTANCE

    def is_right_clear(self):

        if self.right_distance is None:
            return False

        return self.right_distance > self.SIDE_SAFE_DISTANCE

    # ============================================================
    # STAGE 6 - AVOIDANCE DIRECTION
    # ============================================================

    def get_best_avoidance_direction(self):

        left = self.left_distance
        right = self.right_distance

        if left is None and right is None:
            return None

        if left is None:
            return "right"

        if right is None:
            return "left"

        if left >= right:
            return "left"

        return "right"

    # ============================================================
    # STAGE 6 - STATUS
    # ============================================================

    def get_status(self):

        return {
            "front": self.front_distance,
            "left": self.left_distance,
            "right": self.right_distance,
            "safe_forward": self.is_safe_forward(),
            "obstacle_ahead": self.obstacle_ahead(),
            "best_avoidance_direction":
                self.get_best_avoidance_direction()
        }

    # ============================================================
    # STAGE 6 - HUMAN READABLE STATUS
    # ============================================================

    def print_status(self):

        def fmt(value):

            if value is None:
                return "no valid return"

            return "%.2f m" % value

        rospy.loginfo(
            "LiDAR | Front: %s | Left: %s | Right: %s" %
            (
                fmt(self.front_distance),
                fmt(self.left_distance),
                fmt(self.right_distance)
            )
        )
