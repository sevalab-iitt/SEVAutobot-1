# LiDAR safety + avoidance

# nano ~/catkin_ws/src/jetauto_llm/scripts/robot/obstacle_avoidance.py

# -*- coding: utf-8 -*-

"""
STAGE 6 - LiDAR OBSTACLE AVOIDANCE

JetAuto LiDAR orientation:

    FRONT = +180 / -180 degrees
    BACK  = 0 degrees
    LEFT  = -90 degrees
    RIGHT = +90 degrees

Responsibilities:
    - Subscribe to /scan
    - Read front, left and right distances
    - Detect obstacles
    - Prevent unsafe forward movement
    - Select the clearer side for avoidance

Python 2 compatible.
"""

import math
import rospy
from sensor_msgs.msg import LaserScan


class ObstacleAvoidance(object):

    # ============================================================
    # CONFIGURATION
    # ============================================================

    FRONT_SAFE_DISTANCE = 0.35
    SIDE_SAFE_DISTANCE = 0.25

    # Front is around +/-180 degrees.
    # Use two windows because the front wraps around
    # -180 / +180.
    FRONT_MIN_ANGLE = 165.0
    FRONT_MAX_ANGLE = 180.0

    FRONT_NEG_MIN_ANGLE = -180.0
    FRONT_NEG_MAX_ANGLE = -165.0

    # Left = -90
    LEFT_MIN_ANGLE = -120.0
    LEFT_MAX_ANGLE = -60.0

    # Right = +90
    RIGHT_MIN_ANGLE = 60.0
    RIGHT_MAX_ANGLE = 120.0

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
    # LIDAR CALLBACK
    # ============================================================

    def scan_callback(self, msg):

        self.front_distance = self.get_front_distance(msg)

        self.left_distance = self.get_sector_distance(
            msg,
            self.LEFT_MIN_ANGLE,
            self.LEFT_MAX_ANGLE
        )

        self.right_distance = self.get_sector_distance(
            msg,
            self.RIGHT_MIN_ANGLE,
            self.RIGHT_MAX_ANGLE
        )

        self.scan_received = True

    # ============================================================
    # FRONT DISTANCE
    # ============================================================

    def get_front_distance(self, scan):

        values = []

        angle = scan.angle_min

        for distance in scan.ranges:

            angle_deg = math.degrees(angle)

            # Front wraps around +/-180 degrees.
            front_angle = (
                angle_deg >= self.FRONT_MIN_ANGLE or
                angle_deg <= self.FRONT_NEG_MAX_ANGLE
            )

            if front_angle:

                if self.is_valid_distance(scan, distance):
                    values.append(distance)

            angle += scan.angle_increment

        if not values:
            return None

        return min(values)

    # ============================================================
    # GENERIC SECTOR DISTANCE
    # ============================================================

    def get_sector_distance(
        self,
        scan,
        min_angle_deg,
        max_angle_deg
    ):

        values = []

        angle = scan.angle_min

        for distance in scan.ranges:

            angle_deg = math.degrees(angle)

            if min_angle_deg <= angle_deg <= max_angle_deg:

                if self.is_valid_distance(scan, distance):
                    values.append(distance)

            angle += scan.angle_increment

        if not values:
            return None

        return min(values)

    # ============================================================
    # VALID LiDAR RETURN
    # ============================================================

    def is_valid_distance(self, scan, distance):

        if math.isnan(distance):
            return False

        if math.isinf(distance):
            return False

        if distance < scan.range_min:
            return False

        if distance > scan.range_max:
            return False

        return True

    # ============================================================
    # VALIDITY
    # ============================================================

    def has_valid_scan(self):

        return self.scan_received

    def has_front_distance(self):

        return self.front_distance is not None

    # ============================================================
    # FORWARD SAFETY
    # ============================================================

    def is_safe_forward(self):

        if self.front_distance is None:
            return False

        return self.front_distance > self.FRONT_SAFE_DISTANCE

    # ============================================================
    # OBSTACLE DETECTION
    # ============================================================

    def obstacle_ahead(self):

        if self.front_distance is None:
            return True

        return self.front_distance <= self.FRONT_SAFE_DISTANCE

    # ============================================================
    # SIDE SAFETY
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
    # BEST AVOIDANCE DIRECTION
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
    # STATUS
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
    # HUMAN READABLE STATUS
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


# ================================================================
# DIRECT TEST
# ================================================================

if __name__ == '__main__':

    rospy.init_node(
        'obstacle_avoidance_test',
        anonymous=True
    )

    avoidance = ObstacleAvoidance()

    rospy.loginfo(
        "Waiting for LiDAR data..."
    )

    rate = rospy.Rate(2)

    while not rospy.is_shutdown():

        print("")
        print("========== OBSTACLE AVOIDANCE ==========")

        print(
            "Available : %s" %
            avoidance.has_valid_scan()
        )

        if avoidance.front_distance is None:
            print("Front     : no valid return")
        else:
            print(
                "Front     : %.2f m" %
                avoidance.front_distance
            )

        if avoidance.left_distance is None:
            print("Left      : no valid return")
        else:
            print(
                "Left      : %.2f m" %
                avoidance.left_distance
            )

        if avoidance.right_distance is None:
            print("Right     : no valid return")
        else:
            print(
                "Right     : %.2f m" %
                avoidance.right_distance
            )

        print(
            "Safe      : %s" %
            avoidance.is_safe_forward()
        )

        print(
            "Obstacle  : %s" %
            avoidance.obstacle_ahead()
        )

        print(
            "Avoid     : %s" %
            avoidance.get_best_avoidance_direction()
        )

        print("=========================================")

        rate.sleep()
"""
python2 -c "import sys; sys.path.insert(0, '$HOME/catkin_ws/src/jetauto_llm/scripts'); from robot.obstacle_avoidance import ObstacleAvoidance; print('OBSTACLE AVOIDANCE MODULE OK')"
"""
