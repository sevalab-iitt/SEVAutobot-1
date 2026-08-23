#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================
# JETAUTO LLM ROBOT INTELLIGENCE
# ROS Melodic / Python 2.7
#
# STAGE 1  - LLM SERVER COMMUNICATION
# STAGE 2  - NATURAL LANGUAGE -> ROBOT COMMAND
# STAGE 3  - LiDAR PERCEPTION
# STAGE 4  - REAL ROBOT CONTROL
# STAGE 5  - MULTI-COMMAND SEQUENCES
# STAGE 6  - LiDAR SAFETY LAYER
# STAGE 7  - ROBOT STATUS / AWARENESS
# STAGE 8  - NATURAL LANGUAGE ROBOT INTERFACE
#
# ============================================================

from __future__ import print_function

import rospy
import requests
import json
import time
import math

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


# ============================================================
# CONFIGURATION
# ============================================================

LLM_URL = "http://127.0.0.1:8081/completion"

# REAL ROBOT
DRY_RUN = False

# Movement speeds
LINEAR_SPEED = 0.10
ANGULAR_SPEED = 0.50

# Safety distance in meters
SAFETY_DISTANCE = 0.40

# Maximum allowed command duration
MAX_DURATION = 10.0

# LLM settings
LLM_TIMEOUT = 60

# LiDAR sectors
FRONT_HALF_ANGLE = 20.0
SIDE_HALF_ANGLE = 35.0


# ============================================================
# STAGE 1
# LLM SERVER COMMUNICATION
# ============================================================

class LLMRobotNode(object):

    def __init__(self):

        rospy.init_node(
            "llm_robot_node",
            anonymous=False
        )

        rospy.loginfo("======================================")
        rospy.loginfo("JETAUTO LLM ROBOT INTELLIGENCE")
        rospy.loginfo("======================================")

        rospy.loginfo("LLM URL: %s", LLM_URL)

        if DRY_RUN:
            rospy.loginfo("DRY_RUN = True")
        else:
            rospy.loginfo("DRY_RUN = False")
            rospy.loginfo("REAL ROBOT CONTROL ENABLED")

        # ====================================================
        # STAGE 4 - ROS MOTOR CONTROL
        # ====================================================

        self.cmd_pub = rospy.Publisher(
            "/jetauto_controller/cmd_vel",
            Twist,
            queue_size=10
        )

        # ====================================================
        # STAGE 3 - LiDAR
        # ====================================================

        self.scan_sub = rospy.Subscriber(
            "/scan",
            LaserScan,
            self.scan_callback,
            queue_size=1
        )

        self.scan_msg = None

        # Current robot state
        self.current_command = "stopped"
        self.is_moving = False

        rospy.sleep(1.0)

        # Make sure robot starts stopped
        self.stop_robot()

        rospy.loginfo("Robot intelligence node ready.")

    # ========================================================
    # STAGE 3
    # LiDAR CALLBACK
    # ========================================================

    def scan_callback(self, msg):

        self.scan_msg = msg

    # ========================================================
    # STAGE 3
    # SAFE FLOAT CHECK
    #
    # Python 2.7 compatible.
    # We DO NOT use rospy.isinf() or math.isfinite().
    # ========================================================

    def valid_range(self, value):

        try:
            value = float(value)

            if value <= 0:
                return False

            if value != value:
                return False

            if value == float("inf"):
                return False

            if value == float("-inf"):
                return False

            return True

        except Exception:
            return False

    # ========================================================
    # STAGE 3
    # GET LiDAR DISTANCE FOR ANGLE SECTOR
    # ========================================================

    def get_sector_distance(self, center_angle_deg, half_width_deg):

        if self.scan_msg is None:
            return None

        msg = self.scan_msg

        center = math.radians(center_angle_deg)
        half = math.radians(half_width_deg)

        start_angle = center - half
        end_angle = center + half

        values = []

        angle = msg.angle_min

        for distance in msg.ranges:

            if angle >= start_angle and angle <= end_angle:

                if self.valid_range(distance):

                    if distance >= msg.range_min and distance <= msg.range_max:

                        values.append(float(distance))

            angle += msg.angle_increment

        if len(values) == 0:
            return None

        # Minimum distance is safest for obstacle detection
        return min(values)

    # ========================================================
    # STAGE 3
    # GET FRONT / LEFT / RIGHT DISTANCES
    # ========================================================

    def get_lidar_state(self):

        front = self.get_sector_distance(
            0.0,
            FRONT_HALF_ANGLE
        )

        left = self.get_sector_distance(
            90.0,
            SIDE_HALF_ANGLE
        )

        right = self.get_sector_distance(
            -90.0,
            SIDE_HALF_ANGLE
        )

        return {
            "front": front,
            "left": left,
            "right": right
        }

    # ========================================================
    # STAGE 7
    # HUMAN-READABLE ROBOT STATUS
    # ========================================================

    def format_distance(self, value):

        if value is None:
            return "no valid return"

        return "%.2f m" % value

    def get_robot_status(self):

        lidar = self.get_lidar_state()

        status = {
            "movement": self.current_command,
            "moving": self.is_moving,
            "lidar_front": lidar["front"],
            "lidar_left": lidar["left"],
            "lidar_right": lidar["right"]
        }

        return status

    def print_robot_status(self):

        status = self.get_robot_status()

        rospy.loginfo(
            "ROBOT STATUS | Movement: %s | Moving: %s",
            status["movement"],
            status["moving"]
        )

        rospy.loginfo(
            "LiDAR | Front: %s | Left: %s | Right: %s",
            self.format_distance(status["lidar_front"]),
            self.format_distance(status["lidar_left"]),
            self.format_distance(status["lidar_right"])
        )

    # ========================================================
    # STAGE 1
    # SEND PROMPT TO LLAMA.CPP
    # ========================================================

    def ask_llm(self, user_command):

        system_prompt = """
You are the intelligence interface of a mobile robot.

The robot has:
- forward movement
- backward movement
- left turning
- right turning
- stop
- LiDAR sensor

You convert natural language into robot commands.

IMPORTANT:
Return ONLY valid JSON.

For ONE command use:

{"action":"move","direction":"forward","duration":2}

For MULTIPLE commands use a JSON ARRAY:

[
 {"action":"move","direction":"forward","duration":2},
 {"action":"turn","direction":"left","duration":1}
]

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
- move requires direction and duration
- turn requires direction and duration
- stop requires only action
- duration must be a number
- maximum duration is 10 seconds
- NEVER return explanations
- NEVER use markdown
- NEVER return ```json
- NEVER invent other actions
"""

        prompt = (
            system_prompt +
            "\n\nUser command: " +
            user_command +
            "\n\nJSON:"
        )

        payload = {
            "prompt": prompt,
            "n_predict": 80,
            "temperature": 0,
            "top_k": 20,
            "top_p": 0.90
        }

        try:

            response = requests.post(
                LLM_URL,
                headers={
                    "Content-Type": "application/json"
                },
                data=json.dumps(payload),
                timeout=LLM_TIMEOUT
            )

            if response.status_code != 200:

                rospy.logerr(
                    "LLM HTTP error: %s",
                    response.status_code
                )

                return None

            data = response.json()

            content = data.get("content", "")

            if content is None:
                return None

            content = content.strip()

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
    # STAGE 5
    # EXTRACT JSON FROM LLM RESPONSE
    #
    # Handles:
    #   {...}
    #   [...]
    #
    # Also handles accidental text before/after JSON.
    # ========================================================

    def extract_json(self, text):

        if not text:
            return None

        text = text.strip()

        # Remove markdown fences if model produces them
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        # ----------------------------------------------------
        # First try entire response
        # ----------------------------------------------------

        try:

            return json.loads(text)

        except Exception:
            pass

        # ----------------------------------------------------
        # Try JSON ARRAY
        # ----------------------------------------------------

        start = text.find("[")
        end = text.rfind("]")

        if start != -1 and end != -1 and end > start:

            candidate = text[start:end + 1]

            try:

                return json.loads(candidate)

            except Exception:
                pass

        # ----------------------------------------------------
        # Try JSON OBJECT
        # ----------------------------------------------------

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1 and end > start:

            candidate = text[start:end + 1]

            try:

                return json.loads(candidate)

            except Exception:
                pass

        rospy.logerr(
            "JSON parsing failed. No valid JSON found."
        )

        return None

    # ========================================================
    # STAGE 5
    # NORMALIZE SINGLE COMMAND / COMMAND ARRAY
    # ========================================================

    def normalize_commands(self, parsed):

        if parsed is None:
            return []

        # Single command
        if isinstance(parsed, dict):

            return [parsed]

        # Multiple commands
        if isinstance(parsed, list):

            commands = []

            for item in parsed:

                if isinstance(item, dict):

                    commands.append(item)

            return commands

        return []

    # ========================================================
    # STAGE 2
    # VALIDATE COMMAND
    # ========================================================

    def validate_command(self, command):

        if not isinstance(command, dict):

            return False

        action = command.get("action")

        if action not in [
            "move",
            "turn",
            "stop"
        ]:

            rospy.logwarn(
                "Invalid action: %s",
                str(action)
            )

            return False

        # Stop needs no direction
        if action == "stop":

            return True

        direction = command.get("direction")

        if direction not in [
            "forward",
            "backward",
            "left",
            "right"
        ]:

            rospy.logwarn(
                "Invalid direction: %s",
                str(direction)
            )

            return False

        duration = command.get("duration")

        try:

            duration = float(duration)

        except Exception:

            rospy.logwarn(
                "Invalid duration."
            )

            return False

        if duration <= 0:

            rospy.logwarn(
                "Duration must be positive."
            )

            return False

        if duration > MAX_DURATION:

            rospy.logwarn(
                "Duration %.2f exceeds maximum. Limiting to %.2f.",
                duration,
                MAX_DURATION
            )

            command["duration"] = MAX_DURATION

        else:

            command["duration"] = duration

        return True
    # ========================================================
    # STAGE 6
    # LiDAR SAFETY CHECK
    #
    # This is deliberately OUTSIDE the LLM.
    # The LLM cannot override this.
    # ========================================================

    def obstacle_ahead(self):

        lidar = self.get_lidar_state()

        front = lidar["front"]

        if front is None:

            # No valid front return.
            # We don't automatically declare it unsafe.
            # But we log it clearly.
            rospy.logwarn(
                "LiDAR front: no valid return."
            )

            return False

        if front < SAFETY_DISTANCE:

            rospy.logwarn(
                "SAFETY: obstacle detected at %.2f m",
                front
            )

            return True

        return False

    # ========================================================
    # STAGE 6
    # SAFETY-AWARE VELOCITY PUBLISH
    # ========================================================

    def publish_velocity(self, linear_x, angular_z):

        # ----------------------------------------------------
        # Forward safety
        # ----------------------------------------------------

        if linear_x > 0:

            if self.obstacle_ahead():

                rospy.logwarn(
                    "Forward movement BLOCKED by LiDAR."
                )

                self.stop_robot()

                return False

        # ----------------------------------------------------
        # REAL ROBOT
        # ----------------------------------------------------

        twist = Twist()

        twist.linear.x = linear_x
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = angular_z

        if DRY_RUN:

            rospy.loginfo(
                "[DRY RUN] velocity linear=%.2f angular=%.2f",
                linear_x,
                angular_z
            )

            return True

        self.cmd_pub.publish(twist)

        return True

    # ========================================================
    # STAGE 4
    # STOP ROBOT
    # ========================================================

    def stop_robot(self):

        twist = Twist()

        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0

        if not DRY_RUN:

            self.cmd_pub.publish(twist)

        self.is_moving = False
        self.current_command = "stopped"

        rospy.loginfo(
            "Robot STOPPED"
        )

    # ========================================================
    # STAGE 4
    # EXECUTE MOVEMENT
    # ========================================================

    def execute_movement(self, direction, duration):

        duration = float(duration)

        rospy.loginfo(
            "Command: move %s for %.2f seconds",
            direction,
            duration
        )

        if direction == "forward":

            linear = LINEAR_SPEED
            angular = 0.0

        elif direction == "backward":

            linear = -LINEAR_SPEED
            angular = 0.0

        elif direction == "left":

            linear = 0.0
            angular = ANGULAR_SPEED

        elif direction == "right":

            linear = 0.0
            angular = -ANGULAR_SPEED

        else:

            rospy.logerr(
                "Unknown movement direction."
            )

            return

        if DRY_RUN:

            rospy.loginfo(
                "[DRY RUN] Would execute: %s %.2f sec",
                direction,
                duration
            )

            time.sleep(duration)

            return

        rospy.loginfo(
            "Executing REAL robot movement."
        )

        self.is_moving = True
        self.current_command = direction

        start_time = time.time()

        rate = rospy.Rate(10)

        while not rospy.is_shutdown():

            elapsed = time.time() - start_time

            if elapsed >= duration:

                break

            # ----------------------------------------------
            # STAGE 6
            # CONTINUOUS LiDAR SAFETY
            # ----------------------------------------------

            if linear > 0:

                if self.obstacle_ahead():

                    rospy.logwarn(
                        "Emergency stop: obstacle ahead."
                    )

                    break

            # ----------------------------------------------
            # Publish velocity
            # ----------------------------------------------

            success = self.publish_velocity(
                linear,
                angular
            )

            if not success:

                break

            rate.sleep()

        self.stop_robot()

    # ========================================================
    # STAGE 4
    # EXECUTE TURN
    # ========================================================

    def execute_turn(self, direction, duration):

        duration = float(duration)

        rospy.loginfo(
            "Command: turn %s for %.2f seconds",
            direction,
            duration
        )

        if direction == "left":

            angular = ANGULAR_SPEED

        elif direction == "right":

            angular = -ANGULAR_SPEED

        else:

            rospy.logerr(
                "Unknown turn direction."
            )

            return

        if DRY_RUN:

            rospy.loginfo(
                "[DRY RUN] Would execute: turn %s for %.2f seconds",
                direction,
                duration
            )

            time.sleep(duration)

            return

        rospy.loginfo(
            "Executing REAL robot turn."
        )

        self.is_moving = True
        self.current_command = "turning_" + direction

        start_time = time.time()

        rate = rospy.Rate(10)

        while not rospy.is_shutdown():

            elapsed = time.time() - start_time

            if elapsed >= duration:

                break

            self.publish_velocity(
                0.0,
                angular
            )

            rate.sleep()

        self.stop_robot()

    # ========================================================
    # STAGE 4 + 5
    # EXECUTE ONE COMMAND
    # ========================================================

    def execute_command(self, command):

        if not self.validate_command(command):

            rospy.logwarn(
                "Command rejected."
            )

            self.stop_robot()

            return False

        action = command.get("action")

        if action == "stop":

            rospy.loginfo(
                "STOP command."
            )

            self.stop_robot()

            return True

        direction = command.get("direction")
        duration = float(command.get("duration"))

        if action == "move":

            self.execute_movement(
                direction,
                duration
            )

            return True

        if action == "turn":

            self.execute_turn(
                direction,
                duration
            )

            return True

        return False

    # ========================================================
    # STAGE 5
    # EXECUTE MULTIPLE COMMANDS
    # ========================================================

    def execute_sequence(self, commands):

        if len(commands) == 0:

            rospy.logerr(
                "No executable commands."
            )

            self.stop_robot()

            return

        rospy.loginfo(
            "Executing command sequence: %d commands",
            len(commands)
        )

        for index, command in enumerate(commands):

            if rospy.is_shutdown():
                break

            rospy.loginfo(
                "========== COMMAND %d / %d ==========",
                index + 1,
                len(commands)
            )

            rospy.loginfo(
                "Command: %s",
                json.dumps(command)
            )

            success = self.execute_command(
                command
            )

            if not success:

                rospy.logwarn(
                    "Command failed. Stopping sequence."
                )

                break

            # Always stop between commands
            self.stop_robot()

            rospy.sleep(0.15)

        self.stop_robot()

        rospy.loginfo(
            "Command sequence finished."
        )

    # ========================================================
    # STAGE 7
    # ANSWER ROBOT STATUS QUESTIONS
    # ========================================================

    def handle_status_question(self, text):

        text_lower = text.lower()

        status_words = [
            "status",
            "what is in front",
            "what's in front",
            "distance",
            "lidar",
            "safe to move",
            "safe to go",
            "obstacle",
            "how far"
        ]

        is_status_question = False

        for word in status_words:

            if word in text_lower:

                is_status_question = True
                break

        if not is_status_question:

            return False

        status = self.get_robot_status()

        front = self.format_distance(
            status["lidar_front"]
        )

        left = self.format_distance(
            status["lidar_left"]
        )

        right = self.format_distance(
            status["lidar_right"]
        )

        # Safety question
        if (
            "safe to move" in text_lower or
            "safe to go" in text_lower
        ):

            if status["lidar_front"] is None:

                print(
                    "I do not have a valid front LiDAR return."
                )

            elif status["lidar_front"] < SAFETY_DISTANCE:

                print(
                    "No. An obstacle is %.2f m ahead." %
                    status["lidar_front"]
                )

            else:

                print(
                    "Yes. Front distance is %.2f m." %
                    status["lidar_front"]
                )

            return True

        print("")
        print("========== ROBOT STATUS ==========")
        print("Movement : %s" % status["movement"])
        print("Moving   : %s" % status["moving"])
        print("Front    : %s" % front)
        print("Left     : %s" % left)
        print("Right    : %s" % right)
        print("==================================")
        print("")

        return True

    # ========================================================
    # STAGE 8
    # LOCAL SIMPLE COMMAND FALLBACK
    #
    # Useful if the LLM fails.
    # ========================================================

    def local_command_fallback(self, text):

        t = text.lower()

        # STOP has highest priority
        if (
            t.strip() == "stop" or
            "emergency stop" in t
        ):

            return [
                {
                    "action": "stop"
                }
            ]

        # ----------------------------------------------
        # Duration extraction
        # ----------------------------------------------

        duration = 1.0

        words = t.replace(",", " ").split()

        for i in range(len(words) - 1):

            try:

                value = float(words[i])

                if (
                    words[i + 1].startswith("second") or
                    words[i + 1].startswith("sec")
                ):

                    duration = value

            except Exception:
                pass

        # ----------------------------------------------
        # Direction
        # ----------------------------------------------

        if "forward" in t:

            return [
                {
                    "action": "move",
                    "direction": "forward",
                    "duration": duration
                }
            ]

        if "backward" in t or "back" in t:

            return [
                {
                    "action": "move",
                    "direction": "backward",
                    "duration": duration
                }
            ]

        if "left" in t:

            return [
                {
                    "action": "turn",
                    "direction": "left",
                    "duration": duration
                }
            ]

        if "right" in t:

            return [
                {
                    "action": "turn",
                    "direction": "right",
                    "duration": duration
                }
            ]

        return []

    # ========================================================
    # STAGE 8
    # HANDLE USER INPUT
    # ========================================================

    def process_user_command(self, text):

        text = text.strip()

        if not text:

            return

        rospy.loginfo(
            "User command: %s",
            text
        )

        # ----------------------------------------------------
        # STAGE 7
        # Handle sensor/status questions locally.
        # This avoids wasting LLM inference time.
        # ----------------------------------------------------

        if self.handle_status_question(text):

            return

        # ----------------------------------------------------
        # STAGE 8
        # Ask LLM
        # ----------------------------------------------------

        response = self.ask_llm(text)

        parsed = self.extract_json(
            response
        )

        # ----------------------------------------------------
        # STAGE 8
        # LLM failed -> local fallback
        # ----------------------------------------------------

        if parsed is None:

            rospy.logwarn(
                "LLM parsing failed. Trying local fallback."
            )

            commands = self.local_command_fallback(
                text
            )

        else:

            commands = self.normalize_commands(
                parsed
            )

        # ----------------------------------------------------
        # Validate commands
        # ----------------------------------------------------

        valid_commands = []

        for command in commands:

            if self.validate_command(command):

                valid_commands.append(command)

        if len(valid_commands) == 0:

            rospy.logerr(
                "Could not understand robot command."
            )

            self.stop_robot()

            return

        rospy.loginfo(
            "Parsed commands: %s",
            json.dumps(valid_commands)
        )

        # ----------------------------------------------------
        # STAGE 5
        # Execute sequence
        # ----------------------------------------------------

        self.execute_sequence(
            valid_commands
        )

    # ========================================================
    # STAGE 8
    # MAIN USER LOOP
    # ========================================================

    def run(self):

        rospy.loginfo(
            "======================================"
        )

        rospy.loginfo(
            "Stages 1-8 loaded."
        )

        rospy.loginfo(
            "Text command interface active."
        )

        rospy.loginfo(
            "======================================"
        )

        while not rospy.is_shutdown():

            try:

                print(
                    "Enter robot command: ",
                    end=""
                )

                text = raw_input()

                if text is None:
                    continue

                text = text.strip()

                if text.lower() in [
                    "exit",
                    "quit"
                ]:

                    rospy.loginfo(
                        "Exiting robot intelligence."
                    )

                    break

                self.process_user_command(
                    text
                )

            except KeyboardInterrupt:

                rospy.loginfo(
                    "Keyboard interrupt."
                )

                break

            except EOFError:

                break

            except Exception as e:

                rospy.logerr(
                    "Main loop error: %s",
                    str(e)
                )

                self.stop_robot()

        self.stop_robot()


# ============================================================
# PROGRAM ENTRY
# ============================================================

if __name__ == "__main__":

    node = LLMRobotNode()

    try:

        node.run()

    except rospy.ROSInterruptException:

        pass

    finally:

        node.stop_robot()


  
      
