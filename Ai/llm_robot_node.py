# ============================================================
# STAGE 1 — LLM COMMAND → JSON
# ============================================================
# Implemented:
# - User enters natural-language command
# - llama.cpp server processes command
# - LLM returns structured JSON
# - JSON is parsed and validated
#
# ============================================================
# STAGE 2 — REAL ROBOT CONTROL
# ============================================================
# New:
# - Publish geometry_msgs/Twist
# - Execute forward/backward/left/right
# - Automatically stop after requested duration
# - STOP command immediately publishes zero velocity
# - Keep LiDAR monitoring
# - Keep DRY_RUN safety option
# ============================================================

---

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import requests
import json
import math
import time

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class LLMRobotNode:

    def __init__(self):

        rospy.init_node("llm_robot_node")

        self.llm_url = "http://127.0.0.1:8081/completion"

        # Keep True until physical movement is fully tested.
        self.dry_run = True

        self.cmd_vel_pub = rospy.Publisher(
            "/jetauto_controller/cmd_vel",
            Twist,
            queue_size=10
        )

        self.scan_sub = rospy.Subscriber(
            "/scan",
            LaserScan,
            self.scan_callback
        )

        self.front_distance = float("inf")
        self.left_distance = float("inf")
        self.right_distance = float("inf")

        rospy.loginfo("LLM Robot Node started")
        rospy.loginfo("DRY_RUN = %s", self.dry_run)

    # ==========================================================
    # LIDAR
    # ==========================================================

    def is_valid_range(self, value, msg):

        if math.isnan(value):
            return False

        if math.isinf(value):
            return False

        if value < msg.range_min:
            return False

        if value > msg.range_max:
            return False

        return True

    def sector_min(self, msg, start_angle, end_angle):

        values = []

        for i, distance in enumerate(msg.ranges):

            angle = (
                msg.angle_min +
                i * msg.angle_increment
            )

            if start_angle <= angle <= end_angle:

                if self.is_valid_range(
                    distance,
                    msg
                ):
                    values.append(distance)

        if values:
            return min(values)

        return float("inf")

    def scan_callback(self, msg):

        if not msg.ranges:
            return

        # Front: -15 to +15 degrees
        self.front_distance = self.sector_min(
            msg,
            math.radians(-15),
            math.radians(15)
        )

        # Left: 60 to 120 degrees
        self.left_distance = self.sector_min(
            msg,
            math.radians(60),
            math.radians(120)
        )

        # Right: -120 to -60 degrees
        self.right_distance = self.sector_min(
            msg,
            math.radians(-120),
            math.radians(-60)
        )

    # ==========================================================
    # LLM
    # ==========================================================

    def ask_llm(self, user_command):

        prompt = """
You are a robot command parser.

Convert the user command into ONE JSON object.

Allowed actions:
move
stop
turn

Allowed directions:
forward
backward
left
right

Output ONLY the JSON object.

Do NOT explain.
Do NOT add text.
Do NOT output multiple commands.
Do NOT output Markdown.

Examples:

User: Move forward for 2 seconds.
Output:
{"action":"move","direction":"forward","duration":2}

User: Move backward for 3 seconds.
Output:
{"action":"move","direction":"backward","duration":3}

User: Turn left.
Output:
{"action":"turn","direction":"left","duration":1}

User: Turn right.
Output:
{"action":"turn","direction":"right","duration":1}

User: Stop.
Output:
{"action":"stop"}

User command:
""" + user_command + """

Output:
"""

        payload = {
            "prompt": prompt,
            "n_predict": 40,
            "temperature": 0.0,
            "stop": [
                "\nUser:",
                "\nOutput:"
            ]
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

            content = data.get(
                "content",
                ""
            ).strip()

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

    # ==========================================================
    # JSON PARSER
    # ==========================================================

    def parse_command(self, response):

        if not response:
            return None

        try:

            # Remove Markdown fences if the model adds them.
            response = response.replace(
                "```json",
                ""
            )

            response = response.replace(
                "```",
                ""
            )

            response = response.strip()

            start = response.find("{")
            end = response.rfind("}")

            if start == -1 or end == -1:
                rospy.logerr(
                    "No JSON object found."
                )
                return None

            json_text = response[
                start:end + 1
            ]

            command = json.loads(
                json_text
            )

            return command

        except Exception as e:

            rospy.logerr(
                "Invalid JSON: %s",
                str(e)
            )

            return None

    # ==========================================================
    # VALIDATION
    # ==========================================================

    def validate_command(self, command):

        if not isinstance(
            command,
            dict
        ):
            return False

        action = command.get(
            "action"
        )

        if action not in [
            "move",
            "stop",
            "turn"
        ]:
            rospy.logerr(
                "Invalid action: %s",
                action
            )
            return False

        if action == "stop":
            return True

        direction = command.get(
            "direction"
        )

        if direction not in [
            "forward",
            "backward",
            "left",
            "right"
        ]:
            rospy.logerr(
                "Invalid direction: %s",
                direction
            )
            return False

        try:

            duration = float(
                command.get(
                    "duration",
                    1
                )
            )

        except Exception:

            rospy.logerr(
                "Invalid duration."
            )

            return False

        # Safety limit
        if duration <= 0:
            return False

        if duration > 10:
            rospy.logerr(
                "Duration exceeds safety limit."
            )
            return False

        return True

    # ==========================================================
    # EXECUTE
    # ==========================================================

    def execute_command(self, command):

        if not self.validate_command(
            command
        ):
            return

        action = command.get(
            "action"
        )

        # ------------------------------------------------------
        # STOP
        # ------------------------------------------------------

        if action == "stop":

            rospy.loginfo(
                "STOP command."
            )

            self.stop_robot()

            return

        direction = command.get(
            "direction"
        )

        duration = float(
            command.get(
                "duration",
                1
            )
        )

        # ------------------------------------------------------
        # FORWARD SAFETY CHECK
        # ------------------------------------------------------

        if direction == "forward":

            if (
                not math.isnan(
                    self.front_distance
                )
                and
                not math.isinf(
                    self.front_distance
                )
            ):

                rospy.loginfo(
                    "LiDAR front distance: %.2f m",
                    self.front_distance
                )

                if self.front_distance < 0.30:

                    rospy.logwarn(
                        "Obstacle too close. "
                        "Forward movement cancelled."
                    )

                    self.stop_robot()

                    return

        # ------------------------------------------------------
        # DRY RUN
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # REAL ROBOT MOVEMENT
        # ------------------------------------------------------

        twist = Twist()

        linear_speed = 0.20
        angular_speed = 0.50

        if action == "move":

            if direction == "forward":
                twist.linear.x = linear_speed

            elif direction == "backward":
                twist.linear.x = -linear_speed

        elif action == "turn":

            if direction == "left":
                twist.angular.z = angular_speed

            elif direction == "right":
                twist.angular.z = -angular_speed

        rate = rospy.Rate(10)

        start_time = time.time()

        while (
            time.time() - start_time
        ) < duration:

            if rospy.is_shutdown():
                break

            # Emergency LiDAR check
            if direction == "forward":

                if (
                    not math.isnan(
                        self.front_distance
                    )
                    and
                    not math.isinf(
                        self.front_distance
                    )
                ):

                    if self.front_distance < 0.30:

                        rospy.logwarn(
                            "Obstacle detected! "
                            "Emergency stop."
                        )

                        break

            self.cmd_vel_pub.publish(
                twist
            )

            rate.sleep()

        self.stop_robot()

    # ==========================================================
    # STOP
    # ==========================================================

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

    # ==========================================================
    # LIDAR STATUS
    # ==========================================================

    def format_distance(self, value):

        if (
            not math.isnan(value)
            and
            not math.isinf(value)
        ):
            return "%.2f m" % value

        return "no valid return"

    def print_lidar_state(self):

        rospy.loginfo(
            "[DRY RUN] LiDAR | "
            "Front: %s | Left: %s | Right: %s",
            self.format_distance(
                self.front_distance
            ),
            self.format_distance(
                self.left_distance
            ),
            self.format_distance(
                self.right_distance
            )
        )

    # ==========================================================
    # MAIN LOOP
    # ==========================================================

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

            # Direct emergency stop
            if user_command.lower() in [
                "stop",
                "halt",
                "emergency stop"
            ]:

                self.stop_robot()

                rospy.loginfo(
                    "Robot stopped."
                )

                continue

            # Ask LLM
            response = self.ask_llm(
                user_command
            )

            if response is None:
                continue

            # Parse JSON
            command = self.parse_command(
                response
            )

            if command is None:
                continue

            rospy.loginfo(
                "Parsed command: %s",
                json.dumps(command)
            )

            # Execute
            self.execute_command(
                command
            )


# ==============================================================
# ENTRY POINT
# ==============================================================

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

---
jetauto@jetauto-desktop:~/catkin_ws$ rosrun jetauto_llm llm_robot_node.py
[INFO] [1787495792.454782]: LLM Robot Node started
[INFO] [1787495792.459603]: DRY_RUN = True
Enter robot command: Move forward for 2 seconds.
[INFO] [1787495799.044617]: User command: Move forward for 2 seconds.
[INFO] [1787495806.929139]: LLM response: {"action":"move","direction":"forward","duration":2}
[INFO] [1787495806.934492]: Parsed command: {"action": "move", "duration": 2, "direction": "forward"}
[INFO] [1787495806.939826]: [DRY RUN] Would execute: move forward for 2.00 seconds
[INFO] [1787495806.946225]: [DRY RUN] LiDAR | Front: no valid return | Left: no valid return | Right: 0.50 m
Enter robot command: Move forward for 2 seconds.
[INFO] [1787495875.643300]: User command: Move forward for 2 seconds.
[INFO] [1787495879.321861]: LLM response: {"action":"move","direction":"forward","duration":2}
[INFO] [1787495879.327486]: Parsed command: {"action": "move", "duration": 2, "direction": "forward"}
[INFO] [1787495879.331905]: [DRY RUN] Would execute: move forward for 2.00 seconds
[INFO] [1787495879.336578]: [DRY RUN] LiDAR | Front: no valid return | Left: 0.20 m | Right: 0.50 m
Enter robot command: Move backward for 2 seconds.
[INFO] [1787495884.648469]: User command: Move backward for 2 seconds.
[INFO] [1787495888.981519]: LLM response: {"action":"move","direction":"backward","duration":2}
[INFO] [1787495888.986599]: Parsed command: {"action": "move", "duration": 2, "direction": "backward"}
[INFO] [1787495888.991602]: [DRY RUN] Would execute: move backward for 2.00 seconds
[INFO] [1787495888.996772]: [DRY RUN] LiDAR | Front: no valid return | Left: 0.20 m | Right: 0.50 m
Enter robot command: Turn left for 2 seconds.
[INFO] [1787495903.184956]: User command: Turn left for 2 seconds.
[INFO] [1787495908.118601]: LLM response: {"action":"turn","direction":"left","duration":2}
[INFO] [1787495908.123646]: Parsed command: {"action": "turn", "duration": 2, "direction": "left"}
[INFO] [1787495908.128181]: [DRY RUN] Would execute: turn left for 2.00 seconds
[INFO] [1787495908.132474]: [DRY RUN] LiDAR | Front: no valid return | Left: 0.20 m | Right: 0.50 m
Enter robot command: Turn right for 2 seconds.
[INFO] [1787495912.402220]: User command: Turn right for 2 seconds.
[INFO] [1787495916.693335]: LLM response: {"action":"turn","direction":"right","duration":2}
[INFO] [1787495916.698619]: Parsed command: {"action": "turn", "duration": 2, "direction": "right"}
[INFO] [1787495916.703784]: [DRY RUN] Would execute: turn right for 2.00 seconds
[INFO] [1787495916.709076]: [DRY RUN] LiDAR | Front: no valid return | Left: 0.20 m | Right: 0.50 m
Enter robot command: Stop.
[INFO] [1787495919.568104]: User command: Stop.
[INFO] [1787495921.553681]: LLM response: {"action":"stop"}
[INFO] [1787495921.558952]: Parsed command: {"action": "stop"}
[INFO] [1787495921.563870]: STOP command.
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


