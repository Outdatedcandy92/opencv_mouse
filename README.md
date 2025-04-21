# Hand Gesture Mouse Control

## Overview
This project uses **OpenCV**, **MediaPipe**, and **PyAutoGUI** to control the mouse pointer and simulate mouse clicks based on hand gestures detected through a webcam. It tracks the position of the index finger to move the mouse and uses gestures involving the index, middle, and ring fingers to perform mouse clicks and holds.
![Image](https://hc-cdn.hel1.your-objectstorage.com/s/v3/370bd274229ef0d69954e89d21f01ef59e489849_gif.gif)

## Features
1. **Mouse Movement**:
   - The mouse pointer moves based on the position of the index finger inside a red bounding box.
   - Movement is smoothed and scaled for responsiveness using DPI multipliers.

2. **Mouse Click**:
   - A left mouse click is triggered when the index and middle fingers are close together.

3. **Mouse Hold**:
   - A left mouse hold is triggered when the index, middle, and ring fingers are close together.
   - The hold is released when the fingers move apart.

4. **Customizable Settings**:
   - DPI multiplier for sensitivity.
   - Debounce timer for click responsiveness.
   - Movement smoothing and thresholds to reduce jitter.

---

## Requirements
- Python 3.7 or higher
- Libraries:
  - `opencv-python`
  - `mediapipe`
  - `pyautogui`

Install the required libraries using:
```bash
pip install opencv-python mediapipe pyautogui
```

## How to Run
1. clone the project
2. Run the script
```bash
python main.py
```
3. Change up the settings variables to your liking

## Usage
- Mouse Movement:
    - Move your index finger inside the red bounding box to control the mouse pointer.
- Mouse Click:
    - Bring your index and middle fingers close together to trigger a left mouse click.
- Mouse Hold:
    - Bring your index, middle, and ring fingers close together to hold the left mouse button.
    - Move the fingers apart to release the hold.
## Customization
You can modify the following variables in the script to suit your preferences:

- `camera_rotation`: Rotate the webcam feed (0, 90, 180, 270 degrees).
- `flip_camera`: Flip the webcam feed horizontally.
- `box_width` and `box_height`: Adjust the size of the red bounding box.
- `dpi_multiplier`: Increase or decrease mouse sensitivity.
- `click_delay`: Adjust the debounce time for mouse clicks.
- `movement_threshold`: Set the minimum movement required to update the mouse position.
## Notes
Ensure proper lighting for accurate hand detection.
Adjust the distance thresholds (50 pixels) for click and hold gestures based on your camera resolution and hand size.
