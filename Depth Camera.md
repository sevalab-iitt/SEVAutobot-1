# Object Tracking
<img width="896" height="329" alt="Screenshot 2026-07-09 124113" src="https://github.com/user-attachments/assets/e4ffa1d1-858f-431e-94a0-7eac720051ae" />

## 1. Stop the APP service

```bash
sudo systemctl stop start_app_node.service
```

## 2. Launch the body tracking node

```bash
roslaunch jetauto_example body_track.launch
```

## 3. Open a new terminal and navigate to the tracker script

```bash
cd ~/jetauto_ws/src/jetauto_example/scripts/tracker/
```

## 4. Run the Object Tracking program

```bash
python3 object_tracking.py
```

If your system uses Python 3 as the default interpreter:

```bash
python object_tracking.py
```

## 5. Stop the program

Press:

```text
Ctrl + C
```

## 6. Restart the APP service

```bash
sudo systemctl restart start_app_node.service
```

---

## Complete Workflow

```bash
sudo systemctl stop start_app_node.service

roslaunch jetauto_example body_track.launch
```

Open another terminal:

```bash
cd ~/jetauto_ws/src/jetauto_example/scripts/tracker/

python3 object_tracking.py
```

After finishing:

```bash
sudo systemctl restart start_app_node.service
```
# Somatosensory Control
<img width="896" height="329" alt="Screenshot 2026-07-09 124113" src="https://github.com/user-attachments/assets/853ec4de-2b08-4504-aa63-d0c9329cb2bf" />

This example enables JetAuto to recognize human body poses using MediaPipe and control the robot through body movements.

## 1. Stop the APP service

```bash
sudo systemctl stop start_app_node.service
```

## 2. Launch the Somatosensory Control node

```bash
roslaunch jetauto_example body_control.launch
```

## 3. Program Behavior

After the launch file starts successfully:

- The Astra Pro Plus depth camera is initialized.
- MediaPipe Pose is loaded for body pose estimation.
- The robot begins tracking the user's body movements.
- Move your body to control the robot according to the predefined gestures.

## 4. Stop the Program

Press:

```text
Ctrl + C
```

## 5. Restart the APP service

```bash
sudo systemctl restart start_app_node.service
```

---

## Complete Workflow

```bash
sudo systemctl stop start_app_node.service

roslaunch jetauto_example body_control.launch
```

When finished:

```bash
sudo systemctl restart start_app_node.service
```

---

## Notes

- Ensure the **Astra Pro Plus** camera is connected before launching the program.
- Stand approximately **1–3 meters** in front of the camera for reliable body pose detection.
- If MediaPipe displays the warning:

```text
Can't find file: mediapipe/modules/pose_detection/pose_detection.tflite
```

the program may still continue to run using the available TensorFlow Lite GPU delegate, but verify that the MediaPipe model files are correctly installed if body detection does not work.

- If you terminate the program using **Ctrl + C**, you may see an OpenCV shutdown exception similar to:

```text
OpenCV Error: (-215) tlsSlots.size() > slotIdx in function 'releaseSlot'
```

This is a known shutdown issue with OpenCV 3.x on some Jetson/ROS Melodic systems and generally occurs during program exit. It does not usually indicate a problem with the body control functionality.
