# Camera access

# -*- coding: utf-8 -*-

"""
STAGE 7 - CAMERA CONTROLLER

JetAuto cameras:
    1. Astra RGB-D camera
       RGB   : /astra_cam/rgb/image_raw
       Depth : /astra_cam/depth/image_raw

    2. USB camera
       RGB   : /usb_cam/image_raw

Responsibilities:
    - Access both cameras
    - Receive RGB frames
    - Receive depth frames from Astra
    - Check camera availability
    - Capture images
    - Save images to disk
    - Provide latest frames to vision modules

Python:
    Python 2 compatible
"""

import os
import time
import rospy

from sensor_msgs.msg import Image

try:
    from cv_bridge import CvBridge
    CV_BRIDGE_AVAILABLE = True
except ImportError:
    CV_BRIDGE_AVAILABLE = False


class CameraController(object):

    # ============================================================
    # CAMERA TOPICS
    # ============================================================

    ASTRA_RGB_TOPIC = "/astra_cam/rgb/image_raw"
    ASTRA_DEPTH_TOPIC = "/astra_cam/depth/image_raw"

    USB_RGB_TOPIC = "/usb_cam/image_raw"

    # ============================================================
    # DEFAULT SAVE DIRECTORY
    # ============================================================

    DEFAULT_SAVE_DIR = os.path.expanduser(
        "~/jetauto_camera_data"
    )

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self, save_dir=None):

        self.save_dir = save_dir or self.DEFAULT_SAVE_DIR

        if not os.path.exists(self.save_dir):
            try:
                os.makedirs(self.save_dir)
            except OSError:
                pass

        self.bridge = None

        if CV_BRIDGE_AVAILABLE:
            self.bridge = CvBridge()

        # Latest ROS images
        self.astra_rgb = None
        self.astra_depth = None
        self.usb_rgb = None

        # Availability flags
        self.astra_rgb_received = False
        self.astra_depth_received = False
        self.usb_rgb_received = False

        # Subscribers
        self.astra_rgb_sub = rospy.Subscriber(
            self.ASTRA_RGB_TOPIC,
            Image,
            self.astra_rgb_callback,
            queue_size=1
        )

        self.astra_depth_sub = rospy.Subscriber(
            self.ASTRA_DEPTH_TOPIC,
            Image,
            self.astra_depth_callback,
            queue_size=1
        )

        self.usb_rgb_sub = rospy.Subscriber(
            self.USB_RGB_TOPIC,
            Image,
            self.usb_rgb_callback,
            queue_size=1
        )

        rospy.loginfo(
            "CameraController initialized"
        )

        rospy.loginfo(
            "Astra RGB  : %s",
            self.ASTRA_RGB_TOPIC
        )

        rospy.loginfo(
            "Astra Depth: %s",
            self.ASTRA_DEPTH_TOPIC
        )

        rospy.loginfo(
            "USB RGB    : %s",
            self.USB_RGB_TOPIC
        )

    # ============================================================
    # CALLBACKS
    # ============================================================

    def astra_rgb_callback(self, msg):

        self.astra_rgb = msg
        self.astra_rgb_received = True

    def astra_depth_callback(self, msg):

        self.astra_depth = msg
        self.astra_depth_received = True

    def usb_rgb_callback(self, msg):

        self.usb_rgb = msg
        self.usb_rgb_received = True

    # ============================================================
    # CAMERA AVAILABILITY
    # ============================================================

    def is_astra_available(self):

        return self.astra_rgb_received

    def is_astra_depth_available(self):

        return self.astra_depth_received

    def is_usb_available(self):

        return self.usb_rgb_received

    # ============================================================
    # GET ROS IMAGE
    # ============================================================

    def get_astra_rgb(self):

        return self.astra_rgb

    def get_astra_depth(self):

        return self.astra_depth

    def get_usb_rgb(self):

        return self.usb_rgb

    # ============================================================
    # CONVERT ROS IMAGE -> OPENCV IMAGE
    # ============================================================

    def ros_to_cv(self, ros_image, encoding="bgr8"):

        if ros_image is None:
            return None

        if self.bridge is None:
            rospy.logwarn(
                "cv_bridge is not available."
            )
            return None

        try:

            return self.bridge.imgmsg_to_cv2(
                ros_image,
                desired_encoding=encoding
            )

        except Exception as e:

            rospy.logerr(
                "Image conversion failed: %s" % str(e)
            )

            return None

    # ============================================================
    # GET OPENCV FRAMES
    # ============================================================

    def get_astra_rgb_cv(self):

        return self.ros_to_cv(
            self.astra_rgb,
            "bgr8"
        )

    def get_astra_depth_cv(self):

        return self.ros_to_cv(
            self.astra_depth,
            "passthrough"
        )

    def get_usb_rgb_cv(self):

        return self.ros_to_cv(
            self.usb_rgb,
            "bgr8"
        )

    # ============================================================
    # SAVE IMAGE
    # ============================================================

    def save_image(self, camera="astra", filename=None):

        if not CV_BRIDGE_AVAILABLE:

            rospy.logerr(
                "Cannot save image: cv_bridge unavailable."
            )

            return None

        # --------------------------------------------------------
        # Select camera
        # --------------------------------------------------------

        if camera == "astra":

            image = self.get_astra_rgb_cv()

        elif camera == "usb":

            image = self.get_usb_rgb_cv()

        else:

            rospy.logerr(
                "Unknown camera: %s" % camera
            )

            return None

        # --------------------------------------------------------
        # Check frame
        # --------------------------------------------------------

        if image is None:

            rospy.logwarn(
                "No image available from %s camera." % camera
            )

            return None

        # --------------------------------------------------------
        # Filename
        # --------------------------------------------------------

        if filename is None:

            timestamp = time.strftime(
                "%Y%m%d_%H%M%S"
            )

            filename = (
                "%s_%s.jpg"
                % (camera, timestamp)
            )

        filepath = os.path.join(
            self.save_dir,
            filename
        )

        # --------------------------------------------------------
        # OpenCV save
        # --------------------------------------------------------

        try:

            import cv2

            success = cv2.imwrite(
                filepath,
                image
            )

            if success:

                rospy.loginfo(
                    "Image saved: %s" % filepath
                )

                return filepath

            else:

                rospy.logerr(
                    "Failed to save image."
                )

                return None

        except Exception as e:

            rospy.logerr(
                "Image save error: %s" % str(e)
            )

            return None

    # ============================================================
    # CAMERA STATUS
    # ============================================================

    def get_status(self):

        return {
            "astra_rgb": self.astra_rgb_received,
            "astra_depth": self.astra_depth_received,
            "usb_rgb": self.usb_rgb_received,
            "cv_bridge": CV_BRIDGE_AVAILABLE,
            "save_directory": self.save_dir
        }

    # ============================================================
    # PRINT STATUS
    # ============================================================

    def print_status(self):

        status = self.get_status()

        print("")
        print("========== CAMERA STATUS ==========")
        print(
            "Astra RGB   : %s"
            % status["astra_rgb"]
        )
        print(
            "Astra Depth : %s"
            % status["astra_depth"]
        )
        print(
            "USB RGB     : %s"
            % status["usb_rgb"]
        )
        print(
            "cv_bridge   : %s"
            % status["cv_bridge"]
        )
        print(
            "Save dir    : %s"
            % status["save_directory"]
        )
        print("===================================")
        print("")

    # ============================================================
    # WAIT FOR CAMERAS
    # ============================================================

    def wait_for_camera(self, timeout=5.0):

        start = time.time()

        while not rospy.is_shutdown():

            if (
                self.astra_rgb_received
                or self.usb_rgb_received
            ):

                return True

            if time.time() - start >= timeout:

                return False

            rospy.sleep(0.1)

        return False


# =================================================================
# DIRECT TEST
# =================================================================

if __name__ == "__main__":

    rospy.init_node(
        "camera_controller_test",
        anonymous=True
    )

    camera = CameraController()

    rospy.loginfo(
        "Waiting for camera frames..."
    )

    camera.wait_for_camera(10.0)

    rate = rospy.Rate(1)

    while not rospy.is_shutdown():

        camera.print_status()

        rate.sleep()
