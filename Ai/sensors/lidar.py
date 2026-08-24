# /scan interface

#nano ~/catkin_ws/src/jetauto_llm/scripts/sensors/lidar.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
============================================================
LiDAR SENSOR MODULE
JetAuto Pro + RPLiDAR A1

Stage 1:
    Basic LiDAR ROS /scan interface.

Stage 2:
    Sector-based distance extraction.

Stage 3:
    Correct JetAuto physical angle convention.

IMPORTANT:
    This robot does NOT use the usual assumption that
    0 degrees is the front.

Measured JetAuto convention:

    FRONT = +180 / -180 degrees
    BACK  = 0 degrees
    LEFT  = -90 degrees
    RIGHT = +90 degrees

This convention is taken from the tested JetAuto
obstacle-avoidance implementation.

The module does NOT control the motors.

It only provides LiDAR information to other modules.

ROS topic:
    /scan

Message:
    sensor_msgs/LaserScan
============================================================
"""

import math
import rospy

from sensor_msgs.msg import LaserScan


class LidarSensor(object):

    # ========================================================
    # STAGE 3:
    # JetAuto-specific LiDAR orientation
    # ========================================================

    FRONT_CENTER = 180.0
    LEFT_CENTER = -90.0
    RIGHT_CENTER = 90.0

    # +/- 30 degrees
    SECTOR_HALF_WIDTH = 30.0

    def __init__(self,
                 topic='/scan',
                 queue_size=1):

        self.topic = topic

        self.front_min = None
        self.left_min = None
        self.right_min = None

        self.closest_distance = None
        self.clearer_side = None

        self.scan_ready = False
        self.last_scan = None

        self.subscriber = rospy.Subscriber(
            self.topic,
            LaserScan,
            self.scan_callback,
            queue_size=queue_size
        )

        rospy.loginfo(
            "LiDAR sensor initialized on %s",
            self.topic
        )

    # ========================================================
    # ANGLE UTILITIES
    # ========================================================

    @staticmethod
    def normalize_angle(angle):
        """
        Normalize angle to (-180, 180].
        """

        while angle > 180.0:
            angle -= 360.0

        while angle <= -180.0:
            angle += 360.0

        return angle

    @classmethod
    def angular_distance(cls, angle_a, angle_b):
        """
        Smallest absolute angular difference.
        """

        return abs(
            cls.normalize_angle(angle_a - angle_b)
        )

    # ========================================================
    # RANGE VALIDATION
    # ========================================================

    @staticmethod
    def valid_range(distance, msg):
        """
        Check whether a LiDAR range is usable.

        Invalid values:
            NaN
            infinity
            below range_min
            above range_max
            <= 0
        """

        if distance is None:
            return False

        if math.isnan(distance):
            return False

        if math.isinf(distance):
            return False

        if distance <= 0.0:
            return False

        if distance < msg.range_min:
            return False

        if distance > msg.range_max:
            return False

        return True

    # ========================================================
    # STAGE 3:
    # LiDAR CALLBACK
    # ========================================================

    def scan_callback(self, msg):

        front_values = []
        left_values = []
        right_values = []

        for index, distance in enumerate(msg.ranges):

            if not self.valid_range(distance, msg):
                continue

            angle_rad = (
                msg.angle_min +
                index * msg.angle_increment
            )

            angle_deg = math.degrees(angle_rad)

            angle_deg = self.normalize_angle(
                angle_deg
            )

            # ------------------------------------------------
            # FRONT
            # JetAuto front = +/-180 degrees
            # ------------------------------------------------

            if self.angular_distance(
                    angle_deg,
                    self.FRONT_CENTER
            ) <= self.SECTOR_HALF_WIDTH:

                front_values.append(distance)

            # ------------------------------------------------
            # LEFT
            # JetAuto left = -90 degrees
            # ------------------------------------------------

            elif self.angular_distance(
                    angle_deg,
                    self.LEFT_CENTER
            ) <= self.SECTOR_HALF_WIDTH:

                left_values.append(distance)

            # ------------------------------------------------
            # RIGHT
            # JetAuto right = +90 degrees
            # ------------------------------------------------

            elif self.angular_distance(
                    angle_deg,
                    self.RIGHT_CENTER
            ) <= self.SECTOR_HALF_WIDTH:

                right_values.append(distance)

        # ----------------------------------------------------
        # Closest obstacle in each sector
        # ----------------------------------------------------

        if front_values:
            self.front_min = min(front_values)
        else:
            self.front_min = None

        if left_values:
            self.left_min = min(left_values)
        else:
            self.left_min = None

        if right_values:
            self.right_min = min(right_values)
        else:
            self.right_min = None

        # ----------------------------------------------------
        # Overall closest valid return
        # ----------------------------------------------------

        all_values = (
            front_values +
            left_values +
            right_values
        )

        if all_values:
            self.closest_distance = min(all_values)
        else:
            self.closest_distance = None

        # ----------------------------------------------------
        # Determine clearer side
        # ----------------------------------------------------

        if (
            self.left_min is not None and
            self.right_min is not None
        ):

            if self.left_min > self.right_min:
                self.clearer_side = 'left'
            else:
                self.clearer_side = 'right'

        elif self.left_min is not None:

            self.clearer_side = 'left'

        elif self.right_min is not None:

            self.clearer_side = 'right'

        else:

            self.clearer_side = None

        self.last_scan = msg
        self.scan_ready = True

    # ========================================================
    # PUBLIC API
    # ========================================================

    def is_available(self):
        """
        Returns True once a LiDAR scan has been received.
        """

        return self.scan_ready

    def get_front_distance(self):
        return self.front_min

    def get_left_distance(self):
        return self.left_min

    def get_right_distance(self):
        return self.right_min

    def get_closest_distance(self):
        return self.closest_distance

    def get_clearer_side(self):
        return self.clearer_side

    # ========================================================
    # STATUS
    # ========================================================

    def get_status(self):

        return {
            'available': self.scan_ready,
            'front': self.front_min,
            'left': self.left_min,
            'right': self.right_min,
            'closest': self.closest_distance,
            'clearer_side': self.clearer_side
        }

    def print_status(self):

        print("")
        print("========== LIDAR STATUS ==========")
        print("Available :", self.scan_ready)

        if self.front_min is None:
            print("Front     : no valid return")
        else:
            print(
                "Front     : %.2f m"
                % self.front_min
            )

        if self.left_min is None:
            print("Left      : no valid return")
        else:
            print(
                "Left      : %.2f m"
                % self.left_min
            )

        if self.right_min is None:
            print("Right     : no valid return")
        else:
            print(
                "Right     : %.2f m"
                % self.right_min
            )

        if self.closest_distance is None:
            print("Closest   : None")
        else:
            print(
                "Closest   : %.2f m"
                % self.closest_distance
            )

        print(
            "Clearer   : %s"
            % str(self.clearer_side)
        )

        print("==================================")
        print("")


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == '__main__':

    rospy.init_node(
        'lidar_sensor_test',
        anonymous=True
    )

    lidar = LidarSensor()

    rospy.loginfo(
        "Waiting for LiDAR data..."
    )

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():

        lidar.print_status()

        rate.sleep()
