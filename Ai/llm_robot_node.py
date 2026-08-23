#!/usr/bin/env python

import rospy
import requests
import json
import math
import time

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class LLMRobotNode:

    # ============================================================
    # STAGE 1 — LLM COMMAND → JSON
    # ============================================================
    # - User enters natural-language command
    # - Command is sent to llama.cpp
    # - Qwen converts it into structured JSON
    # - JSON is parsed and validated
    #
    # ============================================================
    # STAGE 2 — REAL ROBOT CONTROL
    # ============================================================
    # NEW:
    # - Publish geometry_msgs/Twist
    # - Control /jetauto_controller/cmd_vel
    # - Forward / backward movement
    # - Left / right turning
    # - Automatic stop after duration
    # - STOP command immediately stops robot
    #
    # DRY_RUN remains available for safety.
    # Change DRY_RUN = False only when ready.
    # ============================================================

    def __init__(self):

        rospy.init_node("llm_robot_node")

        rospy.loginfo("LLM Robot Node started")

        # --------------------------------------------------------
        # SAFETY SWITCH
        # --------------------------------------------------------
        # True  = do not move robot
        # False = actual robot movement
        #
        self.DRY_RUN = True

        rospy.loginfo("DRY_RUN = %s", self.DRY_RUN)

        # --------------------------------------------------------
        # LLM SERVER
        # --------------------------------------------------------

        self.llm_url = "http://127.0.0.1:8081/completion"

        # --------------------------------------------------------
        # ROS PUBLISHER
        # --------------------------------------------------------

        self.cmd_vel_pub = rospy.Publisher(
            "/jetauto_controller/cmd_vel",
            Twist,
            queue_size=10
        )

        # --------------------------------------------------------
        # LIDAR
        # --------------------------------------------------------

        self.front_distance = float("inf")
        self.left_distance = float("inf")
        self.right_distance = float("inf")

        self.scan_sub = rospy.Subscriber(
            "/scan",
            LaserScan,
            self.scan_callback
        )

        # --------------------------------------------------------
        # ROBOT SPEED
        # --------------------------------------------------------

        self.linear_speed = 0.20
        self.angular_speed = 0.50

        rospy.sleep(1.0)

    # ============================================================
    # STAGE 1 — LiDAR CALLBACK
    # ============================================================

    def scan_callback(self, msg):

        ranges = msg.ranges

        if not ranges:
            return

        total = len(ranges)

        # Convert angle to index
        def angle_to_index(angle):

            index = int(
                (angle - msg.angle_min)
                / msg.angle_increment
            )

            if index < 0:
                index = 0

            if index >= total:
                index = total - 1

            return index

        # --------------------------------------------------------
        # Helper for valid LiDAR values
        # --------------------------------------------------------

        def valid_values(values):

            result = []

            for value in values:

                if (
                    value >= msg.range_min
                    and value <= msg.range_max
                    and not math.isnan(value)
                    and not math.isinf(value)
                ):
                    result.append(value)

            return result

        # --------------------------------------------------------
        # Front
        # --------------------------------------------------------

        front_center = angle_to_index(0.0)

        front_width = 15

        front_values = valid_values(
            ranges[
                max(0, front_center - front_width):
                min(total, front_center + front_width + 1)
            ]
        )

        # --------------------------------------------------------
        # Left
        # --------------------------------------------------------

        left_center = angle_to_index(math.pi / 2.0)

        left_values = valid_values(
            ranges[
                max(0, left_center - front_width):
                min(total, left_center + front_width + 1)
            ]
        )

        # --------------------------------------------------------
        # Right
        # --------------------------------------------------------

        right_center = angle_to_index(-math.pi / 2.0)

        right_values = valid_values(
            ranges[
                max(0, right_center - front_width):
                min(total, right_center + front_width + 1)
            ]
        )

        # --------------------------------------------------------
        # Use minimum valid distance
        # --------------------------------------------------------

        if front_values:
            self.front_distance = min(front_values)
        else:
            self.front_distance = float("inf")

        if left_values:
            self.left_distance = min(left_values)
        else:
            self.left_distance = float("inf")

        if right_values:
            self.right_distance = min(right_values)
        else:
            self.right_distance = float("inf")

    # ============================================================
    # STAGE 1 — LLM REQUEST
    # ============================================================

    def ask_llm(self, user_command):

        prompt = """
You control a mobile robot.

Convert the user's command into ONLY one valid JSON object.

Allowed actions:
- move
- turn
- stop

Allowed directions:
- forward
- backward
- left
- right

For move:
{"action":"move","direction":"forward","duration":2}

For turn:
{"action":"turn","direction":"left","duration":2}

For stop:
{"action":"stop"}

Rules:
- Output ONLY JSON.
- Do not explain anything.
- Do not output multiple commands.
- duration must be a number in seconds.

User command:
""" + user_command

        payload = {
            "prompt": prompt,
            "n_predict": 40,
            "temperature": 0
        }

        try:

            response = requests.post(
                self.llm_url,
                json=payload,
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

    # ============================================================
    # STAGE 1 — JSON EXTRACTION
    # ============================================================

    def parse_command(self, response):

        if not response:
            return None

        # --------------------------------------------------------
        # First try complete response
        # --------------------------------------------------------

        try:

            command = json.loads(response)

            return command

        except Exception:
            pass

        # --------------------------------------------------------
        # Try extracting JSON from response
        # --------------------------------------------------------

        start = response.find("{")
        end = response.rfind("}")

        if start == -1 or end == -1:
            return None

        json_text = response[start:end + 1]

        try:

            command = json.loads(json_text)

            return command

        except Exception as e:

            rospy.logerr(
                "JSON parsing failed: %s",
                str(e)
            )

            return None

    # ============================================================
    # STAGE 1 — COMMAND VALIDATION
    # ============================================================

    def validate_command(self, command):

        if not isinstance(command, dict):
            return False

        action = command.get("action")

        # --------------------------------------------------------
        # STOP
        # --------------------------------------------------------

        if action == "stop":

            return True

        # --------------------------------------------------------
        # MOVE / TURN
        # --------------------------------------------------------

        if action not in ["move", "turn"]:
            return False

        direction = command.get("direction")

        if direction not in [
            "forward",
            "backward",
            "left",
            "right"
        ]:
            return False

        try:

            duration = float(
                command.get("duration", 0)
            )

        except Exception:

            return False

        # --------------------------------------------------------
        # Safety limits
        # --------------------------------------------------------

        if duration <= 0:
            return False

        if duration > 10:
            rospy.logwarn(
                "Duration limited to 10 seconds"
            )

            command["duration"] = 10.0

        return True

    # ============================================================
    # STAGE 2 — PUBLISH VELOCITY
    # ============================================================

    def publish_velocity(
        self,
        linear_x=0.0,
        angular_z=0.0
    ):

        msg = Twist()

        msg.linear.x = linear_x
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = angular_z

        self.cmd_vel_pub.publish(msg)

    # ============================================================
    # STAGE 2 — STOP ROBOT
    # ============================================================

    def stop_robot(self):

        self.publish_velocity(
            0.0,
            0.0
        )

        rospy.loginfo(
            "Robot STOPPED"
        )

    # ============================================================
    # STAGE 2 — EXECUTE MOVEMENT
    # ============================================================

    def execute_command(self, command):

        if not self.validate_command(command):

            rospy.logerr(
                "Invalid command: %s",
                str(command)
            )

            self.stop_robot()

            return

        action = command.get("action")

        # ========================================================
        # STOP
        # ========================================================

        if action == "stop":

            rospy.loginfo(
                "STOP command."
            )

            self.stop_robot()

            return

        direction = command.get("direction")

        try:

            duration = float(
                command.get("duration", 0)
            )

        except Exception:

            self.stop_robot()

            return

        # ========================================================
        # STAGE 2 — DETERMINE VELOCITY
        # ========================================================

        linear_x = 0.0
        angular_z = 0.0

        if action == "move":

            if direction == "forward":

                linear_x = self.linear_speed

            elif direction == "backward":

                linear_x = -self.linear_speed

        elif action == "turn":

            if direction == "left":

                angular_z = self.angular_speed

            elif direction == "right":

                angular_z = -self.angular_speed

        rospy.loginfo(
            "Command: %s %s for %.2f seconds",
            action,
            direction,
            duration
        )

        # ========================================================
        # STAGE 2 — DRY RUN
        # ========================================================

        if self.DRY_RUN:

            rospy.loginfo(
                "[DRY RUN] Would execute: %s %s for %.2f seconds",
                action,
                direction,
                duration
            )

            self.print_lidar_status()

            return

        # ========================================================
        # STAGE 2 — REAL ROBOT MOVEMENT
        # ========================================================

        rospy.loginfo(
            "[REAL ROBOT] Executing movement"
        )

        rate = rospy.Rate(10)

        start_time = time.time()

        while not rospy.is_shutdown():

            elapsed = time.time() - start_time

            if elapsed >= duration:
                break

            # ----------------------------------------------------
            # Publish velocity
            # ----------------------------------------------------

            self.publish_velocity(
                linear_x,
                angular_z
            )

            rate.sleep()

        # --------------------------------------------------------
        # ALWAYS STOP AFTER MOVEMENT
        # --------------------------------------------------------

        self.stop_robot()

        rospy.loginfo(
            "Movement complete."
        )

    # ============================================================
    # STAGE 1 — LiDAR STATUS
    # ============================================================

    def format_distance(self, distance):

        if math.isnan(distance) or math.isinf(distance):

            return "no valid return"

        return "%.2f m" % distance

    def print_lidar_status(self):

        rospy.loginfo(
            "LiDAR | Front: %s | Left: %s | Right: %s",
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

    # ============================================================
    # MAIN LOOP
    # ============================================================

    def run(self):

        while not rospy.is_shutdown():

            try:

                user_command = raw_input(
                    "Enter robot command: "
                )

            except (EOFError, KeyboardInterrupt):

                self.stop_robot()

                break

            user_command = user_command.strip()

            if not user_command:
                continue

            rospy.loginfo(
                "User command: %s",
                user_command
            )

            # ----------------------------------------------------
            # Ask LLM
            # ----------------------------------------------------

            response = self.ask_llm(
                user_command
            )

            if response is None:

                self.stop_robot()

                continue

            # ----------------------------------------------------
            # Parse JSON
            # ----------------------------------------------------

            command = self.parse_command(
                response
            )

            if command is None:

                rospy.logerr(
                    "Could not parse LLM response."
                )

                self.stop_robot()

                continue

            rospy.loginfo(
                "Parsed command: %s",
                json.dumps(command)
            )

            # ----------------------------------------------------
            # Execute
            # ----------------------------------------------------

            self.execute_command(
                command
            )


# ================================================================
# PROGRAM ENTRY POINT
# ================================================================

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


