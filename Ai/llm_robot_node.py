#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import requests
import json
import math

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class LLMRobotNode:

    def __init__(self):

        rospy.init_node("llm_robot_node")

        # --------------------------------------------------
        # PARAMETERS
        # --------------------------------------------------

        self.llm_url = "http://127.0.0.1:8081/completion"

        # Keep DRY_RUN = True for testing.
        # Change to False only when we are ready to move
        # the physical robot.
        self.dry_run = True

        # Robot movement topic
        self.cmd_vel_pub = rospy.Publisher(
            "/jetauto_controller/cmd_vel",
            Twist,
            queue_size=10
        )

        # LiDAR
        self.scan_sub = rospy.Subscriber(
            "/scan",
            LaserScan,
            self.scan_callback
        )

        # Latest LiDAR values
        self.front_distance = float("inf")
        self.left_distance = float("inf")
        self.right_distance = float("inf")

        rospy.loginfo("LLM Robot Node started")
        rospy.loginfo("DRY_RUN = %s", self.dry_run)

    # ======================================================
    # LIDAR
    # ======================================================

    def scan_callback(self, msg):

        ranges = msg.ranges

        if not ranges:
            return

        def valid_distance(value):

            # Ignore:
            #   NaN
            #   +inf
            #   -inf
            #   zero
            #   values outside LiDAR limits

            if math.isnan(value):
                return False

            if math.isinf(value):
                return False

            if value < msg.range_min:
                return False

            if value > msg.range_max:
                return False

            return True

        def sector_min(start_angle, end_angle):

            values = []

            for i, distance in enumerate(ranges):

                angle = msg.angle_min + i * msg.angle_increment

                if start_angle <= angle <= end_angle:

                    if valid_distance(distance):
                        values.append(distance)

            if values:
                return min(values)

            return float("inf")

        # --------------------------------------------------
        # LiDAR coordinate convention
        #
        #       +90 = left
        #         0 = front
        #       -90 = right
        # --------------------------------------------------

        self.front_distance = sector_min(
            math.radians(-15),
            math.radians(15)
        )

        self.left_distance = sector_min(
            math.radians(60),
            math.radians(120)
        )

        self.right_distance = sector_min(
            math.radians(-120),
            math.radians(-60)
        )

    # ======================================================
    # LLM
    # ======================================================

    def ask_llm(self, user_command):

        system_prompt = """
You control a mobile robot.

Convert the user's natural-language command into ONLY valid JSON.

Allowed actions:
- move
- stop
- turn

Allowed directions:
- forward
- backward
- left
- right

JSON format examples:

Move forward for 2 seconds:
{"action":"move","direction":"forward","duration":2}

Move backward for 3 seconds:
{"action":"move","direction":"backward","duration":3}

Turn left:
{"action":"turn","direction":"left","duration":1}

Turn right:
{"action":"turn","direction":"right","duration":1}

Stop:
{"action":"stop"}

Rules:
- Output ONLY JSON.
- Do not explain anything.
- Do not use Markdown.
- Do not add text before or after JSON.
"""

        prompt = system_prompt + "\nUser command: " + user_command

        payload = {
            "prompt": prompt,
            "n_predict": 40,
            "temperature": 0.0
        }

        try:

            response = requests.post(
                self.llm_url,
                headers={
                    "Content-Type": "application/json"
                },
                data=json.dumps(payload),
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            content = data.get("content", "").strip()

            rospy.loginfo(
                "LLM response: %s",
                content
            )

            return content

        except Exception as e:

            rospy.logerr(
                "LLM request failed: %s",
                str(e)
            )

            return None

    # ======================================================
    # JSON PARSER
    # ======================================================

    def parse_command(self, response):

        if not response:
            return None

        try:

            # Remove accidental Markdown fences
            response = response.replace(
                "```json",
                ""
            )

            response = response.replace(
                "```",
                ""
            )

            response = response.strip()

            # Find JSON object if model adds extra text
            start = response.find("{")
            end = response.rfind("}")

            if start == -1 or end == -1:
                rospy.logerr(
                    "No JSON object found in LLM response"
                )
                return None

            json_text = response[start:end + 1]

            command = json.loads(json_text)

            rospy.loginfo(
                "Parsed command: %s",
                json.dumps(command)
            )

            return command

        except Exception as e:

            rospy.logerr(
                "Invalid JSON from LLM: %s",
                str(e)
            )

            return None

    # ======================================================
    # COMMAND VALIDATION
    # ======================================================

    def validate_command(self, command):

        if not isinstance(command, dict):
            return False

        action = command.get("action")

        allowed_actions = [
            "move",
            "stop",
            "turn"
        ]

        if action not in allowed_actions:
            rospy.logerr(
                "Invalid action: %s",
                action
            )
            return False

        if action != "stop":

            direction = command.get("direction")

            allowed_directions = [
                "forward",
                "backward",
                "left",
                "right"
            ]

            if direction not in allowed_directions:

                rospy.logerr(
                    "Invalid direction: %s",
                    direction
                )

                return False

            duration = command.get(
                "duration",
                1
            )

            try:

                duration = float(duration)

            except:

                rospy.logerr(
                    "Invalid duration"
                )

                return False

            # Safety limit
            if duration <= 0 or duration > 10:

                rospy.logerr(
                    "Unsafe duration: %.2f",
                    duration
                )

                return False

        return True

    # ======================================================
    # ROBOT MOVEMENT
    # ======================================================

    def execute_command(self, command):

        if not self.validate_command(command):
            return

        action = command["action"]

        # --------------------------------------------------
        # STOP
        # --------------------------------------------------

        if action == "stop":

            rospy.loginfo(
                "Executing STOP"
            )

            self.stop_robot()

            return

        direction = command["direction"]

        duration = float(
            command.get(
                "duration",
                1
            )
        )

        # --------------------------------------------------
        # SAFETY CHECK
        # --------------------------------------------------

        # Only block forward movement when a REAL
        # obstacle is detected.

        if direction == "forward":

            if math.isfinite(
                self.front_distance
            ):

                rospy.loginfo(
                    "LiDAR front distance: %.2f m",
                    self.front_distance
                )

                # Emergency stop distance
                if self.front_distance < 0.30:

                    rospy.logwarn(
                        "Obstacle too close! "
                        "Forward movement cancelled."
                    )

                    self.stop_robot()

                    return

        # --------------------------------------------------
        # DRY RUN
        # --------------------------------------------------

        if self.dry_run:

            rospy.loginfo(
                "[DRY RUN] Would execute: "
                "%s %s for %.2f seconds",
                action,
                direction,
                duration
            )

            self.print_lidar_state()

            return

        # --------------------------------------------------
        # REAL MOVEMENT
        # --------------------------------------------------

        twist = Twist()

        speed = 0.2

        if action == "move":

            if direction == "forward":

                twist.linear.x = speed

            elif direction == "backward":

                twist.linear.x = -speed

        elif action == "turn":

            turn_speed = 0.5

            if direction == "left":

                twist.angular.z = turn_speed

            elif direction == "right":

                twist.angular.z = -turn_speed

        rospy.loginfo(
            "Executing: %s %s for %.2f seconds",
            action,
            direction,
            duration
        )

        rate = rospy.Rate(10)

        start_time = rospy.Time.now()

        while (
            rospy.Time.now() - start_time
        ).to_sec() < duration:

            # Continuous emergency check
            if direction == "forward":

                if math.isfinite(
                    self.front_distance
                ):

                    if self.front_distance < 0.30:

                        rospy.logwarn(
                            "Obstacle detected during movement!"
                        )

                        break

            self.cmd_vel_pub.publish(
                twist
            )

            rate.sleep()

        self.stop_robot()

    # ======================================================
    # STOP ROBOT
    # ======================================================

    def stop_robot(self):

        twist = Twist()

        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0

        self.cmd_vel_pub.publish(
            twist
        )

    # ======================================================
    # LIDAR STATUS
    # ======================================================

    def print_lidar_state(self):

        def format_distance(value):

            if math.isfinite(value):

                return "%.2f m" % value

            return "no valid return"

        rospy.loginfo(
            "[DRY RUN] LiDAR | "
            "Front: %s | Left: %s | Right: %s",
            format_distance(
                self.front_distance
            ),
            format_distance(
                self.left_distance
            ),
            format_distance(
                self.right_distance
            )
        )

    # ======================================================
    # MAIN LOOP
    # ======================================================

    def run(self):

        while not rospy.is_shutdown():

            try:

                user_command = raw_input(
                    "Enter robot command: "
                )

            except EOFError:

                break

            user_command = user_command.strip()

            if not user_command:
                continue

            rospy.loginfo(
                "User command: %s",
                user_command
            )

            # --------------------------------------------------
            # Direct emergency stop
            # --------------------------------------------------

            if user_command.lower() in [
                "stop",
                "emergency stop",
                "halt"
            ]:

                self.stop_robot()

                rospy.loginfo(
                    "Robot stopped."
                )

                continue

            # --------------------------------------------------
            # Ask LLM
            # --------------------------------------------------

            response = self.ask_llm(
                user_command
            )

            if response is None:

                rospy.logerr(
                    "No response from LLM."
                )

                continue

            # --------------------------------------------------
            # Parse JSON
            # --------------------------------------------------

            command = self.parse_command(
                response
            )

            if command is None:

                rospy.logerr(
                    "Could not parse LLM command."
                )

                continue

            # --------------------------------------------------
            # Execute
            # --------------------------------------------------

            self.execute_command(
                command
            )


# ==========================================================
# PROGRAM ENTRY
# ==========================================================

if __name__ == "__main__":

    try:

        node = LLMRobotNode()

        node.run()

    except rospy.ROSInterruptException:

        pass

"""
Save 
Ctrl+O
Enter
Ctrl+X
---
chmod +x ~/catkin_ws/src/jetauto_llm/scripts/llm_robot_node.py
---
cd ~/catkin_ws
catkin_make
---
source ~/catkin_ws/devel/setup.bash
---
rosrun jetauto_llm llm_robot_node.py

and enter:
Move forward for 2 seconds.

output we got:-

jetauto@jetauto-desktop:~/catkin_ws$ rosrun jetauto_llm llm_robot_node.py
[INFO] [1787493942.577492]: LLM Robot Node started
[INFO] [1787493942.583887]: DRY_RUN = True
Enter robot command: Move forward for 2 seconds.
[INFO] [1787493969.367135]: User command: Move forward for 2 seconds.
[INFO] [1787493975.567392]: LLM response: {"action": "move", "direction": "forward", "duration": 2}
[INFO] [1787493975.573785]: Parsed command: {"action": "move", "direction": "forward", "duration": 2}
[INFO] [1787493975.579202]: [DRY RUN] Would execute: move forward for 2.0 seconds
"""
---

#Python Dependencies
"""
sudo apt-get update
sudo apt-get install python-requests

verify using:
python -c "import requests; print(requests.__version__)"

run: 
source ~/catkin_ws/devel/setup.bash
rosrun jetauto_llm llm_robot_node.py
"""
