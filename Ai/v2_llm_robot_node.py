#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ============================================================
# JETAUTO LLM ROBOT NODE
#
# STAGE 1  - Basic LLM robot commands
# STAGE 2  - LiDAR integration
# STAGE 3  - Real robot movement
# STAGE 4  - Multi-command execution
# STAGE 5  - Robust JSON parsing
# STAGE 6  - Local llama.cpp / Qwen integration
# STAGE 7  - Robot status / LiDAR queries
# STAGE 8  - Sequential command execution
# STAGE 9  - LiDAR safety + autonomous obstacle avoidance
#
# IMPORTANT:
# The LLM decides WHAT the robot should do.
# The safety controller decides WHETHER it is safe to do it.
#
# Architecture:
#
# USER
#   |
#   v
# LOCAL QWEN / LLAMA.CPP
#   |
#   v
# COMMAND PARSER
#   |
#   +----------------------+
#   |                      |
#   v                      v
# NORMAL COMMAND       AUTONOMOUS MODE
#   |                      |
#   +----------+-----------+
#              |
#              v
#       SAFETY CONTROLLER
#              |
#           /scan
#              |
#       LiDAR obstacle check
#              |
#              v
#     /jetauto_controller/cmd_vel
#
# Python 2 / ROS Melodic compatible
# ============================================================


# ============================================================
# STAGE 1 - BASIC IMPORTS
# ============================================================

import rospy
import json
import math
import time
import re
import requests

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool


# ============================================================
# STAGE 2 - CONFIGURATION
# ============================================================

# ------------------------------------------------------------
# LLM SERVER
# ------------------------------------------------------------

LLM_URL = "http://127.0.0.1:8081/completion"

LLM_TIMEOUT = 60


# ------------------------------------------------------------
# ROBOT CONTROL
# ------------------------------------------------------------

# IMPORTANT:
# False = REAL ROBOT
# True  = simulation / dry run

DRY_RUN = False


# ------------------------------------------------------------
# ROBOT SPEED
# ------------------------------------------------------------

LINEAR_SPEED = 0.20
TURN_SPEED = 0.60


# ============================================================
# STAGE 9 - LIDAR SAFETY PARAMETERS
# ============================================================

# These follow the obstacle avoidance approach from
# the existing JetAuto LiDAR controller.

FRONT_STOP_DIST = 0.50

BOXED_IN_DIST = 0.40

REVERSE_TIME = 0.80

TURN_TIME = 0.70

CONTROL_RATE_HZ = 10


# ------------------------------------------------------------
# IMPORTANT:
# Your robot's measured LiDAR angle convention:
#
# FRONT = +180 / -180
# BACK  = 0
# LEFT  = -90
# RIGHT = +90
# ------------------------------------------------------------

FRONT_CENTER = 180.0
LEFT_CENTER = -90.0
RIGHT_CENTER = 90.0

SECTOR_HALF_WIDTH = 30.0


# ------------------------------------------------------------
# Autonomous movement
# ------------------------------------------------------------

AUTONOMOUS_FORWARD_SPEED = 0.20


# ------------------------------------------------------------
# Safety behavior
# ------------------------------------------------------------

# If LiDAR has no valid front reading, we DO NOT automatically
# stop the robot in autonomous mode because your current LiDAR
# can return inf in portions of the scan.
#
# However, the user can change this to True if desired.
#
# Recommended for first testing:
# False

STOP_IF_FRONT_INVALID = False


# ============================================================
# STAGE 2 - ANGLE FUNCTIONS
# ============================================================

def normalize_deg(angle):
    """
    Normalize angle to (-180, 180].
    """

    while angle > 180.0:
        angle -= 360.0

    while angle <= -180.0:
        angle += 360.0

    return angle


def angular_distance(a, b):
    """
    Smallest absolute difference between two angles.
    """

    return abs(normalize_deg(a - b))


# ============================================================
# STAGE 2 + STAGE 9
# LIDAR SAFETY CONTROLLER
# ============================================================

class LidarSafetyController(object):

    def __init__(self, parent):

        self.parent = parent

        # ----------------------------------------------------
        # ROS publisher
        # ----------------------------------------------------

        self.cmd_pub = rospy.Publisher(
            "/jetauto_controller/cmd_vel",
            Twist,
            queue_size=10
        )

        # ----------------------------------------------------
        # LiDAR subscriber
        # ----------------------------------------------------

        rospy.Subscriber(
            "/scan",
            LaserScan,
            self.scan_callback,
            queue_size=1
        )

        # ----------------------------------------------------
        # Pause subscriber
        # ----------------------------------------------------

        rospy.Subscriber(
            "/auto_explore/pause",
            Bool,
            self.pause_callback,
            queue_size=1
        )

        # ----------------------------------------------------
        # LiDAR values
        # ----------------------------------------------------

        self.front_min = float("inf")
        self.left_min = float("inf")
        self.right_min = float("inf")

        self.scan_ready = False

        # ----------------------------------------------------
        # Autonomous state
        #
        # FORWARD
        # AVOID_TURN
        # REVERSE
        # PAUSED
        # ----------------------------------------------------

        self.state = "FORWARD"

        self.state_until = 0.0

        # +1 = left
        # -1 = right

        self.turn_direction = 1.0

        self.paused = False

        self.rate = rospy.Rate(CONTROL_RATE_HZ)

    # ========================================================
    # STAGE 9 - LIDAR CALLBACK
    # ========================================================

    def scan_callback(self, msg):

        front_values = []
        left_values = []
        right_values = []

        for i, distance in enumerate(msg.ranges):

            # ------------------------------------------------
            # Ignore invalid values
            # ------------------------------------------------

            if distance <= 0.0:
                continue

            if distance > msg.range_max:
                continue

            if math.isinf(distance):
                continue

            if math.isnan(distance):
                continue

            # ------------------------------------------------
            # Convert index to angle
            # ------------------------------------------------

            angle_rad = (
                msg.angle_min +
                i * msg.angle_increment
            )

            angle_deg = math.degrees(angle_rad)

            angle_deg = normalize_deg(angle_deg)

            # ------------------------------------------------
            # FRONT
            # ------------------------------------------------

            if angular_distance(
                    angle_deg,
                    FRONT_CENTER
            ) <= SECTOR_HALF_WIDTH:

                front_values.append(distance)

            # ------------------------------------------------
            # LEFT
            # ------------------------------------------------

            elif angular_distance(
                    angle_deg,
                    LEFT_CENTER
            ) <= SECTOR_HALF_WIDTH:

                left_values.append(distance)

            # ------------------------------------------------
            # RIGHT
            # ------------------------------------------------

            elif angular_distance(
                    angle_deg,
                    RIGHT_CENTER
            ) <= SECTOR_HALF_WIDTH:

                right_values.append(distance)

        # ----------------------------------------------------
        # Minimum distance in each sector
        # ----------------------------------------------------

        if front_values:
            self.front_min = min(front_values)
        else:
            self.front_min = float("inf")

        if left_values:
            self.left_min = min(left_values)
        else:
            self.left_min = float("inf")

        if right_values:
            self.right_min = min(right_values)
        else:
            self.right_min = float("inf")

        self.scan_ready = True

    # ========================================================
    # STAGE 9 - PAUSE
    # ========================================================

    def pause_callback(self, msg):

        self.paused = msg.data

        if self.paused:

            rospy.logwarn(
                "[LIDAR SAFETY] PAUSED"
            )

            self.stop()

        else:

            rospy.loginfo(
                "[LIDAR SAFETY] RESUMED"
            )

            self.state = "FORWARD"

    # ========================================================
    # STAGE 9 - PUBLISH TWIST
    # ========================================================

    def publish_twist(self, linear, angular):

        if self.parent.dry_run:

            rospy.loginfo(
                "[DRY RUN] Twist linear=%.2f angular=%.2f",
                linear,
                angular
            )

            return

        msg = Twist()

        msg.linear.x = linear
        msg.linear.y = 0.0
        msg.linear.z = 0.0

        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = angular

        self.cmd_pub.publish(msg)

    # ========================================================
    # STAGE 9 - STOP
    # ========================================================

    def stop(self):

        self.publish_twist(
            0.0,
            0.0
        )

    # ========================================================
    # STAGE 9 - CHOOSE TURN DIRECTION
    # ========================================================

    def choose_turn_direction(self):

        if self.left_min > self.right_min:

            return 1.0

        else:

            return -1.0

    # ========================================================
    # STAGE 9 - PRINT STATUS
    # ========================================================

    def get_status(self):

        return {
            "front": self.front_min,
            "left": self.left_min,
            "right": self.right_min
        }

    # ========================================================
    # STAGE 9 - FRONT SAFETY CHECK
    # ========================================================

    def front_blocked(self):

        if not self.scan_ready:

            return True

        if math.isinf(self.front_min):

            if STOP_IF_FRONT_INVALID:

                return True

            return False

        return (
            self.front_min <=
            FRONT_STOP_DIST
        )

    # ========================================================
    # STAGE 9 - AUTONOMOUS OBSTACLE AVOIDANCE
    # ========================================================

    def autonomous_step(self):

        if self.paused:

            self.stop()

            return

        if not self.scan_ready:

            rospy.logwarn_throttle(
                2.0,
                "[AUTONOMOUS] Waiting for LiDAR..."
            )

            self.stop()

            return

        now = rospy.get_time()

        # ====================================================
        # FORWARD
        # ====================================================

        if self.state == "FORWARD":

            # ------------------------------------------------
            # Obstacle detected
            # ------------------------------------------------

            if self.front_blocked():

                rospy.logwarn(
                    "[AUTONOMOUS] OBSTACLE "
                    "Front=%.2f Left=%.2f Right=%.2f",
                    self.front_min,
                    self.left_min,
                    self.right_min
                )

                # --------------------------------------------
                # Boxed in
                # --------------------------------------------

                boxed_in = (

                    self.front_min <= BOXED_IN_DIST and
                    self.left_min <= BOXED_IN_DIST and
                    self.right_min <= BOXED_IN_DIST

                )

                self.stop()

                if boxed_in:

                    rospy.logwarn(
                        "[AUTONOMOUS] BOXED IN -> REVERSE"
                    )

                    self.state = "REVERSE"

                    self.state_until = (
                        now +
                        REVERSE_TIME
                    )

                else:

                    self.turn_direction = (
                        self.choose_turn_direction()
                    )

                    self.state = "AVOID_TURN"

                    self.state_until = (
                        now +
                        TURN_TIME
                    )

                    if self.turn_direction > 0:

                        direction = "LEFT"

                    else:

                        direction = "RIGHT"

                    rospy.logwarn(
                        "[AUTONOMOUS] "
                        "TURN %s",
                        direction
                    )

            else:

                # --------------------------------------------
                # Clear path
                # --------------------------------------------

                self.publish_twist(
                    AUTONOMOUS_FORWARD_SPEED,
                    0.0
                )

        # ====================================================
        # AVOID TURN
        # ====================================================

        elif self.state == "AVOID_TURN":

            self.publish_twist(
                0.0,
                self.turn_direction *
                TURN_SPEED
            )

            # ------------------------------------------------
            # Stop turning when enough time has passed
            # OR front becomes clear
            # ------------------------------------------------

            if (

                now >= self.state_until

                or

                (
                    not math.isinf(self.front_min)
                    and
                    self.front_min >
                    FRONT_STOP_DIST * 1.3
                )

            ):

                self.stop()

                self.state = "FORWARD"

                rospy.loginfo(
                    "[AUTONOMOUS] "
                    "Path cleared -> FORWARD"
                )

        # ====================================================
        # REVERSE
        # ====================================================

        elif self.state == "REVERSE":

            self.publish_twist(
                -AUTONOMOUS_FORWARD_SPEED,
                0.0
            )

            if now >= self.state_until:

                self.stop()

                self.turn_direction = (
                    self.choose_turn_direction()
                )

                self.state = "AVOID_TURN"

                self.state_until = (
                    now +
                    TURN_TIME
                )

                if self.turn_direction > 0:

                    direction = "LEFT"

                else:

                    direction = "RIGHT"

                rospy.loginfo(
                    "[AUTONOMOUS] "
                    "Reverse complete -> TURN %s",
                    direction
                )

    # ========================================================
    # STAGE 9 - AUTONOMOUS LOOP
    # ========================================================

    def run_autonomous(self):

        rospy.loginfo(
            "=========================================="
        )

        rospy.loginfo(
            "AUTONOMOUS OBSTACLE AVOIDANCE STARTED"
        )

        rospy.loginfo(
            "LiDAR safety controller is active."
        )

        rospy.loginfo(
            "=========================================="
        )

        self.state = "FORWARD"

        while not rospy.is_shutdown():

            self.autonomous_step()

            self.rate.sleep()

        self.stop()


# ============================================================
# STAGE 5 - JSON EXTRACTION
# ============================================================

def extract_json_objects(text):

    objects = []

    if not text:
        return objects

    # --------------------------------------------------------
    # Remove markdown fences
    # --------------------------------------------------------

    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    # --------------------------------------------------------
    # Find balanced JSON objects
    # --------------------------------------------------------

    start = -1

    depth = 0

    in_string = False

    escaped = False

    for i in range(len(text)):

        char = text[i]

        if in_string:

            if escaped:

                escaped = False

            elif char == "\\":

                escaped = True

            elif char == '"':

                in_string = False

            continue

        if char == '"':

            in_string = True

        elif char == "{":

            if depth == 0:

                start = i

            depth += 1

        elif char == "}":

            if depth > 0:

                depth -= 1

            if depth == 0 and start >= 0:

                candidate = text[
                    start:i + 1
                ]

                try:

                    obj = json.loads(
                        candidate
                    )

                    objects.append(obj)

                except Exception:

                    pass

                start = -1

    return objects


# ============================================================
# STAGE 5 - NORMALIZE COMMAND
# ============================================================

def normalize_command(command):

    if not isinstance(
            command,
            dict
    ):

        return None

    action = command.get(
        "action"
    )

    if not action:

        return None

    action = str(
        action
    ).lower().strip()

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    if action == "stop":

        return {
            "action": "stop"
        }

    # --------------------------------------------------------
    # AUTONOMOUS
    # --------------------------------------------------------

    if action in [
        "autonomous",
        "avoid",
        "explore",
        "autonomous_avoid",
        "obstacle_avoidance"
    ]:

        return {
            "action": "autonomous_avoid"
        }

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if action in [
        "status",
        "robot_status",
        "sensor_status"
    ]:

        return {
            "action": "status"
        }

    # --------------------------------------------------------
    # MOVE
    # --------------------------------------------------------

    if action == "move":

        direction = str(
            command.get(
                "direction",
                "forward"
            )
        ).lower().strip()

        try:

            duration = float(
                command.get(
                    "duration",
                    1
                )
            )

        except Exception:

            duration = 1.0

        if direction not in [
            "forward",
            "backward"
        ]:

            return None

        if duration < 0.1:

            duration = 0.1

        if duration > 30:

            duration = 30

        return {
            "action": "move",
            "direction": direction,
            "duration": duration
        }

    # --------------------------------------------------------
    # TURN
    # --------------------------------------------------------

    if action == "turn":

        direction = str(
            command.get(
                "direction",
                "left"
            )
        ).lower().strip()

        try:

            duration = float(
                command.get(
                    "duration",
                    1
                )
            )

        except Exception:

            duration = 1.0

        if direction not in [
            "left",
            "right"
        ]:

            return None

        if duration < 0.1:

            duration = 0.1

        if duration > 20:

            duration = 20

        return {
            "action": "turn",
            "direction": direction,
            "duration": duration
        }

    return None


# ============================================================
# STAGE 5 - NATURAL LANGUAGE FALLBACK
# ============================================================

def natural_language_fallback(text):

    if not text:

        return None

    lower = text.lower()

    # --------------------------------------------------------
    # STOP
    # --------------------------------------------------------

    if re.search(
            r"\bstop\b",
            lower
    ):

        return {
            "action": "stop"
        }

    # --------------------------------------------------------
    # AUTONOMOUS OBSTACLE AVOIDANCE
    # --------------------------------------------------------

    autonomous_words = [

        "avoid obstacle",
        "avoid obstacles",
        "obstacle avoidance",
        "until you see an obstacle",
        "until there is an obstacle",
        "until you encounter an obstacle",
        "keep moving and avoid",
        "go around obstacles",
        "avoid anything in front",
        "don't hit anything",
        "do not hit anything",
        "without hitting",
        "explore while avoiding"

    ]

    for phrase in autonomous_words:

        if phrase in lower:

            return {
                "action": "autonomous_avoid"
            }

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if (
        "what is in front" in lower
        or
        "what's in front" in lower
        or
        "robot status" in lower
        or
        "sensor status" in lower
        or
        "lidar status" in lower
        or
        "is it safe" in lower
    ):

        return {
            "action": "status"
        }

    # --------------------------------------------------------
    # MOVE
    # --------------------------------------------------------

    move_match = re.search(
        r"(forward|backward).*?(\d+(?:\.\d+)?)\s*second",
        lower
    )

    if move_match:

        return {
            "action": "move",
            "direction": move_match.group(1),
            "duration": float(
                move_match.group(2)
            )
        }

    # --------------------------------------------------------
    # TURN
    # --------------------------------------------------------

    turn_match = re.search(
        r"(left|right).*?(\d+(?:\.\d+)?)\s*second",
        lower
    )

    if turn_match:

        return {
            "action": "turn",
            "direction": turn_match.group(1),
            "duration": float(
                turn_match.group(2)
            )
        }

    return None


# ============================================================
# STAGE 6 - LLM ROBOT NODE
# ============================================================

class LLMRobotNode(object):

    def __init__(self):

        rospy.init_node(
            "llm_robot_node"
        )

        # ----------------------------------------------------
        # Configuration
        # ----------------------------------------------------

        self.dry_run = DRY_RUN

        # ----------------------------------------------------
        # LLM session
        # ----------------------------------------------------

        self.session = requests.Session()

        # ----------------------------------------------------
        # Safety controller
        # ----------------------------------------------------

        self.safety = LidarSafetyController(
            self
        )

        # ----------------------------------------------------
        # State
        # ----------------------------------------------------

        self.current_movement = "stopped"

        self.running_autonomous = False

        rospy.loginfo(
            "LLM Robot Node started"
        )

        rospy.loginfo(
            "DRY_RUN = %s",
            self.dry_run
        )

        if not self.dry_run:

            rospy.loginfo(
                "REAL ROBOT CONTROL ENABLED"
            )

        else:

            rospy.logwarn(
                "DRY RUN ENABLED"
            )

        rospy.on_shutdown(
            self.shutdown
        )

    # ========================================================
    # STAGE 6 - LLM PROMPT
    # ========================================================

    def build_prompt(self, user_command):

        prompt = """
You are the intelligence of a mobile robot called JetAuto.

Convert the user's command into robot actions.

OUTPUT ONLY VALID JSON.

Do not explain anything.

For ONE action use:

{"action":"move","direction":"forward","duration":2}

or:

{"action":"move","direction":"backward","duration":2}

or:

{"action":"turn","direction":"left","duration":2}

or:

{"action":"turn","direction":"right","duration":2}

or:

{"action":"stop"}

or:

{"action":"status"}

For obstacle avoidance / autonomous movement use:

{"action":"autonomous_avoid"}

Use autonomous_avoid when the user asks the robot to:
- move until it sees an obstacle
- avoid obstacles
- go around obstacles
- keep moving while avoiding obstacles
- explore while avoiding obstacles
- move without hitting anything

The autonomous obstacle avoidance controller uses LiDAR.
Do NOT output multiple JSON objects for one command.

USER COMMAND:
%s
""" % user_command

        return prompt

    # ========================================================
    # STAGE 6 - CALL LOCAL QWEN
    # ========================================================

    def ask_llm(self, user_command):

        prompt = self.build_prompt(
            user_command
        )

        payload = {

            "prompt": prompt,

            "n_predict": 60,

            "temperature": 0,

            "top_k": 20,

            "top_p": 0.8,

            "stream": False

        }

        try:

            response = self.session.post(
                LLM_URL,
                json=payload,
                timeout=LLM_TIMEOUT
            )

            response.raise_for_status()

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
    # STAGE 5 - PARSE LLM RESPONSE
    # ========================================================

    def parse_response(self, response):

        if not response:

            return None

        # ----------------------------------------------------
        # First try JSON extraction
        # ----------------------------------------------------

        objects = extract_json_objects(
            response
        )

        if objects:

            # Prefer the first valid normalized command

            for obj in objects:

                command = normalize_command(
                    obj
                )

                if command:

                    return command

        # ----------------------------------------------------
        # Natural language fallback
        # ----------------------------------------------------

        rospy.logwarn(
            "JSON parsing failed. "
            "Trying natural-language fallback."
        )

        return natural_language_fallback(
            response
        )

    # ========================================================
    # STAGE 7 - ROBOT STATUS
    # ========================================================

    def print_status(self):

        front = self.safety.front_min

        left = self.safety.left_min

        right = self.safety.right_min

        rospy.loginfo(
            ""
        )

        rospy.loginfo(
            "========== ROBOT STATUS =========="
        )

        rospy.loginfo(
            "Movement : %s",
            self.current_movement
        )

        rospy.loginfo(
            "Moving   : %s",
            self.current_movement != "stopped"
        )

        if math.isinf(front):

            front_text = "no valid return"

        else:

            front_text = "%.2f m" % front

        if math.isinf(left):

            left_text = "no valid return"

        else:

            left_text = "%.2f m" % left

        if math.isinf(right):

            right_text = "no valid return"

        else:

            right_text = "%.2f m" % right

        rospy.loginfo(
            "Front    : %s",
            front_text
        )

        rospy.loginfo(
            "Left     : %s",
            left_text
        )

        rospy.loginfo(
            "Right    : %s",
            right_text
        )

        rospy.loginfo(
            "================================="
        )

    # ========================================================
    # STAGE 7 - SAFETY STATUS
    # ========================================================

    def is_front_safe(self):

        if not self.safety.scan_ready:

            return False

        if math.isinf(
                self.safety.front_min
        ):

            return not STOP_IF_FRONT_INVALID

        return (
            self.safety.front_min >
            FRONT_STOP_DIST
        )

    # ========================================================
    # STAGE 3 + STAGE 9
    # NORMAL MOVEMENT
    # ========================================================

    def execute_move(
            self,
            direction,
            duration
    ):

        rospy.loginfo(
            "Command: move %s for %.2f seconds",
            direction,
            duration
        )

        # ----------------------------------------------------
        # Safety check before forward movement
        # ----------------------------------------------------

        if direction == "forward":

            if not self.is_front_safe():

                rospy.logwarn(
                    "[SAFETY] Forward movement blocked."
                )

                self.stop_robot()

                return

        # ----------------------------------------------------
        # Select velocity
        # ----------------------------------------------------

        if direction == "forward":

            velocity = LINEAR_SPEED

        else:

            velocity = -LINEAR_SPEED

        # ----------------------------------------------------
        # Dry run
        # ----------------------------------------------------

        if self.dry_run:

            rospy.loginfo(
                "[DRY RUN] Would execute: "
                "move %s for %.2f seconds",
                direction,
                duration
            )

            self.current_movement = direction

            time.sleep(
                duration
            )

            self.current_movement = "stopped"

            return

        # ----------------------------------------------------
        # REAL ROBOT
        # ----------------------------------------------------

        rospy.loginfo(
            "Executing REAL robot movement."
        )

        start = rospy.get_time()

        self.current_movement = direction

        rate = rospy.Rate(
            CONTROL_RATE_HZ
        )

        while not rospy.is_shutdown():

            elapsed = (
                rospy.get_time() -
                start
            )

            if elapsed >= duration:

                break

            # ----------------------------------------------
            # Forward safety override
            # ----------------------------------------------

            if direction == "forward":

                if self.safety.front_blocked():

                    rospy.logwarn(
                        "[SAFETY] Obstacle detected "
                        "during forward movement."
                    )

                    self.stop_robot()

                    self.current_movement = "stopped"

                    return

            self.safety.publish_twist(
                velocity,
                0.0
            )

            rate.sleep()

        self.stop_robot()

    # ========================================================
    # STAGE 3 - TURN
    # ========================================================

    def execute_turn(
            self,
            direction,
            duration
    ):

        rospy.loginfo(
            "Command: turn %s for %.2f seconds",
            direction,
            duration
        )

        if direction == "left":

            angular = TURN_SPEED

        else:

            angular = -TURN_SPEED

        if self.dry_run:

            rospy.loginfo(
                "[DRY RUN] Would execute: "
                "turn %s for %.2f seconds",
                direction,
                duration
            )

            self.current_movement = (
                "turn_" + direction
            )

            time.sleep(
                duration
            )

            self.current_movement = "stopped"

            return

        rospy.loginfo(
            "Executing REAL robot turn."
        )

        start = rospy.get_time()

        self.current_movement = (
            "turn_" + direction
        )

        rate = rospy.Rate(
            CONTROL_RATE_HZ
        )

        while not rospy.is_shutdown():

            elapsed = (
                rospy.get_time() -
                start
            )

            if elapsed >= duration:

                break

            self.safety.publish_twist(
                0.0,
                angular
            )

            rate.sleep()

        self.stop_robot()

    # ========================================================
    # STAGE 3 - STOP
    # ========================================================

    def stop_robot(self):

        self.safety.stop()

        self.current_movement = "stopped"

        rospy.loginfo(
            "Robot STOPPED"
        )

    # ========================================================
    # STAGE 9 - AUTONOMOUS MODE
    # ========================================================

    def execute_autonomous(self):

        rospy.loginfo(
            ""
        )

        rospy.loginfo(
            "=========================================="
        )

        rospy.loginfo(
            "STARTING AUTONOMOUS OBSTACLE AVOIDANCE"
        )

        rospy.loginfo(
            "Robot will move forward continuously."
        )

        rospy.loginfo(
            "LiDAR will detect obstacles."
        )

        rospy.loginfo(
            "Robot will stop, turn or reverse."
        )

        rospy.loginfo(
            "=========================================="
        )

        self.running_autonomous = True

        self.current_movement = (
            "autonomous_avoidance"
        )

        # ----------------------------------------------------
        # This loop is intentionally blocking.
        #
        # The user can stop it with:
        #
        # Ctrl+C
        #
        # or another ROS command publishing zero velocity.
        # ----------------------------------------------------

        try:

            self.safety.run_autonomous()

        except Exception as e:

            rospy.logerr(
                "Autonomous controller error: %s",
                str(e)
            )

            self.stop_robot()

        self.running_autonomous = False

        self.current_movement = "stopped"

    # ========================================================
    # STAGE 4 + STAGE 8
    # EXECUTE COMMAND
    # ========================================================

    def execute_command(self, command):

        if not command:

            rospy.logerr(
                "No valid command."
            )

            self.stop_robot()

            return

        rospy.loginfo(
            "Parsed command: %s",
            json.dumps(
                command
            )
        )

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

        # ----------------------------------------------------
        # STATUS
        # ----------------------------------------------------

        if action == "status":

            self.print_status()

            return

        # ----------------------------------------------------
        # AUTONOMOUS
        # ----------------------------------------------------

        if action == "autonomous_avoid":

            self.execute_autonomous()

            return

        # ----------------------------------------------------
        # MOVE
        # ----------------------------------------------------

        if action == "move":

            self.execute_move(

                command.get(
                    "direction",
                    "forward"
                ),

                float(
                    command.get(
                        "duration",
                        1
                    )
                )

            )

            return

        # ----------------------------------------------------
        # TURN
        # ----------------------------------------------------

        if action == "turn":

            self.execute_turn(

                command.get(
                    "direction",
                    "left"
                ),

                float(
                    command.get(
                        "duration",
                        1
                    )
                )

            )

            return

        # ----------------------------------------------------
        # Unknown
        # ----------------------------------------------------

        rospy.logwarn(
            "Unknown action: %s",
            action
        )

        self.stop_robot()

    # ========================================================
    # STAGE 4 + STAGE 8
    # MULTI-COMMAND EXECUTION
    # ========================================================

    def execute_multiple_commands(
            self,
            commands
    ):

        if not commands:

            return

        total = len(
            commands
        )

        rospy.loginfo(
            "Executing %d commands.",
            total
        )

        for index, command in enumerate(
                commands
        ):

            if rospy.is_shutdown():

                break

            rospy.loginfo(
                "========== COMMAND %d / %d ==========",
                index + 1,
                total
            )

            rospy.loginfo(
                "Command: %s",
                json.dumps(
                    command
                )
            )

            self.execute_command(
                command
            )

            # ------------------------------------------------
            # Autonomous mode owns its own loop.
            # If it returns, continue.
            # ------------------------------------------------

            if command.get(
                    "action"
            ) == "stop":

                break

            rospy.sleep(
                0.1
            )

        self.stop_robot()

        rospy.loginfo(
            "Command sequence finished."
        )

    # ========================================================
    # STAGE 5
    # PARSE MULTIPLE JSON OBJECTS
    # ========================================================

    def parse_multiple_commands(
            self,
            response
    ):

        objects = extract_json_objects(
            response
        )

        commands = []

        for obj in objects:

            command = normalize_command(
                obj
            )

            if command:

                commands.append(
                    command
                )

        return commands

    # ========================================================
    # STAGE 7
    # DIRECT SENSOR QUESTIONS
    # ========================================================

    def handle_direct_question(
            self,
            user_command
    ):

        lower = user_command.lower()

        # ----------------------------------------------------
        # FRONT QUESTION
        # ----------------------------------------------------

        if (
            "what is in front" in lower
            or
            "what's in front" in lower
        ):

            self.print_status()

            return True

        # ----------------------------------------------------
        # SAFE QUESTION
        # ----------------------------------------------------

        if "safe to move forward" in lower:

            if self.is_front_safe():

                if math.isinf(
                        self.safety.front_min
                ):

                    rospy.loginfo(
                        "No valid front LiDAR return."
                    )

                else:

                    rospy.loginfo(
                        "Forward path currently appears "
                        "safe. Front=%.2f m",
                        self.safety.front_min
                    )

            else:

                rospy.logwarn(
                    "Forward movement is NOT safe."
                )

            return True

        return False

    # ========================================================
    # STAGE 1-9
    # MAIN RUN LOOP
    # ========================================================

    def run(self):

        rospy.loginfo(
            ""
        )

        rospy.loginfo(
            "=========================================="
        )

        rospy.loginfo(
            "JetAuto LLM Robot"
        )

        rospy.loginfo(
            "Stages 1-9 loaded"
        )

        rospy.loginfo(
            "LiDAR safety controller loaded"
        )

        rospy.loginfo(
            "=========================================="
        )

        while not rospy.is_shutdown():

            try:

                # ------------------------------------------------
                # USER INPUT
                # ------------------------------------------------

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

            rospy.loginfo(
                "User command: %s",
                user_command
            )

            # ------------------------------------------------
            # Direct sensor question
            # ------------------------------------------------

            if self.handle_direct_question(
                    user_command
            ):

                continue

            # ------------------------------------------------
            # Ask LLM
            # ------------------------------------------------

            response = self.ask_llm(
                user_command
            )

            if not response:

                self.stop_robot()

                continue

            # ------------------------------------------------
            # Try multiple JSON commands
            # ------------------------------------------------

            commands = (
                self.parse_multiple_commands(
                    response
                )
            )

            # ------------------------------------------------
            # If multiple commands found
            # ------------------------------------------------

            if len(commands) > 1:

                self.execute_multiple_commands(
                    commands
                )

                continue

            # ------------------------------------------------
            # If one command found
            # ------------------------------------------------

            if len(commands) == 1:

                self.execute_command(
                    commands[0]
                )

                continue

            # ------------------------------------------------
            # Try normal parser
            # ------------------------------------------------

            command = self.parse_response(
                response
            )

            if command:

                self.execute_command(
                    command
                )

                continue

            # ------------------------------------------------
            # Nothing worked
            # ------------------------------------------------

            rospy.logerr(
                "Could not parse LLM response."
            )

            self.stop_robot()

    # ========================================================
    # SHUTDOWN
    # ========================================================

    def shutdown(self):

        rospy.loginfo(
            "Shutting down LLM Robot Node."
        )

        try:

            self.safety.stop()

            # Publish several stop messages
            # to make sure the motor controller receives it.

            for _ in range(6):

                self.safety.stop()

                rospy.sleep(
                    0.05
                )

        except Exception:

            pass


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:

        node = LLMRobotNode()

        node.run()

    except rospy.ROSInterruptException:

        pass

    except KeyboardInterrupt:

        pass


