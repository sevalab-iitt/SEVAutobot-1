## The ROS robo control layer.

cd ~/catkin_ws/src
mkdir -p jetauto_ai/scripts
mkdir -p jetauto_ai/config
mkdir -p jetauto_ai/launch
---
cd ~/catkin_ws/src/jetauto_ai
touch package.xml
touch CMakeLists.txt
---
```
jetauto_ai/
├── CMakeLists.txt
├── package.xml
│
├── scripts/
│   ├── ai_agent.py
│   ├── robot_tools.py
│   └── safety.py
│
├── config/
│   └── robot.yaml
│
└── launch/
    └── ai.launch
```
    <img width="913" height="362" alt="image" src="https://github.com/user-attachments/assets/ac1dd6bd-e0c6-4a47-8883-b5e3b3a1020b" />

Step 2 — Create robot_tools.py

Run:

cd ~/catkin_ws/src/jetauto_ai/scripts
nano robot_tools.py

Paste this:

#!/usr/bin/env python3


import rospy
from geometry_msgs.msg import Twist




class JetAutoRobot:
    def __init__(self):
        rospy.init_node("jetauto_robot_tools", anonymous=True)


        self.cmd_pub = rospy.Publisher(
            "/jetauto_controller/cmd_vel",
            Twist,
            queue_size=10
        )


        rospy.sleep(1)


    def stop(self):
        msg = Twist()
        self.cmd_pub.publish(msg)
        rospy.loginfo("JetAuto: STOP")


    def move_forward(self, speed=0.1, duration=1.0):
        msg = Twist()
        msg.linear.x = speed


        rate = rospy.Rate(20)
        end_time = rospy.Time.now() + rospy.Duration(duration)


        rospy.loginfo(
            "JetAuto: moving forward | speed=%.2f | duration=%.2f",
            speed,
            duration
        )


        while rospy.Time.now() < end_time and not rospy.is_shutdown():
            self.cmd_pub.publish(msg)
            rate.sleep()


        self.stop()


    def move_backward(self, speed=0.1, duration=1.0):
        msg = Twist()
        msg.linear.x = -speed


        rate = rospy.Rate(20)
        end_time = rospy.Time.now() + rospy.Duration(duration)


        rospy.loginfo(
            "JetAuto: moving backward | speed=%.2f | duration=%.2f",
            speed,
            duration
        )


        while rospy.Time.now() < end_time and not rospy.is_shutdown():
            self.cmd_pub.publish(msg)
            rate.sleep()


        self.stop()


    def rotate(self, angular_speed=0.5, duration=1.0):
        msg = Twist()
        msg.angular.z = angular_speed


        rate = rospy.Rate(20)
        end_time = rospy.Time.now() + rospy.Duration(duration)


        rospy.loginfo(
            "JetAuto: rotating | speed=%.2f | duration=%.2f",
            angular_speed,
            duration
        )


        while rospy.Time.now() < end_time and not rospy.is_shutdown():
            self.cmd_pub.publish(msg)
            rate.sleep()


        self.stop()




if __name__ == "__main__":
    robot = JetAutoRobot()


    rospy.loginfo("JetAuto robot tools ready.")


    rospy.spin()

Save:

Ctrl+O → Enter → Ctrl+X

Then:

chmod +x robot_tools.py
Step 3 — Test it

Run:

cd ~/catkin_ws
catkin_make

Then:

source devel/setup.bash

Start the tool:

rosrun jetauto_ai robot_tools.py

You should see:

JetAuto robot tools ready.

Leave it running.

Step 4 — Test the actual Python tool

Open another terminal:

source ~/catkin_ws/devel/setup.bash

Then:

python3 -c "
import sys
sys.path.append('$HOME/catkin_ws/src/jetauto_ai/scripts')
from robot_tools import JetAutoRobot
import rospy


robot = JetAutoRobot()
robot.move_forward(0.1, 1.0)
"

1. Replace package.xml

Run:

cd ~/catkin_ws/src/jetauto_ai
nano package.xml

Paste:

<?xml version="1.0"?>
<package format="2">


  <name>jetauto_ai</name>
  <version>0.0.1</version>


  <description>AI intelligence layer for JetAuto</description>


  <maintainer email="jetauto@localhost">jetauto</maintainer>
  <license>MIT</license>


  <buildtool_depend>catkin</buildtool_depend>


  <depend>rospy</depend>
  <depend>geometry_msgs</depend>


</package>

Save:

Ctrl+O → Enter → Ctrl+X

2. Build again
cd ~/catkin_ws
catkin_make

You should now get something similar to:

[100%] Built target ...

Then:

source ~/catkin_ws/devel/setup.bash
3. Check that ROS sees the package
rospack find jetauto_ai

It should return:

/home/jetauto/catkin_ws/src/jetauto_ai
4. Then start our robot tool
rosrun jetauto_ai robot_tools.py


cd ~/catkin_ws/src/jetauto_ai
nano package.xml
change to this <maintainer email="jetauto@example.com">jetauto</maintainer>

chmod +x ~/catkin_ws/src/jetauto_ai/scripts/robot_tools.py
cd ~/catkin_ws
catkin_make
```
jetauto@jetauto-desktop:~/catkin_ws$ catkin_make
Base path: /home/jetauto/catkin_ws
Source space: /home/jetauto/catkin_ws/src
Build space: /home/jetauto/catkin_ws/build
Devel space: /home/jetauto/catkin_ws/devel
Install space: /home/jetauto/catkin_ws/install
####
#### Running command: "cmake /home/jetauto/catkin_ws/src -DCATKIN_DEVEL_PREFIX=/home/jetauto/catkin_ws/devel -DCMAKE_INSTALL_PREFIX=/home/jetauto/catkin_ws/install -G Unix Makefiles" in "/home/jetauto/catkin_ws/build"
####
-- Using CATKIN_DEVEL_PREFIX: /home/jetauto/catkin_ws/devel
-- Using CMAKE_PREFIX_PATH: /home/jetauto/catkin_ws/devel;/home/jetauto/jetauto_ws/devel;/opt/ros/melodic
-- This workspace overlays: /home/jetauto/catkin_ws/devel;/home/jetauto/jetauto_ws/devel;/opt/ros/melodic
-- Found PythonInterp: /usr/bin/python2 (found suitable version "2.7.17", minimum required is "2")
-- Using PYTHON_EXECUTABLE: /usr/bin/python2
-- Using Debian Python package layout
-- Using empy: /usr/bin/empy
-- Using CATKIN_ENABLE_TESTING: ON
-- Call enable_testing()
-- Using CATKIN_TEST_RESULTS_DIR: /home/jetauto/catkin_ws/build/test_results
-- Found gtest sources under '/usr/src/googletest': gtests will be built
-- Found gmock sources under '/usr/src/googletest': gmock will be built
-- Found PythonInterp: /usr/bin/python2 (found version "2.7.17")
-- Using Python nosetests: /usr/bin/nosetests-2.7
-- catkin 0.7.29
-- BUILD_SHARED_LIBS is on
-- BUILD_SHARED_LIBS is on
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- ~~  traversing 4 packages in topological order:
-- ~~  - jetauto_ai
-- ~~  - astra_demo
-- ~~  - pointcloud_segmentation
-- ~~  - jetauto_pointcloud_mapping
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- +++ processing catkin package: 'jetauto_ai'
-- ==> add_subdirectory(jetauto_ai)
-- +++ processing catkin package: 'astra_demo'
-- ==> add_subdirectory(astra_demo)
-- +++ processing catkin package: 'pointcloud_segmentation'
-- ==> add_subdirectory(pointcloud_segmentation)
-- +++ processing catkin package: 'jetauto_pointcloud_mapping'
-- ==> add_subdirectory(jetauto_pointcloud_mapping)
-- Using these message generators: gencpp;geneus;genlisp;gennodejs;genpy
-- Configuring done
-- Generating done
-- Build files have been written to: /home/jetauto/catkin_ws/build
####
#### Running command: "make -j4 -l4" in "/home/jetauto/catkin_ws/build"
####
jetauto@jetauto-desktop:~/catkin_ws$ source ~/catkin_ws/devel/setup.bash
jetauto@jetauto-desktop:~/catkin_ws$ rospack find jetauto_ai
/home/jetauto/catkin_ws/src/jetauto_ai
jetauto@jetauto-desktop:~/catkin_ws$ source devel/setup.bash
jetauto@jetauto-desktop:~/catkin_ws$ rosrun jetauto_ai robot_tools.py
[INFO] [1787171124.121105]: JetAuto robot tools ready.
```
jetauto@jetauto-desktop:~$ source ~/catkin_ws/devel/setup.bash
jetauto@jetauto-desktop:~$ cd ~/catkin_ws/
jetauto@jetauto-desktop:~/catkin_ws$ source ~/catkin_ws/devel/setup.bash
jetauto@jetauto-desktop:~/catkin_ws$ python3 -c "
> import sys
> sys.path.append('$HOME/catkin_ws/src/jetauto_ai/scripts')
> from robot_tools import JetAutoRobot
> import rospy
>
> robot = JetAutoRobot()
> robot.move_forward(0.1, 1.0)
> "
[INFO] [1787171205.237217]: JetAuto: moving forward | speed=0.10 | duration=1.00
[INFO] [1787171206.237379]: JetAuto: STOP

```
Python function
      ↓
JetAutoRobot.move_forward()
      ↓
ROS Publisher
      ↓
/jetauto_controller/cmd_vel
      ↓
JetAuto
```
---

## LLM 

installing the OpenAI Python SDK

python3 -m pip install --user --upgrade openai

```
jetauto@jetauto-desktop:~/catkin_ws$ python3 -m pip install --user --upgrade openai
/usr/lib/python3/dist-packages/secretstorage/dhcrypto.py:15: CryptographyDeprecationWarning: Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in cryptography and will be removed in a future release.
  from cryptography.utils import int_from_bytes
Collecting openai
  Downloading openai-0.10.5.tar.gz (157 kB)
     |██                              | 10 kB 748 kB/s eta 0:00:     |████▏                           | 20 kB 958 kB/s eta 0:00:     |██████▎                         | 30 kB 648 kB/s eta 0:00:     |████████▍                       | 40 kB 538 kB/s eta 0:00:     |██████████▍                     | 51 kB 638 kB/s eta 0:00:     |████████████▌                   | 61 kB 760 kB/s eta 0:00:     |██████████████▋                 | 71 kB 719 kB/s eta 0:00:     |████████████████▊               | 81 kB 817 kB/s eta 0:00:     |██████████████████▊             | 92 kB 769 kB/s eta 0:00:     |████████████████████▉           | 102 kB 619 kB/s eta 0:00     |███████████████████████         | 112 kB 619 kB/s eta 0:00     |█████████████████████████       | 122 kB 619 kB/s eta 0:00     |███████████████████████████     | 133 kB 619 kB/s eta 0:00     |█████████████████████████████▏  | 143 kB 619 kB/s eta 0:00     |███████████████████████████████▎| 153 kB 619 kB/s eta 0:00     |████████████████████████████████| 157 kB 619 kB/s         
  Preparing metadata (setup.py) ... done
Requirement already satisfied: requests>=2.20 in /usr/local/lib/python3.6/dist-packages (from openai) (2.27.1)
Requirement already satisfied: tqdm in /usr/local/lib/python3.6/dist-packages (from openai) (4.64.0)
  Downloading openai-0.10.4.tar.gz (157 kB)
     |██                              | 10 kB 1.8 MB/s eta 0:00:     |████▏                           | 20 kB 1.3 MB/s eta 0:00:     |██████▎                         | 30 kB 1.8 MB/s eta 0:00:     |████████▎                       | 40 kB 1.2 MB/s eta 0:00:     |██████████▍                     | 51 kB 1.1 MB/s eta 0:00:     |████████████▌                   | 61 kB 1.3 MB/s eta 0:00:     |██████████████▋                 | 71 kB 1.0 MB/s eta 0:00:     |████████████████▋               | 81 kB 1.1 MB/s eta 0:00:     |██████████████████▊             | 92 kB 1.3 MB/s eta 0:00:     |████████████████████▉           | 102 kB 1.0 MB/s eta 0:00     |███████████████████████         | 112 kB 1.0 MB/s eta 0:00     |█████████████████████████       | 122 kB 1.0 MB/s eta 0:00     |███████████████████████████     | 133 kB 1.0 MB/s eta 0:00     |█████████████████████████████▏  | 143 kB 1.0 MB/s eta 0:00     |███████████████████████████████▎| 153 kB 1.0 MB/s eta 0:00     |████████████████████████████████| 157 kB 1.0 MB/s         
  Preparing metadata (setup.py) ... done
  Downloading openai-0.10.3.tar.gz (157 kB)
     |██                              | 10 kB 307 kB/s eta 0:00:     |████▏                           | 20 kB 307 kB/s eta 0:00:     |██████▎                         | 30 kB 458 kB/s eta 0:00:     |████████▍                       | 40 kB 444 kB/s eta 0:00:     |██████████▍                     | 51 kB 523 kB/s eta 0:00:     |████████████▌                   | 61 kB 625 kB/s eta 0:00:     |██████████████▋                 | 71 kB 503 kB/s eta 0:00:     |████████████████▊               | 81 kB 573 kB/s eta 0:00:     |██████████████████▉             | 92 kB 592 kB/s eta 0:00:     |████████████████████▉           | 102 kB 585 kB/s eta 0:00     |███████████████████████         | 112 kB 585 kB/s eta 0:00     |█████████████████████████       | 122 kB 585 kB/s eta 0:00     |███████████████████████████▏    | 133 kB 585 kB/s eta 0:00     |█████████████████████████████▏  | 143 kB 585 kB/s eta 0:00     |███████████████████████████████▎| 153 kB 585 kB/s eta 0:00     |████████████████████████████████| 157 kB 585 kB/s         
  Preparing metadata (setup.py) ... done
  Downloading openai-0.10.2.tar.gz (156 kB)
     |██                              | 10 kB 560 kB/s eta 0:00:     |████▏                           | 20 kB 843 kB/s eta 0:00:     |██████▎                         | 30 kB 1.2 MB/s eta 0:00:     |████████▍                       | 40 kB 1.1 MB/s eta 0:00:     |██████████▌                     | 51 kB 558 kB/s eta 0:00:     |████████████▌                   | 61 kB 666 kB/s eta 0:00:     |██████████████▋                 | 71 kB 513 kB/s eta 0:00:     |████████████████▊               | 81 kB 585 kB/s eta 0:00:     |██████████████████▉             | 92 kB 656 kB/s eta 0:00:     |█████████████████████           | 102 kB 597 kB/s eta 0:00     |███████████████████████         | 112 kB 597 kB/s eta 0:00     |█████████████████████████       | 122 kB 597 kB/s eta 0:00     |███████████████████████████▏    | 133 kB 597 kB/s eta 0:00     |█████████████████████████████▎  | 143 kB 597 kB/s eta 0:00     |███████████████████████████████▍| 153 kB 597 kB/s eta 0:00     |████████████████████████████████| 156 kB 597 kB/s         
  Preparing metadata (setup.py) ... done
  Downloading openai-0.10.1.tar.gz (155 kB)
     |██                              | 10 kB 212 kB/s eta 0:00:     |████▏                           | 20 kB 420 kB/s eta 0:00:     |██████▎                         | 30 kB 388 kB/s eta 0:00:     |████████▍                       | 40 kB 514 kB/s eta 0:00:     |██████████▌                     | 51 kB 605 kB/s eta 0:00:     |████████████▋                   | 61 kB 600 kB/s eta 0:00:     |██████████████▊                 | 71 kB 697 kB/s eta 0:00:     |████████████████▉               | 81 kB 613 kB/s eta 0:00:     |███████████████████             | 92 kB 642 kB/s eta 0:00:     |█████████████████████           | 102 kB 711 kB/s eta 0:00     |███████████████████████▏        | 112 kB 711 kB/s eta 0:00     |█████████████████████████▏      | 122 kB 711 kB/s eta 0:00     |███████████████████████████▎    | 133 kB 711 kB/s eta 0:00     |█████████████████████████████▍  | 143 kB 711 kB/s eta 0:00     |███████████████████████████████▌| 153 kB 711 kB/s eta 0:00     |████████████████████████████████| 155 kB 711 kB/s         
  Preparing metadata (setup.py) ... done
  Downloading openai-0.10.0.tar.gz (155 kB)
     |██                              | 10 kB 198 kB/s eta 0:00:     |████▏                           | 20 kB 346 kB/s eta 0:00:     |██████▎                         | 30 kB 514 kB/s eta 0:00:     |████████▍                       | 40 kB 488 kB/s eta 0:00:     |██████████▌                     | 51 kB 490 kB/s eta 0:00:     |████████████▋                   | 61 kB 584 kB/s eta 0:00:     |██████████████▊                 | 71 kB 502 kB/s eta 0:00:     |████████████████▉               | 81 kB 571 kB/s eta 0:00:     |███████████████████             | 92 kB 533 kB/s eta 0:00:     |█████████████████████           | 102 kB 529 kB/s eta 0:00     |███████████████████████▏        | 112 kB 529 kB/s eta 0:00     |█████████████████████████▎      | 122 kB 529 kB/s eta 0:00     |███████████████████████████▍    | 133 kB 529 kB/s eta 0:00     |█████████████████████████████▌  | 143 kB 529 kB/s eta 0:00     |███████████████████████████████▋| 153 kB 529 kB/s eta 0:00     |████████████████████████████████| 155 kB 529 kB/s         
  Preparing metadata (setup.py) ... done
  Downloading openai-0.9.4.tar.gz (156 kB)
     |██                              | 10 kB 447 kB/s eta 0:00:     |████▏                           | 20 kB 871 kB/s eta 0:00:     |██████▎                         | 30 kB 680 kB/s eta 0:00:     |████████▍                       | 40 kB 895 kB/s eta 0:00:     |██████████▌                     | 51 kB 814 kB/s eta 0:00:     |████████████▋                   | 61 kB 813 kB/s eta 0:00:     |██████████████▊                 | 71 kB 942 kB/s eta 0:00:     |████████████████▉               | 81 kB 978 kB/s eta 0:00:     |███████████████████             | 92 kB 1.1 MB/s eta 0:00:     |█████████████████████           | 102 kB 1.2 MB/s eta 0:00     |███████████████████████         | 112 kB 1.2 MB/s eta 0:00     |█████████████████████████▏      | 122 kB 1.2 MB/s eta 0:00     |███████████████████████████▎    | 133 kB 1.2 MB/s eta 0:00     |█████████████████████████████▍  | 143 kB 1.2 MB/s eta 0:00     |███████████████████████████████▌| 153 kB 1.2 MB/s eta 0:00     |████████████████████████████████| 156 kB 1.2 MB/s         
  Preparing metadata (setup.py) ... done
  Downloading openai-0.9.3.tar.gz (155 kB)
     |██                              | 10 kB 1.6 MB/s eta 0:00:     |████▏                           | 20 kB 586 kB/s eta 0:00:     |██████▎                         | 30 kB 864 kB/s eta 0:00:     |████████▍                       | 40 kB 822 kB/s eta 0:00:     |██████████▌                     | 51 kB 502 kB/s eta 0:00:     |████████████▋                   | 61 kB 600 kB/s eta 0:00:     |██████████████▊                 | 71 kB 529 kB/s eta 0:00:     |████████████████▉               | 81 kB 602 kB/s eta 0:00:     |███████████████████             | 92 kB 610 kB/s eta 0:00:     |█████████████████████           | 102 kB 650 kB/s eta 0:00     |███████████████████████▏        | 112 kB 650 kB/s eta 0:00     |█████████████████████████▏      | 122 kB 650 kB/s eta 0:00     |███████████████████████████▎    | 133 kB 650 kB/s eta 0:00     |█████████████████████████████▍  | 143 kB 650 kB/s eta 0:00     |███████████████████████████████▌| 153 kB 650 kB/s eta 0:00     |████████████████████████████████| 155 kB 650 kB/s         
  Preparing metadata (setup.py) ... done
  Downloading openai-0.9.2.tar.gz (155 kB)
     |██                              | 10 kB 405 kB/s eta 0:00:     |████▏                           | 20 kB 498 kB/s eta 0:00:     |██████▎                         | 30 kB 737 kB/s eta 0:00:     |████████▍                       | 40 kB 404 kB/s eta 0:00:     |██████████▌                     | 51 kB 414 kB/s eta 0:00:     |████████████▋                   | 61 kB 495 kB/s eta 0:00:     |██████████████▊                 | 71 kB 499 kB/s eta 0:00:     |████████████████▉               | 81 kB 568 kB/s eta 0:00:     |███████████████████             | 92 kB 555 kB/s eta 0:00:     |█████████████████████           | 102 kB 534 kB/s eta 0:00     |███████████████████████▏        | 112 kB 534 kB/s eta 0:00     |█████████████████████████▎      | 122 kB 534 kB/s eta 0:00     |███████████████████████████▎    | 133 kB 534 kB/s eta 0:00     |█████████████████████████████▍  | 143 kB 534 kB/s eta 0:00     |███████████████████████████████▌| 153 kB 534 kB/s eta 0:00     |████████████████████████████████| 155 kB 534 kB/s         
  Preparing metadata (setup.py) ... done
  Downloading openai-0.9.1.tar.gz (156 kB)
     |██                              | 10 kB 427 kB/s eta 0:00:     |████▏                           | 20 kB 835 kB/s eta 0:00:     |██████▎                         | 30 kB 589 kB/s eta 0:00:     |████████▍                       | 40 kB 777 kB/s eta 0:00:     |██████████▌                     | 51 kB 900 kB/s eta 0:00:     |████████████▋                   | 61 kB 812 kB/s eta 0:00:     |██████████████▊                 | 71 kB 934 kB/s eta 0:00:     |████████████████▉               | 81 kB 1.1 MB/s eta 0:00:     |███████████████████             | 92 kB 1.2 MB/s eta 0:00:     |█████████████████████           | 102 kB 1.3 MB/s eta 0:00     |███████████████████████         | 112 kB 1.3 MB/s eta 0:00     |█████████████████████████▏      | 122 kB 1.3 MB/s eta 0:00     |███████████████████████████▎    | 133 kB 1.3 MB/s eta 0:00     |█████████████████████████████▍  | 143 kB 1.3 MB/s eta 0:00     |███████████████████████████████▌| 153 kB 1.3 MB/s eta 0:00     |████████████████████████████████| 156 kB 1.3 MB/s         
  Preparing metadata (setup.py) ... done
  Downloading openai-0.9.0.tar.gz (155 kB)
     |██                              | 10 kB 412 kB/s eta 0:00:     |████▏                           | 20 kB 538 kB/s eta 0:00:     |██████▎                         | 30 kB 791 kB/s eta 0:00:     |████████▍                       | 40 kB 556 kB/s eta 0:00:     |██████████▌                     | 51 kB 375 kB/s eta 0:00:     |████████████▋                   | 61 kB 448 kB/s eta 0:00:     |██████████████▊                 | 71 kB 521 kB/s eta 0:00:     |████████████████▉               | 81 kB 593 kB/s eta 0:00:     |███████████████████             | 92 kB 539 kB/s eta 0:00:     |█████████████████████           | 102 kB 511 kB/s eta 0:00     |███████████████████████▏        | 112 kB 511 kB/s eta 0:00     |█████████████████████████▎      | 122 kB 511 kB/s eta 0:00     |███████████████████████████▎    | 133 kB 511 kB/s eta 0:00     |█████████████████████████████▍  | 143 kB 511 kB/s eta 0:00     |███████████████████████████████▌| 153 kB 511 kB/s eta 0:00     |████████████████████████████████| 155 kB 511 kB/s         
  Preparing metadata (setup.py) ... done
  Downloading openai-0.8.0.tar.gz (147 kB)
     |██▏                             | 10 kB 355 kB/s eta 0:00:     |████▍                           | 20 kB 310 kB/s eta 0:00:     |██████▋                         | 30 kB 461 kB/s eta 0:00:     |████████▉                       | 40 kB 560 kB/s eta 0:00:     |███████████                     | 51 kB 463 kB/s eta 0:00:     |█████████████▎                  | 61 kB 553 kB/s eta 0:00:     |███████████████▌                | 71 kB 564 kB/s eta 0:00:     |█████████████████▊              | 81 kB 642 kB/s eta 0:00:     |████████████████████            | 92 kB 686 kB/s eta 0:00:     |██████████████████████▏         | 102 kB 644 kB/s eta 0:00     |████████████████████████▍       | 112 kB 644 kB/s eta 0:00     |██████████████████████████▋     | 122 kB 644 kB/s eta 0:00     |████████████████████████████▉   | 133 kB 644 kB/s eta 0:00     |███████████████████████████████ | 143 kB 644 kB/s eta 0:00     |████████████████████████████████| 147 kB 17 kB/s          
  Preparing metadata (setup.py) ... done
Requirement already satisfied: urllib3<1.27,>=1.21.1 in /home/jetauto/.local/lib/python3.6/site-packages (from requests>=2.20->openai) (1.26.12)
Requirement already satisfied: certifi>=2017.4.17 in /usr/lib/python3/dist-packages (from requests>=2.20->openai) (2018.1.18)
Requirement already satisfied: charset-normalizer~=2.0.0 in /usr/local/lib/python3.6/dist-packages (from requests>=2.20->openai) (2.0.12)
Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.6/dist-packages (from requests>=2.20->openai) (3.3)
Requirement already satisfied: importlib-resources in /usr/local/lib/python3.6/dist-packages (from tqdm->openai) (5.4.0)
Requirement already satisfied: zipp>=3.1.0 in /usr/local/lib/python3.6/dist-packages (from importlib-resources->tqdm->openai) (3.6.0)
Building wheels for collected packages: openai
  Building wheel for openai (setup.py) ... done
  Created wheel for openai: filename=openai-0.8.0-py3-none-any.whl size=158525 sha256=a382527e6192675a626eec79888e7d97f3bb2cbd3b49a1b755c49b9eef43be16
  Stored in directory: /home/jetauto/.cache/pip/wheels/4e/3f/5c/b2d5d333479d94790b102b14ace60d6313c20d7034cb7e035b
Successfully built openai
Installing collected packages: openai
Successfully installed openai-0.8.0
```
python3 -c "import openai; print(openai.__version__)"
for uninstalling use python3 -m pip uninstall openai

installing different openAI SDK 

jetauto@jetauto-desktop:~/catkin_ws$ python3.8 -m pip install --user --upgrade "pip<24.1"
Collecting pip<24.1
  Cache entry deserialization failed, entry ignored
  Downloading https://files.pythonhosted.org/packages/8a/6a/19e9fe04fca059ccf770861c7d5721ab4c2aebc539889e97c7977528a53b/pip-24.0-py3-none-any.whl (2.1MB)
    0% |▏                               | 10kB 518kB/s eta 0:00:    0% |▎                               | 20kB 493kB/s eta 0:00:    1% |▌                               | 30kB 730kB/s eta 0:00:    1% |▋                               | 40kB 742kB/s eta 0:00:    2% |▊                               | 51kB 652kB/s eta 0:00:    2% |█                               | 61kB 777kB/s eta 0:00:    3% |█                               | 71kB 537kB/s eta 0:00:    3% |█▎                              | 81kB 612kB/s eta 0:00:    4% |█▍                              | 92kB 590kB/s eta 0:00:    4% |█▌                              | 102kB 550kB/s eta 0:00    5% |█▊                              | 112kB 613kB/s eta 0:00    5% |█▉                              | 122kB 602kB/s eta 0:00    6% |██                              | 133kB 539kB/s eta 0:00    6% |██▏                             | 143kB 578kB/s eta 0:00    7% |██▎                             | 153kB 593kB/s eta 0:00    7% |██▌                             | 163kB 593kB/s eta 0:00    8% |██▋                             | 174kB 779kB/s eta 0:00    8% |██▉                             | 184kB 655kB/s eta 0:00    9% |███                             | 194kB 762kB/s eta 0:00    9% |███                             | 204kB 707kB/s eta 0:00    10% |███▎                            | 215kB 705kB/s eta 0:0    10% |███▍                            | 225kB 849kB/s eta 0:0    11% |███▋                            | 235kB 886kB/s eta 0:0    11% |███▊                            | 245kB 886kB/s eta 0:0    12% |███▉                            | 256kB 858kB/s eta 0:0    12% |████                            | 266kB 814kB/s eta 0:0    13% |████▏                           | 276kB 905kB/s eta 0:0    13% |████▍                           | 286kB 962kB/s eta 0:0    14% |████▌                           | 296kB 778kB/s eta 0:0    14% |████▋                           | 307kB 1.1MB/s eta 0:0    15% |████▉                           | 317kB 1.0MB/s eta 0:0    15% |█████                           | 327kB 1.0MB/s eta 0:0    16% |█████▏                          | 337kB 1.0MB/s eta 0:0    16% |█████▎                          | 348kB 981kB/s eta 0:0    16% |█████▍                          | 358kB 1.2MB/s eta 0:0    17% |█████▋                          | 368kB 1.1MB/s eta 0:0    17% |█████▊                          | 378kB 1.0MB/s eta 0:0    18% |██████                          | 389kB 1.2MB/s eta 0:0    18% |██████                          | 399kB 1.6MB/s eta 0:0    19% |██████▏                         | 409kB 1.6MB/s eta 0:0    19% |██████▍                         | 419kB 1.5MB/s eta 0:0    20% |██████▌                         | 430kB 1.3MB/s eta 0:0    20% |██████▊                         | 440kB 1.5MB/s eta 0:0    21% |██████▉                         | 450kB 1.4MB/s eta 0:0    21% |███████                         | 460kB 1.2MB/s eta 0:0    22% |███████▏                        | 471kB 1.5MB/s eta 0:0    22% |███████▎                        | 481kB 1.5MB/s eta 0:0    23% |███████▌                        | 491kB 1.5MB/s eta 0:0    23% |███████▋                        | 501kB 1.5MB/s eta 0:0    24% |███████▊                        | 512kB 1.3MB/s eta 0:0    24% |████████                        | 522kB 1.5MB/s eta 0:0    25% |████████                        | 532kB 1.4MB/s eta 0:0    25% |████████▎                       | 542kB 954kB/s eta 0:0    26% |████████▍                       | 552kB 1.1MB/s eta 0:0    26% |████████▌                       | 563kB 1.2MB/s eta 0:0    27% |████████▊                       | 573kB 1.2MB/s eta 0:0    27% |████████▉                       | 583kB 1.0MB/s eta 0:0    28% |█████████                       | 593kB 843kB/s eta 0:0    28% |█████████▏                      | 604kB 906kB/s eta 0:0    29% |█████████▎                      | 614kB 925kB/s eta 0:0    29% |█████████▌                      | 624kB 797kB/s eta 0:0    30% |█████████▋                      | 634kB 958kB/s eta 0:0    30% |█████████▉                      | 645kB 793kB/s eta 0:0    31% |██████████                      | 655kB 792kB/s eta 0:0    31% |██████████                      | 665kB 774kB/s eta 0:0    32% |██████████▎                     | 675kB 648kB/s eta 0:0    32% |██████████▍                     | 686kB 771kB/s eta 0:0    32% |██████████▋                     | 696kB 849kB/s eta 0:0    33% |██████████▊                     | 706kB 849kB/s eta 0:0    33% |██████████▉                     | 716kB 890kB/s eta 0:0    34% |███████████                     | 727kB 925kB/s eta 0:0    34% |███████████▏                    | 737kB 925kB/s eta 0:0    35% |███████████▍                    | 747kB 1.4MB/s eta 0:0    35% |███████████▌                    | 757kB 1.2MB/s eta 0:0    36% |███████████▋                    | 768kB 1.2MB/s eta 0:0    36% |███████████▉                    | 778kB 1.4MB/s eta 0:0    37% |████████████                    | 788kB 1.3MB/s eta 0:0    37% |████████████▏                   | 798kB 1.4MB/s eta 0:0    38% |████████████▎                   | 808kB 1.2MB/s eta 0:0    38% |████████████▍                   | 819kB 1.2MB/s eta 0:0    39% |████████████▋                   | 829kB 1.1MB/s eta 0:0    39% |████████████▊                   | 839kB 1.0MB/s eta 0:0    40% |████████████▉                   | 849kB 1.3MB/s eta 0:0    40% |█████████████                   | 860kB 1.5MB/s eta 0:0    41% |█████████████▏                  | 870kB 976kB/s eta 0:0    41% |█████████████▍                  | 880kB 1.1MB/s eta 0:0    42% |█████████████▌                  | 890kB 1.1MB/s eta 0:0    42% |█████████████▋                  | 901kB 1.1MB/s eta 0:0    43% |█████████████▉                  | 911kB 1.1MB/s eta 0:0    43% |██████████████                  | 921kB 985kB/s eta 0:0    44% |██████████████▏                 | 931kB 1.2MB/s eta 0:0    44% |██████████████▎                 | 942kB 1.1MB/s eta 0:0    45% |██████████████▍                 | 952kB 853kB/s eta 0:0    45% |██████████████▋                 | 962kB 875kB/s eta 0:0    46% |██████████████▊                 | 972kB 1.3MB/s eta 0:0    46% |███████████████                 | 983kB 1.3MB/s eta 0:0    47% |███████████████                 | 993kB 1.5MB/s eta 0:0    47% |███████████████▏                | 1.0MB 1.2MB/s eta 0:0    48% |███████████████▍                | 1.0MB 1.4MB/s eta 0:0    48% |███████████████▌                | 1.0MB 1.3MB/s eta 0:0    49% |███████████████▊                | 1.0MB 1.2MB/s eta 0:0    49% |███████████████▉                | 1.0MB 1.4MB/s eta 0:0    49% |████████████████                | 1.1MB 1.4MB/s eta 0:0    50% |████████████████▏               | 1.1MB 1.4MB/s eta 0:0    50% |████████████████▎               | 1.1MB 1.4MB/s eta 0:0    51% |████████████████▌               | 1.1MB 1.3MB/s eta 0:0    51% |████████████████▋               | 1.1MB 1.4MB/s eta 0:0    52% |████████████████▊               | 1.1MB 1.6MB/s eta 0:0    52% |█████████████████               | 1.1MB 1.5MB/s eta 0:0    53% |█████████████████               | 1.1MB 2.1MB/s eta 0:0    53% |█████████████████▎              | 1.1MB 1.4MB/s eta 0:0    54% |█████████████████▍              | 1.1MB 1.4MB/s eta 0:0    54% |█████████████████▌              | 1.2MB 1.7MB/s eta 0:0    55% |█████████████████▊              | 1.2MB 1.6MB/s eta 0:0    55% |█████████████████▉              | 1.2MB 1.6MB/s eta 0:0    56% |██████████████████              | 1.2MB 1.6MB/s eta 0:0    56% |██████████████████▏             | 1.2MB 1.5MB/s eta 0:0    57% |██████████████████▎             | 1.2MB 1.6MB/s eta 0:0    57% |██████████████████▌             | 1.2MB 1.4MB/s eta 0:0    58% |██████████████████▋             | 1.2MB 1.4MB/s eta 0:0    58% |██████████████████▉             | 1.2MB 1.6MB/s eta 0:0    59% |███████████████████             | 1.2MB 1.4MB/s eta 0:0    59% |███████████████████             | 1.3MB 1.7MB/s eta 0:0    60% |███████████████████▎            | 1.3MB 1.3MB/s eta 0:0    60% |███████████████████▍            | 1.3MB 1.2MB/s eta 0:0    61% |███████████████████▋            | 1.3MB 1.3MB/s eta 0:0    61% |███████████████████▊            | 1.3MB 1.4MB/s eta 0:0    62% |███████████████████▉            | 1.3MB 1.4MB/s eta 0:0    62% |████████████████████            | 1.3MB 1.2MB/s eta 0:0    63% |████████████████████▏           | 1.3MB 1.2MB/s eta 0:0    63% |████████████████████▍           | 1.3MB 1.5MB/s eta 0:0    64% |████████████████████▌           | 1.4MB 1.4MB/s eta 0:0    64% |████████████████████▋           | 1.4MB 1.0MB/s eta 0:0    65% |████████████████████▉           | 1.4MB 1.2MB/s eta 0:0    65% |█████████████████████           | 1.4MB 1.3MB/s eta 0:0    65% |█████████████████████▏          | 1.4MB 1.3MB/s eta 0:0    66% |█████████████████████▎          | 1.4MB 1.0MB/s eta 0:0    66% |█████████████████████▍          | 1.4MB 909kB/s eta 0:0    67% |█████████████████████▋          | 1.4MB 1.2MB/s eta 0:0    67% |█████████████████████▊          | 1.4MB 977kB/s eta 0:0    68% |██████████████████████          | 1.4MB 758kB/s eta 0:0    68% |██████████████████████          | 1.5MB 843kB/s eta 0:0    69% |██████████████████████▏         | 1.5MB 1.1MB/s eta 0:0    69% |██████████████████████▍         | 1.5MB 1.1MB/s eta 0:0    70% |██████████████████████▌         | 1.5MB 1.0MB/s eta 0:0    70% |██████████████████████▊         | 1.5MB 1.0MB/s eta 0:0    71% |██████████████████████▉         | 1.5MB 1.3MB/s eta 0:0    71% |███████████████████████         | 1.5MB 1.3MB/s eta 0:0    72% |███████████████████████▏        | 1.5MB 1.3MB/s eta 0:0    72% |███████████████████████▎        | 1.5MB 1.6MB/s eta 0:0    73% |███████████████████████▌        | 1.5MB 1.9MB/s eta 0:0    73% |███████████████████████▋        | 1.6MB 1.9MB/s eta 0:0    74% |███████████████████████▊        | 1.6MB 1.8MB/s eta 0:0    74% |████████████████████████        | 1.6MB 1.8MB/s eta 0:0    75% |████████████████████████        | 1.6MB 2.0MB/s eta 0:0    75% |████████████████████████▎       | 1.6MB 1.7MB/s eta 0:0    76% |████████████████████████▍       | 1.6MB 1.6MB/s eta 0:0    76% |████████████████████████▌       | 1.6MB 2.0MB/s eta 0:0    77% |████████████████████████▊       | 1.6MB 1.1MB/s eta 0:0    77% |████████████████████████▉       | 1.6MB 1.1MB/s eta 0:0    78% |█████████████████████████       | 1.6MB 1.4MB/s eta 0:0    78% |█████████████████████████▏      | 1.7MB 1.2MB/s eta 0:0    79% |█████████████████████████▎      | 1.7MB 1.2MB/s eta 0:0    79% |█████████████████████████▌      | 1.7MB 1.1MB/s eta 0:0    80% |█████████████████████████▋      | 1.7MB 943kB/s eta 0:0    80% |█████████████████████████▊      | 1.7MB 1.0MB/s eta 0:0    81% |██████████████████████████      | 1.7MB 1.1MB/s eta 0:0    81% |██████████████████████████      | 1.7MB 1.1MB/s eta 0:0    82% |██████████████████████████▎     | 1.7MB 1.4MB/s eta 0:0    82% |██████████████████████████▍     | 1.7MB 1.3MB/s eta 0:0    82% |██████████████████████████▌     | 1.8MB 1.3MB/s eta 0:0    83% |██████████████████████████▊     | 1.8MB 1.5MB/s eta 0:0    83% |██████████████████████████▉     | 1.8MB 1.0MB/s eta 0:0    84% |███████████████████████████     | 1.8MB 1.2MB/s eta 0:0    84% |███████████████████████████▏    | 1.8MB 1.3MB/s eta 0:0    85% |███████████████████████████▎    | 1.8MB 1.3MB/s eta 0:0    85% |███████████████████████████▌    | 1.8MB 1.2MB/s eta 0:0    86% |███████████████████████████▋    | 1.8MB 845kB/s eta 0:0    86% |███████████████████████████▉    | 1.8MB 1.0MB/s eta 0:0    87% |████████████████████████████    | 1.8MB 1.0MB/s eta 0:0    87% |████████████████████████████    | 1.9MB 1.0MB/s eta 0:0    88% |████████████████████████████▎   | 1.9MB 1.1MB/s eta 0:0    88% |████████████████████████████▍   | 1.9MB 865kB/s eta 0:0    89% |████████████████████████████▋   | 1.9MB 865kB/s eta 0:0    89% |████████████████████████████▊   | 1.9MB 794kB/s eta 0:0    90% |████████████████████████████▉   | 1.9MB 718kB/s eta 0:0    90% |█████████████████████████████   | 1.9MB 767kB/s eta 0:0    91% |█████████████████████████████▏  | 1.9MB 746kB/s eta 0:0    91% |█████████████████████████████▍  | 1.9MB 672kB/s eta 0:0    92% |█████████████████████████████▌  | 1.9MB 722kB/s eta 0:0    92% |█████████████████████████████▋  | 2.0MB 666kB/s eta 0:0    93% |█████████████████████████████▉  | 2.0MB 665kB/s eta 0:0    93% |██████████████████████████████  | 2.0MB 842kB/s eta 0:0    94% |██████████████████████████████▏ | 2.0MB 717kB/s eta 0:0    94% |██████████████████████████████▎ | 2.0MB 802kB/s eta 0:0    95% |██████████████████████████████▍ | 2.0MB 706kB/s eta 0:0    95% |██████████████████████████████▋ | 2.0MB 597kB/s eta 0:0    96% |██████████████████████████████▊ | 2.0MB 774kB/s eta 0:0    96% |███████████████████████████████ | 2.0MB 687kB/s eta 0:0    97% |███████████████████████████████ | 2.0MB 687kB/s eta 0:0    97% |███████████████████████████████▏| 2.1MB 519kB/s eta 0:0    98% |███████████████████████████████▍| 2.1MB 420kB/s eta 0:0    98% |███████████████████████████████▌| 2.1MB 461kB/s eta 0:0    98% |███████████████████████████████▊| 2.1MB 472kB/s eta 0:0    99% |███████████████████████████████▉| 2.1MB 472kB/s eta 0:0    99% |████████████████████████████████| 2.1MB 552kB/s eta 0:0    100% |████████████████████████████████| 2.1MB 172kB/s
Installing collected packages: pip
Successfully installed pip-24.0
jetauto@jetauto-desktop:~/catkin_ws$ python3.8 -m pip --version
pip 24.0 from /home/jetauto/.local/lib/python3.8/site-packages/pip (python 3.8)


```
jetauto@jetauto-desktop:~/catkin_ws$ python3.8 -m pip --version
pip 24.0 from /home/jetauto/.local/lib/python3.8/site-packages/pip (python 3.8)
jetauto@jetauto-desktop:~/catkin_ws$ python3.8 -m pip install --user "openai==1.78.0"
Collecting openai==1.78.0
  Downloading openai-1.78.0-py3-none-any.whl.metadata (25 kB)
Collecting anyio<5,>=3.5.0 (from openai==1.78.0)
  Downloading anyio-4.5.2-py3-none-any.whl.metadata (4.7 kB)
Collecting distro<2,>=1.7.0 (from openai==1.78.0)
  Downloading distro-1.9.0-py3-none-any.whl.metadata (6.8 kB)
Collecting httpx<1,>=0.23.0 (from openai==1.78.0)
  Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting jiter<1,>=0.4.0 (from openai==1.78.0)
  Downloading jiter-0.9.1-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl.metadata (5.2 kB)
Collecting pydantic<3,>=1.9.0 (from openai==1.78.0)
  Downloading pydantic-2.10.6-py3-none-any.whl.metadata (30 kB)
Collecting sniffio (from openai==1.78.0)
  Downloading sniffio-1.3.1-py3-none-any.whl.metadata (3.9 kB)
Collecting tqdm>4 (from openai==1.78.0)
  Downloading tqdm-4.70.0-py3-none-any.whl.metadata (57 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━ 57.3/57.3 kB 1.6 MB/s eta 0:00:00
Collecting typing-extensions<5,>=4.11 (from openai==1.78.0)
  Downloading typing_extensions-4.13.2-py3-none-any.whl.metadata (3.0 kB)
Collecting idna>=2.8 (from anyio<5,>=3.5.0->openai==1.78.0)
  Downloading idna-3.15-py3-none-any.whl.metadata (7.7 kB)
Collecting exceptiongroup>=1.0.2 (from anyio<5,>=3.5.0->openai==1.78.0)
  Downloading exceptiongroup-1.3.1-py3-none-any.whl.metadata (6.7 kB)
Requirement already satisfied: certifi in /usr/lib/python3/dist-packages (from httpx<1,>=0.23.0->openai==1.78.0) (2018.1.18)
Collecting httpcore==1.* (from httpx<1,>=0.23.0->openai==1.78.0)
  Downloading httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Collecting h11>=0.16 (from httpcore==1.*->httpx<1,>=0.23.0->openai==1.78.0)
  Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting annotated-types>=0.6.0 (from pydantic<3,>=1.9.0->openai==1.78.0)
  Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.27.2 (from pydantic<3,>=1.9.0->openai==1.78.0)
  Downloading pydantic_core-2.27.2-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl.metadata (6.6 kB)
Downloading openai-1.78.0-py3-none-any.whl (680 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 680.4/680.4 kB 1.1 MB/s eta 0:00:00
Downloading anyio-4.5.2-py3-none-any.whl (89 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 89.8/89.8 kB 982.5 kB/s eta 0:00:00
Downloading distro-1.9.0-py3-none-any.whl (20 kB)
Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 73.5/73.5 kB 707.9 kB/s eta 0:00:00
Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 78.8/78.8 kB 733.2 kB/s eta 0:00:00
Downloading jiter-0.9.1-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl (1.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB 915.2 kB/s eta 0:00:00
Downloading pydantic-2.10.6-py3-none-any.whl (431 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 431.7/431.7 kB 1.2 MB/s eta 0:00:00
Downloading pydantic_core-2.27.2-cp38-cp38-manylinux_2_17_aarch64.manylinux2014_aarch64.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 866.3 kB/s eta 0:00:00
Downloading sniffio-1.3.1-py3-none-any.whl (10 kB)
Downloading tqdm-4.70.0-py3-none-any.whl (80 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━ 80.2/80.2 kB 1.1 MB/s eta 0:00:00
Downloading typing_extensions-4.13.2-py3-none-any.whl (45 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 45.8/45.8 kB 639.0 kB/s eta 0:00:00
Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
Downloading exceptiongroup-1.3.1-py3-none-any.whl (16 kB)
Downloading idna-3.15-py3-none-any.whl (72 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━ 72.3/72.3 kB 717.0 kB/s eta 0:00:00
Downloading h11-0.16.0-py3-none-any.whl (37 kB)
DEPRECATION: distro-info 0.18ubuntu0.18.04.1 has a non-standard version number. pip 24.1 will enforce this behaviour change. A possible replacement is to upgrade to a newer version of distro-info or contact the author to suggest that they release a version with a conforming version number. Discussion can be found at https://github.com/pypa/pip/issues/12063
Installing collected packages: typing-extensions, tqdm, sniffio, jiter, idna, h11, distro, pydantic-core, httpcore, exceptiongroup, annotated-types, pydantic, anyio, httpx, openai
Successfully installed annotated-types-0.7.0 anyio-4.5.2 distro-1.9.0 exceptiongroup-1.3.1 h11-0.16.0 httpcore-1.0.9 httpx-0.28.1 idna-3.15 jiter-0.9.1 openai-1.78.0 pydantic-2.10.6 pydantic-core-2.27.2 sniffio-1.3.1 tqdm-4.70.0 typing-extensions-4.13.2
```
jetauto@jetauto-desktop:~/catkin_ws$ python3.8 -c "from openai import OpenAI; print('OpenAI SDK OK')"
OpenAI SDK OK

jetauto@jetauto-desktop:~/catkin_ws$ export OPENAI_API_KEY="YOUR_REAL_KEY_HERE"
jetauto@jetauto-desktop:~/catkin_ws$ python3.8 -c "import os; print('API key loaded:', bool(os.getenv('OPENAI_API_KEY')))"
API key loaded: True
jetauto@jetauto-desktop:~/catkin_ws$ python3 -m pip install --user "Flask==2.0.3"
/usr/lib/python3/dist-packages/secretstorage/dhcrypto.py:15: CryptographyDeprecationWarning: Python 3.6 is no longer supported by the Python core team. Therefore, support for it is deprecated in cryptography and will be removed in a future release.
  from cryptography.utils import int_from_bytes
Collecting Flask==2.0.3
  Downloading Flask-2.0.3-py3-none-any.whl (95 kB)
     |███▍                            | 10 kB 443 kB/s eta 0:00:     |██████▉                         | 20 kB 367 kB/s eta 0:00:     |██████████▎                     | 30 kB 545 kB/s eta 0:00:     |█████████████▊                  | 40 kB 599 kB/s eta 0:00:     |█████████████████▏              | 51 kB 600 kB/s eta 0:00:     |████████████████████▋           | 61 kB 716 kB/s eta 0:00:     |████████████████████████        | 71 kB 724 kB/s eta 0:00:     |███████████████████████████▍    | 81 kB 823 kB/s eta 0:00:     |██████████████████████████████▉ | 92 kB 839 kB/s eta 0:00:     |████████████████████████████████| 95 kB 636 kB/s          
Requirement already satisfied: Werkzeug>=2.0 in /usr/local/lib/python3.6/dist-packages (from Flask==2.0.3) (2.0.3)
Collecting itsdangerous>=2.0
  Downloading itsdangerous-2.0.1-py3-none-any.whl (18 kB)
Collecting Jinja2>=3.0
  Downloading Jinja2-3.0.3-py3-none-any.whl (133 kB)
     |██▌                             | 10 kB 1.3 MB/s eta 0:00:     |█████                           | 20 kB 559 kB/s eta 0:00:     |███████▍                        | 30 kB 827 kB/s eta 0:00:     |█████████▉                      | 40 kB 819 kB/s eta 0:00:     |████████████▎                   | 51 kB 970 kB/s eta 0:00:     |██████████████▊                 | 61 kB 1.0 MB/s eta 0:00:     |█████████████████▏              | 71 kB 1.0 MB/s eta 0:00:     |███████████████████▋            | 81 kB 1.2 MB/s eta 0:00:     |██████████████████████          | 92 kB 1.2 MB/s eta 0:00:     |████████████████████████▌       | 102 kB 1.4 MB/s eta 0:00     |███████████████████████████     | 112 kB 1.4 MB/s eta 0:00     |█████████████████████████████▍  | 122 kB 1.4 MB/s eta 0:00     |███████████████████████████████▉| 133 kB 1.4 MB/s eta 0:00     |████████████████████████████████| 133 kB 1.4 MB/s         
Requirement already satisfied: click>=7.1.2 in /home/jetauto/.local/lib/python3.6/site-packages (from Flask==2.0.3) (8.0.4)
Requirement already satisfied: importlib-metadata in /usr/local/lib/python3.6/dist-packages (from click>=7.1.2->Flask==2.0.3) (4.8.3)
Collecting MarkupSafe>=2.0
  Downloading MarkupSafe-2.0.1-cp36-cp36m-manylinux_2_17_aarch64.manylinux2014_aarch64.whl (26 kB)
Requirement already satisfied: dataclasses in /usr/local/lib/python3.6/dist-packages (from Werkzeug>=2.0->Flask==2.0.3) (0.8)
Requirement already satisfied: typing-extensions>=3.6.4 in /usr/local/lib/python3.6/dist-packages (from importlib-metadata->click>=7.1.2->Flask==2.0.3) (4.1.1)
Requirement already satisfied: zipp>=0.5 in /usr/local/lib/python3.6/dist-packages (from importlib-metadata->click>=7.1.2->Flask==2.0.3) (3.6.0)
Installing collected packages: MarkupSafe, Jinja2, itsdangerous, Flask
Successfully installed Flask-2.0.3 Jinja2-3.0.3 MarkupSafe-2.0.1 itsdangerous-2.0.1
jetauto@jetauto-desktop:~/catkin_ws$ python3 -c "import flask; print(flask.__version__)"
2.0.3

---
jetauto@jetauto-desktop:~$ echo "===== MODEL ====="
===== MODEL =====
jetauto@jetauto-desktop:~$ cat /proc/device-tree/model
NVIDIA Jetson Nano Developer Kitjetauto@jetauto-desktop:~$
jetauto@jetauto-desktop:~$ echo "===== MEMORY ====="
===== MEMORY =====
jetauto@jetauto-desktop:~$ free -h
              total        used        free      shared  buff/cache   available
Mem:           3.9G        2.3G        631M         37M        983M        1.4G
Swap:          3.9G         51M        3.9G
jetauto@jetauto-desktop:~$
jetauto@jetauto-desktop:~$ echo "===== GPU ====="
===== GPU =====
jetauto@jetauto-desktop:~$ tegrastats --interval 1000
RAM 2437/3964MB (lfb 107x4MB) SWAP 51/4030MB (cached 2MB) CPU [31%@1479,27%@1479,100%@1479,100%@1479] EMC_FREQ 0% GR3D_FREQ 0% PLL@33.5C CPU@36C iwlwifi@35C PMIC@50C GPU@34.5C AO@45.5C thermal@35.25C
RAM 2437/3964MB (lfb 107x4MB) SWAP 51/4030MB (cached 2MB) CPU [25%@1479,28%@1479,100%@1479,100%@1479] EMC_FREQ 0% GR3D_FREQ 0% PLL@33C CPU@36C iwlwifi@35C PMIC@50C GPU@34.5C AO@45C thermal@35.25C
RAM 2437/3964MB (lfb 107x4MB) SWAP 51/4030MB (cached 2MB) CPU [29%@1479,29%@1479,100%@1479,100%@1479] EMC_FREQ 0% GR3D_FREQ 0% PLL@33.5C CPU@36C iwlwifi@35C PMIC@50C GPU@34.5C AO@45.5C thermal@35.25C
RAM 2437/3964MB (lfb 107x4MB) SWAP 51/4030MB (cached 2MB) CPU [28%@1479,28%@1479,100%@1479,100%@1479] EMC_FREQ 0% GR3D_FREQ 0% PLL@33C CPU@36C iwlwifi@35C PMIC@50C GPU@34.5C AO@46C thermal@35.25C
RAM 2437/3964MB (lfb 107x4MB) SWAP 51/4030MB (cached 2MB) CPU [30%@1479,26%@1479,100%@1479,100%@1479] EMC_FREQ 0% GR3D_FREQ 0% PLL@33.5C CPU@36C iwlwifi@36C PMIC@50C GPU@34.5C AO@45.5C thermal@35.25C
RAM 2437/3964MB (lfb 107x4MB) SWAP 51/4030MB (cached 2MB) CPU [25%@1479,25%@1479,100%@1479,100%@1479] EMC_FREQ 0% GR3D_FREQ 0% PLL@33C CPU@36C iwlwifi@35C PMIC@50C GPU@34.5C AO@45.5C thermal@35.75C
^C
jetauto@jetauto-desktop:~$ echo "===== CUDA ====="
===== CUDA =====
jetauto@jetauto-desktop:~$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2021 NVIDIA Corporation
Built on Sun_Feb_28_22:34:44_PST_2021
Cuda compilation tools, release 10.2, V10.2.300
Build cuda_10.2_r440.TC440_70.29663091_0
jetauto@jetauto-desktop:~$ echo "===== JETPACK ====="
===== JETPACK =====
jetauto@jetauto-desktop:~$ dpkg-query --show nvidia-l4t-core 2>/dev/null
nvidia-l4t-core 32.7.3-20221122092935
jetauto@jetauto-desktop:~$

---
jetauto@jetauto-desktop:~$ gcc --version
gcc (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0
Copyright (C) 2017 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

jetauto@jetauto-desktop:~$ g++ --version
g++ (Ubuntu/Linaro 7.5.0-3ubuntu1~18.04) 7.5.0
Copyright (C) 2017 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

jetauto@jetauto-desktop:~$ cmake --version
cmake version 3.10.2

CMake suite maintained and supported by Kitware (kitware.com/cmake).
jetauto@jetauto-desktop:~$ cd ~/catkin_ws/
jetauto@jetauto-desktop:~/catkin_ws$ mkdir -p ~/local_ai
jetauto@jetauto-desktop:~/catkin_ws$ cd ~/local_ai
jetauto@jetauto-desktop:~/local_ai$ git clone https://github.com/kreier/llama.cpp-jetson.git
Cloning into 'llama.cpp-jetson'...
remote: Enumerating objects: 223, done.
remote: Counting objects: 100% (223/223), done.
remote: Compressing objects: 100% (180/180), done.
remote: Total 223 (delta 98), reused 124 (delta 39), pack-reused 0 (from 0)
Receiving objects: 100% (223/223), 1.58 MiB | 848.00 KiB/s, done.
Resolving deltas: 100% (98/98), done.
jetauto@jetauto-desktop:~/local_ai$ cd ~/local_ai/llama.cpp-jetson
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ ls
docs  LICENSE  patch  README.md
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ git log -1 --oneline
cba793e (HEAD -> main, origin/main, origin/HEAD) Add LFM2.5-1.2B-Thinking section to README
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$

Current                 Required
-------                 --------
CUDA 10.2       ✅      CUDA 10.2
GCC 7.5         ❌      GCC 8.5
CMake 3.10.2    ❌      CMake ≥3.14

so installing GCC and Cmake as required
```
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ apt-cache policy gcc-8 g++-8
gcc-8:
  Installed: (none)
  Candidate: 8.4.0-1ubuntu1~18.04
  Version table:
     8.4.0-1ubuntu1~18.04 500
        500 http://ports.ubuntu.com/ubuntu-ports bionic-updates/universe arm64 Packages
        500 http://ports.ubuntu.com/ubuntu-ports bionic-security/universe arm64 Packages
     8-20180414-1ubuntu2 500
        500 http://ports.ubuntu.com/ubuntu-ports bionic/universe arm64 Packages
g++-8:
  Installed: (none)
  Candidate: 8.4.0-1ubuntu1~18.04
  Version table:
     8.4.0-1ubuntu1~18.04 500
        500 http://ports.ubuntu.com/ubuntu-ports bionic-updates/universe arm64 Packages
        500 http://ports.ubuntu.com/ubuntu-ports bionic-security/universe arm64 Packages
     8-20180414-1ubuntu2 500
        500 http://ports.ubuntu.com/ubuntu-ports bionic/universe arm64 Packages
```
---
```
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ sudo apt update
Get:1 file:/var/cuda-repo-l4t-10-2-local  InRelease
Ign:1 file:/var/cuda-repo-l4t-10-2-local  InRelease
Get:2 file:/var/visionworks-repo  InRelease
Ign:2 file:/var/visionworks-repo  InRelease
Get:3 file:/var/visionworks-sfm-repo  InRelease
Ign:3 file:/var/visionworks-sfm-repo  InRelease
Get:4 file:/var/visionworks-tracking-repo  InRelease
Ign:4 file:/var/visionworks-tracking-repo  InRelease
Get:5 file:/var/cuda-repo-l4t-10-2-local  Release [564 B]
Get:6 file:/var/visionworks-repo  Release [2,001 B]
Get:5 file:/var/cuda-repo-l4t-10-2-local  Release [564 B]
0% [5 Release 0 B/564 B 0%] [Connecting to ports.ubuntu.com] [C
Get:7 file:/var/visionworks-sfm-repo  Release [2,005 B]
Get:6 file:/var/visionworks-repo  Release [2,001 B]
Get:7 file:/var/visionworks-sfm-repo  Release [2,005 B]
Get:8 file:/var/visionworks-tracking-repo  Release [2,010 B]
Get:8 file:/var/visionworks-tracking-repo  Release [2,010 B]
Hit:9 https://repo.download.nvidia.com/jetson/common r32.7 InRelease
Hit:10 http://ppa.launchpad.net/deadsnakes/ppa/ubuntu bionic InRelease
Hit:11 http://ports.ubuntu.com/ubuntu-ports bionic InRelease
Hit:13 http://ports.ubuntu.com/ubuntu-ports bionic-updates InRelease
Get:14 https://repo.download.nvidia.com/jetson/t210 r32.7 InRelease [2,553 B]
Hit:16 http://ports.ubuntu.com/ubuntu-ports bionic-backports InRelease
Get:12 http://packages.ros.org/ros/ubuntu bionic InRelease [4,680 B]
Hit:17 http://ports.ubuntu.com/ubuntu-ports bionic-security InRelease
Err:12 http://packages.ros.org/ros/ubuntu bionic InRelease
  The following signatures were invalid: EXPKEYSIG F42ED6FBAB17C654 Open Robotics <info@osrfoundation.org>
Fetched 7,233 B in 5s (1,536 B/s)
Reading package lists... Done
Building dependency tree
Reading state information... Done
231 packages can be upgraded. Run 'apt list --upgradable' to see them.
W: An error occurred during the signature verification. The repository is not updated and the previous index files will be used. GPG error: http://packages.ros.org/ros/ubuntu bionic InRelease: The following signatures were invalid: EXPKEYSIG F42ED6FBAB17C654 Open Robotics <info@osrfoundation.org>
W: Failed to fetch http://packages.ros.org/ros/ubuntu/dists/bionic/InRelease  The following signatures were invalid: EXPKEYSIG F42ED6FBAB17C654 Open Robotics <info@osrfoundation.org>
W: Some index files failed to download. They have been ignored, or old ones used instead.
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ sudo apt install gcc-8 g++-8 -y
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following additional packages will be installed:
  cpp-8 libasan5 libgcc-8-dev libstdc++-8-dev libubsan1
Suggested packages:
  gcc-8-locales gcc-8-doc libstdc++6-8-dbg libgcc1-dbg
  libgomp1-dbg libitm1-dbg libatomic1-dbg libasan5-dbg
  liblsan0-dbg libtsan0-dbg libubsan1-dbg libmpx2-dbg
  libquadmath0-dbg libstdc++-8-doc
The following NEW packages will be installed:
  cpp-8 g++-8 gcc-8 libasan5 libgcc-8-dev libstdc++-8-dev
  libubsan1
0 upgraded, 7 newly installed, 0 to remove and 231 not upgraded.
Need to get 21.6 MB of archives.
After this operation, 88.6 MB of additional disk space will be used.
Get:1 http://ports.ubuntu.com/ubuntu-ports bionic-updates/universe arm64 cpp-8 arm64 8.4.0-1ubuntu1~18.04 [5,715 kB]
Get:2 http://ports.ubuntu.com/ubuntu-ports bionic-updates/main arm64 libasan5 arm64 8.4.0-1ubuntu1~18.04 [338 kB]
Get:3 http://ports.ubuntu.com/ubuntu-ports bionic-updates/main arm64 libubsan1 arm64 8.4.0-1ubuntu1~18.04 [114 kB]
Get:4 http://ports.ubuntu.com/ubuntu-ports bionic-updates/main arm64 libgcc-8-dev arm64 8.4.0-1ubuntu1~18.04 [854 kB]
Get:5 http://ports.ubuntu.com/ubuntu-ports bionic-updates/universe arm64 gcc-8 arm64 8.4.0-1ubuntu1~18.04 [6,516 kB]
Get:6 http://ports.ubuntu.com/ubuntu-ports bionic-updates/universe arm64 libstdc++-8-dev arm64 8.4.0-1ubuntu1~18.04 [1,512 kB]
Get:7 http://ports.ubuntu.com/ubuntu-ports bionic-updates/universe arm64 g++-8 arm64 8.4.0-1ubuntu1~18.04 [6,562 kB]
Fetched 21.6 MB in 27s (796 kB/s)
Selecting previously unselected package cpp-8.
(Reading database ... 260887 files and directories currently installed.)
Preparing to unpack .../0-cpp-8_8.4.0-1ubuntu1~18.04_arm64.deb ...
Unpacking cpp-8 (8.4.0-1ubuntu1~18.04) ...
Selecting previously unselected package libasan5:arm64.
Preparing to unpack .../1-libasan5_8.4.0-1ubuntu1~18.04_arm64.deb ...
Unpacking libasan5:arm64 (8.4.0-1ubuntu1~18.04) ...
Selecting previously unselected package libubsan1:arm64.
Preparing to unpack .../2-libubsan1_8.4.0-1ubuntu1~18.04_arm64.deb ...
Unpacking libubsan1:arm64 (8.4.0-1ubuntu1~18.04) ...
Selecting previously unselected package libgcc-8-dev:arm64.
Preparing to unpack .../3-libgcc-8-dev_8.4.0-1ubuntu1~18.04_arm64.deb ...
Unpacking libgcc-8-dev:arm64 (8.4.0-1ubuntu1~18.04) ...
Selecting previously unselected package gcc-8.
Preparing to unpack .../4-gcc-8_8.4.0-1ubuntu1~18.04_arm64.deb ...
Unpacking gcc-8 (8.4.0-1ubuntu1~18.04) ...
Selecting previously unselected package libstdc++-8-dev:arm64.
Preparing to unpack .../5-libstdc++-8-dev_8.4.0-1ubuntu1~18.04_arm64.deb ...
Unpacking libstdc++-8-dev:arm64 (8.4.0-1ubuntu1~18.04) ...
Selecting previously unselected package g++-8.
Preparing to unpack .../6-g++-8_8.4.0-1ubuntu1~18.04_arm64.deb ...
Unpacking g++-8 (8.4.0-1ubuntu1~18.04) ...
Setting up cpp-8 (8.4.0-1ubuntu1~18.04) ...
Setting up libasan5:arm64 (8.4.0-1ubuntu1~18.04) ...
Setting up libubsan1:arm64 (8.4.0-1ubuntu1~18.04) ...
Setting up libgcc-8-dev:arm64 (8.4.0-1ubuntu1~18.04) ...
Setting up libstdc++-8-dev:arm64 (8.4.0-1ubuntu1~18.04) ...
Setting up gcc-8 (8.4.0-1ubuntu1~18.04) ...
Setting up g++-8 (8.4.0-1ubuntu1~18.04) ...
Processing triggers for man-db (2.8.3-2ubuntu0.1) ...
Processing triggers for libc-bin (2.27-3ubuntu1.6) ...
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ gcc-8 --version
gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ g++-8 --version
g++-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

```
```
GCC 7.5       → unchanged → ROS
GCC 8.4       → installed → llama.cpp
CUDA 10.2     → ready
CMake 3.10.2  → still needs upgrade
```
---
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ apt-cache policy cmake
cmake:
  Installed: 3.10.2-1ubuntu2.18.04.2
  Candidate: 3.10.2-1ubuntu2.18.04.2
  Version table:
 *** 3.10.2-1ubuntu2.18.04.2 500
        500 http://ports.ubuntu.com/ubuntu-ports bionic-updates/main arm64 Packages
        100 /var/lib/dpkg/status
     3.10.2-1ubuntu2 500
        500 http://ports.ubuntu.com/ubuntu-ports bionic/main arm64 Packages

---
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ ls -l /usr/local/bin/cmake 2>/dev/null
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ which cmake
/usr/bin/cmake
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ cd ~/local_ai
jetauto@jetauto-desktop:~/local_ai$ wget https://cmake.org/files/v3.27/cmake-3.27.1.tar.gz
--2026-08-20 03:14:33--  https://cmake.org/files/v3.27/cmake-3.27.1.tar.gz
Resolving cmake.org (cmake.org)... 66.194.253.25
Connecting to cmake.org (cmake.org)|66.194.253.25|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 10977868 (10M) [application/x-gzip]
Saving to: ‘cmake-3.27.1.tar.gz’

cmake-3.27.1.ta 100%[=======>]  10.47M   930KB/s    in 22s

2026-08-20 03:14:57 (483 KB/s) - ‘cmake-3.27.1.tar.gz’ saved [10977868/10977868]

jetauto@jetauto-desktop:~/local_ai$ tar -xzf cmake-3.27.1.tar.gz

jetauto@jetauto-desktop:~/local_ai$ cd cmake-3.27.1
jetauto@jetauto-desktop:~/local_ai/cmake-3.27.1$ ./bootstrap --prefix=$HOME/local_ai/cmake-3.27.1
---------------------------------------------
CMake 3.27.1, Copyright 2000-2023 Kitware, Inc. and Contributors
Found GNU toolchain
C compiler on this system is: gcc
C++ compiler on this system is: g++
Makefile processor on this system is: make
g++ has setenv
g++ has unsetenv
g++ does not have environ in stdlib.h
g++ has stl wstring
g++ has <ext/stdio_filebuf.h>
---------------------------------------------
cd ~/local_ai
wget https://cmake.org/files/v3.27/cmake-3.27.1.tar.gz

tar -xzf cmake-3.27.1.tar.gz
cd cmake-3.27.1

./bootstrap --prefix=$HOME/local_ai/cmake-3.27.1

make -j2

make install


jetauto@jetauto-desktop:~/local_ai/cmake-3.27.1$ ~/local_ai/cmake-3.27.1/bin/cmake --version
cmake version 3.27.1

CMake suite maintained and supported by Kitware (kitware.com/cmake).

```
/usr/bin/cmake
    ↓
3.10.2
    ↓
ROS/system tools


~/local_ai/cmake-3.27.1/bin/cmake
    ↓
3.27.1
    ↓
llama.cpp build
---
Jetson Nano 4 GB
├── CUDA 10.2             ✅
├── GCC 7.5               → untouched
├── GCC 8.4               ✅ for llama.cpp
├── CMake 3.10.2          → system/ROS
└── CMake 3.27.1          ✅ for llama.cpp
```
LIDAR:   A1
CAMERA:  AstraProPlus
MACHINE: JetAutoPro
HOST:    jetauto_1
MASTER:  jetauto_1

jetauto@jetauto-desktop:~$ sudo du -xhd1 /usr 2>/dev/null | sort -h
8.0K    /usr/games
20K     /usr/locale
72K     /usr/libexec
1.8M    /usr/3rdparty
37M     /usr/sbin
131M    /usr/NX
391M    /usr/include
513M    /usr/bin
792M    /usr/src
1.5G    /usr/share
4.6G    /usr/local
6.4G    /usr/lib
15G     /usr
jetauto@jetauto-desktop:~$ sudo du -xhd1 /usr/local 2>/dev/null | sort -h
4.0K    /usr/local/games
4.0K    /usr/local/src
8.0K    /usr/local/jtop
8.0K    /usr/local/sbin
8.0K    /usr/local/startup
12K     /usr/local/jetson_stats
40K     /usr/local/etc
1.8M    /usr/local/include
4.4M    /usr/local/bin
6.8M    /usr/local/stow
24M     /usr/local/share
1.8G    /usr/local/lib
2.9G    /usr/local/cuda-10.2
4.6G    /usr/local
jetauto@jetauto-desktop:~$ sudo du -xhd1 /usr/lib 2>/dev/null | sort -h | tail -20
5.3M    /usr/lib/p7zip
6.4M    /usr/lib/cups
8.4M    /usr/lib/ruby
12M     /usr/lib/cmake
13M     /usr/lib/qt5
15M     /usr/lib/xorg
25M     /usr/lib/git-core
50M     /usr/lib/sbcl
93M     /usr/lib/debug
98M     /usr/lib/python3.6
107M    /usr/lib/python3
107M    /usr/lib/python3.8
131M    /usr/lib/snapd
156M    /usr/lib/gcc
199M    /usr/lib/libreoffice
207M    /usr/lib/llvm-6.0
280M    /usr/lib/chromium-browser
423M    /usr/lib/python2.7
4.3G    /usr/lib/aarch64-linux-gnu
6.4G    /usr/lib
jetauto@jetauto-desktop:~$ sudo du -xhd1 /usr/local/lib 2>/dev/null | sort -h
8.0K    /usr/local/lib/python3.8
12K     /usr/local/lib/python2.7
144K    /usr/local/lib/pkgconfig
1.8G    /usr/local/lib
1.8G    /usr/local/lib/python3.6
jetauto@jetauto-desktop:~$ sudo du -xhd1 /usr/src 2>/dev/null | sort -h
2.2M    /usr/src/cudnn_samples_v8
6.2M    /usr/src/googletest
69M     /usr/src/nvidia
84M     /usr/src/linux-headers-4.9.299-tegra-ubuntu18.04_aarch64
95M     /usr/src/jetson_multimedia_api
537M    /usr/src/tensorrt
792M    /usr/src
jetauto@jetauto-desktop:~$ sudo du -xhd1 /usr/src 2>/dev/null | sort -h
2.2M    /usr/src/cudnn_samples_v8
6.2M    /usr/src/googletest
69M     /usr/src/nvidia
84M     /usr/src/linux-headers-4.9.299-tegra-ubuntu18.04_aarch64
95M     /usr/src/jetson_multimedia_api
537M    /usr/src/tensorrt
792M    /usr/src
jetauto@jetauto-desktop:~$ du -h --max-depth=1 ~/local_ai/cmake-3.27.1 2>/dev/null | sort -h
44K     /home/jetauto/local_ai/cmake-3.27.1/Licenses
96K     /home/jetauto/local_ai/cmake-3.27.1/doc
116K    /home/jetauto/local_ai/cmake-3.27.1/Packaging
236K    /home/jetauto/local_ai/cmake-3.27.1/Testing
288K    /home/jetauto/local_ai/cmake-3.27.1/Auxiliary
812K    /home/jetauto/local_ai/cmake-3.27.1/Templates
2.6M    /home/jetauto/local_ai/cmake-3.27.1/CMakeFiles
7.9M    /home/jetauto/local_ai/cmake-3.27.1/Modules
11M     /home/jetauto/local_ai/cmake-3.27.1/Help
19M     /home/jetauto/local_ai/cmake-3.27.1/share
56M     /home/jetauto/local_ai/cmake-3.27.1/Utilities
64M     /home/jetauto/local_ai/cmake-3.27.1/bin
99M     /home/jetauto/local_ai/cmake-3.27.1/Bootstrap.cmk
99M     /home/jetauto/local_ai/cmake-3.27.1/Source
121M    /home/jetauto/local_ai/cmake-3.27.1/Tests
480M    /home/jetauto/local_ai/cmake-3.27.1
jetauto@jetauto-desktop:~$ rm ~/local_ai/cmake-3.27.1.tar.gz
jetauto@jetauto-desktop:~$ sudo du -xhd1 /usr/local/lib/python3.6 2>/dev/null | sort -h
1.8G    /usr/local/lib/python3.6
1.8G    /usr/local/lib/python3.6/dist-packages
jetauto@jetauto-desktop:~$ sudo du -xhd1 /usr/local/lib/python3.6/dist-packages 2>/dev/null | sort -h | tail -30
8.0M    /usr/local/lib/python3.6/dist-packages/pygments
8.5M    /usr/local/lib/python3.6/dist-packages/pywt
9.5M    /usr/local/lib/python3.6/dist-packages/Pillow.libs
9.6M    /usr/local/lib/python3.6/dist-packages/Cython
9.8M    /usr/local/lib/python3.6/dist-packages/virtualenv
10M     /usr/local/lib/python3.6/dist-packages/jedi
12M     /usr/local/lib/python3.6/dist-packages/cryptography
12M     /usr/local/lib/python3.6/dist-packages/networkx
12M     /usr/local/lib/python3.6/dist-packages/pip
13M     /usr/local/lib/python3.6/dist-packages/tensorboard
17M     /usr/local/lib/python3.6/dist-packages/caffe2
18M     /usr/local/lib/python3.6/dist-packages/jupyterlab
22M     /usr/local/lib/python3.6/dist-packages/numpy.libs
22M     /usr/local/lib/python3.6/dist-packages/scipy.libs
26M     /usr/local/lib/python3.6/dist-packages/numpy
28M     /usr/local/lib/python3.6/dist-packages/twisted
30M     /usr/local/lib/python3.6/dist-packages/matplotlib-3.3.4-py3.6-linux-aarch64.egg
40M     /usr/local/lib/python3.6/dist-packages/torchvision
41M     /usr/local/lib/python3.6/dist-packages/notebook
49M     /usr/local/lib/python3.6/dist-packages/pandas
55M     /usr/local/lib/python3.6/dist-packages/mediapipe
65M     /usr/local/lib/python3.6/dist-packages/sympy
66M     /usr/local/lib/python3.6/dist-packages/opencv_contrib_python.libs
66M     /usr/local/lib/python3.6/dist-packages/scipy
76M     /usr/local/lib/python3.6/dist-packages/skimage
94M     /usr/local/lib/python3.6/dist-packages/onnxruntime
96M     /usr/local/lib/python3.6/dist-packages/sklearn
173M    /usr/local/lib/python3.6/dist-packages/grpc
569M    /usr/local/lib/python3.6/dist-packages/torch
1.8G    /usr/local/lib/python3.6/dist-packages
jetauto@jetauto-desktop:~$ dpkg -l | grep cuda-repo
ii  cuda-repo-l4t-10-2-local                           10.2.460-1                                 arm64        cuda repository configuration files
jetauto@jetauto-desktop:~$ ls -lah /var/cuda-repo-l4t-10-2-local | head -30
total 1.1G
drwxr-xr-x  2 root root 4.0K Feb 23  2022 .
drwxr-xr-x 20 root root 4.0K Jun  1  2022 ..
-rw-r--r--  1 root root 1.6K Mar  3  2021 7fa2af80.pub
-rw-r--r--  1 root root 2.5K Mar  3  2021 cuda-command-line-tools-10-2_10.2.460-1_arm64.deb
-rw-r--r--  1 root root 2.4K Mar  3  2021 cuda-compiler-10-2_10.2.460-1_arm64.deb
-rw-r--r--  1 root root 123K Mar  3  2021 cuda-cudart-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root 1.5M Mar  3  2021 cuda-cudart-dev-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  89K Mar  3  2021 cuda-cuobjdump-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root 3.0M Mar  3  2021 cuda-cupti-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root 111K Mar  3  2021 cuda-cupti-dev-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  55M Mar  3  2021 cuda-documentation-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  23K Mar  3  2021 cuda-driver-dev-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root 2.1M Mar  3  2021 cuda-gdb-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  34M Mar  3  2021 cuda-gdb-src-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root 2.5K Mar  3  2021 cuda-libraries-10-2_10.2.460-1_arm64.deb
-rw-r--r--  1 root root 2.5K Mar  3  2021 cuda-libraries-dev-10-2_10.2.460-1_arm64.deb
-rw-r--r--  1 root root 119K Mar  3  2021 cuda-memcheck-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root 2.4K Mar  3  2021 cuda-minimal-build-10-2_10.2.460-1_arm64.deb
-rw-r--r--  1 root root  15M Mar  3  2021 cuda-nvcc-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  22M Mar  3  2021 cuda-nvdisasm-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  47M Mar  3  2021 cuda-nvgraph-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  30M Mar  3  2021 cuda-nvgraph-dev-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  65K Mar  3  2021 cuda-nvml-dev-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root 1.1M Mar  3  2021 cuda-nvprof-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  46K Mar  3  2021 cuda-nvprune-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root 5.6M Mar  3  2021 cuda-nvrtc-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  22K Mar  3  2021 cuda-nvrtc-dev-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  51K Mar  3  2021 cuda-nvtx-10-2_10.2.300-1_arm64.deb
-rw-r--r--  1 root root  60M Mar  3  2021 cuda-samples-10-2_10.2.300-1_arm64.deb
jetauto@jetauto-desktop:~$ sudo du -h --max-depth=1 /var/cache 2>/dev/null | sort -h
4.0K    /var/cache/apparmor
4.0K    /var/cache/gdm
4.0K    /var/cache/lightdm
8.0K    /var/cache/PackageKit
40K     /var/cache/dictionaries-common
148K    /var/cache/ldconfig
452K    /var/cache/cracklib
504K    /var/cache/man
884K    /var/cache/fontconfig
1.2M    /var/cache/fwupd
1.3M    /var/cache/samba
1.6M    /var/cache/snapd
5.1M    /var/cache/debconf
9.0M    /var/cache/app-info
76M     /var/cache/apt
96M     /var/cache
jetauto@jetauto-desktop:~$ apt-cache policy cuda-toolkit-10-2
cuda-toolkit-10-2:
  Installed: 10.2.460-1
  Candidate: 10.2.460-1
  Version table:
 *** 10.2.460-1 500
        500 file:/var/cuda-repo-l4t-10-2-local  Packages
        500 https://repo.download.nvidia.com/jetson/common r32.7/main arm64 Packages
        100 /var/lib/dpkg/status
jetauto@jetauto-desktop:~$ dpkg -l | grep -E '^ii.*cuda'
ii  cuda-command-line-tools-10-2                       10.2.460-1                                 arm64        CUDA command-line tools
ii  cuda-compiler-10-2                                 10.2.460-1                                 arm64        CUDA compiler
ii  cuda-cudart-10-2                                   10.2.300-1                                 arm64        CUDA Runtime native Libraries
ii  cuda-cudart-dev-10-2                               10.2.300-1                                 arm64        CUDA Runtime native dev links, headers
ii  cuda-cuobjdump-10-2                                10.2.300-1                                 arm64        CUDA cuobjdump
ii  cuda-cupti-10-2                                    10.2.300-1                                 arm64        CUDA profiling tools runtime libs.
ii  cuda-cupti-dev-10-2                                10.2.300-1                                 arm64        CUDA profiling tools interface.
ii  cuda-documentation-10-2                            10.2.300-1                                 arm64        CUDA documentation
ii  cuda-driver-dev-10-2                               10.2.300-1                                 arm64        CUDA Driver native dev stub library
ii  cuda-gdb-10-2                                      10.2.300-1                                 arm64        CUDA-GDB
ii  cuda-libraries-10-2                                10.2.460-1                                 arm64        CUDA Libraries 10.2 meta-package
ii  cuda-libraries-dev-10-2                            10.2.460-1                                 arm64        CUDA Libraries 10.2 development meta-package
ii  cuda-memcheck-10-2                                 10.2.300-1                                 arm64        CUDA-MEMCHECK
ii  cuda-nvcc-10-2                                     10.2.300-1                                 arm64        CUDA nvcc
ii  cuda-nvdisasm-10-2                                 10.2.300-1                                 arm64        CUDA disassembler
ii  cuda-nvgraph-10-2                                  10.2.300-1                                 arm64        NVGRAPH native runtime libraries
ii  cuda-nvgraph-dev-10-2                              10.2.300-1                                 arm64        NVGRAPH native dev links, headers
ii  cuda-nvml-dev-10-2                                 10.2.300-1                                 arm64        NVML native dev links, headers
ii  cuda-nvprof-10-2                                   10.2.300-1                                 arm64        CUDA Profiler tools
ii  cuda-nvprune-10-2                                  10.2.300-1                                 arm64        CUDA nvprune
ii  cuda-nvrtc-10-2                                    10.2.300-1                                 arm64        NVRTC native runtime libraries
ii  cuda-nvrtc-dev-10-2                                10.2.300-1                                 arm64        NVRTC native dev links, headers
ii  cuda-nvtx-10-2                                     10.2.300-1                                 arm64        NVIDIA Tools Extension
ii  cuda-repo-l4t-10-2-local                           10.2.460-1                                 arm64        cuda repository configuration files
ii  cuda-samples-10-2                                  10.2.300-1                                 arm64        CUDA example applications
ii  cuda-toolkit-10-2                                  10.2.460-1                                 arm64        CUDA Toolkit 10.2 meta-package
ii  cuda-tools-10-2                                    10.2.460-1                                 arm64        CUDA Tools meta-package
ii  cuda-visual-tools-10-2                             10.2.460-1                                 arm64        CUDA visual tools
ii  graphsurgeon-tf                                    8.2.1-1+cuda10.2                           arm64        GraphSurgeon for TensorRT package
ii  libcudnn8                                          8.2.1.32-1+cuda10.2                        arm64        cuDNN runtime libraries
ii  libcudnn8-dev                                      8.2.1.32-1+cuda10.2                        arm64        cuDNN development libraries and headers
ii  libcudnn8-samples                                  8.2.1.32-1+cuda10.2                        arm64        cuDNN documents and samples
ii  libnvinfer-bin                                     8.2.1-1+cuda10.2                           arm64        TensorRT binaries
ii  libnvinfer-dev                                     8.2.1-1+cuda10.2                           arm64        TensorRT development libraries and headers
ii  libnvinfer-doc                                     8.2.1-1+cuda10.2                           all          TensorRT documentation
ii  libnvinfer-plugin-dev                              8.2.1-1+cuda10.2                           arm64        TensorRT plugin libraries
ii  libnvinfer-plugin8                                 8.2.1-1+cuda10.2                           arm64        TensorRT plugin libraries
ii  libnvinfer-samples                                 8.2.1-1+cuda10.2                           all          TensorRT samples
ii  libnvinfer8                                        8.2.1-1+cuda10.2                           arm64        TensorRT runtime libraries
ii  libnvonnxparsers-dev                               8.2.1-1+cuda10.2                           arm64        TensorRT ONNX libraries
ii  libnvonnxparsers8                                  8.2.1-1+cuda10.2                           arm64        TensorRT ONNX libraries
ii  libnvparsers-dev                                   8.2.1-1+cuda10.2                           arm64        TensorRT parsers libraries
ii  libnvparsers8                                      8.2.1-1+cuda10.2                           arm64        TensorRT parsers libraries
ii  nvidia-container-csv-cuda                          10.2.460-1                                 arm64        Jetpack CUDA CSV file
ii  nvidia-container-csv-cudnn                         8.2.1.32-1+cuda10.2                        arm64        Jetpack CUDNN CSV file
ii  nvidia-container-csv-tensorrt                      8.2.1.8-1+cuda10.2                         arm64        Jetpack TensorRT CSV file
ii  nvidia-l4t-cuda                                    32.7.3-20221122092935                      arm64        NVIDIA CUDA Package
ii  python3-libnvinfer                                 8.2.1-1+cuda10.2                           arm64        Python 3 bindings for TensorRT
ii  python3-libnvinfer-dev                             8.2.1-1+cuda10.2                           arm64        Python 3 development package for TensorRT
ii  tensorrt                                           8.2.1.8-1+cuda10.2                         arm64        Meta package of TensorRT
ii  uff-converter-tf                                   8.2.1-1+cuda10.2                           arm64        UFF converter for TensorRT package
jetauto@jetauto-desktop:~$ sudo apt-get clean
jetauto@jetauto-desktop:~$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   27G  1.3G  96% /
jetauto@jetauto-desktop:~$ du -h --max-depth=2 ~/.ros 2>/dev/null | sort -h | tail -30
3.3M    /home/jetauto/.ros/log/f5641a32-9ae4-11f1-a6eb-02428986abe0
3.8M    /home/jetauto/.ros/log/a6c7648c-9c5c-11f1-bb65-024229c3984d
3.8M    /home/jetauto/.ros/log/dcbbf21c-8b2a-11f1-9063-0242c144b8fc
3.9M    /home/jetauto/.ros/log/648eee74-9b93-11f1-a268-0242ba32ccdb
4.0M    /home/jetauto/.ros/rosdep
4.0M    /home/jetauto/.ros/rosdep/sources.cache
4.2M    /home/jetauto/.ros/log/c45a0aec-948a-11f1-9f82-30894aa6c421
4.2M    /home/jetauto/.ros/log/d30de296-8a7d-11f1-be5c-0242abb74d47
4.4M    /home/jetauto/.ros/log/8217e16a-9b8b-11f1-85b5-30894aa6c421
4.4M    /home/jetauto/.ros/log/beb478c8-8f1e-11f1-b9b3-30894aa6c421
5.3M    /home/jetauto/.ros/log/2595a932-890b-11f1-873a-0242de4ec7bd
5.8M    /home/jetauto/.ros/log/1481810a-925e-11f1-9725-024259ef7f99
6.0M    /home/jetauto/.ros/log/4a88f59e-89e4-11f1-8cef-0242fccb2268
7.0M    /home/jetauto/.ros/log/4ae2bad6-970c-11f1-9b91-02428a79ab2a
7.0M    /home/jetauto/.ros/log/d9003668-917b-11f1-8cfc-0242961ff000
7.8M    /home/jetauto/.ros/log/899577ae-8abf-11f1-8a95-024280b1230c
8.1M    /home/jetauto/.ros/log/393b75e4-8cd4-11f1-91d1-0242a6b26852
8.2M    /home/jetauto/.ros/log/c3448092-97d7-11f1-bae8-024264f2a62a
11M     /home/jetauto/.ros/log/ab68de4a-89ff-11f1-931f-024286fe2b3d
12M     /home/jetauto/.ros/log/456affbc-8a52-11f1-839f-02423e91d645
13M     /home/jetauto/.ros/log/38c05508-9107-11f1-9861-0242920dd263
14M     /home/jetauto/.ros/log/ea964b48-8a86-11f1-8b34-02424f66aaaa
17M     /home/jetauto/.ros/log/8aa5a4f4-89e6-11f1-9547-024255d41a2c
22M     /home/jetauto/.ros/log/7259ecee-96f6-11f1-8753-024279a0e9f9
29M     /home/jetauto/.ros/log/a4190842-9551-11f1-95a3-024290f0e0ed
31M     /home/jetauto/.ros/log/969c3110-90b7-11f1-a843-30894aa6c421
165M    /home/jetauto/.ros/log/f0a80706-8914-11f1-b8c1-0242c45929d4
200M    /home/jetauto/.ros/log/44b759c4-892d-11f1-be1f-02420ffa214a
686M    /home/jetauto/.ros/log
857M    /home/jetauto/.ros
jetauto@jetauto-desktop:~$ du -h --max-depth=2 ~/jetauto_third_party 2>/dev/null | sort -h | tail -30
8.2M    /home/jetauto/jetauto_third_party/YDLidar-SDK/build
8.9M    /home/jetauto/jetauto_third_party/my_data/Annotations
11M     /home/jetauto/jetauto_third_party/AstraSDK/samples
12M     /home/jetauto/jetauto_third_party/Pangolin/build
12M     /home/jetauto/jetauto_third_party/xf_tts/bin
12M     /home/jetauto/jetauto_third_party/xf_tts/libs
13M     /home/jetauto/jetauto_third_party/octomap/octomap
14M     /home/jetauto/jetauto_third_party/octomap/octovis
14M     /home/jetauto/jetauto_third_party/yolov5/runs
15M     /home/jetauto/jetauto_third_party/garbage_data
15M     /home/jetauto/jetauto_third_party/garbage_data/JPEGImages
15M     /home/jetauto/jetauto_third_party/Pangolin
17M     /home/jetauto/jetauto_third_party/YDLidar-SDK
18M     /home/jetauto/jetauto_third_party/ORB_SLAM3/build
24M     /home/jetauto/jetauto_third_party/ORB_SLAM3/Thirdparty
24M     /home/jetauto/jetauto_third_party/xf_tts
31M     /home/jetauto/jetauto_third_party/octomap
34M     /home/jetauto/jetauto_third_party/yolov5
51M     /home/jetauto/jetauto_third_party/ORB_SLAM3/evaluation
59M     /home/jetauto/jetauto_third_party/AstraSDK/lib
70M     /home/jetauto/jetauto_third_party/AstraSDK
148M    /home/jetauto/jetauto_third_party/ORB_SLAM2/Vocabulary
157M    /home/jetauto/jetauto_third_party/my_data/JPEGImages
165M    /home/jetauto/jetauto_third_party/ORB_SLAM2
167M    /home/jetauto/jetauto_third_party/my_data
180M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Vocabulary
674M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples
680M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples_old
1.6G    /home/jetauto/jetauto_third_party/ORB_SLAM3
2.2G    /home/jetauto/jetauto_third_party
jetauto@jetauto-desktop:~$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   27G  1.3G  96% /
jetauto@jetauto-desktop:~$ rm -rf ~/.ros/log/*
jetauto@jetauto-desktop:~$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   27G  1.9G  94% /
jetauto@jetauto-desktop:~$ du -h --max-depth=1 ~/jetauto_third_party/ORB_SLAM3/Examples_old | sort -h
28K     /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples_old/RGB-D-Inertial
1.7M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples_old/RGB-D
5.7M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples_old/ROS
6.6M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples_old/Monocular
6.6M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples_old/Stereo
330M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples_old/Monocular-Inertial
330M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples_old/Stereo-Inertial
680M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples_old
jetauto@jetauto-desktop:~$ du -h --max-depth=1 ~/jetauto_third_party/ORB_SLAM3/Examples | sort -h
28K     /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples/RGB-D-Inertial
48K     /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples/Calibration
1.7M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples/RGB-D
6.5M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples/Stereo
6.6M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples/Monocular
330M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples/Monocular-Inertial
330M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples/Stereo-Inertial
674M    /home/jetauto/jetauto_third_party/ORB_SLAM3/Examples
jetauto@jetauto-desktop:~$ find ~/jetauto_third_party/ORB_SLAM3/Examples_old -type f | wc -l
630
jetauto@jetauto-desktop:~$ find ~/jetauto_third_party/ORB_SLAM3/Examples -type f | wc -l
323
jetauto@jetauto-desktop:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   27G  1.9G  94% /
none            1.8G     0  1.8G   0% /dev
tmpfs           2.0G   88K  2.0G   1% /dev/shm
tmpfs           2.0G   40M  1.9G   3% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
tmpfs           397M  120K  397M   1% /run/user/1000
jetauto@jetauto-desktop:~$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   27G  1.9G  94% /
jetauto@jetauto-desktop:~$ rm -rf ~/jetauto_third_party/ORB_SLAM3/Examples_old
jetauto@jetauto-desktop:~$ df -h /
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   26G  2.6G  91% /
jetauto@jetauto-desktop:~$ lsusb
Bus 002 Device 002: ID 0bda:0411 Realtek Semiconductor Corp.
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 003: ID 8087:0a2b Intel Corp.
Bus 001 Device 039: ID 32e6:9005
Bus 001 Device 009: ID 1a86:7523 QinHeng Electronics HL-340 USB-Serial adapter
Bus 001 Device 014: ID 32c2:0018
Bus 001 Device 006: ID 214b:7250
Bus 001 Device 011: ID 2bc5:050f
Bus 001 Device 008: ID 2bc5:060f
Bus 001 Device 005: ID 05e3:0608 Genesys Logic, Inc. Hub
Bus 001 Device 012: ID 2563:0526
Bus 001 Device 004: ID 1a86:8091 QinHeng Electronics
Bus 001 Device 040: ID 14cd:1212 Super Top microSD card reader (SY-T18)
Bus 001 Device 002: ID 0bda:5411 Realtek Semiconductor Corp.
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
jetauto@jetauto-desktop:~$ lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINT,MODEL
NAME           SIZE FSTYPE LABEL      MOUNTPOINT MODEL
loop0           16M vfat   L4T-README
sda           59.5G                              Storage Device
└─sda1        59.5G exfat  LLM
mtdblock0        4M
mmcblk0       29.7G
├─mmcblk0p1   29.7G ext4              /
├─mmcblk0p2    128K
├─mmcblk0p3    448K
├─mmcblk0p4    576K
├─mmcblk0p5     64K
├─mmcblk0p6    192K
├─mmcblk0p7    384K
├─mmcblk0p8     64K
├─mmcblk0p9    448K
├─mmcblk0p10   448K
├─mmcblk0p11   768K
├─mmcblk0p12    64K
├─mmcblk0p13   192K
└─mmcblk0p14   128K
zram0        495.5M                   [SWAP]
zram1        495.5M                   [SWAP]
zram2        495.5M                   [SWAP]
zram3        495.5M                   [SWAP]
jetauto@jetauto-desktop:~$ sudo mkdir -p /mnt/llm
jetauto@jetauto-desktop:~$ sudo mount /dev/sda1 /mnt/llm
mount: /mnt/llm: unknown filesystem type 'exfat'.
jetauto@jetauto-desktop:~$ df -h /mnt/llm
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   26G  2.6G  91% /
jetauto@jetauto-desktop:~$ apt-cache policy exfat-fuse exfat-utils
exfat-fuse:
  Installed: (none)
  Candidate: 1.2.8-1
  Version table:
     1.2.8-1 500
        500 http://ports.ubuntu.com/ubuntu-ports bionic/universe arm64 Packages
exfat-utils:
  Installed: (none)
  Candidate: 1.2.8-1
  Version table:
     1.2.8-1 500
        500 http://ports.ubuntu.com/ubuntu-ports bionic/universe arm64 Packages
jetauto@jetauto-desktop:~$ which mount.exfat
jetauto@jetauto-desktop:~$ sudo apt install exfat-fuse exfat-utils -y
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following NEW packages will be installed:
  exfat-fuse exfat-utils
0 upgraded, 2 newly installed, 0 to remove and 231 not upgraded.
Need to get 55.7 kB of archives.
After this operation, 249 kB of additional disk space will be used.
Get:1 http://ports.ubuntu.com/ubuntu-ports bionic/universe arm64 exfat-fuse arm64 1.2.8-1 [21.4 kB]
Get:2 http://ports.ubuntu.com/ubuntu-ports bionic/universe arm64 exfat-utils arm64 1.2.8-1 [34.3 kB]
Fetched 55.7 kB in 2s (24.8 kB/s)
Selecting previously unselected package exfat-fuse.
(Reading database ... 261829 files and directories currently installed.)
Preparing to unpack .../exfat-fuse_1.2.8-1_arm64.deb ...
Unpacking exfat-fuse (1.2.8-1) ...
Selecting previously unselected package exfat-utils.
Preparing to unpack .../exfat-utils_1.2.8-1_arm64.deb ...
Unpacking exfat-utils (1.2.8-1) ...
Setting up exfat-utils (1.2.8-1) ...
Setting up exfat-fuse (1.2.8-1) ...
Processing triggers for man-db (2.8.3-2ubuntu0.1) ...
jetauto@jetauto-desktop:~$ sudo mount -t exfat /dev/sda1 /mnt/llm
FUSE exfat 1.2.8
jetauto@jetauto-desktop:~$ df -h /mnt/llm
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        60G   17M   60G   1% /mnt/llm
jetauto@jetauto-desktop:~$ apt-cache policy exfat-fuse exfat-utils
exfat-fuse:
  Installed: 1.2.8-1
  Candidate: 1.2.8-1
  Version table:
 *** 1.2.8-1 500
        500 http://ports.ubuntu.com/ubuntu-ports bionic/universe arm64 Packages
        100 /var/lib/dpkg/status
exfat-utils:
  Installed: 1.2.8-1
  Candidate: 1.2.8-1
  Version table:
 *** 1.2.8-1 500
        500 http://ports.ubuntu.com/ubuntu-ports bionic/universe arm64 Packages
        100 /var/lib/dpkg/status
jetauto@jetauto-desktop:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   26G  2.5G  92% /
none            1.8G     0  1.8G   0% /dev
tmpfs           2.0G   88K  2.0G   1% /dev/shm
tmpfs           2.0G   40M  1.9G   3% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
tmpfs           397M  120K  397M   1% /run/user/1000
/dev/sda1        60G   17M   60G   1% /mnt/llm

jetauto@jetauto-desktop:~$ echo "JetAuto AI storage test" > /mnt/llm/test.txt
jetauto@jetauto-desktop:~$ cat /mnt/llm/test.txt
JetAuto AI storage test
jetauto@jetauto-desktop:~$ rm /mnt/llm/test.txt
jetauto@jetauto-desktop:~$ cd /mnt/llm/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp$ git clone https://github.com/ggml-org/llama.cpp llama5050gpu.cpp
Cloning into 'llama5050gpu.cpp'...
error: chmod on /mnt/llm/llama.cpp/llama5050gpu.cpp/.git/config.lock failed: Operation not permitted
fatal: could not set 'core.filemode' to 'false'
jetauto@jetauto-desktop:/mnt/llm/llama.cpp$ sudo umount /mnt/llm
umount: /mnt/llm: target is busy.
jetauto@jetauto-desktop:/mnt/llm/llama.cpp$ cd ..
jetauto@jetauto-desktop:/mnt/llm$ cd ..
jetauto@jetauto-desktop:/mnt$ cd ..
jetauto@jetauto-desktop:/$ sudo umount /mnt/llm
jetauto@jetauto-desktop:/$ lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINT,MODEL
NAME           SIZE FSTYPE LABEL      MOUNTPOINT MODEL
loop0           16M vfat   L4T-README
sda           59.5G                              Storage Device
└─sda1        59.5G exfat  LLM
mtdblock0        4M
mmcblk0       29.7G
├─mmcblk0p1   29.7G ext4              /
├─mmcblk0p2    128K
├─mmcblk0p3    448K
├─mmcblk0p4    576K
├─mmcblk0p5     64K
├─mmcblk0p6    192K
├─mmcblk0p7    384K
├─mmcblk0p8     64K
├─mmcblk0p9    448K
├─mmcblk0p10   448K
├─mmcblk0p11   768K
├─mmcblk0p12    64K
├─mmcblk0p13   192K
└─mmcblk0p14   128K
zram0        495.5M                   [SWAP]
zram1        495.5M                   [SWAP]
zram2        495.5M                   [SWAP]
zram3        495.5M                   [SWAP]
jetauto@jetauto-desktop:/$ sudo mkfs.ext4 -L LLM /dev/sda1
mke2fs 1.44.1 (24-Mar-2018)
/dev/sda1 contains a exfat file system labelled 'LLM'
Proceed anyway? (y,N) y
Creating filesystem with 15587840 4k blocks and 3899392 inodes
Filesystem UUID: db6ca292-a845-4a35-bc07-e1c98503a671
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
        4096000, 7962624, 11239424

Allocating group tables: done
Writing inode tables: done
Creating journal (65536 blocks): done
Writing superblocks and filesystem accounting information:   0/4done

jetauto@jetauto-desktop:/$ sudo mkdir -p /mnt/llm
jetauto@jetauto-desktop:/$ sudo mount /dev/sda1 /mnt/llm
jetauto@jetauto-desktop:/$ df -h /mnt/llm
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        59G   53M   56G   1% /mnt/llm
jetauto@jetauto-desktop:/$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   26G  2.5G  92% /
none            1.8G     0  1.8G   0% /dev
tmpfs           2.0G   88K  2.0G   1% /dev/shm
tmpfs           2.0G   40M  1.9G   3% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
tmpfs           397M  120K  397M   1% /run/user/1000
/dev/sda1        59G   53M   56G   1% /mnt/llm
jetauto@jetauto-desktop:/$ lsblk -o NAME,SIZE,FSTYPE,LABEL,MOUNTPOINT,MODEL
NAME           SIZE FSTYPE LABEL      MOUNTPOINT MODEL
loop0           16M vfat   L4T-README
sda           59.5G                              Storage Device
└─sda1        59.5G ext4   LLM        /mnt/llm
mtdblock0        4M
mmcblk0       29.7G
├─mmcblk0p1   29.7G ext4              /
├─mmcblk0p2    128K
├─mmcblk0p3    448K
├─mmcblk0p4    576K
├─mmcblk0p5     64K
├─mmcblk0p6    192K
├─mmcblk0p7    384K
├─mmcblk0p8     64K
├─mmcblk0p9    448K
├─mmcblk0p10   448K
├─mmcblk0p11   768K
├─mmcblk0p12    64K
├─mmcblk0p13   192K
└─mmcblk0p14   128K
zram0        495.5M                   [SWAP]
zram1        495.5M                   [SWAP]
zram2        495.5M                   [SWAP]
zram3        495.5M                   [SWAP]
jetauto@jetauto-desktop:/$ touch /mnt/llm/test
touch: cannot touch '/mnt/llm/test': Permission denied
jetauto@jetauto-desktop:/$ chmod 755 /mnt/llm/test
chmod: cannot access '/mnt/llm/test': No such file or directory
jetauto@jetauto-desktop:/$ ls -l /mnt/llm/test
ls: cannot access '/mnt/llm/test': No such file or directory
jetauto@jetauto-desktop:/$ rm /mnt/llm/test
rm: cannot remove '/mnt/llm/test': No such file or directory
jetauto@jetauto-desktop:/$ sudo chown -R jetauto:jetauto /mnt/llm
jetauto@jetauto-desktop:/$ ls -ld /mnt/llm
drwxr-xr-x 3 jetauto jetauto 4096 Aug 21 23:40 /mnt/llm
jetauto@jetauto-desktop:/$ touch /mnt/llm/test
jetauto@jetauto-desktop:/$ chmod 755 /mnt/llm/test
jetauto@jetauto-desktop:/$ ls -l /mnt/llm/test
-rwxr-xr-x 1 jetauto jetauto 0 Aug 21 23:43 /mnt/llm/test
jetauto@jetauto-desktop:/$ rm /mnt/llm/test

jetauto@jetauto-desktop:/$
jetauto@jetauto-desktop:/$ mkdir -p /mnt/llm/{llama.cpp,models,builds,cache,projects}
jetauto@jetauto-desktop:/$ ls -lah /mnt/llm
total 44K
drwxr-xr-x 8 jetauto jetauto 4.0K Aug 21 23:45 .
drwxr-xr-x 3 root    root    4.0K Aug 21 23:26 ..
drwxrwxr-x 2 jetauto jetauto 4.0K Aug 21 23:45 builds
drwxrwxr-x 2 jetauto jetauto 4.0K Aug 21 23:45 cache
drwxrwxr-x 2 jetauto jetauto 4.0K Aug 21 23:45 llama.cpp
drwx------ 2 jetauto jetauto  16K Aug 21 23:40 lost+found
drwxrwxr-x 2 jetauto jetauto 4.0K Aug 21 23:45 models
drwxrwxr-x 2 jetauto jetauto 4.0K Aug 21 23:45 projects
jetauto@jetauto-desktop:/$ client_loop: send disconnect: Connection reset

C:\Users\rajm4>ssh jetauto@10.23.84.204
jetauto@10.23.84.204's password:
Welcome to Ubuntu 18.04.6 LTS (GNU/Linux 4.9.299-tegra aarch64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

227 updates can be applied immediately.
171 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable

Last login: Fri Aug 21 22:45:45 2026 from 10.23.84.183
LIDAR:   A1
CAMERA:  AstraProPlus
MACHINE: JetAutoPro
HOST:    jetauto_1
MASTER:  jetauto_1
ROS_HOSTNAME: 10.23.84.204
ROS_MASTER_URI: http://10.23.84.204:11311
jetauto@jetauto-desktop:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   26G  2.6G  91% /
none            1.7G     0  1.7G   0% /dev
tmpfs           2.0G   88K  2.0G   1% /dev/shm
tmpfs           2.0G   23M  2.0G   2% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
tmpfs           396M  136K  396M   1% /run/user/1000
/dev/sda1        59G   53M   56G   1% /media/jetauto/LLM
jetauto@jetauto-desktop:~$ mount | grep -E 'sda1|/mnt/llm|/media/jetauto/LLM'
/dev/sda1 on /media/jetauto/LLM type ext4 (rw,nosuid,nodev,relatime,data=ordered,uhelper=udisks2)
jetauto@jetauto-desktop:~$ sudo umount /media/jetauto/LLM
jetauto@jetauto-desktop:~$ sudo mount /dev/sda1 /mnt/llm
jetauto@jetauto-desktop:~$ ls -ld /mnt/llm
drwxr-xr-x 8 jetauto jetauto 4096 Aug 21 23:45 /mnt/llm
jetauto@jetauto-desktop:~$ Connection to 10.23.84.204 closed by remote host.
Connection to 10.23.84.204 closed.

C:\Users\rajm4>ssh jetauto@10.23.84.204
jetauto@10.23.84.204's password:
Welcome to Ubuntu 18.04.6 LTS (GNU/Linux 4.9.299-tegra aarch64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

227 updates can be applied immediately.
171 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable

Last login: Fri Aug 21 23:48:06 2026 from 10.23.84.183
LIDAR:   A1
CAMERA:  AstraProPlus
MACHINE: JetAutoPro
HOST:    jetauto_1
MASTER:  jetauto_1
ROS_HOSTNAME: 10.23.84.204
ROS_MASTER_URI: http://10.23.84.204:11311
jetauto@jetauto-desktop:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   26G  2.6G  91% /
none            1.7G     0  1.7G   0% /dev
tmpfs           2.0G   88K  2.0G   1% /dev/shm
tmpfs           2.0G   31M  2.0G   2% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
tmpfs           396M  112K  396M   1% /run/user/1000
/dev/sda1        59G   53M   56G   1% /media/jetauto/LLM
jetauto@jetauto-desktop:~$ sudo blkid /dev/sda1
/dev/sda1: LABEL="LLM" UUID="db6ca292-a845-4a35-bc07-e1c98503a671" TYPE="ext4"
jetauto@jetauto-desktop:~$ sudo blkid /dev/sda1
/dev/sda1: LABEL="LLM" UUID="db6ca292-a845-4a35-bc07-e1c98503a671" TYPE="ext4"
jetauto@jetauto-desktop:~$ sudo nano /etc/fstab
jetauto@jetauto-desktop:~$ sudo nano /etc/fstab
Use "fg" to return to nano.

[1]+  Stopped                 sudo nano /etc/fstab

jetauto@jetauto-desktop:~$ sudo nano /etc/fstab
jetauto@jetauto-desktop:~$ sudo nano /etc/fstab
jetauto@jetauto-desktop:~$ sudo umount /media/jetauto/LLM
jetauto@jetauto-desktop:~$ sudo mkdir -p /mnt/llm
jetauto@jetauto-desktop:~$ sudo mount -a
jetauto@jetauto-desktop:~$ df -h /mnt/llm
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        59G   53M   56G   1% /mnt/llm
jetauto@jetauto-desktop:~$ ls -ld /mnt/llm
drwxr-xr-x 8 jetauto jetauto 4096 Aug 21 23:45 /mnt/llm
jetauto@jetauto-desktop:~$ Connection to 10.23.84.204 closed by remote host.
Connection to 10.23.84.204 closed.

C:\Users\rajm4>ssh jetauto@10.23.84.204
jetauto@10.23.84.204's password:
Welcome to Ubuntu 18.04.6 LTS (GNU/Linux 4.9.299-tegra aarch64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

227 updates can be applied immediately.
171 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable

Last login: Fri Aug 21 23:52:24 2026 from 10.23.84.183
LIDAR:   A1
CAMERA:  AstraProPlus
MACHINE: JetAutoPro
HOST:    jetauto_1
MASTER:  jetauto_1
ROS_HOSTNAME: 10.23.84.204
ROS_MASTER_URI: http://10.23.84.204:11311
jetauto@jetauto-desktop:~$ df -h /mnt/llm
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        59G   53M   56G   1% /mnt/llm
jetauto@jetauto-desktop:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/mmcblk0p1   30G   26G  2.6G  91% /
none            1.7G     0  1.7G   0% /dev
tmpfs           2.0G   88K  2.0G   1% /dev/shm
tmpfs           2.0G   24M  2.0G   2% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/sda1        59G   53M   56G   1% /mnt/llm
tmpfs           396M  116K  396M   1% /run/user/1000
jetauto@jetauto-desktop:~$ cd /mnt/llm/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp$ git clone https://github.com/ggml-org/llama.cpp llama5050gpu.cpp
Cloning into 'llama5050gpu.cpp'...
remote: Enumerating objects: 115502, done.
remote: Counting objects: 100% (1545/1545), done.
remote: Compressing objects: 100% (703/703), done.
Receiving objects:  12% (13861/115502), 10.36 MiB | 4.13 MiB/s  Receiving objects:  12% (14996/115502), 10.36 MiB | 4.13 MiB/s  Receiving objects:  13% (15016/115502), 12.38 MiB | 4.12 MiB/s  Receiving objects:  14% (16171/115502), 14.03 MiB | 4.00 MiB/s  Receiving objects:  14% (16219/115502), 14.03 MiB | 4.00 MiB/s  Receiving objects:  14% (17165/115502), 19.43 MiB | 3.91 MiB/s  Receiving objects:  14% (17170/115502), 22.71 MiB | 3.66 MiB/s  Receiving objects:  14% (17177/115502), 24.32 MiB | 3.50 MiB/s  Receiving objects:  14% (17178/115502), 29.50 MiB | 3.39 MiB/s  Receiving objects:  14% (17184/115502), 33.29 MiB | 3.31 MiB/s  Receiving objects:  14% (17192/115502), 37.25 MiB | 3.58 MiB/s  Receiving objects:  15% (17326/115502), 39.26 MiB | 3.61 MiB/s  Receiving objects:  15% (17438/115502), 39.26 MiB | 3.61 MiB/s  Receiving objects:  16% (18481/115502), 43.25 MiB | 3.78 MiB/s  Receiving objects:  16% (19357/115502), 43.25 MiB | 3.78 MiB/s  Receiving objects:  17% (19636/115502), 45.24 MiB | 3.81 MiB/s  Receiving objects:  17% (19990/115502), 47.30 MiB | 3.89 MiB/s  Receiving objects:  18% (20791/115502), 49.32 MiB | 3.85 MiB/s  Receiving objects:  18% (21284/115502), 51.10 MiB | 3.88 MiB/s  Receiving objects:  19% (21946/115502), 52.89 MiB | 3.84 MiB/s  Receiving objects:  19% (22234/115502), 55.00 MiB | 3.87 MiB/s  Receiving objects:  20% (23101/115502), 59.13 MiB | 3.89 MiB/s  Receiving objects:  20% (23455/115502), 59.13 MiB | 3.89 MiB/s  Receiving objects:  20% (23999/115502), 62.89 MiB | 3.86 MiB/s  Receiving objects:  21% (24256/115502), 64.69 MiB | 3.78 MiB/s  Receiving objects:  21% (24600/115502), 66.16 MiB | 3.70 MiB/s  Receiving objects:  22% (25411/115502), 69.41 MiB | 3.64 MiB/s  Receiving objects:  22% (25648/115502), 69.41 MiB | 3.64 MiB/s  Receiving objects:  23% (26566/115502), 70.63 MiB | 3.44 MiB/s  Receiving objects:  23% (26948/115502), 72.07 MiB | 3.30 MiB/s  Receiving objects:  23% (27708/115502), 75.14 MiB | 3.03 MiB/s  Receiving objects:  24% (27721/115502), 75.14 MiB | 3.03 MiB/s  Receiving objects:  24% (28499/115502), 78.23 MiB | 2.97 MiB/s  Receiving objects:  25% (28876/115502), 79.76 MiB | 2.96 MiB/s  Receiving objects:  25% (29003/115502), 81.33 MiB | 2.88 MiB/s  Receiving objects:  25% (29749/115502), 84.40 MiB | 3.00 MiB/s  Receiving objects:  26% (30031/115502), 85.92 MiB | 3.01 MiB/s  Receiving objects:  26% (30289/115502), 87.73 MiB | 3.04 MiB/s  Receiving objects:  27% (31186/115502), 89.72 MiB | 3.18 MiB/s  Receiving objects:  27% (31528/115502), 91.66 MiB | 3.25 MiB/s  Receiving objects:  28% (32341/115502), 93.56 MiB | 3.34 MiB/s  Receiving objects:  28% (32418/115502), 95.19 MiB | 3.39 MiB/s  Receiving objects:  29% (33496/115502), 97.04 MiB | 3.45 MiB/s  Receiving objects:  29% (34175/115502), 99.07 MiB | 3.60 MiB/s  Receiving objects:  29% (34642/115502), 103.20 MiB | 3.80 MiB/s Receiving objects:  30% (34651/115502), 103.20 MiB | 3.80 MiB/s Receiving objects:  30% (34994/115502), 107.04 MiB | 3.82 MiB/s Receiving objects:  30% (35582/115502), 110.60 MiB | 3.77 MiB/s Receiving objects:  31% (35806/115502), 110.60 MiB | 3.77 MiB/s Receiving objects:  31% (36410/115502), 114.04 MiB | 3.73 MiB/s Receiving objects:  31% (36711/115502), 117.15 MiB | 3.56 MiB/s Receiving objects:  31% (36911/115502), 119.48 MiB | 3.15 MiB/s Receiving objects:  32% (36961/115502), 119.48 MiB | 3.15 MiB/s Receiving objects:  32% (38060/115502), 120.82 MiB | 3.00 MiB/s Receiving objects:  33% (38116/115502), 122.02 MiB | 2.69 MiB/s Receiving objects:  33% (38634/115502), 124.41 MiB | 2.77 MiB/s Receiving objects:  33% (39239/115502), 127.31 MiB | 2.66 MiB/s Receiving objects:  34% (39271/115502), 127.31 MiB | 2.66 MiB/s Receiving objects:  34% (39325/115502), 129.97 MiB | 2.33 MiB/s Receiving objects:  34% (39600/115502), 132.64 MiB | 2.63 MiB/s Receiving objects:  34% (40416/115502), 135.64 MiB | 2.71 MiB/s Receiving objects:  35% (40426/115502), 135.64 MiB | 2.71 MiB/s Receiving objects:  35% (40766/115502), 138.51 MiB | 2.76 MiB/s Receiving objects:  35% (41120/115502), 139.82 MiB | 2.71 MiB/s Receiving objects:  36% (41581/115502), 141.22 MiB | 2.74 MiB/s Receiving objects:  36% (41931/115502), 143.72 MiB | 3.02 MiB/s Receiving objects:  36% (42372/115502), 145.03 MiB | 2.72 MiB/s Receiving objects:  37% (42736/115502), 148.21 MiB | 2.76 MiB/s Receiving objects:  37% (42740/115502), 149.77 MiB | 2.76 MiB/s Receiving objects:  37% (42934/115502), 152.48 MiB | 2.79 MiB/s Receiving objects:  37% (43155/115502), 155.47 MiB | 2.84 MiB/s Receiving objects:  37% (43508/115502), 158.35 MiB | 2.90 MiB/s Receiving objects:  37% (43826/115502), 160.00 MiB | 2.89 MiB/s Receiving objects:  38% (43891/115502), 160.00 MiB | 2.89 MiB/s Receiving objects:  38% (44286/115502), 163.38 MiB | 2.96 MiB/s Receiving objects:  39% (45046/115502), 164.93 MiB | 3.01 MiB/s Receiving objects:  39% (45092/115502), 166.44 MiB | 3.02 MiB/s Receiving objects:  39% (45968/115502), 171.86 MiB | 3.23 MiB/s Receiving objects:  40% (46201/115502), 173.38 MiB | 3.27 MiB/s Receiving objects:  40% (46756/115502), 173.38 MiB | 3.27 MiB/s Receiving objects:  41% (47356/115502), 173.38 MiB | 3.27 MiB/s Receiving objects:  41% (48246/115502), 176.58 MiB | 3.20 MiB/s Receiving objects:  42% (48511/115502), 178.05 MiB | 3.17 MiB/s Receiving objects:  42% (49213/115502), 179.46 MiB | 3.16 MiB/s Receiving objects:  43% (49666/115502), 180.74 MiB | 3.10 MiB/s Receiving objects:  43% (49830/115502), 182.25 MiB | 3.07 MiB/s Receiving objects:  43% (49884/115502), 185.29 MiB | 2.91 MiB/s Receiving objects:  43% (49978/115502), 188.82 MiB | 2.66 MiB/s Receiving objects:  43% (50102/115502), 189.95 MiB | 2.59 MiB/s Receiving objects:  43% (50124/115502), 192.23 MiB | 2.49 MiB/s Receiving objects:  43% (50405/115502), 194.93 MiB | 2.41 MiB/s Receiving objects:  43% (50435/115502), 197.50 MiB | 2.38 MiB/s Receiving objects:  43% (50490/115502), 200.33 MiB | 2.51 MiB/s Receiving objects:  43% (50530/115502), 203.25 MiB | 2.67 MiB/s Receiving objects:  43% (50666/115502), 206.03 MiB | 2.74 MiB/s Receiving objects:  44% (50821/115502), 207.64 MiB | 2.78 MiB/s Receiving objects:  44% (51290/115502), 209.28 MiB | 2.88 MiB/s Receiving objects:  44% (51675/115502), 212.67 MiB | 3.05 MiB/s Receiving objects:  44% (51843/115502), 216.28 MiB | 3.19 MiB/s Receiving objects:  45% (51976/115502), 216.28 MiB | 3.19 MiB/s Receiving objects:  45% (52227/115502), 219.46 MiB | 3.20 MiB/s Receiving objects:  45% (52255/115502), 220.98 MiB | 3.24 MiB/s Receiving objects:  46% (53131/115502), 222.97 MiB | 3.32 MiB/s Receiving objects:  46% (53993/115502), 228.10 MiB | 3.76 MiB/s Receiving objects:  46% (54063/115502), 231.73 MiB | 3.75 MiB/s Receiving objects:  46% (54213/115502), 233.36 MiB | 3.73 MiB/s Receiving objects:  47% (54286/115502), 237.27 MiB | 3.93 MiB/s Receiving objects:  47% (54507/115502), 239.29 MiB | 4.04 MiB/s Receiving objects:  47% (54772/115502), 243.63 MiB | 3.98 MiB/s Receiving objects:  47% (54997/115502), 244.55 MiB | 3.62 MiB/s Receiving objects:  47% (55164/115502), 249.47 MiB | 3.86 MiB/s Receiving objects:  48% (55441/115502), 249.47 MiB | 3.86 MiB/s Receiving objects:  48% (55806/115502), 254.50 MiB | 4.18 MiB/s Receiving objects:  48% (56426/115502), 258.38 MiB | 4.14 MiB/s Receiving objects:  48% (56513/115502), 261.86 MiB | 3.94 MiB/s Receiving objects:  49% (56596/115502), 261.86 MiB | 3.94 MiB/s Receiving objects:  49% (56897/115502), 265.27 MiB | 3.93 MiB/s Receiving objects:  49% (57032/115502), 268.68 MiB | 3.68 MiB/s Receiving objects:  49% (57459/115502), 272.59 MiB | 3.54 MiB/s Receiving objects:  49% (57564/115502), 276.42 MiB | 3.59 MiB/s Receiving objects:  49% (57723/115502), 277.91 MiB | 3.36 MiB/s Receiving objects:  50% (57751/115502), 280.30 MiB | 3.50 MiB/s Receiving objects:  50% (57888/115502), 283.33 MiB | 3.38 MiB/s Receiving objects:  51% (58907/115502), 285.00 MiB | 3.38 MiB/s Receiving objects:  51% (59559/115502), 286.52 MiB | 3.29 MiB/s Receiving objects:  51% (59624/115502), 288.36 MiB | 3.27 MiB/s Receiving objects:  52% (60062/115502), 290.94 MiB | 3.02 MiB/s Receiving objects:  52% (60589/115502), 290.94 MiB | 3.02 MiB/s Receiving objects:  53% (61217/115502), 292.26 MiB | 3.14 MiB/s Receiving objects:  54% (62372/115502), 293.97 MiB | 2.99 MiB/s Receiving objects:  54% (62620/115502), 295.53 MiB | 3.00 MiB/s Receiving objects:  54% (62972/115502), 297.19 MiB | 3.06 MiB/s Receiving objects:  54% (63187/115502), 299.86 MiB | 2.94 MiB/s Receiving objects:  55% (63527/115502), 302.09 MiB | 2.71 MiB/s Receiving objects:  55% (63534/115502), 302.09 MiB | 2.71 MiB/s Receiving objects:  55% (63654/115502), 304.55 MiB | 2.68 MiB/s Receiving objects:  55% (64017/115502), 307.21 MiB | 2.54 MiB/s Receiving objects:  55% (64041/115502), 309.86 MiB | 2.39 MiB/s Receiving objects:  55% (64373/115502), 312.79 MiB | 2.56 MiB/s Receiving objects:  56% (64682/115502), 312.79 MiB | 2.56 MiB/s Receiving objects:  56% (65658/115502), 315.29 MiB | 2.66 MiB/s Receiving objects:  57% (65837/115502), 315.29 MiB | 2.66 MiB/s Receiving objects:  57% (66944/115502), 319.09 MiB | 2.93 MiB/s Receiving objects:  58% (66992/115502), 319.09 MiB | 2.93 MiB/s Receiving objects:  58% (67578/115502), 323.21 MiB | 3.21 MiB/s Receiving objects:  58% (67771/115502), 327.56 MiB | 3.56 MiB/s Receiving objects:  59% (68147/115502), 329.42 MiB | 3.65 MiB/s Receiving objects:  59% (68411/115502), 331.13 MiB | 3.79 MiB/s Receiving objects:  59% (68909/115502), 334.08 MiB | 3.71 MiB/s Receiving objects:  60% (69302/115502), 335.79 MiB | 3.66 MiB/s Receiving objects:  60% (69749/115502), 337.59 MiB | 3.60 MiB/s Receiving objects:  60% (70192/115502), 340.52 MiB | 3.28 MiB/s Receiving objects:  61% (70457/115502), 341.54 MiB | 3.06 MiB/s Receiving objects:  61% (70946/115502), 343.27 MiB | 3.04 MiB/s Receiving objects:  62% (71612/115502), 343.27 MiB | 3.04 MiB/s Receiving objects:  62% (72642/115502), 346.80 MiB | 3.09 MiB/s Receiving objects:  63% (72767/115502), 346.80 MiB | 3.09 MiB/s Receiving objects:  64% (73922/115502), 348.25 MiB | 3.11 MiB/s Receiving objects:  64% (74137/115502), 349.77 MiB | 3.06 MiB/s Receiving objects:  64% (74749/115502), 352.89 MiB | 2.98 MiB/s Receiving objects:  65% (75077/115502), 352.89 MiB | 2.98 MiB/s Receiving objects:  65% (75724/115502), 354.77 MiB | 3.13 MiB/s Receiving objects:  66% (76232/115502), 357.86 MiB | 3.20 MiB/s Receiving objects:  66% (77321/115502), 359.08 MiB | 3.01 MiB/s Receiving objects:  67% (77387/115502), 359.08 MiB | 3.01 MiB/s Receiving objects:  68% (78542/115502), 359.08 MiB | 3.01 MiB/s Receiving objects:  69% (79697/115502), 360.48 MiB | 2.99 MiB/s Receiving objects:  70% (80852/115502), 360.48 MiB | 2.99 MiB/s Receiving objects:  70% (81008/115502), 360.48 MiB | 2.99 MiB/s Receiving objects:  71% (82007/115502), 362.00 MiB | 3.00 MiB/s Receiving objects:  71% (83132/115502), 363.66 MiB | 3.04 MiB/s Receiving objects:  72% (83162/115502), 363.66 MiB | 3.04 MiB/s Receiving objects:  73% (84317/115502), 366.18 MiB | 2.91 MiB/s Receiving objects:  74% (85472/115502), 366.18 MiB | 2.91 MiB/s Receiving objects:  74% (85826/115502), 366.18 MiB | 2.91 MiB/s Receiving objects:  75% (86627/115502), 367.71 MiB | 2.83 MiB/s Receiving objects:  76% (87782/115502), 367.71 MiB | 2.83 MiB/s Receiving objects:  77% (88937/115502), 369.02 MiB | 2.79 MiB/s Receiving objects:  77% (89962/115502), 369.02 MiB | 2.79 MiB/s Receiving objects:  78% (90092/115502), 369.02 MiB | 2.79 MiB/s Receiving objects:  79% (91247/115502), 370.39 MiB | 2.75 MiB/s Receiving objects:  80% (92402/115502), 371.96 MiB | 2.84 MiB/s Receiving objects:  81% (93557/115502), 371.96 MiB | 2.84 MiB/s Receiving objects:  82% (94712/115502), 371.96 MiB | 2.84 MiB/s Receiving objects:  82% (94737/115502), 371.96 MiB | 2.84 MiB/s Receiving objects:  83% (95867/115502), 373.78 MiB | 2.93 MiB/s Receiving objects:  84% (97022/115502), 373.78 MiB | 2.93 MiB/s Receiving objects:  85% (98177/115502), 375.03 MiB | 2.88 MiB/s Receiving objects:  85% (99063/115502), 376.84 MiB | 2.91 MiB/s Receiving objects:  85% (99216/115502), 380.11 MiB | 3.06 MiB/s Receiving objects:  85% (99296/115502), 383.48 MiB | 3.18 MiB/s Receiving objects:  86% (99332/115502), 383.48 MiB | 3.18 MiB/s Receiving objects:  86% (99418/115502), 387.36 MiB | 3.38 MiB/s Receiving objects:  86% (99500/115502), 390.40 MiB | 3.36 MiB/s Receiving objects:  86% (99706/115502), 393.28 MiB | 3.21 MiB/s Receiving objects:  86% (99917/115502), 397.25 MiB | 3.42 MiB/s Receiving objects:  86% (100212/115502), 397.86 MiB | 2.40 MiB/sReceiving objects:  87% (100487/115502), 397.86 MiB | 2.40 MiB/sReceiving objects:  88% (101642/115502), 397.86 MiB | 2.40 MiB/sReceiving objects:  89% (102797/115502), 404.52 MiB | 3.16 MiB/sReceiving objects:  89% (103881/115502), 404.52 MiB | 3.16 MiB/sReceiving objects:  90% (103952/115502), 404.52 MiB | 3.16 MiB/sReceiving objects:  91% (105107/115502), 404.52 MiB | 3.16 MiB/sReceiving objects:  92% (106262/115502), 406.08 MiB | 3.11 MiB/sReceiving objects:  92% (107391/115502), 409.83 MiB | 3.24 MiB/sReceiving objects:  92% (107394/115502), 412.71 MiB | 3.05 MiB/sReceiving objects:  93% (107417/115502), 412.71 MiB | 3.05 MiB/sReceiving objects:  94% (108572/115502), 412.71 MiB | 3.05 MiB/sReceiving objects:  94% (109507/115502), 412.71 MiB | 3.05 MiB/sReceiving objects:  95% (109727/115502), 412.71 MiB | 3.05 MiB/sReceiving objects:  96% (110882/115502), 416.30 MiB | 3.28 MiB/sReceiving objects:  97% (112037/115502), 416.30 MiB | 3.28 MiB/sReceiving objects:  97% (113185/115502), 417.85 MiB | 3.23 MiB/sReceiving objects:  98% (113192/115502), 417.85 MiB | 3.23 MiB/sReceiving objects:  99% (114347/115502), 419.59 MiB | 4.41 MiB/sremote: Total 115502 (delta 1205), reused 863 (delta 841), pack-reused 113957 (from 2)
Receiving objects: 100% (115502/115502), 421.73 MiB | 3.49 MiB/sReceiving objects: 100% (115502/115502), 422.16 MiB | 3.23 MiB/s, done.
Resolving deltas: 100% (81208/81208), done.
Checking out files: 100% (3450/3450), done.
jetauto@jetauto-desktop:/mnt/llm/llama.cpp$ cd /mnt/llm/llama.cpp/llama5050gpu.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ git log -1 --oneline
5a32f7b66 (HEAD -> master, origin/master, origin/HEAD) model: add dots3-note (#27060)
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ git cat-file -t 23106f9
commit
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ git checkout 23106f9
Checking out files: 100% (3697/3697), done.
Note: checking out '23106f9'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b <new-branch-name>

HEAD is now at 23106f94e gguf-split : --merge now respects --dry-run option (#12681)
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ git checkout -b llamaJetsonNanoCUDA
Switched to a new branch 'llamaJetsonNanoCUDA'
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ git log -1 --oneline
23106f94e (HEAD -> llamaJetsonNanoCUDA, tag: b5050) gguf-split : --merge now respects --dry-run option (#12681)
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ gcc-8 --version
gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ g++-8 --version
g++-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2021 NVIDIA Corporation
Built on Sun_Feb_28_22:34:44_PST_2021
Cuda compilation tools, release 10.2, V10.2.300
Build cuda_10.2_r440.TC440_70.29663091_0
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ ~/local_ai/cmake-3.27.1/bin/cmake --version
cmake version 3.27.1

CMake suite maintained and supported by Kitware (kitware.com/cmake).
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ ls -ld /usr/local/cuda
lrwxrwxrwx 1 root root 22 Feb 23  2022 /usr/local/cuda -> /etc/alternatives/cuda
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ ls /usr/local/cuda/lib64/libcudart.so*
/usr/local/cuda/lib64/libcudart.so
/usr/local/cuda/lib64/libcudart.so.10.2
/usr/local/cuda/lib64/libcudart.so.10.2.300
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ cd /mnt/llm/llama.cpp/llama5050gpu.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ rm -rf /mnt/llm/builds/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ mkdir -p /mnt/llm/builds/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ ~/local_ai/cmake-3.27.1/bin/cmake -S /mnt/llm/llama.cpp/llama5050gpu.cpp \
> -B /mnt/llm/builds/llama.cpp \
> -DCMAKE_C_COMPILER=gcc-8 \
> -DCMAKE_CXX_COMPILER=g++-8 \
> -DGGML_CUDA=ON
-- The C compiler identification is GNU 8.4.0
-- The CXX compiler identification is GNU 8.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/gcc-8 - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/g++-8 - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found Git: /usr/bin/git (found version "2.17.1")
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
-- Check if compiler accepts -pthread
-- Check if compiler accepts -pthread - yes
-- Found Threads: TRUE
-- Warning: ccache not found - consider installing it for faster compilation or disable this warning with GGML_CCACHE=OFF
-- CMAKE_SYSTEM_PROCESSOR: aarch64
-- Including CPU backend
-- Found OpenMP_C: -fopenmp (found version "4.5")
-- Found OpenMP_CXX: -fopenmp (found version "4.5")
-- Found OpenMP: TRUE (found version "4.5")
-- ARM detected
-- Performing Test GGML_COMPILER_SUPPORTS_FP16_FORMAT_I3E
-- Performing Test GGML_COMPILER_SUPPORTS_FP16_FORMAT_I3E - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_dotprod
-- Performing Test GGML_MACHINE_SUPPORTS_dotprod - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nodotprod
-- Performing Test GGML_MACHINE_SUPPORTS_nodotprod - Success
-- Performing Test GGML_MACHINE_SUPPORTS_i8mm
-- Performing Test GGML_MACHINE_SUPPORTS_i8mm - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_noi8mm
-- Performing Test GGML_MACHINE_SUPPORTS_noi8mm - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_sve
-- Performing Test GGML_MACHINE_SUPPORTS_sve - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nosve
-- Performing Test GGML_MACHINE_SUPPORTS_nosve - Success
-- Performing Test GGML_MACHINE_SUPPORTS_sme
-- Performing Test GGML_MACHINE_SUPPORTS_sme - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nosme
-- Performing Test GGML_MACHINE_SUPPORTS_nosme - Failed
-- ARM feature FMA enabled
-- Adding CPU backend variant ggml-cpu: -mcpu=cortex-a57+crypto+nodotprod+nosve
-- Found CUDAToolkit: /usr/local/cuda/include (found version "10.2.300")
-- CUDA Toolkit found
-- Using CUDA architectures: 50;61;70;75;80
-- The CUDA compiler identification is NVIDIA 10.2.300
-- Detecting CUDA compiler ABI info
-- Detecting CUDA compiler ABI info - failed
-- Check for working CUDA compiler: /usr/local/cuda/bin/nvcc
-- Check for working CUDA compiler: /usr/local/cuda/bin/nvcc - broken
CMake Error at /home/jetauto/local_ai/cmake-3.27.1/share/cmake-3.27/Modules/CMakeTestCUDACompiler.cmake:100 (message):
  The CUDA compiler

    "/usr/local/cuda/bin/nvcc"

  is not able to compile a simple test program.

  It fails with the following output:

    Change Dir: '/mnt/llm/builds/llama.cpp/CMakeFiles/CMakeScratch/TryCompile-DT4xZ3'

    Run Build Command(s): /home/jetauto/local_ai/cmake-3.27.1/bin/cmake -E env VERBOSE=1 /usr/bin/make -f Makefile cmTC_9ec74/fast
    /usr/bin/make  -f CMakeFiles/cmTC_9ec74.dir/build.make CMakeFiles/cmTC_9ec74.dir/build
    make[1]: Entering directory '/mnt/llm/builds/llama.cpp/CMakeFiles/CMakeScratch/TryCompile-DT4xZ3'
    Building CUDA object CMakeFiles/cmTC_9ec74.dir/main.cu.o
    /usr/local/cuda/bin/nvcc -forward-unknown-to-host-compiler   "--generate-code=arch=compute_50,code=[compute_50,sm_50]" "--generate-code=arch=compute_61,code=[compute_61,sm_61]" "--generate-code=arch=compute_70,code=[compute_70,sm_70]" "--generate-code=arch=compute_75,code=[compute_75,sm_75]" "--generate-code=arch=compute_80,code=[compute_80,sm_80]" -MD -MT CMakeFiles/cmTC_9ec74.dir/main.cu.o -MF CMakeFiles/cmTC_9ec74.dir/main.cu.o.d -x cu -c /mnt/llm/builds/llama.cpp/CMakeFiles/CMakeScratch/TryCompile-DT4xZ3/main.cu -o CMakeFiles/cmTC_9ec74.dir/main.cu.o
    nvcc fatal   : Unsupported gpu architecture 'compute_80'
    CMakeFiles/cmTC_9ec74.dir/build.make:78: recipe for target 'CMakeFiles/cmTC_9ec74.dir/main.cu.o' failed
    make[1]: *** [CMakeFiles/cmTC_9ec74.dir/main.cu.o] Error 1
    make[1]: Leaving directory '/mnt/llm/builds/llama.cpp/CMakeFiles/CMakeScratch/TryCompile-DT4xZ3'
    Makefile:127: recipe for target 'cmTC_9ec74/fast' failed
    make: *** [cmTC_9ec74/fast] Error 2





  CMake will not be able to correctly generate this project.
Call Stack (most recent call first):
  ggml/src/ggml-cuda/CMakeLists.txt:25 (enable_language)


-- Configuring incomplete, errors occurred!
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -E "GGML_CUDA|CMAKE_CUDA|CMAKE_CXX_COMPILER" \
> /mnt/llm/builds/llama.cpp/CMakeCache.txt
CMAKE_CUDA_COMPILER:FILEPATH=/usr/local/cuda/bin/nvcc
CMAKE_CUDA_FLAGS:STRING=
CMAKE_CUDA_FLAGS_DEBUG:STRING=-g
CMAKE_CUDA_FLAGS_MINSIZEREL:STRING=-O1 -DNDEBUG
CMAKE_CUDA_FLAGS_RELEASE:STRING=-O3 -DNDEBUG
CMAKE_CUDA_FLAGS_RELWITHDEBINFO:STRING=-O2 -g -DNDEBUG
CMAKE_CXX_COMPILER:STRING=/usr/bin/g++-8
CMAKE_CXX_COMPILER_AR:FILEPATH=/usr/bin/gcc-ar-8
CMAKE_CXX_COMPILER_RANLIB:FILEPATH=/usr/bin/gcc-ranlib-8
GGML_CUDA:BOOL=ON
GGML_CUDA_COMPRESSION_MODE:STRING=size
GGML_CUDA_F16:BOOL=OFF
GGML_CUDA_FA:BOOL=ON
GGML_CUDA_FA_ALL_QUANTS:BOOL=OFF
GGML_CUDA_FORCE_CUBLAS:BOOL=OFF
GGML_CUDA_FORCE_MMQ:BOOL=OFF
GGML_CUDA_GRAPHS:BOOL=ON
GGML_CUDA_NO_PEER_COPY:BOOL=OFF
GGML_CUDA_NO_VMM:BOOL=OFF
GGML_CUDA_PEER_MAX_BATCH_SIZE:STRING=128
//ADVANCED property for variable: CMAKE_CUDA_COMPILER
CMAKE_CUDA_COMPILER-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CUDA_FLAGS
CMAKE_CUDA_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CUDA_FLAGS_DEBUG
CMAKE_CUDA_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CUDA_FLAGS_MINSIZEREL
CMAKE_CUDA_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CUDA_FLAGS_RELEASE
CMAKE_CUDA_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CUDA_FLAGS_RELWITHDEBINFO
CMAKE_CUDA_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_COMPILER
CMAKE_CXX_COMPILER-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_COMPILER_AR
CMAKE_CXX_COMPILER_AR-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_COMPILER_RANLIB
CMAKE_CXX_COMPILER_RANLIB-ADVANCED:INTERNAL=1
//STRINGS property for variable: GGML_CUDA_COMPRESSION_MODE
GGML_CUDA_COMPRESSION_MODE-STRINGS:INTERNAL=none;speed;balance;size
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ rm -rf /mnt/llm/builds/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ mkdir -p /mnt/llm/builds/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ ~/local_ai/cmake-3.27.1/bin/cmake \
> -S /mnt/llm/llama.cpp/llama5050gpu.cpp \
> -B /mnt/llm/builds/llama.cpp \
> -DCMAKE_C_COMPILER=gcc-8 \
> -DCMAKE_CXX_COMPILER=g++-8 \
> -DGGML_CUDA=ON \
> -DCMAKE_CUDA_ARCHITECTURES=53
-- The C compiler identification is GNU 8.4.0
-- The CXX compiler identification is GNU 8.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/gcc-8 - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/g++-8 - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found Git: /usr/bin/git (found version "2.17.1")
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
-- Check if compiler accepts -pthread
-- Check if compiler accepts -pthread - yes
-- Found Threads: TRUE
-- Warning: ccache not found - consider installing it for faster compilation or disable this warning with GGML_CCACHE=OFF
-- CMAKE_SYSTEM_PROCESSOR: aarch64
-- Including CPU backend
-- Found OpenMP_C: -fopenmp (found version "4.5")
-- Found OpenMP_CXX: -fopenmp (found version "4.5")
-- Found OpenMP: TRUE (found version "4.5")
-- ARM detected
-- Performing Test GGML_COMPILER_SUPPORTS_FP16_FORMAT_I3E
-- Performing Test GGML_COMPILER_SUPPORTS_FP16_FORMAT_I3E - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_dotprod
-- Performing Test GGML_MACHINE_SUPPORTS_dotprod - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nodotprod
-- Performing Test GGML_MACHINE_SUPPORTS_nodotprod - Success
-- Performing Test GGML_MACHINE_SUPPORTS_i8mm
-- Performing Test GGML_MACHINE_SUPPORTS_i8mm - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_noi8mm
-- Performing Test GGML_MACHINE_SUPPORTS_noi8mm - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_sve
-- Performing Test GGML_MACHINE_SUPPORTS_sve - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nosve
-- Performing Test GGML_MACHINE_SUPPORTS_nosve - Success
-- Performing Test GGML_MACHINE_SUPPORTS_sme
-- Performing Test GGML_MACHINE_SUPPORTS_sme - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nosme
-- Performing Test GGML_MACHINE_SUPPORTS_nosme - Failed
-- ARM feature FMA enabled
-- Adding CPU backend variant ggml-cpu: -mcpu=cortex-a57+crypto+nodotprod+nosve
-- Found CUDAToolkit: /usr/local/cuda/include (found version "10.2.300")
-- CUDA Toolkit found
-- Using CUDA architectures: 53
-- The CUDA compiler identification is NVIDIA 10.2.300
-- Detecting CUDA compiler ABI info
-- Detecting CUDA compiler ABI info - done
-- Check for working CUDA compiler: /usr/local/cuda/bin/nvcc - skipped
-- Detecting CUDA compile features
-- Detecting CUDA compile features - done
-- CUDA host compiler is GNU 7.5.0

-- Including CUDA backend
-- Looking for pthread_create in pthreads
-- Looking for pthread_create in pthreads - not found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - found
-- Configuring done (11.1s)
CMake Error in ggml/src/ggml-cuda/CMakeLists.txt:
  Target "ggml-cuda" requires the language dialect "CUDA17" (with compiler
  extensions).  But the current compiler "NVIDIA" does not support this, or
  CMake does not know the flags to enable it.


-- Generating done (0.6s)
CMake Generate step failed.  Build files cannot be regenerated correctly.
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -E "GGML_CUDA|CMAKE_CUDA|CMAKE_CXX_COMPILER" /mnt/llm/builds/llama.cpp/CMakeCache.txt
CMAKE_CUDA_ARCHITECTURES:UNINITIALIZED=53
CMAKE_CUDA_COMPILER:FILEPATH=/usr/local/cuda/bin/nvcc
CMAKE_CUDA_FLAGS:STRING=
CMAKE_CUDA_FLAGS_DEBUG:STRING=-g
CMAKE_CUDA_FLAGS_MINSIZEREL:STRING=-O1 -DNDEBUG
CMAKE_CUDA_FLAGS_RELEASE:STRING=-O3 -DNDEBUG
CMAKE_CUDA_FLAGS_RELWITHDEBINFO:STRING=-O2 -g -DNDEBUG
CMAKE_CXX_COMPILER:STRING=/usr/bin/g++-8
CMAKE_CXX_COMPILER_AR:FILEPATH=/usr/bin/gcc-ar-8
CMAKE_CXX_COMPILER_RANLIB:FILEPATH=/usr/bin/gcc-ranlib-8
GGML_CUDA:BOOL=ON
GGML_CUDA_COMPRESSION_MODE:STRING=size
GGML_CUDA_F16:BOOL=OFF
GGML_CUDA_FA:BOOL=ON
GGML_CUDA_FA_ALL_QUANTS:BOOL=OFF
GGML_CUDA_FORCE_CUBLAS:BOOL=OFF
GGML_CUDA_FORCE_MMQ:BOOL=OFF
GGML_CUDA_GRAPHS:BOOL=ON
GGML_CUDA_NO_PEER_COPY:BOOL=OFF
GGML_CUDA_NO_VMM:BOOL=OFF
GGML_CUDA_PEER_MAX_BATCH_SIZE:STRING=128
//ADVANCED property for variable: CMAKE_CUDA_COMPILER
CMAKE_CUDA_COMPILER-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CUDA_FLAGS
CMAKE_CUDA_FLAGS-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CUDA_FLAGS_DEBUG
CMAKE_CUDA_FLAGS_DEBUG-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CUDA_FLAGS_MINSIZEREL
CMAKE_CUDA_FLAGS_MINSIZEREL-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CUDA_FLAGS_RELEASE
CMAKE_CUDA_FLAGS_RELEASE-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CUDA_FLAGS_RELWITHDEBINFO
CMAKE_CUDA_FLAGS_RELWITHDEBINFO-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_COMPILER
CMAKE_CXX_COMPILER-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_COMPILER_AR
CMAKE_CXX_COMPILER_AR-ADVANCED:INTERNAL=1
//ADVANCED property for variable: CMAKE_CXX_COMPILER_RANLIB
CMAKE_CXX_COMPILER_RANLIB-ADVANCED:INTERNAL=1
//STRINGS property for variable: GGML_CUDA_COMPRESSION_MODE
GGML_CUDA_COMPRESSION_MODE-STRINGS:INTERNAL=none;speed;balance;size
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -R "CUDA17" -n /mnt/llm/llama.cpp/llama5050gpu.cpp/ggml/src/ggml-cuda
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -R "CMAKE_CUDA_STANDARD\|CUDA_STANDARD" -n /mnt/llm/llama.cpp/llama5050gpu.cpp/ggml
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ /usr/local/cuda/bin/nvcc --help | grep -i std | head -20
        to stdout.
--std {c++03|c++11|c++14},...                   (-std)          
        Do not implicitly consider member functions of std::initializer_list as __host__
        Do not implicitly consider std::move and std::forward as __host__ __device__
        of the table. If the file name is '-', the timing data is generated in stdout.
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ /usr/local/cuda/bin/nvcc -ccbin gcc-8 --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2021 NVIDIA Corporation
Built on Sun_Feb_28_22:34:44_PST_2021
Cuda compilation tools, release 10.2, V10.2.300
Build cuda_10.2_r440.TC440_70.29663091_0
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ echo $CC

jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ echo $CXX

jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ rm -rf /mnt/llm/builds/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ mkdir -p /mnt/llm/builds/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ CC=gcc-8 CXX=g++-8 \
> ~/local_ai/cmake-3.27.1/bin/cmake \
> -S /mnt/llm/llama.cpp/llama5050gpu.cpp \
> -B /mnt/llm/builds/llama.cpp \
> -DCMAKE_C_COMPILER=gcc-8 \
> -DCMAKE_CXX_COMPILER=g++-8 \
> -DCMAKE_CUDA_HOST_COMPILER=g++-8 \
> -DCMAKE_CUDA_ARCHITECTURES=53 \
> -DCMAKE_CUDA_STANDARD=14 \
> -DCMAKE_CUDA_STANDARD_REQUIRED=ON \
> -DGGML_CUDA=ON
-- The C compiler identification is GNU 8.4.0
-- The CXX compiler identification is GNU 8.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/gcc-8 - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/g++-8 - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found Git: /usr/bin/git (found version "2.17.1")
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
-- Check if compiler accepts -pthread
-- Check if compiler accepts -pthread - yes
-- Found Threads: TRUE
-- Warning: ccache not found - consider installing it for faster compilation or disable this warning with GGML_CCACHE=OFF
-- CMAKE_SYSTEM_PROCESSOR: aarch64
-- Including CPU backend
-- Found OpenMP_C: -fopenmp (found version "4.5")
-- Found OpenMP_CXX: -fopenmp (found version "4.5")
-- Found OpenMP: TRUE (found version "4.5")
-- ARM detected
-- Performing Test GGML_COMPILER_SUPPORTS_FP16_FORMAT_I3E
-- Performing Test GGML_COMPILER_SUPPORTS_FP16_FORMAT_I3E - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_dotprod
-- Performing Test GGML_MACHINE_SUPPORTS_dotprod - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nodotprod
-- Performing Test GGML_MACHINE_SUPPORTS_nodotprod - Success
-- Performing Test GGML_MACHINE_SUPPORTS_i8mm
-- Performing Test GGML_MACHINE_SUPPORTS_i8mm - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_noi8mm
-- Performing Test GGML_MACHINE_SUPPORTS_noi8mm - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_sve
-- Performing Test GGML_MACHINE_SUPPORTS_sve - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nosve
-- Performing Test GGML_MACHINE_SUPPORTS_nosve - Success
-- Performing Test GGML_MACHINE_SUPPORTS_sme
-- Performing Test GGML_MACHINE_SUPPORTS_sme - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nosme
-- Performing Test GGML_MACHINE_SUPPORTS_nosme - Failed
-- ARM feature FMA enabled
-- Adding CPU backend variant ggml-cpu: -mcpu=cortex-a57+crypto+nodotprod+nosve
-- Found CUDAToolkit: /usr/local/cuda/include (found version "10.2.300")
-- CUDA Toolkit found
-- Using CUDA architectures: 53
-- The CUDA compiler identification is NVIDIA 10.2.300
-- Detecting CUDA compiler ABI info
-- Detecting CUDA compiler ABI info - done
-- Check for working CUDA compiler: /usr/local/cuda/bin/nvcc - skipped
-- Detecting CUDA compile features
-- Detecting CUDA compile features - done
-- CUDA host compiler is GNU 8.4.0

-- Including CUDA backend
-- Looking for pthread_create in pthreads
-- Looking for pthread_create in pthreads - not found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - found
-- Configuring done (11.4s)
-- Generating done (0.6s)
-- Build files have been written to: /mnt/llm/builds/llama.cpp

GCC/G++       8.4.0       ✅
CUDA          10.2        ✅
CMake         3.27.1      ✅
CUDA runtime  10.2.300    ✅
llama.cpp     23106f94e   ✅
Branch        llamaJetsonNanoCUDA
Storage       ext4 /mnt/llm ✅

sudo nano /usr/local/cuda/include/cuda_bf16.h
```
#ifndef CUDA_BF16_H
#define CUDA_BF16_H

#include <cuda_fp16.h>

// Define nv_bfloat16 as half
typedef half nv_bfloat16;

#endif // CUDA_BF16_H
```
sudo nano /usr/local/cuda/include/cuda_bf16.hpp
```
#ifndef CUDA_BF16_HPP
#define CUDA_BF16_HPP

#include "cuda_bf16.h"

namespace cuda {

    class BFloat16 {
    public:
        nv_bfloat16 value;

        __host__ __device__ BFloat16() : value(0) {}
        __host__ __device__ BFloat16(float f) { value = __float2half(f); }
        __host__ __device__ operator float() const { return __half2float(value); }
    };

} // namespace cuda

#endif // CUDA_BF16_HPP
```
ls -l /usr/local/cuda/include/cuda_bf16.h
ls -l /usr/local/cuda/include/cuda_bf16.hpp

Storage
└── /mnt/llm
    ├── llama.cpp/
    │   └── llama5050gpu.cpp/
    ├── models/
    ├── builds/
    ├── cache/
    └── projects/

Compiler
├── GCC 8.4.0
└── G++ 8.4.0

Build
└── CMake 3.27.1

CUDA
└── CUDA 10.2

llama.cpp
├── Commit: 23106f94e
├── Tag: b5050
└── Branch: llamaJetsonNanoCUDA

jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ git log --oneline --all -10
cba793e (HEAD -> main, origin/main, origin/HEAD) Add LFM2.5-1.2B-Thinking section to README
15ba3a7 Can we compile for Liquid?
a944a17 two processes concurrently
678a3cb include small images above bigger subsections for readability
bff1a3e prerequisites
c293067 include small logos for better readability
f3778c7 include Gemma 3 logo
603909b Merge branch 'main' of https://github.com/kreier/llama.cpp-jetson
86415f4 updated graph, include comparison CPU
1c3e9e5 improve wording of a few instructions
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ sudo nano /usr/local/cuda/include/cuda_bf16.h
                                                                
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ ls -l /usr/local/cuda/include/cuda_bf16.h
-rw-r--r-- 1 root root 144 Aug 22 00:36 /usr/local/cuda/include/cuda_bf16.h
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ ls -l /usr/local/cuda/include/cuda_bf16.hpp
-rw-r--r-- 1 root root 412 Aug 22 00:36 /usr/local/cuda/include/cuda_bf16.hpp
jetauto@jetauto-desktop:~/local_ai/llama.cpp-jetson$ cd /mnt/llm/llama.cpp/llama5050gpu.cpp
                                                                
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -n "CMAKE_CUDA_ARCHITECTURES" CMakeLists.txt | head
3:if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES)
4:    set(CMAKE_CUDA_ARCHITECTURES 50 61)
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ nano ggml/CMakeLists.txt
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -n -A3 -B2 "set_target_properties(ggml" ggml/CMakeLists.txt
272-    include/gguf.h)
273-
274:set_target_properties(ggml PROPERTIES PUBLIC_HEADER "${GGML_PUBLIC_HEADERS}")
275-target_link_libraries(ggml PRIVATE stdc++fs)
276-add_link_options(-Wl,--copy-dt-needed-entries)
277-#if (GGML_METAL)
278:#    set_target_properties(ggml PROPERTIES RESOURCE "${CMAKE_CURRENT_SOURCE_DIR}/src/ggml-metal.metal")
279-#endif()
280-install(TARGETS ggml LIBRARY PUBLIC_HEADER)
281-install(TARGETS ggml-base LIBRARY)
                                                                
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -n "static.*__device__" ggml/src/ggml-cuda/common.cuh
268:static __device__ int ggml_cuda_get_physical_warp_size() {
277:static __device__ void no_device_code(
304:static __device__ __forceinline__ int warp_reduce_sum(int x) {
317:static __device__ __forceinline__ float warp_reduce_sum(float x) {
326:static __device__ __forceinline__ float2 warp_reduce_sum(float2 a) {
336:static __device__ __forceinline__ half2 warp_reduce_sum(half2 a) {
351:static __device__ __forceinline__ float warp_reduce_max(float x) {
359:static __device__ __forceinline__ half ggml_cuda_hmax(const half a, const half b) {
375:static __device__ __forceinline__ half2 ggml_cuda_hmax2(const half2 a, const half2 b) {
393:static __device__ __forceinline__ half2 warp_reduce_max(half2 x) {
407:static __device__ __forceinline__ uint32_t __hgt2_mask(const half2 a, const half2 b) {
414:static __device__ __forceinline__ int ggml_cuda_dp4a(const int a, const int b, int c) {
455:static constexpr __device__ int8_t kvalues_iq4nl[16] = {-127, -104, -83, -65, -49, -35, -22, -10, 1, 13, 25, 38, 53, 69, 89, 113};
459:static __device__ __forceinline__ float get_alibi_slope(
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ nano ggml/src/ggml-cuda/common.cuh
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ nano ggml/src/ggml-cuda/common.cuh
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -n "static.*__device__" ggml/src/ggml-cuda/common.cuh
268:static __device__ int ggml_cuda_get_physical_warp_size() {
277:static __device__ void no_device_code(
304:static __device__ __forceinline__ int warp_reduce_sum(int x) {
317:static __device__ __forceinline__ float warp_reduce_sum(float x) {
326:static __device__ __forceinline__ float2 warp_reduce_sum(float2 a) {
336:static __device__ __forceinline__ half2 warp_reduce_sum(half2 a) {
351:static __device__ __forceinline__ float warp_reduce_max(float x) {
359:static __device__ __forceinline__ half ggml_cuda_hmax(const half a, const half b) {
375:static __device__ __forceinline__ half2 ggml_cuda_hmax2(const half2 a, const half2 b) {
393:static __device__ __forceinline__ half2 warp_reduce_max(half2 x) {
407:static __device__ __forceinline__ uint32_t __hgt2_mask(const half2 a, const half2 b) {
414:static __device__ __forceinline__ int ggml_cuda_dp4a(const int a, const int b, int c) {
455:static __device__ int8_t kvalues_iq4nl[16] = {-127, -104, -83, -65, -49, -35, -22, -10, 1, 13, 25, 38, 53, 69, 89, 113};
459:static __device__ __forceinline__ float get_alibi_slope(
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -n "kvalues_iq4nl" ggml/src/ggml-cuda/common.cuh
455:static __device__ int8_t kvalues_iq4nl[16] = {-127, -104, -83, -65, -49, -35, -22, -10, 1, 13, 25, 38, 53, 69, 89, 113};
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -R -n "__builtin_assume" ggml/src/ggml-cuda/
ggml/src/ggml-cuda/fattn-vec-f16.cuh:73:    __builtin_assume(tid < D);
ggml/src/ggml-cuda/common.cuh:185:#define GGML_CUDA_ASSUME(x) __builtin_assume(x)
ggml/src/ggml-cuda/fattn-vec-f32.cuh:71:    __builtin_assume(tid < D);
ggml/src/ggml-cuda/fattn-common.cuh:623:    __builtin_assume(tid < D);
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ nano ggml/src/ggml-cuda/fattn-common.cuh
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ nano ggml/src/ggml-cuda/fattn-vec-f32.cuh
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ nano ggml/src/ggml-cuda/fattn-vec-f16.cuh
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ grep -R -n "__builtin_assume" ggml/src/ggml-cuda/
ggml/src/ggml-cuda/fattn-vec-f16.cuh:73:    // __builtin_assume(tid < D);
ggml/src/ggml-cuda/common.cuh:185:#define GGML_CUDA_ASSUME(x) __builtin_assume(x)
ggml/src/ggml-cuda/fattn-vec-f32.cuh:71:    // __builtin_assume(tid < D);
ggml/src/ggml-cuda/fattn-common.cuh:623:    // __builtin_assume(tid < D);

jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ git diff -- ggml/src/ggml-cuda/common.cuh
diff --git a/ggml/src/ggml-cuda/common.cuh b/ggml/src/ggml-cuda/common.cuh
index 8284a0017..0efa5b558 100644
--- a/ggml/src/ggml-cuda/common.cuh
+++ b/ggml/src/ggml-cuda/common.cuh
@@ -265,7 +265,7 @@ static bool cp_async_available(const int cc) {
     return cc < GGML_CUDA_CC_OFFSET_AMD && ggml_cuda_highest_compiled_arch(cc) >= GGML_CUDA_CC_AMPERE;
 }

-static constexpr __device__ int ggml_cuda_get_physical_warp_size() {
+static __device__ int ggml_cuda_get_physical_warp_size() {
 #if defined(GGML_USE_HIP) && defined(__HIP_PLATFORM_AMD__)
     return __AMDGCN_WAVEFRONT_SIZE;
 #else
@@ -452,7 +452,7 @@ static __device__ __forceinline__ int ggml_cuda_dp4a(const int a, const int b, i
 }

 // TODO: move to ggml-common.h
-static constexpr __device__ int8_t kvalues_iq4nl[16] = {-127, -104, -83, -65, -49, -35, -22, -10, 1, 13, 25, 38, 53, 69, 89, 113};
+static __device__ int8_t kvalues_iq4nl[16] = {-127, -104, -83, -65, -49, -35, -22, -10, 1, 13, 25, 38, 53, 69, 89, 113};

 typedef void (*dequantize_kernel_t)(const void * vx, const int64_t ib, const int iqs, dfloat2 & v);

jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ git show HEAD:ggml/src/ggml-cuda/common.cuh | sed -n '255,465p' | grep -n -B2 -A2 "constexpr.*__device__"
12-}
13-
14:static constexpr __device__ int ggml_cuda_get_physical_warp_size() {
15-#if defined(GGML_USE_HIP) && defined(__HIP_PLATFORM_AMD__)
16-    return __AMDGCN_WAVEFRONT_SIZE;
--
199-
200-// TODO: move to ggml-common.h
201:static constexpr __device__ int8_t kvalues_iq4nl[16] = {-127, -104, -83, -65, -49, -35, -22, -10, 1, 13, 25, 38, 53, 69, 89, 113};
202-
203-typedef void (*dequantize_kernel_t)(const void * vx, const int64_t ib, const int iqs, dfloat2 & v);
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ git status --short
 M CMakeLists.txt
 M ggml/CMakeLists.txt
 M ggml/src/ggml-cuda/common.cuh
 M ggml/src/ggml-cuda/fattn-common.cuh
 M ggml/src/ggml-cuda/fattn-vec-f16.cuh
 M ggml/src/ggml-cuda/fattn-vec-f32.cuh
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ git diff > /mnt/llm/projects/llamaJetsonNanoCUDA.patch
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ ls -lh /mnt/llm/projects/llamaJetsonNanoCUDA.patch
-rw-rw-r-- 1 jetauto jetauto 3.7K Aug 22 01:10 /mnt/llm/projects/llamaJetsonNanoCUDA.patch
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ rm -rf /mnt/llm/builds/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ mkdir -p /mnt/llm/builds/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ CC=gcc-8 CXX=g++-8 \
> ~/local_ai/cmake-3.27.1/bin/cmake \
> -S /mnt/llm/llama.cpp/llama5050gpu.cpp \
> -B /mnt/llm/builds/llama.cpp \
> -DCMAKE_C_COMPILER=gcc-8 \
> -DCMAKE_CXX_COMPILER=g++-8 \
> -DCMAKE_CUDA_HOST_COMPILER=g++-8 \
> -DCMAKE_CUDA_ARCHITECTURES=53 \
> -DCMAKE_CUDA_STANDARD=14 \
> -DCMAKE_CUDA_STANDARD_REQUIRED=ON \
> -DGGML_CUDA=ON
-- The C compiler identification is GNU 8.4.0
-- The CXX compiler identification is GNU 8.4.0
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working C compiler: /usr/bin/gcc-8 - skipped
-- Detecting C compile features
-- Detecting C compile features - done
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/g++-8 - skipped
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found Git: /usr/bin/git (found version "2.17.1")
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
-- Check if compiler accepts -pthread
-- Check if compiler accepts -pthread - yes
-- Found Threads: TRUE
-- Warning: ccache not found - consider installing it for faster compilation or disable this warning with GGML_CCACHE=OFF
-- CMAKE_SYSTEM_PROCESSOR: aarch64
-- Including CPU backend
-- Found OpenMP_C: -fopenmp (found version "4.5")
-- Found OpenMP_CXX: -fopenmp (found version "4.5")
-- Found OpenMP: TRUE (found version "4.5")
-- ARM detected
-- Performing Test GGML_COMPILER_SUPPORTS_FP16_FORMAT_I3E
-- Performing Test GGML_COMPILER_SUPPORTS_FP16_FORMAT_I3E - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_dotprod
-- Performing Test GGML_MACHINE_SUPPORTS_dotprod - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nodotprod
-- Performing Test GGML_MACHINE_SUPPORTS_nodotprod - Success
-- Performing Test GGML_MACHINE_SUPPORTS_i8mm
-- Performing Test GGML_MACHINE_SUPPORTS_i8mm - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_noi8mm
-- Performing Test GGML_MACHINE_SUPPORTS_noi8mm - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_sve
-- Performing Test GGML_MACHINE_SUPPORTS_sve - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nosve
-- Performing Test GGML_MACHINE_SUPPORTS_nosve - Success
-- Performing Test GGML_MACHINE_SUPPORTS_sme
-- Performing Test GGML_MACHINE_SUPPORTS_sme - Failed
-- Performing Test GGML_MACHINE_SUPPORTS_nosme
-- Performing Test GGML_MACHINE_SUPPORTS_nosme - Failed
-- ARM feature FMA enabled
-- Adding CPU backend variant ggml-cpu: -mcpu=cortex-a57+crypto+nodotprod+nosve
-- Found CUDAToolkit: /usr/local/cuda/include (found version "10.2.300")
-- CUDA Toolkit found
-- Using CUDA architectures: 53
-- The CUDA compiler identification is NVIDIA 10.2.300
-- Detecting CUDA compiler ABI info
-- Detecting CUDA compiler ABI info - done
-- Check for working CUDA compiler: /usr/local/cuda/bin/nvcc - skipped
-- Detecting CUDA compile features
-- Detecting CUDA compile features - done
-- CUDA host compiler is GNU 8.4.0

-- Including CUDA backend
-- Looking for pthread_create in pthreads
-- Looking for pthread_create in pthreads - not found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - found
-- Configuring done (12.8s)
-- Generating done (0.6s)
-- Build files have been written to: /mnt/llm/builds/llama.cpp

# important lines are 
-- Found CUDAToolkit: /usr/local/cuda/include (found version "10.2.300")
-- Using CUDA architectures: 53
-- The CUDA compiler identification is NVIDIA 10.2.300
-- Check for working CUDA compiler: /usr/local/cuda/bin/nvcc - skipped
-- CUDA host compiler is GNU 8.4.0
-- Including CUDA backend
-- Configuring done
-- Generating done
-- Build files have been written to: /mnt/llm/builds/llama.cpp

CUDA compiler detection/configuration stage successfull 


# Check the generated configuration
CUDA                 10.2.300
CUDA architecture   53
CUDA standard       C++14
CUDA host compiler  g++-8
C++ compiler        g++-8
GGML_CUDA           ON

/mnt/llm → 55 GB free
/        → 2.6 GB free

# Build llama.cpp

jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ ls -lh /tmp/ggml-cpu-quants-test.o
-rw-rw-r-- 1 jetauto jetauto 71K Aug 23 00:59 /tmp/ggml-cpu-quants-test.o
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ file /tmp/ggml-cpu-quants-test.o
/tmp/ggml-cpu-quants-test.o: ELF 64-bit LSB relocatable, ARM aarch64, version 1 (SYSV), not stripped
jetauto@jetauto-desktop:/mnt/llm/llama.cpp/llama5050gpu.cpp$ cd /mnt/llm/builds/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/builds/llama.cpp$ cmake --build . --target ggml-cpu -- -j2
[ 16%] Building C object ggml/src/CMakeFiles/ggml-base.dir/ggml-quants.c.o
[ 16%] Linking CXX shared library ../../bin/libggml-base.so
[ 33%] Built target ggml-base
[ 33%] Building CXX object ggml/src/CMakeFiles/ggml-cpu.dir/ggml-cpu/ggml-cpu.cpp.o
[ 50%] Building C object ggml/src/CMakeFiles/ggml-cpu.dir/ggml-cpu/ggml-cpu.c.o
[ 50%] Building CXX object ggml/src/CMakeFiles/ggml-cpu.dir/ggml-cpu/ggml-cpu-aarch64.cpp.o
[ 50%] Building C object ggml/src/CMakeFiles/ggml-cpu.dir/ggml-cpu/ggml-cpu-quants.c.o
[ 50%] Building CXX object ggml/src/CMakeFiles/ggml-cpu.dir/ggml-cpu/ggml-cpu-traits.cpp.o
[ 66%] Building CXX object ggml/src/CMakeFiles/ggml-cpu.dir/ggml-cpu/amx/amx.cpp.o
[ 66%] Building CXX object ggml/src/CMakeFiles/ggml-cpu.dir/ggml-cpu/amx/mmq.cpp.o
[ 66%] Building CXX object ggml/src/CMakeFiles/ggml-cpu.dir/ggml-cpu/binary-ops.cpp.o
[ 83%] Building CXX object ggml/src/CMakeFiles/ggml-cpu.dir/ggml-cpu/unary-ops.cpp.o
[ 83%] Building CXX object ggml/src/CMakeFiles/ggml-cpu.dir/ggml-cpu/llamafile/sgemm.cpp.o
[ 83%] Linking CXX shared library ../../bin/libggml-cpu.so
[100%] Built target ggml-cpu
jetauto@jetauto-desktop:/mnt/llm/builds/llama.cpp$ cmake --build . -- -j2
[  0%] Generating build details from Git
[  2%] Built target ggml-base
-- Found Git: /usr/bin/git (found version "2.17.1")
[  3%] Built target sha256
[  4%] Built target xxhash
[  4%] Built target sha1
[  4%] Generating build details from Git
-- Found Git: /usr/bin/git (found version "2.17.1")
[  4%] Linking CUDA shared library ../../../bin/libggml-cuda.so
[  4%] Built target build_info
[  8%] Built target ggml-cpu
[ 37%] Built target ggml-cuda
[ 37%] Building CXX object ggml/src/CMakeFiles/ggml.dir/ggml-backend-reg.cpp.o
[ 38%] Linking CXX shared library ../../bin/libggml.so
[ 38%] Built target ggml
[ 38%] Building CXX object examples/gguf-hash/CMakeFiles/llama-gguf-hash.dir/gguf-hash.cpp.o
[ 38%] Building CXX object src/CMakeFiles/llama.dir/llama.cpp.o
[ 39%] Linking CXX executable ../../bin/llama-gguf-hash
[ 39%] Built target llama-gguf-hash
[ 40%] Building CXX object src/CMakeFiles/llama.dir/llama-adapter.cpp.o
[ 41%] Building CXX object examples/gguf/CMakeFiles/llama-gguf.dir/gguf.cpp.o
[ 41%] Linking CXX executable ../../bin/llama-gguf
[ 41%] Built target llama-gguf
[ 41%] Building CXX object src/CMakeFiles/llama.dir/llama-arch.cpp.o
[ 41%] Building CXX object src/CMakeFiles/llama.dir/llama-batch.cpp.o
[ 42%] Building CXX object src/CMakeFiles/llama.dir/llama-chat.cpp.o
[ 42%] Building CXX object src/CMakeFiles/llama.dir/llama-context.cpp.o
[ 42%] Building CXX object src/CMakeFiles/llama.dir/llama-grammar.cpp.o
[ 43%] Building CXX object src/CMakeFiles/llama.dir/llama-graph.cpp.o
[ 43%] Building CXX object src/CMakeFiles/llama.dir/llama-hparams.cpp.o
[ 43%] Building CXX object src/CMakeFiles/llama.dir/llama-impl.cpp.o
[ 44%] Building CXX object src/CMakeFiles/llama.dir/llama-io.cpp.o
[ 44%] Building CXX object src/CMakeFiles/llama.dir/llama-kv-cache.cpp.o
[ 44%] Building CXX object src/CMakeFiles/llama.dir/llama-memory.cpp.o
[ 45%] Building CXX object src/CMakeFiles/llama.dir/llama-mmap.cpp.o
[ 45%] Building CXX object src/CMakeFiles/llama.dir/llama-model-loader.cpp.o
[ 45%] Building CXX object src/CMakeFiles/llama.dir/llama-model.cpp.o
[ 46%] Building CXX object src/CMakeFiles/llama.dir/llama-quant.cpp.o
[ 46%] Building CXX object src/CMakeFiles/llama.dir/llama-sampling.cpp.o
[ 46%] Building CXX object src/CMakeFiles/llama.dir/llama-vocab.cpp.o
[ 47%] Building CXX object src/CMakeFiles/llama.dir/unicode-data.cpp.o
[ 47%] Building CXX object src/CMakeFiles/llama.dir/unicode.cpp.o
[ 47%] Linking CXX shared library ../bin/libllama.so
[ 47%] Built target llama
[ 48%] Building CXX object common/CMakeFiles/common.dir/arg.cpp.o
[ 48%] Building C object tests/CMakeFiles/test-c.dir/test-c.c.o
[ 48%] Linking C executable ../bin/test-c
[ 48%] Built target test-c
[ 48%] Building CXX object common/CMakeFiles/common.dir/chat.cpp.o
[ 48%] Building CXX object common/CMakeFiles/common.dir/common.cpp.o
[ 48%] Building CXX object examples/simple/CMakeFiles/llama-simple.dir/simple.cpp.o
[ 49%] Linking CXX executable ../../bin/llama-simple
[ 49%] Built target llama-simple
[ 50%] Building CXX object common/CMakeFiles/common.dir/console.cpp.o
[ 50%] Building CXX object examples/simple-chat/CMakeFiles/llama-simple-chat.dir/simple-chat.cpp.o
[ 50%] Linking CXX executable ../../bin/llama-simple-chat
[ 50%] Built target llama-simple-chat
[ 50%] Building CXX object common/CMakeFiles/common.dir/json-schema-to-grammar.cpp.o
[ 50%] Building CXX object examples/quantize-stats/CMakeFiles/llama-quantize-stats.dir/quantize-stats.cpp.o
[ 51%] Linking CXX executable ../../bin/llama-quantize-stats
[ 51%] Built target llama-quantize-stats
[ 51%] Building CXX object common/CMakeFiles/common.dir/llguidance.cpp.o
[ 51%] Building CXX object examples/llava/CMakeFiles/llava.dir/llava.cpp.o
[ 51%] Building CXX object examples/llava/CMakeFiles/llava.dir/clip.cpp.o
[ 52%] Building CXX object common/CMakeFiles/common.dir/log.cpp.o
[ 52%] Building CXX object common/CMakeFiles/common.dir/ngram-cache.cpp.o
[ 52%] Building CXX object common/CMakeFiles/common.dir/sampling.cpp.o
[ 53%] Building CXX object common/CMakeFiles/common.dir/speculative.cpp.o
[ 53%] Linking CXX static library libcommon.a
[ 53%] Built target common
[ 54%] Building CXX object tests/CMakeFiles/test-tokenizer-0.dir/test-tokenizer-0.cpp.o
[ 54%] Linking CXX executable ../bin/test-tokenizer-0
[ 54%] Built target test-tokenizer-0
[ 55%] Building CXX object tests/CMakeFiles/test-sampling.dir/test-sampling.cpp.o
[ 55%] Building CXX object tests/CMakeFiles/test-sampling.dir/get-model.cpp.o
[ 55%] Linking CXX executable ../bin/test-sampling
[ 55%] Built target test-sampling
[ 56%] Building CXX object tests/CMakeFiles/test-grammar-parser.dir/test-grammar-parser.cpp.o
[ 56%] Building CXX object tests/CMakeFiles/test-grammar-parser.dir/get-model.cpp.o
[ 56%] Linking CXX executable ../bin/test-grammar-parser
[ 56%] Built target test-grammar-parser
[ 57%] Building CXX object tests/CMakeFiles/test-grammar-integration.dir/test-grammar-integration.cpp.o
[ 57%] Built target llava
[ 57%] Building CXX object tests/CMakeFiles/test-grammar-integration.dir/get-model.cpp.o
[ 58%] Building CXX object tests/CMakeFiles/test-llama-grammar.dir/test-llama-grammar.cpp.o
[ 58%] Building CXX object tests/CMakeFiles/test-llama-grammar.dir/get-model.cpp.o
[ 58%] Linking CXX executable ../bin/test-llama-grammar
[ 58%] Built target test-llama-grammar
[ 59%] Building CXX object tests/CMakeFiles/test-chat.dir/test-chat.cpp.o
[ 59%] Linking CXX executable ../bin/test-grammar-integration
[ 59%] Built target test-grammar-integration
[ 59%] Building CXX object tests/CMakeFiles/test-chat.dir/get-model.cpp.o
[ 60%] Building CXX object tests/CMakeFiles/test-json-schema-to-grammar.dir/test-json-schema-to-grammar.cpp.o
[ 60%] Building CXX object tests/CMakeFiles/test-json-schema-to-grammar.dir/get-model.cpp.o
[ 60%] Linking CXX executable ../bin/test-json-schema-to-grammar
[ 60%] Built target test-json-schema-to-grammar
[ 60%] Building CXX object tests/CMakeFiles/test-tokenizer-1-bpe.dir/test-tokenizer-1-bpe.cpp.o
[ 60%] Linking CXX executable ../bin/test-chat
[ 60%] Built target test-chat
[ 60%] Building CXX object tests/CMakeFiles/test-tokenizer-1-spm.dir/test-tokenizer-1-spm.cpp.o
[ 61%] Linking CXX executable ../bin/test-tokenizer-1-bpe
[ 61%] Built target test-tokenizer-1-bpe
[ 62%] Building CXX object tests/CMakeFiles/test-log.dir/test-log.cpp.o
[ 62%] Building CXX object tests/CMakeFiles/test-log.dir/get-model.cpp.o
[ 62%] Linking CXX executable ../bin/test-log
[ 62%] Built target test-log
[ 62%] Building CXX object tests/CMakeFiles/test-arg-parser.dir/test-arg-parser.cpp.o
[ 62%] Linking CXX executable ../bin/test-tokenizer-1-spm
[ 62%] Built target test-tokenizer-1-spm
[ 63%] Building CXX object tests/CMakeFiles/test-chat-template.dir/test-chat-template.cpp.o
[ 63%] Building CXX object tests/CMakeFiles/test-arg-parser.dir/get-model.cpp.o
[ 64%] Linking CXX executable ../bin/test-arg-parser
[ 64%] Built target test-arg-parser
[ 64%] Building CXX object tests/CMakeFiles/test-chat-template.dir/get-model.cpp.o
[ 65%] Building CXX object tests/CMakeFiles/test-gguf.dir/test-gguf.cpp.o
[ 65%] Linking CXX executable ../bin/test-chat-template
[ 65%] Built target test-chat-template
[ 65%] Building CXX object tests/CMakeFiles/test-gguf.dir/get-model.cpp.o
[ 65%] Building CXX object tests/CMakeFiles/test-backend-ops.dir/test-backend-ops.cpp.o
[ 65%] Linking CXX executable ../bin/test-gguf
[ 65%] Built target test-gguf
[ 65%] Building CXX object tests/CMakeFiles/test-backend-ops.dir/get-model.cpp.o
[ 66%] Building CXX object tests/CMakeFiles/test-model-load-cancel.dir/test-model-load-cancel.cpp.o
[ 66%] Building CXX object tests/CMakeFiles/test-model-load-cancel.dir/get-model.cpp.o
[ 66%] Linking CXX executable ../bin/test-model-load-cancel
[ 66%] Built target test-model-load-cancel
[ 66%] Building CXX object tests/CMakeFiles/test-autorelease.dir/test-autorelease.cpp.o
[ 66%] Building CXX object tests/CMakeFiles/test-autorelease.dir/get-model.cpp.o
[ 67%] Linking CXX executable ../bin/test-autorelease
[ 67%] Built target test-autorelease
[ 67%] Building CXX object tests/CMakeFiles/test-barrier.dir/test-barrier.cpp.o
[ 67%] Building CXX object tests/CMakeFiles/test-barrier.dir/get-model.cpp.o
[ 68%] Linking CXX executable ../bin/test-barrier
[ 68%] Built target test-barrier
[ 69%] Building CXX object tests/CMakeFiles/test-quantize-fns.dir/test-quantize-fns.cpp.o
[ 69%] Building CXX object tests/CMakeFiles/test-quantize-fns.dir/get-model.cpp.o
[ 69%] Linking CXX executable ../bin/test-quantize-fns
[ 69%] Built target test-quantize-fns
[ 70%] Building CXX object tests/CMakeFiles/test-quantize-perf.dir/test-quantize-perf.cpp.o
[ 70%] Building CXX object tests/CMakeFiles/test-quantize-perf.dir/get-model.cpp.o
[ 70%] Linking CXX executable ../bin/test-quantize-perf
[ 70%] Built target test-quantize-perf
[ 71%] Building CXX object tests/CMakeFiles/test-rope.dir/test-rope.cpp.o
[ 71%] Building CXX object tests/CMakeFiles/test-rope.dir/get-model.cpp.o
[ 71%] Linking CXX executable ../bin/test-rope
[ 71%] Built target test-rope
[ 71%] Building CXX object examples/batched-bench/CMakeFiles/llama-batched-bench.dir/batched-bench.cpp.o
[ 72%] Linking CXX executable ../../bin/llama-batched-bench
[ 72%] Built target llama-batched-bench
[ 73%] Building CXX object examples/batched/CMakeFiles/llama-batched.dir/batched.cpp.o
[ 73%] Linking CXX executable ../../bin/llama-batched
[ 73%] Built target llama-batched
[ 74%] Building CXX object examples/embedding/CMakeFiles/llama-embedding.dir/embedding.cpp.o
[ 74%] Linking CXX executable ../../bin/llama-embedding
[ 74%] Built target llama-embedding
[ 74%] Building CXX object examples/eval-callback/CMakeFiles/llama-eval-callback.dir/eval-callback.cpp.o
[ 75%] Linking CXX executable ../../bin/llama-eval-callback
[ 75%] Built target llama-eval-callback
[ 76%] Building CXX object examples/gbnf-validator/CMakeFiles/llama-gbnf-validator.dir/gbnf-validator.cpp.o
[ 76%] Linking CXX executable ../../bin/llama-gbnf-validator
[ 76%] Built target llama-gbnf-validator
[ 76%] Building CXX object examples/gguf-split/CMakeFiles/llama-gguf-split.dir/gguf-split.cpp.o
[ 77%] Linking CXX executable ../bin/test-backend-ops
[ 77%] Linking CXX executable ../../bin/llama-gguf-split
[ 77%] Built target test-backend-ops
[ 78%] Building CXX object examples/gritlm/CMakeFiles/llama-gritlm.dir/gritlm.cpp.o
[ 78%] Built target llama-gguf-split
[ 78%] Building CXX object examples/imatrix/CMakeFiles/llama-imatrix.dir/imatrix.cpp.o
[ 78%] Linking CXX executable ../../bin/llama-gritlm
[ 78%] Built target llama-gritlm
[ 78%] Building CXX object examples/infill/CMakeFiles/llama-infill.dir/infill.cpp.o
[ 78%] Linking CXX executable ../../bin/llama-infill
[ 78%] Built target llama-infill
[ 78%] Building CXX object examples/llama-bench/CMakeFiles/llama-bench.dir/llama-bench.cpp.o
[ 79%] Linking CXX executable ../../bin/llama-imatrix
[ 79%] Built target llama-imatrix
[ 79%] Building CXX object examples/lookahead/CMakeFiles/llama-lookahead.dir/lookahead.cpp.o
[ 79%] Linking CXX executable ../../bin/llama-lookahead
[ 79%] Built target llama-lookahead
[ 80%] Building CXX object examples/lookup/CMakeFiles/llama-lookup.dir/lookup.cpp.o
[ 80%] Linking CXX executable ../../bin/llama-lookup
[ 80%] Built target llama-lookup
[ 80%] Building CXX object examples/lookup/CMakeFiles/llama-lookup-create.dir/lookup-create.cpp.o
[ 81%] Linking CXX executable ../../bin/llama-lookup-create
[ 81%] Built target llama-lookup-create
[ 81%] Building CXX object examples/lookup/CMakeFiles/llama-lookup-merge.dir/lookup-merge.cpp.o
[ 81%] Linking CXX executable ../../bin/llama-lookup-merge
[ 81%] Built target llama-lookup-merge
[ 82%] Building CXX object examples/lookup/CMakeFiles/llama-lookup-stats.dir/lookup-stats.cpp.o
[ 82%] Linking CXX executable ../../bin/llama-lookup-stats
[ 82%] Built target llama-lookup-stats
[ 83%] Building CXX object examples/main/CMakeFiles/llama-cli.dir/main.cpp.o
[ 83%] Linking CXX executable ../../bin/llama-bench
[ 83%] Built target llama-bench
[ 83%] Building CXX object examples/parallel/CMakeFiles/llama-parallel.dir/parallel.cpp.o
[ 83%] Linking CXX executable ../../bin/llama-cli
[ 83%] Built target llama-cli
[ 84%] Building CXX object examples/passkey/CMakeFiles/llama-passkey.dir/passkey.cpp.o
[ 84%] Linking CXX executable ../../bin/llama-parallel
[ 84%] Built target llama-parallel
[ 84%] Building CXX object examples/perplexity/CMakeFiles/llama-perplexity.dir/perplexity.cpp.o
[ 84%] Linking CXX executable ../../bin/llama-passkey
[ 84%] Built target llama-passkey
[ 85%] Building CXX object examples/quantize/CMakeFiles/llama-quantize.dir/quantize.cpp.o
[ 85%] Linking CXX executable ../../bin/llama-quantize
[ 85%] Built target llama-quantize
[ 86%] Building CXX object examples/retrieval/CMakeFiles/llama-retrieval.dir/retrieval.cpp.o
[ 87%] Linking CXX executable ../../bin/llama-perplexity
[ 87%] Built target llama-perplexity
[ 87%] Generating loading.html.hpp
[ 87%] Generating index.html.gz.hpp
[ 87%] Linking CXX executable ../../bin/llama-retrieval
[ 87%] Built target llama-retrieval
[ 87%] Building CXX object examples/save-load-state/CMakeFiles/llama-save-load-state.dir/save-load-state.cpp.o
[ 88%] Building CXX object examples/server/CMakeFiles/llama-server.dir/server.cpp.o
[ 89%] Linking CXX executable ../../bin/llama-save-load-state
[ 89%] Built target llama-save-load-state
[ 89%] Building CXX object examples/run/CMakeFiles/llama-run.dir/run.cpp.o
[ 90%] Building CXX object examples/run/CMakeFiles/llama-run.dir/linenoise.cpp/linenoise.cpp.o
/mnt/llm/llama.cpp/llama5050gpu.cpp/examples/run/linenoise.cpp/linenoise.cpp: In function ‘size_t defaultNextCharLen(const char*, size_t, size_t, size_t*)’:
/mnt/llm/llama.cpp/llama5050gpu.cpp/examples/run/linenoise.cpp/linenoise.cpp:624:29: warning: ‘cp’ may be used uninitialized in this function [-Wmaybe-uninitialized]
         if (!isCombiningChar(cp)) {
              ~~~~~~~~~~~~~~~^~~~
/mnt/llm/llama.cpp/llama5050gpu.cpp/examples/run/linenoise.cpp/linenoise.cpp: In function ‘size_t defaultPrevCharLen(const char*, size_t, size_t, size_t*)’:
/mnt/llm/llama.cpp/llama5050gpu.cpp/examples/run/linenoise.cpp/linenoise.cpp:597:29: warning: ‘cp’ may be used uninitialized in this function [-Wmaybe-uninitialized]
         if (!isCombiningChar(cp)) {
              ~~~~~~~~~~~~~~~^~~~
[ 90%] Linking CXX executable ../../bin/llama-run
[ 90%] Built target llama-run
[ 91%] Building CXX object examples/speculative/CMakeFiles/llama-speculative.dir/speculative.cpp.o
[ 91%] Linking CXX executable ../../bin/llama-speculative
[ 91%] Built target llama-speculative
[ 91%] Building CXX object examples/speculative-simple/CMakeFiles/llama-speculative-simple.dir/speculative-simple.cpp.o
[ 92%] Linking CXX executable ../../bin/llama-speculative-simple
[ 92%] Built target llama-speculative-simple
[ 92%] Building CXX object examples/tokenize/CMakeFiles/llama-tokenize.dir/tokenize.cpp.o
[ 92%] Linking CXX executable ../../bin/llama-tokenize
[ 92%] Built target llama-tokenize
[ 93%] Building CXX object examples/tts/CMakeFiles/llama-tts.dir/tts.cpp.o
[ 93%] Linking CXX executable ../../bin/llama-tts
[ 93%] Built target llama-tts
[ 93%] Building CXX object examples/gen-docs/CMakeFiles/llama-gen-docs.dir/gen-docs.cpp.o
[ 93%] Linking CXX executable ../../bin/llama-gen-docs
[ 93%] Built target llama-gen-docs
[ 93%] Building CXX object examples/convert-llama2c-to-ggml/CMakeFiles/llama-convert-llama2c-to-ggml.dir/convert-llama2c-to-ggml.cpp.o
[ 94%] Linking CXX executable ../../bin/llama-convert-llama2c-to-ggml
[ 94%] Built target llama-convert-llama2c-to-ggml
[ 94%] Building CXX object examples/cvector-generator/CMakeFiles/llama-cvector-generator.dir/cvector-generator.cpp.o
[ 94%] Linking CXX executable ../../bin/llama-cvector-generator
[ 94%] Built target llama-cvector-generator
[ 94%] Building CXX object examples/export-lora/CMakeFiles/llama-export-lora.dir/export-lora.cpp.o
[ 94%] Linking CXX executable ../../bin/llama-export-lora
[ 94%] Built target llama-export-lora
[ 94%] Linking CXX static library libllava_static.a
[ 94%] Built target llava_static
[ 95%] Linking CXX shared library ../../bin/libllava_shared.so
[ 95%] Built target llava_shared
[ 96%] Building CXX object examples/llava/CMakeFiles/llama-llava-cli.dir/llava-cli.cpp.o
[ 96%] Linking CXX executable ../../bin/llama-llava-cli
[ 96%] Built target llama-llava-cli
[ 96%] Building CXX object examples/llava/CMakeFiles/llama-minicpmv-cli.dir/minicpmv-cli.cpp.o
[ 96%] Linking CXX executable ../../bin/llama-server
[ 97%] Linking CXX executable ../../bin/llama-minicpmv-cli
[ 97%] Built target llama-minicpmv-cli
[ 97%] Built target llama-server
[ 97%] Building CXX object examples/llava/CMakeFiles/llama-gemma3-cli.dir/gemma3-cli.cpp.o
[ 97%] Building CXX object examples/llava/CMakeFiles/llama-qwen2vl-cli.dir/qwen2vl-cli.cpp.o
[ 98%] Linking CXX executable ../../bin/llama-gemma3-cli
[ 98%] Built target llama-gemma3-cli
[ 98%] Building CXX object examples/llava/CMakeFiles/llama-llava-clip-quantize-cli.dir/clip-quantize-cli.cpp.o
[ 98%] Linking CXX executable ../../bin/llama-qwen2vl-cli
[ 98%] Built target llama-qwen2vl-cli
[ 98%] Building CXX object pocs/vdot/CMakeFiles/llama-vdot.dir/vdot.cpp.o
[ 99%] Linking CXX executable ../../bin/llama-llava-clip-quantize-cli
[ 99%] Built target llama-llava-clip-quantize-cli
[ 99%] Building CXX object pocs/vdot/CMakeFiles/llama-q8dot.dir/q8dot.cpp.o
[100%] Linking CXX executable ../../bin/llama-vdot
[100%] Built target llama-vdot
[100%] Linking CXX executable ../../bin/llama-q8dot
[100%] Built target llama-q8dot
jetauto@jetauto-desktop:/mnt/llm/builds/llama.cpp$

---
[100%] Built target llama-vdot
[100%] Built target llama-q8dot

```
GCC 8 intrinsic error
        ↓
GCC-8 compatibility fix
        ↓
ggml-cpu test compilation ✅
        ↓
ggml-cpu target ✅
        ↓
FULL llama.cpp build ✅
```

bin/llama-cli          1.7M
bin/libggml-cpu.so    521K
```
libggml.so
libggml-base.so
libggml-cpu.so
libggml-cuda.so
libgomp.so.1
```

llama-cli is therefore loading both CPU and CUDA GGML backends:

CPU  → libggml-cpu.so
CUDA → libggml-cuda.so

jetauto@jetauto-desktop:/mnt/llm/builds/llama.cpp$ bin/llama-cli --list-devices
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA Tegra X1, compute capability 5.3, VMM: no
Available devices:
  CUDA0: NVIDIA Tegra X1 (3963 MiB, 1330 MiB free)

```
Component	Status
CPU	AArch64
Compiler	GCC 8.4.0
CPU backend	✅ ON
AArch64 CPU backend	✅ ON
CUDA backend	✅ ON
CUDA compiler	/usr/local/cuda/bin/nvcc
CUDA architecture	53
CUDA device	Tegra X1
CUDA memory detected	~3.96 GB
CUDA FA	ON
CUDA graphs	ON
llama.cpp	v5050

Most importantly:

CMAKE_CUDA_ARCHITECTURES=53
GGML_CUDA:BOOL=ON
GGML_CPU_AARCH64:BOOL=ON
```

mkdir -p /mnt/llm/models
cd /mnt/llm/models


Download Qwen2.5 1.5B Q4_K_M
wget -O qwen2.5-1.5b-instruct-q4_k_m.gguf \
https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf

verify 
ls -lh /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf

file /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf

du -h /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf

Then we run it

cd /mnt/llm/builds/llama.cpp

bin/llama-cli \
  -m /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf \
  -ngl 99 \
  -c 2048 \
  -p "You are the AI assistant running on a JetAuto robot. Explain what a LiDAR sensor does in one short paragraph."

  Qwen2.5 1.5B
       ↓
GGUF
       ↓
llama.cpp
       ↓
CUDA / Tegra X1
       ↓
response

Once that works, then we move to the interesting part:

LLM
 ↓
ROS interface
 ↓
LiDAR + camera state
 ↓
decision
 ↓
JetAuto action

DONE

HTTP request sent, awaiting response... 206 Partial Content
Length: 1117320736 (1.0G), 821437338 (783M) remaining [application/octet-stream]
Saving to: ‘qwen2.5-1.5b-instruct-q4_k_m.gguf’

qwen2.5-1.5b-in 100%[++=====>]   1.04G  3.03MB/s    in 5m 27s

2026-08-23 03:50:28 (2.39 MB/s) - ‘qwen2.5-1.5b-instruct-q4_k_m.gguf’ saved [1117320736/1117320736]

```
jetauto@jetauto-desktop:/mnt/llm/models$ wget -c -O qwen2.5-1.5b-instruct-q4_k_m.gguf \
> https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
--2026-08-23 03:44:59--  https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf
Resolving huggingface.co (huggingface.co)... 13.225.5.100, 13.225.5.30, 13.225.5.26, ...
Connecting to huggingface.co (huggingface.co)|13.225.5.100|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://us.aws.cdn.hf.co/xet-bridge-us/66e98ae0be5913b903da60c1/6ca5463cf24c16cd56d7ad7461524d813b07b3f29889b2fbdbb8286a7e97a14a?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27qwen2.5-1.5b-instruct-q4_k_m.gguf%3B+filename%3D%22qwen2.5-1.5b-instruct-q4_k_m.gguf%22%3B&user_id=public&X-Xet-Cas-Uid=public&Expires=1787440499&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly91cy5hd3MuY2RuLmhmLmNvL3hldC1icmlkZ2UtdXMvNjZlOThhZTBiZTU5MTNiOTAzZGE2MGMxLzZjYTU0NjNjZjI0YzE2Y2Q1NmQ3YWQ3NDYxNTI0ZDgxM2IwN2IzZjI5ODg5YjJmYmRiYjgyODZhN2U5N2ExNGFcXD9yZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPWlubGluZSUzQitmaWxlbmFtZSUyQSUzRFVURi04JTI3JTI3cXdlbjIuNS0xLjViLWluc3RydWN0LXE0X2tfbS5nZ3VmJTNCK2ZpbGVuYW1lJTNEJTIycXdlbjIuNS0xLjViLWluc3RydWN0LXE0X2tfbS5nZ3VmJTIyJTNCJnVzZXJfaWQ9cHVibGljJlgtWGV0LUNhcy1VaWQ9cHVibGljIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJFcG9jaFRpbWUiOjE3ODc0NDA0OTl9fX1dfQ__&Signature=MEYCIQCi57NXhZI2OzHqZPUStSL9g3hzoIa2E9Ve%7E1HhkLFbagIhAIK4fk7oaLiC4YyyDk07lEi4M6SYj4rBUMpzmiDtHFUf&Key-Pair-Id=01KXEF4KZ1B6FV465MAWR4M21F [following]
--2026-08-23 03:45:00--  https://us.aws.cdn.hf.co/xet-bridge-us/66e98ae0be5913b903da60c1/6ca5463cf24c16cd56d7ad7461524d813b07b3f29889b2fbdbb8286a7e97a14a?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27qwen2.5-1.5b-instruct-q4_k_m.gguf%3B+filename%3D%22qwen2.5-1.5b-instruct-q4_k_m.gguf%22%3B&user_id=public&X-Xet-Cas-Uid=public&Expires=1787440499&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly91cy5hd3MuY2RuLmhmLmNvL3hldC1icmlkZ2UtdXMvNjZlOThhZTBiZTU5MTNiOTAzZGE2MGMxLzZjYTU0NjNjZjI0YzE2Y2Q1NmQ3YWQ3NDYxNTI0ZDgxM2IwN2IzZjI5ODg5YjJmYmRiYjgyODZhN2U5N2ExNGFcXD9yZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPWlubGluZSUzQitmaWxlbmFtZSUyQSUzRFVURi04JTI3JTI3cXdlbjIuNS0xLjViLWluc3RydWN0LXE0X2tfbS5nZ3VmJTNCK2ZpbGVuYW1lJTNEJTIycXdlbjIuNS0xLjViLWluc3RydWN0LXE0X2tfbS5nZ3VmJTIyJTNCJnVzZXJfaWQ9cHVibGljJlgtWGV0LUNhcy1VaWQ9cHVibGljIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJFcG9jaFRpbWUiOjE3ODc0NDA0OTl9fX1dfQ__&Signature=MEYCIQCi57NXhZI2OzHqZPUStSL9g3hzoIa2E9Ve%7E1HhkLFbagIhAIK4fk7oaLiC4YyyDk07lEi4M6SYj4rBUMpzmiDtHFUf&Key-Pair-Id=01KXEF4KZ1B6FV465MAWR4M21F
Resolving us.aws.cdn.hf.co (us.aws.cdn.hf.co)... 54.169.134.11, 13.215.180.201, 13.214.85.108, ...
Connecting to us.aws.cdn.hf.co (us.aws.cdn.hf.co)|54.169.134.11|:443... connected.
HTTP request sent, awaiting response... 206 Partial Content
Length: 1117320736 (1.0G), 821437338 (783M) remaining [application/octet-stream]
Saving to: ‘qwen2.5-1.5b-instruct-q4_k_m.gguf’

qwen2.5-1.5b-in 100%[++=====>]   1.04G  3.03MB/s    in 5m 27s

2026-08-23 03:50:28 (2.39 MB/s) - ‘qwen2.5-1.5b-instruct-q4_k_m.gguf’ saved [1117320736/1117320736]

jetauto@jetauto-desktop:/mnt/llm/models$ ls -lh /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf
-rw-rw-r-- 1 jetauto jetauto 1.1G Aug 23 03:50 /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf
jetauto@jetauto-desktop:/mnt/llm/models$ file /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf
/mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf: data
jetauto@jetauto-desktop:/mnt/llm/models$ du -h /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf
1.1G    /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf
jetauto@jetauto-desktop:/mnt/llm/models$ cd /mnt/llm/builds/llama.cpp
jetauto@jetauto-desktop:/mnt/llm/builds/llama.cpp$
jetauto@jetauto-desktop:/mnt/llm/builds/llama.cpp$ bin/llama-cli \
>   -m /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf \
>   -ngl 99 \
>   -c 2048 \
>   -p "You are the AI assistant running on a JetAuto robot. Explain what a LiDAR sensor does in one short paragraph."
ggml_cuda_init: GGML_CUDA_FORCE_MMQ:    no
ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
ggml_cuda_init: found 1 CUDA devices:
  Device 0: NVIDIA Tegra X1, compute capability 5.3, VMM: no
build: 5050 (23106f94e) with gcc-8 (Ubuntu/Linaro 8.4.0-1ubuntu1~18.04) 8.4.0 for aarch64-linux-gnu
main: llama backend init
main: load the model and apply lora adapter, if any
llama_model_load_from_file_impl: using device CUDA0 (NVIDIA Tegra X1) - 505 MiB free
llama_model_loader: loaded meta data with 26 key-value pairs and 339 tensors from /mnt/llm/models/qwen2.5-1.5b-instruct-q4_k_m.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen2
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                               general.name str              = qwen2.5-1.5b-instruct
llama_model_loader: - kv   3:                            general.version str              = v0.1
llama_model_loader: - kv   4:                           general.finetune str              = qwen2.5-1.5b-instruct
llama_model_loader: - kv   5:                         general.size_label str              = 1.8B
llama_model_loader: - kv   6:                          qwen2.block_count u32              = 28
llama_model_loader: - kv   7:                       qwen2.context_length u32              = 32768
llama_model_loader: - kv   8:                     qwen2.embedding_length u32              = 1536
llama_model_loader: - kv   9:                  qwen2.feed_forward_length u32              = 8960
llama_model_loader: - kv  10:                 qwen2.attention.head_count u32              = 12
llama_model_loader: - kv  11:              qwen2.attention.head_count_kv u32              = 2
llama_model_loader: - kv  12:                       qwen2.rope.freq_base f32              = 1000000.000000
llama_model_loader: - kv  13:     qwen2.attention.layer_norm_rms_epsilon f32              = 0.000001
llama_model_loader: - kv  14:                          general.file_type u32              = 15
llama_model_loader: - kv  15:                       tokenizer.ggml.model str              = gpt2
llama_model_loader: - kv  16:                         tokenizer.ggml.pre str              = qwen2
llama_model_loader: - kv  17:                      tokenizer.ggml.tokens arr[str,151936]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  18:                  tokenizer.ggml.token_type arr[i32,151936]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  19:                      tokenizer.ggml.merges arr[str,151387]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "Ġ t",...
llama_model_loader: - kv  20:                tokenizer.ggml.eos_token_id u32              = 151645
llama_model_loader: - kv  21:            tokenizer.ggml.padding_token_id u32              = 151643
llama_model_loader: - kv  22:                tokenizer.ggml.bos_token_id u32              = 151643
llama_model_loader: - kv  23:               tokenizer.ggml.add_bos_token bool             = false
llama_model_loader: - kv  24:                    tokenizer.chat_template str              = {%- if tools %}\n    {{- '<|im_start|>...
llama_model_loader: - kv  25:               general.quantization_version u32              = 2
llama_model_loader: - type  f32:  141 tensors
llama_model_loader: - type q4_K:  169 tensors
llama_model_loader: - type q6_K:   29 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q4_K - Medium
print_info: file size   = 1.04 GiB (5.00 BPW)
load: special tokens cache size = 22
load: token to piece cache size = 0.9310 MB
print_info: arch             = qwen2
print_info: vocab_only       = 0
print_info: n_ctx_train      = 32768
print_info: n_embd           = 1536
print_info: n_layer          = 28
print_info: n_head           = 12
print_info: n_head_kv        = 2
print_info: n_rot            = 128
print_info: n_swa            = 0
print_info: n_swa_pattern    = 1
print_info: n_embd_head_k    = 128
print_info: n_embd_head_v    = 128
print_info: n_gqa            = 6
print_info: n_embd_k_gqa     = 256
print_info: n_embd_v_gqa     = 256
print_info: f_norm_eps       = 0.0e+00
print_info: f_norm_rms_eps   = 1.0e-06
print_info: f_clamp_kqv      = 0.0e+00
print_info: f_max_alibi_bias = 0.0e+00
print_info: f_logit_scale    = 0.0e+00
print_info: f_attn_scale     = 0.0e+00
print_info: n_ff             = 8960
print_info: n_expert         = 0
print_info: n_expert_used    = 0
print_info: causal attn      = 1
print_info: pooling type     = 0
print_info: rope type        = 2
print_info: rope scaling     = linear
print_info: freq_base_train  = 1000000.0
print_info: freq_scale_train = 1
print_info: n_ctx_orig_yarn  = 32768
print_info: rope_finetuned   = unknown
print_info: ssm_d_conv       = 0
print_info: ssm_d_inner      = 0
print_info: ssm_d_state      = 0
print_info: ssm_dt_rank      = 0
print_info: ssm_dt_b_c_rms   = 0
print_info: model type       = 1.5B
print_info: model params     = 1.78 B
print_info: general.name     = qwen2.5-1.5b-instruct
print_info: vocab type       = BPE
print_info: n_vocab          = 151936
print_info: n_merges         = 151387
print_info: BOS token        = 151643 '<|endoftext|>'
print_info: EOS token        = 151645 '<|im_end|>'
print_info: EOT token        = 151643 '<|endoftext|>'
print_info: PAD token        = 151643 '<|endoftext|>'
print_info: LF token         = 198 'Ċ'
print_info: FIM PRE token    = 151659 '<|fim_prefix|>'
print_info: FIM SUF token    = 151661 '<|fim_suffix|>'
print_info: FIM MID token    = 151660 '<|fim_middle|>'
print_info: FIM PAD token    = 151662 '<|fim_pad|>'
print_info: FIM REP token    = 151663 '<|repo_name|>'
print_info: FIM SEP token    = 151664 '<|file_sep|>'
print_info: EOG token        = 151643 '<|endoftext|>'
print_info: EOG token        = 151645 '<|im_end|>'
print_info: EOG token        = 151662 '<|fim_pad|>'
print_info: EOG token        = 151663 '<|repo_name|>'
print_info: EOG token        = 151664 '<|file_sep|>'
print_info: max token length = 256
load_tensors: loading model tensors, this can take a while... (mmap = true)
load_tensors: offloading 28 repeating layers to GPU
load_tensors: offloading output layer to GPU
load_tensors: offloaded 29/29 layers to GPU
load_tensors:        CUDA0 model buffer size =   934.70 MiB
load_tensors:   CPU_Mapped model buffer size =   125.19 MiB
.........................................................................
llama_context: constructing llama_context
llama_context: n_seq_max     = 1
llama_context: n_ctx         = 2048
llama_context: n_ctx_per_seq = 2048
llama_context: n_batch       = 2048
llama_context: n_ubatch      = 512
llama_context: causal_attn   = 1
llama_context: flash_attn    = 0
llama_context: freq_base     = 1000000.0
llama_context: freq_scale    = 1
llama_context: n_ctx_per_seq (2048) < n_ctx_train (32768) -- the full capacity of the model will not be utilized
llama_context:  CUDA_Host  output buffer size =     0.58 MiB
init: kv_size = 2048, offload = 1, type_k = 'f16', type_v = 'f16', n_layer = 28, can_shift = 1
init:      CUDA0 KV buffer size =    56.00 MiB
llama_context: KV self size  =   56.00 MiB, K (f16):   28.00 MiB, V (f16):   28.00 MiB
llama_context:      CUDA0 compute buffer size =   299.75 MiB
llama_context:  CUDA_Host compute buffer size =     7.01 MiB
llama_context: graph nodes  = 1042
llama_context: graph splits = 2
common_init_from_params: setting dry_penalty_last_n to ctx_size = 2048
common_init_from_params: warming up the model with an empty run - please wait ... (--no-warmup to disable)
main: llama threadpool init, n_threads = 4
main: chat template is available, enabling conversation mode (disable it with -no-cnv)
*** User-specified prompt will pre-start conversation, did you mean to set --system-prompt (-sys) instead?
main: chat template example:
<|im_start|>system
You are a helpful assistant<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there<|im_end|>
<|im_start|>user
How are you?<|im_end|>
<|im_start|>assistant


system_info: n_threads = 4 (n_threads_batch = 4) / 4 | CUDA : USE_GRAPHS = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : NEON = 1 | ARM_FMA = 1 | LLAMAFILE = 1 | OPENMP = 1 | AARCH64_REPACK = 1 |

main: interactive mode on.
sampler seed: 2138302536
sampler params:
        repeat_last_n = 64, repeat_penalty = 1.000, frequency_penalty = 0.000, presence_penalty = 0.000
        dry_multiplier = 0.000, dry_base = 1.750, dry_allowed_length = 2, dry_penalty_last_n = 2048
        top_k = 40, top_p = 0.950, min_p = 0.050, xtc_probability = 0.000, xtc_threshold = 0.100, typical_p = 1.000, top_n_sigma = -1.000, temp = 0.800
        mirostat = 0, mirostat_lr = 0.100, mirostat_ent = 5.000
sampler chain: logits -> logit-bias -> penalties -> dry -> top-k -> typical -> top-p -> min-p -> xtc -> temp-ext -> dist
generate: n_ctx = 2048, n_batch = 2048, n_predict = -1, n_keep = 0

== Running in interactive mode. ==
 - Press Ctrl+C to interject at any time.
 - Press Return to return control to the AI.
 - To return control without starting a new line, end your input with '/'.
 - If you want to submit another line, end your input with '\'.
 - Not using system message. To change it, set a different value via -sys PROMPT

system
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.
user
You are the AI assistant running on a JetAuto robot. Explain what a LiDAR sensor does in one short paragraph.
assistant
A LiDAR sensor emits light pulses or laser beams to measure distances to objects and create a 3D map of the environment around it.

>
llama_perf_sampler_print:    sampling time =      22.51 ms /    84 runs   (    0.27 ms per token,  3731.67 tokens per second)
llama_perf_context_print:        load time =  134035.02 ms
llama_perf_context_print: prompt eval time =    2776.77 ms /    54 tokens (   51.42 ms per token,    19.45 tokens per second)
llama_perf_context_print:        eval time =    7107.82 ms /    29 runs   (  245.10 ms per token,     4.08 tokens per second)
llama_perf_context_print:       total time =  526517.45 ms /    83 tokens
Interrupted by user
```

```
Jetson Nano
   ↓
Qwen 2.5 1.5B Q4_K_M
   ↓
llama.cpp
   ↓
CUDA0 — Tegra X1
   ↓
HTTP API :8081
   ↓
/health → {"status":"ok"} ✅
```

Next: test actual inference through the API

1. LLM
   ↓
2. LLM HTTP API
   ↓
3. Robot intelligence layer
   ↓
4. Connect ROS topics/sensors
   ↓
5. Give LLM structured sensor information
   ↓
6. LLM decides / interprets
   ↓
7. Robot executes safe predefined actions

   LiDAR
  ↓
/scan
  ↓
Perception / state extraction
  ↓
"Obstacle 0.6 m ahead"
  ↓
Qwen
  ↓
"Stop and turn left"
  ↓
ROS controller
  ↓
/cmd_vel
  ↓
JetAuto
