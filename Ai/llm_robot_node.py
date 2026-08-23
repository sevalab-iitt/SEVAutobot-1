#!/usr/bin/env python3

import json
import requests
import rospy
from geometry_msgs.msg import Twist


LLM_URL = "http://127.0.0.1:8081/completion"

DRY_RUN = True

MAX_DURATION = 5.0
LINEAR_SPEED = 0.15
ANGULAR_SPEED = 0.5


class LLMRobotNode:

    def __init__(self):
        rospy.init_node("llm_robot_node")

        self.cmd_pub = rospy.Publisher(
            "/jetauto_controller/cmd_vel",
            Twist,
            queue_size=10
        )

        rospy.loginfo("LLM Robot Node started")
        rospy.loginfo("DRY_RUN = %s", DRY_RUN)

    def ask_llm(self, user_command):

        prompt = (
            "You control a mobile robot. "
            "Convert the user command into JSON. "
            "Allowed actions: move, stop, turn. "
            "Allowed directions: forward, backward, left, right. "
            "Output ONLY valid JSON. "
            "If duration is not specified, use 1 second. "
            "User command: " + user_command
        )

        payload = {
            "prompt": prompt,
            "n_predict": 40,
            "temperature": 0
        }

        response = requests.post(
            LLM_URL,
            json=payload,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        content = result["content"].strip()

        rospy.loginfo("LLM response: %s", content)

        return json.loads(content)

    def execute_command(self, command):

        action = command.get("action")
        direction = command.get("direction")
        duration = float(command.get("duration", 1))

        # Safety validation
        allowed_actions = ["move", "stop", "turn"]
        allowed_directions = ["forward", "backward", "left", "right"]

        if action not in allowed_actions:
            rospy.logwarn("Invalid action: %s", action)
            return

        if direction is not None and direction not in allowed_directions:
            rospy.logwarn("Invalid direction: %s", direction)
            return

        duration = min(max(duration, 0.1), MAX_DURATION)

        if action == "stop":
            self.stop_robot()
            return

        twist = Twist()

        if action == "move":

            if direction == "forward":
                twist.linear.x = LINEAR_SPEED

            elif direction == "backward":
                twist.linear.x = -LINEAR_SPEED

        elif action == "turn":

            if direction == "left":
                twist.angular.z = ANGULAR_SPEED

            elif direction == "right":
                twist.angular.z = -ANGULAR_SPEED

        if DRY_RUN:

            rospy.loginfo(
                "[DRY RUN] Would execute: %s %s for %.1f seconds",
                action,
                direction,
                duration
            )

            return

        rospy.loginfo(
            "Executing: %s %s for %.1f seconds",
            action,
            direction,
            duration
        )

        start_time = rospy.Time.now()

        rate = rospy.Rate(20)

        while (
            rospy.Time.now() - start_time
        ).to_sec() < duration and not rospy.is_shutdown():

            self.cmd_pub.publish(twist)
            rate.sleep()

        self.stop_robot()

    def stop_robot(self):

        twist = Twist()

        if DRY_RUN:
            rospy.loginfo("[DRY RUN] Would STOP robot")
            return

        self.cmd_pub.publish(twist)

        rospy.loginfo("Robot stopped")

    def run_command(self, user_command):

        rospy.loginfo("User command: %s", user_command)

        try:

            command = self.ask_llm(user_command)

            rospy.loginfo(
                "Parsed command: %s",
                json.dumps(command)
            )

            self.execute_command(command)

        except requests.exceptions.RequestException as e:

            rospy.logerr("LLM request failed: %s", e)

        except json.JSONDecodeError as e:

            rospy.logerr("Invalid JSON from LLM: %s", e)

        except Exception as e:

            rospy.logerr("Command failed: %s", e)


if __name__ == "__main__":

    node = LLMRobotNode()

    try:

        command = input(
            "Enter robot command: "
        )

        node.run_command(command)

    except KeyboardInterrupt:

        pass
