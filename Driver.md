#  What is a Driver in ROS?
In ROS, a driver is a Python or C++ node that:
##### • Talks directly to a hardware device (camera, LiDAR, motors, servos)
• Reads sensor data and publishes it to a ROS topic
• Receives ROS commands and sends them to the hardware
Every driver lives as a .py or .cpp file inside a ROS package under ~/jetauto_ws/src/.


Step 1 — SSH Into the Robot
1 # From your laptop
2 ssh jetauto@192 .168.1. xxx # replace xxx with robot IP
3 # password : hiwonder
4
5 # Source the workspace immediately
6 source ~/ jetauto_ws / devel / setup . bash
