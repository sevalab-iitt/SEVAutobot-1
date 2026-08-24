# Robot state

# nano ~/catkin_ws/src/jetauto_llm/scripts/robot/robot_status.py

# -*- coding: utf-8 -*-

"""
STAGE 7 - ROBOT STATUS

Purpose:
    Maintains the current high-level state of the robot.

Responsibilities:
    - Track movement state
    - Track current action
    - Track direction
    - Track duration
    - Track LiDAR safety information
    - Provide status to the main LLM orchestrator

Python:
    Python 2 compatible
"""

import rospy


class RobotStatus(object):

    # ============================================================
    # STAGE 7 - INITIALIZATION
    # ============================================================

    def __init__(self):

        self.action = "stop"
        self.direction = None
        self.duration = 0.0

        self.moving = False
        self.obstacle_detected = False

        self.front_distance = None
        self.left_distance = None
        self.right_distance = None

        self.last_command = None

        rospy.loginfo("RobotStatus initialized")

    # ============================================================
    # STAGE 7 - MOVEMENT STATE
    # ============================================================

    def set_movement(self, action, direction=None, duration=0.0):

        self.action = action
        self.direction = direction
        self.duration = float(duration)

        if action == "stop":
            self.moving = False
        else:
            self.moving = True

    def set_stopped(self):

        self.action = "stop"
        self.direction = None
        self.duration = 0.0
        self.moving = False

    # ============================================================
    # STAGE 7 - COMMAND STATE
    # ============================================================

    def set_last_command(self, command):

        self.last_command = command

    # ============================================================
    # STAGE 7 - LIDAR STATE
    # ============================================================

    def update_lidar(
        self,
        front=None,
        left=None,
        right=None
    ):

        self.front_distance = front
        self.left_distance = left
        self.right_distance = right

    # ============================================================
    # STAGE 7 - OBSTACLE STATE
    # ============================================================

    def set_obstacle(self, detected):

        self.obstacle_detected = bool(detected)

    # ============================================================
    # STAGE 7 - STATUS
    # ============================================================

    def get_status(self):

        return {
            "action": self.action,
            "direction": self.direction,
            "duration": self.duration,
            "moving": self.moving,
            "obstacle_detected": self.obstacle_detected,
            "front_distance": self.front_distance,
            "left_distance": self.left_distance,
            "right_distance": self.right_distance,
            "last_command": self.last_command
        }

    # ============================================================
    # STAGE 7 - HUMAN READABLE STATUS
    # ============================================================

    def print_status(self):

        rospy.loginfo("========== ROBOT STATUS ==========")
        rospy.loginfo(
            "Action     : %s" % self.action
        )
        rospy.loginfo(
            "Direction  : %s" % self.direction
        )
        rospy.loginfo(
            "Duration   : %.2f s" % self.duration
        )
        rospy.loginfo(
            "Moving     : %s" % self.moving
        )
        rospy.loginfo(
            "Obstacle   : %s" % self.obstacle_detected
        )

        if self.front_distance is None:
            front = "no valid return"
        else:
            front = "%.2f m" % self.front_distance

        if self.left_distance is None:
            left = "no valid return"
        else:
            left = "%.2f m" % self.left_distance

        if self.right_distance is None:
            right = "no valid return"
        else:
            right = "%.2f m" % self.right_distance

        rospy.loginfo(
            "Front      : %s" % front
        )
        rospy.loginfo(
            "Left       : %s" % left
        )
        rospy.loginfo(
            "Right      : %s" % right
        )

        rospy.loginfo(
            "=================================")

"""
  python2 -c "import sys; sys.path.insert(0, '$HOME/catkin_ws/src/jetauto_llm/scripts'); from robot.robot_status import RobotStatus; print('ROBOT STATUS MODULE OK')"
"""
