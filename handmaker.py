import cv2
import mediapipe as mp

# Initialize Mediapipe Hands and Drawing modules
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Define a function to detect a peace sign gesture (index and middle fingers raised)
def is_peace_sign(landmarks, handedness):
    if handedness != "Right":
        return False

    # Landmarks for the index, middle, ring, pinky fingers, and thumb
    index_tip = landmarks[8]
    index_dip = landmarks[7]
    middle_tip = landmarks[12]
    middle_dip = landmarks[11]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]

    # Check if the index and middle fingers are raised and other fingers are down
    index_raised = index_tip.y < index_dip.y  # Index finger tip is above its lower joint
    middle_raised = middle_tip.y < middle_dip.y  # Middle finger tip is above its lower joint
    other_fingers_down = (
        ring_tip.y > landmarks[15].y and  # Ring finger tip is below its lower joint
        pinky_tip.y > landmarks[19].y     # Pinky finger tip is below its lower joint
    )

    # Check if the thumb is folded (thumb tip is near the thumb IP joint)
    thumb_folded = abs(thumb_tip.x - thumb_ip.x) < 0.05 and abs(thumb_tip.y - thumb_ip.y) < 0.05

    return index_raised and middle_raised and other_fingers_down and thumb_folded

# Start video capture
cap = cv2.VideoCapture(0)

with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for a mirror-like effect
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame for hand landmarks
        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, hand_handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                # Extract handedness label
                handedness_label = hand_handedness.classification[0].label
                
                # Check if the peace sign gesture is detected
                if is_peace_sign(hand_landmarks.landmark, handedness_label):
                    cv2.putText(frame, "Peace Sign Detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the frame
        cv2.imshow("Hand Detection", frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
