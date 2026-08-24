 # Forward/back/turn/stop

# cd ~/catkin_ws/src/jetauto_llm

#nano scripts/robot/movement.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
JETAUTO LLM ROBOT
=================

Stage 1-8 compatible movement module.

Purpose:
    Handles low-level robot movement through:
        /jetauto_controller/cmd_vel

Supported:
    - forward
    - backward
    - left
    - right
    - stop

This module does NOT:
    - communicate with the LLM
    - read LiDAR
    - process cameras
    - control the arm

Those will be separate modules.

ROS:
    Ubuntu 18.04
    ROS Melodic
    Python 2.7 compatible
"""

import rospy
from geometry_msgs.msg import Twist


class MovementController(object):

    def __init__(self):
        """
        Initialize the movement controller.
        """

        self.cmd_vel_topic = "/jetauto_controller/cmd_vel"

        # Default speeds.
        # These can later be moved to robot_config.yaml.
        self.linear_speed = 0.10
        self.angular_speed = 0.50

        self.cmd_pub = rospy.Publisher(
            self.cmd_vel_topic,
            Twist,
            queue_size=10
        )

        # Give ROS publisher time to connect.
        rospy.sleep(0.2)

        rospy.loginfo(
            "MovementController initialized: %s",
            self.cmd_vel_topic
        )

    # ============================================================
    # STAGE 1-4:
    # BASIC MOVEMENT
    # ============================================================

    def forward(self, speed=None):
        """
        Move robot forward.
        """

        if speed is None:
            speed = self.linear_speed

        msg = Twist()
        msg.linear.x = abs(float(speed))

        self.cmd_pub.publish(msg)

    def backward(self, speed=None):
        """
        Move robot backward.
        """

        if speed is None:
            speed = self.linear_speed

        msg = Twist()
        msg.linear.x = -abs(float(speed))

        self.cmd_pub.publish(msg)

    def left(self, speed=None):
        """
        Turn robot left.
        """

        if speed is None:
            speed = self.angular_speed

        msg = Twist()
        msg.angular.z = abs(float(speed))

        self.cmd_pub.publish(msg)

    def right(self, speed=None):
        """
        Turn robot right.
        """

        if speed is None:
            speed = self.angular_speed

        msg = Twist()
        msg.angular.z = -abs(float(speed))

        self.cmd_pub.publish(msg)

    # ============================================================
    # STAGE 1-8:
    # STOP
    # ============================================================

    def stop(self):
        """
        Immediately stop the robot.
        """

        msg = Twist()

        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0

        self.cmd_pub.publish(msg)

        rospy.loginfo("Robot STOPPED")

    # ============================================================
    # GENERIC MOVEMENT
    # ============================================================

    def execute(self, direction, duration):
        """
        Execute a movement for a specified duration.

        Example:

            execute("forward", 2)
            execute("left", 1)
        """

        try:
            duration = float(duration)
        except (TypeError, ValueError):
            rospy.logwarn(
                "Invalid movement duration: %s",
                str(duration)
            )
            self.stop()
            return False

        if duration <= 0.0:
            rospy.logwarn(
                "Movement duration must be > 0"
            )
            self.stop()
            return False

        direction = str(direction).lower().strip()

        rospy.loginfo(
            "Movement: %s for %.2f seconds",
            direction,
            duration
        )

        if direction == "forward":
            self.forward()

        elif direction == "backward":
            self.backward()

        elif direction == "left":
            self.left()

        elif direction == "right":
            self.right()

        else:
            rospy.logwarn(
                "Unknown movement direction: %s",
                direction
            )
            self.stop()
            return False

        # Keep publishing while moving.
        #
        # This is safer than publishing only once because
        # the motor controller receives continuous commands.
        rate = rospy.Rate(20)

        start_time = rospy.Time.now()

        while not rospy.is_shutdown():

            elapsed = (
                rospy.Time.now() - start_time
            ).to_sec()

            if elapsed >= duration:
                break

            rate.sleep()

            # Continue command.
            if direction == "forward":
                self.forward()

            elif direction == "backward":
                self.backward()

            elif direction == "left":
                self.left()

            elif direction == "right":
                self.right()

        self.stop()

        return True

    # ============================================================
    # SAFETY
    # ============================================================

    def emergency_stop(self):
        """
        Emergency stop.

        Kept separate from normal stop so that future
        obstacle-avoidance and safety modules can call it.
        """

        rospy.logwarn(
            "EMERGENCY STOP"
        )

        self.stop()

    # ============================================================
    # VELOCITY CONTROL
    # ============================================================

    def set_velocity(self, linear_x=0.0, angular_z=0.0):
        """
        Direct velocity control.

        Useful later for:
            - obstacle avoidance
            - visual servoing
            - navigation
            - pixel-to-distance control
            - autonomous behaviors
        """

        msg = Twist()

        msg.linear.x = float(linear_x)
        msg.angular.z = float(angular_z)

        self.cmd_pub.publish(msg)

    # ============================================================
    # TEST
    # ============================================================

    def test_stop(self):
        """
        Simple module test.
        """

        rospy.loginfo(
            "MovementController test: STOP"
        )

        self.stop()


# ================================================================
# STANDALONE TEST
# ================================================================

if __name__ == "__main__":

    rospy.init_node(
        "movement_controller_test"
    )

    controller = MovementController()

    rospy.loginfo(
        "Movement module test started."
    )

    controller.test_stop()

    rospy.loginfo(
        "Movement module test finished."
    )


"""
source ~/catkin_ws/devel/setup.bash

python2 -c "import sys; sys.path.insert(0, '$HOME/catkin_ws/src/jetauto_llm/scripts'); from robot.movement import MovementController; print('MOVEMENT MODULE OK')"
"""
