import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Variables for camera customization
camera_rotation = 180  # Rotate the camera feed by 180 degrees (can be 90, 180, 270, or 0 for no rotation)
flip_camera = False  # Flip the camera feed horizontally if set to True

# Variables for the red box dimensions
box_width = 600  # Width of the red box in pixels
box_height = 400  # Height of the red box in pixels

# Screen dimensions and mouse movement settings
screen_width, screen_height = pyautogui.size()  # Get the screen resolution (width and height)
last_click_time = 0  # Timestamp of the last mouse click to enforce click delay
click_delay = 0.2  # Minimum delay (in seconds) between consecutive mouse clicks
prev_screen_x, prev_screen_y = 0, 0  # Previous mouse cursor position on the screen
movement_threshold = 10  # Minimum movement (in pixels) required to update the mouse position
dpi_multiplier = 1.5  # Multiplier to adjust for high-DPI screens
smoothing_factor = 0.9  # Factor for smoothing mouse movement (closer to 1 means smoother movement)
smoothed_x, smoothed_y = 0, 0  # Smoothed mouse cursor position

# Function to calculate Euclidean distance
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Open the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Rotate and flip the frame if needed
    if camera_rotation == 90:
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif camera_rotation == 180:
        frame = cv2.rotate(frame, cv2.ROTATE_180)
    elif camera_rotation == 270:
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    if flip_camera:
        frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Frame dimensions and red box coordinates
    frame_height, frame_width, _ = frame.shape
    center_x, center_y = frame_width // 2, frame_height // 2
    top_left = (center_x - box_width // 2, center_y - box_height // 2)
    bottom_right = (center_x + box_width // 2, center_y + box_height // 2)
    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get finger tip positions
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            index_x, index_y = int(index_finger_tip.x * frame_width), int(index_finger_tip.y * frame_height)
            middle_x, middle_y = int(middle_finger_tip.x * frame_width), int(middle_finger_tip.y * frame_height)
            ring_x, ring_y = int(ring_finger_tip.x * frame_width), int(ring_finger_tip.y * frame_height)

            # Check if the index finger is inside the red box
            if top_left[0] <= index_x <= bottom_right[0] and top_left[1] <= index_y <= bottom_right[1]:
                relative_x = index_x - top_left[0]
                relative_y = index_y - top_left[1]
                screen_x = int((relative_x / box_width) * screen_width * dpi_multiplier)
                screen_y = int((relative_y / box_height) * screen_height * dpi_multiplier)

                # Apply smoothing and move the mouse
                smoothed_x = smoothing_factor * screen_x + (1 - smoothing_factor) * smoothed_x
                smoothed_y = smoothing_factor * screen_y + (1 - smoothing_factor) * smoothed_y
                if abs(smoothed_x - prev_screen_x) > movement_threshold or abs(smoothed_y - prev_screen_y) > movement_threshold:
                    pyautogui.moveTo(int(smoothed_x), int(smoothed_y))
                    prev_screen_x, prev_screen_y = smoothed_x, smoothed_y

                # Calculate distances between fingers
                distance_index_middle = calculate_distance(index_x, index_y, middle_x, middle_y)
                distance_middle_ring = calculate_distance(middle_x, middle_y, ring_x, ring_y)

                # Handle mouse click
                current_time = time.time()
                if distance_index_middle < 50 and (current_time - last_click_time) > click_delay:
                    pyautogui.click()
                    last_click_time = current_time
                    print("Mouse Clicked!")

                # Handle mouse hold (three fingers up)
                if distance_index_middle < 50 and distance_middle_ring < 50:
                    pyautogui.mouseDown()
                    print("Mouse Hold!")
                else:
                    pyautogui.mouseUp()
                    print("Mouse Released!")

                # Draw a circle at the index finger tip
                cv2.circle(frame, (index_x, index_y), 10, (255, 0, 0), -1)

    cv2.imshow("Hand Pose Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
hands.close()