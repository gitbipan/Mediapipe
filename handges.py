import cv2
import mediapipe as mp
import serial
import time

# Setup serial communication (Change COM Port if needed)
try:
    ser = serial.Serial('COM6', 9600, timeout=1)  # Change 'COM8' to match Arduino port
    time.sleep(2)  # Wait for connection to establish
except:
    print("❌ ERROR: Could not connect to Arduino. Check COM port.")

# Initialize MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Open Camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame for a mirror effect
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process hands
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the landmarks for the index finger and thumb
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Calculate distance between index finger tip and thumb tip
            distance = ((index_tip.x - thumb_tip.x) ** 2 + (index_tip.y - thumb_tip.y) ** 2) ** 0.5

            # If fingers are touching (threshold ~ 0.05)
            if distance < 0.05:
                cv2.putText(frame, "Press Detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                ser.write(b'H')  # Send ON signal to Arduino
            else:
                ser.write(b'L')  # Send OFF signal

    cv2.imshow("Hand Gesture", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
ser.close()
