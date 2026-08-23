#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================
# JETAUTO LLM ROBOT CONTROLLER
#
# STAGE 1:
#   Natural language command -> LLM
#
# STAGE 2:
#   ROS integration + LiDAR /scan
#
# STAGE 3:
#   Robust LLM response extraction + validation
#
# STAGE 4:
#   REAL ROBOT MOVEMENT
#   LLM output -> validated command -> /cmd_vel
#
# SAFETY:
#   - STOP always has priority
#   - Forward movement requires valid LiDAR
#   - Forward movement is continuously checked by LiDAR
#   - Maximum movement duration is limited
#   - Invalid LLM responses never move the robot
#
# ============================================================

from __future__ import print_function

import rospy
import requests
import json
import time
import math
import re

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class LLMRobotNode(object):

    # ========================================================
    # STAGE 1 - INITIALIZATION
    # ========================================================

    def __init__(self):

        rospy.init_node(
            'llm_robot_node',
            anonymous=False
        )

        # ----------------------------------------------------
        # Local llama.cpp server
        # ----------------------------------------------------

        self.llm_url = "http://127.0.0.1:8081/completion"

        # ----------------------------------------------------
        # ROS velocity publisher
        # ----------------------------------------------------

        self.cmd_vel_pub = rospy.Publisher(
            '/jetauto_controller/cmd_vel',
            Twist,
            queue_size=10
        )

        # ----------------------------------------------------
        # LiDAR subscriber
        # ----------------------------------------------------

        self.scan_sub = rospy.Subscriber(
            '/scan',
            LaserScan,
            self.scan_callback
        )

        # ====================================================
        # STAGE 4 - REAL ROBOT CONTROL
        # ====================================================

        # False = REAL ROBOT
        # True  = simulation/dry run

        self.DRY_RUN = False

        # ----------------------------------------------------
        # Robot speeds
        # ----------------------------------------------------

        self.linear_speed = 0.15
        self.angular_speed = 0.40

        # ----------------------------------------------------
        # Safety distance
        # ----------------------------------------------------

        self.safety_distance = 0.25

        # ----------------------------------------------------
        # Maximum allowed command duration
        # ----------------------------------------------------

        self.max_duration = 10.0

        # ----------------------------------------------------
        # LiDAR state
        # ----------------------------------------------------

        self.front_distance = float('inf')
        self.left_distance = float('inf')
        self.right_distance = float('inf')

        self.scan_received = False

        # ----------------------------------------------------
        # Allowed commands
        # ----------------------------------------------------

        self.allowed_actions = [
            'move',
            'turn',
            'stop'
        ]

        self.allowed_directions = [
            'forward',
            'backward',
            'left',
            'right'
        ]

        rospy.loginfo("LLM Robot Node started")
        rospy.loginfo("DRY_RUN = %s", self.DRY_RUN)

        if not self.DRY_RUN:
            rospy.loginfo("REAL ROBOT CONTROL ENABLED")

    # ========================================================
    # STAGE 2 - LiDAR CALLBACK
    # ========================================================

    def scan_callback(self, msg):

        if msg is None:
            return

        ranges = msg.ranges

        if not ranges:
            return

        total = len(ranges)

        # ----------------------------------------------------
        # Convert angle to array index
        # ----------------------------------------------------

        def angle_to_index(angle):

            index = int(
                (angle - msg.angle_min) /
                msg.angle_increment
            )

            if index < 0:
                index = 0

            if index >= total:
                index = total - 1

            return index

        # ----------------------------------------------------
        # Get minimum valid distance in a sector
        # ----------------------------------------------------

        def sector_distance(center_angle, width):

            start_angle = center_angle - width
            end_angle = center_angle + width

            start_index = angle_to_index(start_angle)
            end_index = angle_to_index(end_angle)

            if start_index > end_index:

                temp = start_index
                start_index = end_index
                end_index = temp

            values = []

            for i in range(
                start_index,
                end_index + 1
            ):

                distance = ranges[i]

                if distance is None:
                    continue

                # Python 2.7 compatible
                if math.isnan(distance):
                    continue

                if math.isinf(distance):
                    continue

                if distance < msg.range_min:
                    continue

                if distance > msg.range_max:
                    continue

                values.append(distance)

            if not values:
                return float('inf')

            return min(values)

        # ----------------------------------------------------
        # Front
        # ----------------------------------------------------

        self.front_distance = sector_distance(
            0.0,
            0.20
        )

        # ----------------------------------------------------
        # Left
        # ----------------------------------------------------

        self.left_distance = sector_distance(
            math.pi / 2.0,
            0.20
        )

        # ----------------------------------------------------
        # Right
        # ----------------------------------------------------

        self.right_distance = sector_distance(
            -math.pi / 2.0,
            0.20
        )

        self.scan_received = True

    # ========================================================
    # STAGE 2 - LiDAR DISPLAY
    # ========================================================

    def format_distance(self, distance):

        if distance is None:
            return "no valid return"

        if math.isnan(distance):
            return "no valid return"

        if math.isinf(distance):
            return "no valid return"

        return "%.2f m" % distance

    def log_lidar_status(self):

        rospy.loginfo(
            "LiDAR | Front: %s | Left: %s | Right: %s",
            self.format_distance(self.front_distance),
            self.format_distance(self.left_distance),
            self.format_distance(self.right_distance)
        )

    # ========================================================
    # STAGE 1 - LLM PROMPT
    # ========================================================

    def build_prompt(self, user_command):

        prompt = """
You control a mobile robot.

Convert the user command into ONE JSON object.

Allowed actions:
move
turn
stop

Allowed directions:
forward
backward
left
right

Rules:

1. Output ONLY JSON.
2. Never output explanations.
3. Never output Markdown.
4. Never output code fences.
5. Never output multiple commands.
6. Move and turn require duration.
7. Stop must be:
{"action":"stop"}

Examples:

User: Move forward for 2 seconds.
{"action":"move","direction":"forward","duration":2}

User: Move backward for 3 seconds.
{"action":"move","direction":"backward","duration":3}

User: Turn left for 2 seconds.
{"action":"turn","direction":"left","duration":2}

User: Turn right for 2 seconds.
{"action":"turn","direction":"right","duration":2}

User: Stop.
{"action":"stop"}

User command:
%s

JSON:
""" % user_command

        return prompt

    # ========================================================
    # STAGE 1 - CALL LLAMA SERVER
    # ========================================================

    def call_llm(self, user_command):

        prompt = self.build_prompt(user_command)

        payload = {
            "prompt": prompt,
            "n_predict": 30,
            "temperature": 0.0,
            "top_k": 1,
            "top_p": 1.0
        }

        try:

            response = requests.post(
                self.llm_url,
                headers={
                    "Content-Type":
                    "application/json"
                },
                data=json.dumps(payload),
                timeout=60
            )

            if response.status_code != 200:

                rospy.logerr(
                    "LLM HTTP error: %s",
                    response.status_code
                )

                return None

            data = response.json()

            content = data.get(
                "content",
                ""
            )

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

    # ========================================================
    # STAGE 3 - CLEAN RESPONSE
    # ========================================================

    def clean_llm_response(self, text):

        if text is None:
            return ""

        text = text.strip()

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```JSON",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        return text.strip()

    # ========================================================
    # STAGE 3 - EXTRACT JSON OBJECT
    # ========================================================

    def extract_json_object(self, text):

        if not text:
            return None

        text = self.clean_llm_response(text)

        for start in range(len(text)):

            if text[start] != '{':
                continue

            depth = 0
            in_string = False
            escaped = False

            for i in range(
                start,
                len(text)
            ):

                char = text[i]

                if escaped:

                    escaped = False
                    continue

                if char == '\\':

                    if in_string:
                        escaped = True

                    continue

                if char == '"':

                    in_string = not in_string
                    continue

                if in_string:
                    continue

                if char == '{':

                    depth += 1

                elif char == '}':

                    depth -= 1

                    if depth == 0:

                        candidate = text[
                            start:i + 1
                        ]

                        try:

                            obj = json.loads(
                                candidate
                            )

                            if isinstance(
                                obj,
                                dict
                            ):
                                return obj

                        except Exception:

                            break

        return None

    # ========================================================
    # STAGE 4 - NATURAL LANGUAGE FALLBACK
    #
    # If the LLM returns:
    #
    # {"command":"Move forward for 2 seconds"}
    #
    # or:
    #
    # Move forward for 2 seconds
    #
    # we convert it ourselves.
    # ========================================================

    def parse_natural_language(self, text):

        if not text:
            return None

        text = text.lower().strip()

        # ----------------------------------------------------
        # Remove common LLM garbage
        # ----------------------------------------------------

        text = text.replace(
            '\n',
            ' '
        )

        text = text.replace(
            '`',
            ''
        )

        # ----------------------------------------------------
        # STOP
        # ----------------------------------------------------

        if re.search(
            r'\b(stop|halt|emergency stop)\b',
            text
        ):

            return {
                "action": "stop"
            }

        # ----------------------------------------------------
        # Duration
        # ----------------------------------------------------

        duration = None

        duration_match = re.search(
            r'([0-9]+(?:\.[0-9]+)?)\s*'
            r'(?:seconds?|secs?|s)\b',
            text
        )

        if duration_match:

            try:

                duration = float(
                    duration_match.group(1)
                )

            except Exception:

                duration = None

        # ----------------------------------------------------
        # If duration is missing, use safe default
        # ----------------------------------------------------

        if duration is None:

            duration = 1.0

        # ----------------------------------------------------
        # Maximum duration
        # ----------------------------------------------------

        if duration > self.max_duration:
            duration = self.max_duration

        # ----------------------------------------------------
        # MOVE FORWARD
        # ----------------------------------------------------

        if re.search(
            r'\b(move|go|drive)\b.*\bforward\b',
            text
        ) or re.search(
            r'\bforward\b',
            text
        ):

            return {
                "action": "move",
                "direction": "forward",
                "duration": duration
            }

        # ----------------------------------------------------
        # MOVE BACKWARD
        # ----------------------------------------------------

        if re.search(
            r'\b(move|go|drive)\b.*\b(backward|back)\b',
            text
        ) or re.search(
            r'\b(backward|back)\b',
            text
        ):

            return {
                "action": "move",
                "direction": "backward",
                "duration": duration
            }

        # ----------------------------------------------------
        # TURN LEFT
        # ----------------------------------------------------

        if re.search(
            r'\b(turn|rotate)\b.*\bleft\b',
            text
        ) or re.search(
            r'\bleft\b',
            text
        ):

            return {
                "action": "turn",
                "direction": "left",
                "duration": duration
            }

        # ----------------------------------------------------
        # TURN RIGHT
        # ----------------------------------------------------

        if re.search(
            r'\b(turn|rotate)\b.*\bright\b',
            text
        ) or re.search(
            r'\bright\b',
            text
        ):

            return {
                "action": "turn",
                "direction": "right",
                "duration": duration
            }

        return None

    # ========================================================
    # STAGE 3 + STAGE 4 - VALIDATE COMMAND
    # ========================================================

    def validate_command(self, command):

        if not isinstance(
            command,
            dict
        ):
            return None

        # ----------------------------------------------------
        # STAGE 4 FALLBACK:
        # {"command":"Move forward for 2 seconds"}
        # ----------------------------------------------------

        if (
            "action" not in command
            and "command" in command
        ):

            command = self.parse_natural_language(
                str(command.get("command"))
            )

            if command is None:
                return None

        # ----------------------------------------------------
        # ACTION
        # ----------------------------------------------------

        action = command.get(
            "action"
        )

        if action is None:

            return None

        action = str(
            action
        ).lower().strip()

        if action not in self.allowed_actions:

            rospy.logerr(
                "Invalid action: %s",
                action
            )

            return None

        # ----------------------------------------------------
        # STOP
        # ----------------------------------------------------

        if action == "stop":

            return {
                "action": "stop"
            }

        # ----------------------------------------------------
        # DIRECTION
        # ----------------------------------------------------

        direction = command.get(
            "direction"
        )

        if direction is None:

            rospy.logerr(
                "Command missing direction"
            )

            return None

        direction = str(
            direction
        ).lower().strip()

        if direction not in self.allowed_directions:

            rospy.logerr(
                "Invalid direction: %s",
                direction
            )

            return None

        # ----------------------------------------------------
        # DURATION
        # ----------------------------------------------------

        duration = command.get(
            "duration"
        )

        if duration is None:

            rospy.logerr(
                "Command missing duration"
            )

            return None

        try:

            duration = float(
                duration
            )

        except Exception:

            rospy.logerr(
                "Invalid duration"
            )

            return None

        if duration <= 0:

            rospy.logerr(
                "Duration must be greater than 0"
            )

            return None

        # ----------------------------------------------------
        # SAFETY LIMIT
        # ----------------------------------------------------

        if duration > self.max_duration:

            rospy.logwarn(
                "Duration too large. "
                "Limiting to %.1f seconds.",
                self.max_duration
            )

            duration = self.max_duration

        return {
            "action": action,
            "direction": direction,
            "duration": duration
        }

    # ========================================================
    # STAGE 3 + STAGE 4 - PARSE COMMAND
    # ========================================================

    def parse_command(self, response):

        if not response:
            return None

        # ----------------------------------------------------
        # First try JSON
        # ----------------------------------------------------

        command = self.extract_json_object(
            response
        )

        if command is not None:

            command = self.validate_command(
                command
            )

            if command is not None:
                return command

        # ----------------------------------------------------
        # If JSON failed, try natural language
        # ----------------------------------------------------

        rospy.logwarn(
            "JSON parsing failed. "
            "Trying natural-language fallback."
        )

        command = self.parse_natural_language(
            response
        )

        if command is None:

            rospy.logerr(
                "Could not understand LLM response."
            )

            return None

        return self.validate_command(
            command
        )

    # ========================================================
    # STAGE 2 + STAGE 4 - LiDAR SAFETY
    # ========================================================

    def lidar_allows_forward(self):

        if not self.scan_received:

            rospy.logwarn(
                "No LiDAR scan received. "
                "Forward movement blocked."
            )

            return False

        if (
            self.front_distance
            < self.safety_distance
        ):

            rospy.logwarn(
                "OBSTACLE: front distance %.2f m",
                self.front_distance
            )

            return False

        return True

    # ========================================================
    # STAGE 4 - EXECUTE COMMAND
    # ========================================================

    def execute_command(self, command):

        if command is None:

            self.stop_robot()

            return

        action = command.get(
            "action"
        )

        # ----------------------------------------------------
        # STOP
        # ----------------------------------------------------

        if action == "stop":

            rospy.loginfo(
                "STOP command."
            )

            self.stop_robot()

            return

        direction = command.get(
            "direction"
        )

        duration = command.get(
            "duration"
        )

        rospy.loginfo(
            "Command: %s %s for %.2f seconds",
            action,
            direction,
            duration
        )

        # ----------------------------------------------------
        # FORWARD LiDAR CHECK
        # ----------------------------------------------------

        if (
            action == "move"
            and direction == "forward"
        ):

            if not self.lidar_allows_forward():

                rospy.logwarn(
                    "Forward movement BLOCKED by LiDAR."
                )

                self.stop_robot()

                return

        # ====================================================
        # STAGE 4 - DRY RUN
        # ====================================================

        if self.DRY_RUN:

            rospy.loginfo(
                "[DRY RUN] Would execute: "
                "%s %s for %.2f seconds",
                action,
                direction,
                duration
            )

            self.log_lidar_status()

            return

        # ====================================================
        # STAGE 4 - CREATE TWIST
        # ====================================================

        twist = Twist()

        # ----------------------------------------------------
        # FORWARD
        # ----------------------------------------------------

        if (
            action == "move"
            and direction == "forward"
        ):

            twist.linear.x = self.linear_speed

        # ----------------------------------------------------
        # BACKWARD
        # ----------------------------------------------------

        elif (
            action == "move"
            and direction == "backward"
        ):

            twist.linear.x = -self.linear_speed

        # ----------------------------------------------------
        # LEFT
        # ----------------------------------------------------

        elif (
            action == "turn"
            and direction == "left"
        ):

            twist.angular.z = self.angular_speed

        # ----------------------------------------------------
        # RIGHT
        # ----------------------------------------------------

        elif (
            action == "turn"
            and direction == "right"
        ):

            twist.angular.z = -self.angular_speed

        else:

            rospy.logerr(
                "Unsupported command."
            )

            self.stop_robot()

            return

        # ====================================================
        # STAGE 4 - REAL ROBOT MOVEMENT
        # ====================================================

        rospy.loginfo(
            "Executing REAL robot movement."
        )

        start_time = time.time()

        rate = rospy.Rate(20)

        while (
            time.time() - start_time
            < duration
        ):

            if rospy.is_shutdown():
                break

            # ------------------------------------------------
            # CONTINUOUS FORWARD LiDAR SAFETY
            # ------------------------------------------------

            if (
                action == "move"
                and direction == "forward"
            ):

                if not self.lidar_allows_forward():

                    rospy.logwarn(
                        "Obstacle detected during "
                        "forward movement."
                    )

                    break

            # ------------------------------------------------
            # Publish velocity
            # ------------------------------------------------

            self.cmd_vel_pub.publish(
                twist
            )

            rate.sleep()

        # ----------------------------------------------------
        # ALWAYS STOP AFTER MOVEMENT
        # ----------------------------------------------------

        self.stop_robot()

    # ========================================================
    # STAGE 4 - STOP ROBOT
    # ========================================================

    def stop_robot(self):

        twist = Twist()

        # ----------------------------------------------------
        # Publish zero velocity several times
        # ----------------------------------------------------

        for _ in range(5):

            self.cmd_vel_pub.publish(
                twist
            )

            time.sleep(0.05)

        rospy.loginfo(
            "Robot STOPPED"
        )

    # ========================================================
    # STAGE 4 - MAIN LOOP
    # ========================================================

    def run(self):

        while not rospy.is_shutdown():

            try:

                user_command = raw_input(
                    "Enter robot command: "
                )

            except EOFError:

                break

            except KeyboardInterrupt:

                break

            if not user_command:
                continue

            user_command = user_command.strip()

            if not user_command:
                continue

            rospy.loginfo(
                "User command: %s",
                user_command
            )

            # ------------------------------------------------
            # DIRECT STOP OVERRIDE
            # ------------------------------------------------

            if user_command.lower() in [
                "stop",
                "halt",
                "emergency stop",
                "emergency_stop"
            ]:

                self.stop_robot()

                continue

            # ------------------------------------------------
            # STAGE 1 - LLM
            # ------------------------------------------------

            response = self.call_llm(
                user_command
            )

            if response is None:

                rospy.logerr(
                    "Could not get LLM response."
                )

                self.stop_robot()

                continue

            # ------------------------------------------------
            # STAGE 3 + STAGE 4 - PARSE
            # ------------------------------------------------

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

            # ------------------------------------------------
            # STAGE 4 - EXECUTE
            # ------------------------------------------------

            self.execute_command(
                command
            )


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == '__main__':

    node = None

    try:

        node = LLMRobotNode()

        node.run()

    except rospy.ROSInterruptException:

        pass

    except KeyboardInterrupt:

        pass

    finally:

        # ----------------------------------------------------
        # FINAL SAFETY STOP
        # ----------------------------------------------------

        if node is not None:

            try:

                node.stop_robot()

            except Exception:

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

And enter:
Do these one at a time

Move forward for 1 second.

Then:

Move backward for 1 second.

Then:

Turn left for 1 second.

Then:

Turn right for 1 second.

Then:

Stop.

"""
---
"""
output we got:-
jetauto@jetauto-desktop:~/catkin_ws$ rosrun jetauto_llm llm_robot_node.py
[INFO] [1787506674.967632]: LLM Robot Node started
[INFO] [1787506674.971900]: DRY_RUN = False
[INFO] [1787506674.980904]: REAL ROBOT CONTROL ENABLED
Enter robot command: Move forward for 1 second.
[INFO] [1787506681.554026]: User command: Move forward for 1 second.
[INFO] [1787506698.395978]: LLM response: {"action":"move","direction":"forward","duration":1}
[INFO] [1787506698.401638]: Parsed command: {"action": "move", "duration": 1.0, "direction": "forward"}
[INFO] [1787506698.406192]: Command: move forward for 1.00 seconds
[INFO] [1787506698.410918]: Executing REAL robot movement.
[INFO] [1787506699.667667]: Robot STOPPED
Enter robot command: Move backward for 1 second.
[INFO] [1787506710.437304]: User command: Move backward for 1 second.
[INFO] [1787506722.339573]: LLM response: {"action":"move","direction":"backward","duration":1}
[INFO] [1787506722.345354]: Parsed command: {"action": "move", "duration": 1.0, "direction": "backward"}
[INFO] [1787506722.350356]: Command: move backward for 1.00 seconds
[INFO] [1787506722.354805]: Executing REAL robot movement.
[INFO] [1787506723.611532]: Robot STOPPED
Enter robot command: Turn left for 1 second.
[INFO] [1787506725.893496]: User command: Turn left for 1 second.
[INFO] [1787506738.339802]: LLM response: {"action":"turn","direction":"left","duration":1}
[INFO] [1787506738.346087]: Parsed command: {"action": "turn", "duration": 1.0, "direction": "left"}
[INFO] [1787506738.351213]: Command: turn left for 1.00 seconds
[INFO] [1787506738.356201]: Executing REAL robot movement.
[INFO] [1787506739.613878]: Robot STOPPED
Enter robot command: Turn right for 1 second.
[INFO] [1787506747.090044]: User command: Turn right for 1 second.
[INFO] [1787506758.971293]: LLM response: {"action":"turn","direction":"right","duration":1}
[INFO] [1787506758.976926]: Parsed command: {"action": "turn", "duration": 1.0, "direction": "right"}
[INFO] [1787506758.981334]: Command: turn right for 1.00 seconds
[INFO] [1787506758.986801]: Executing REAL robot movement.
[INFO] [1787506760.243786]: Robot STOPPED
Enter robot command: Stop.
[INFO] [1787506772.701489]: User command: Stop.
[INFO] [1787506777.779100]: LLM response: {"action":"stop"}
[INFO] [1787506777.788917]: Parsed command: {"action": "stop"}
[INFO] [1787506777.793894]: STOP command.
[INFO] [1787506778.050904]: Robot STOPPED
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


