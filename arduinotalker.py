import cv2
import mediapipe as mp
import streamlit as st
import pyttsx3
import pyautogui
import time
import serial
from streamlit_modal import Modal

import streamlit.components.v1 as components


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

st.sidebar.image("logo.png", use_column_width=True)

logo = "logo.png"
col1, col2, col3 = st.columns(3)
col2.image(logo, width=250)

original_title = '<h4 style="font-family: sans-serif; color:White; font-size: 20px; text-shadow: 2px 2px 4px #000000;">Please pick your lighting style: </h4>'
st.markdown(original_title, unsafe_allow_html=True)

# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://raw.githubusercontent.com/JohanJVillanueva/SelfAI-2.0/refs/heads/main/bg3.jpg");
    background-size: cover;
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

def text_to_speech(message):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(message)
    engine.runAndWait()

def is_peace_sign(landmarks):
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    thumb_tip = landmarks[4]

    index_raised = index_tip.y < landmarks[6].y
    middle_raised = middle_tip.y < landmarks[10].y
    thumb_raised = thumb_tip.x > landmarks[3].x

    ring_finger_bent = landmarks[16].y > landmarks[14].y
    pinky_bent = landmarks[20].y > landmarks[18].y

    return index_raised and middle_raised and thumb_raised and ring_finger_bent and pinky_bent

def is_five_fingers_open_right_hand(hand_landmarks, hand_label):
    if hand_label != "Right":
        return False

    fingers_open = [
        hand_landmarks[8].y < hand_landmarks[6].y,  # Index finger
        hand_landmarks[12].y < hand_landmarks[10].y,  # Middle finger
        hand_landmarks[16].y < hand_landmarks[14].y,  # Ring finger
        hand_landmarks[20].y < hand_landmarks[18].y,  # Pinky
        hand_landmarks[4].x < hand_landmarks[3].x  # Thumb on the left side (flipped for right hand)
    ]
    return all(fingers_open)



def main():
    #st.sidebar.title("Settings")
    #max_num_hands = st.sidebar.slider('Max number of hands:', 1, 4, 2, 1)
    #min_detection_confidence = st.sidebar.slider('Minimum detection confidence:', 0.1, 1.0, 0.5, 0.1)
    image_placeholder = st.empty()
    run = st.sidebar.button('Start Hand Tracking')

    left, middle, right = st.columns(3)
    if left.button("💡Double Bounce Lighting", use_container_width=True):
        image_placeholder.image("doublebounce.png")
        print("hello1")
        text_to_speech("Setting up Double Bounce Lighting, Please wait for the lights to turn on")
        # Initialize the serial connection
        serialcomm = serial.Serial('COM10', 9600)
        serialcomm.timeout = 1

        try:
            while True:
                # Message to be sent
                message = "lightsetup1"

                # Send the message
                serialcomm.write(message.encode())

                # Wait for a response
                time.sleep(0.5)

                # Print the response from the serial device
                response = serialcomm.readline().decode('ascii').strip()
                if response:
                    print(f"Response: {response}")
                    print("Response received. Closing serial communication.")
                    break  # Exit the loop once a response is received

        except KeyboardInterrupt:
            # Graceful exit on keyboard interrupt
            print("\nProgram terminated by user.")

        finally:
            # Close the serial connection
            serialcomm.close()
            print("Serial communication closed.")
        image_placeholder.empty()
        run = True



    if middle.button("💡 Rembrandt Lighting", use_container_width=True):
        image_placeholder.image("rembrandt.png")
        print("hello2")
        text_to_speech("Setting up Rembrandt Lighting, Please wait for the lights to turn on")
                # Initialize the serial connection
        serialcomm = serial.Serial('COM12', 9600)
        serialcomm.timeout = 1

        try:
            while True:
                # Message to be sent
                message = "lightsetup2"

                # Send the message
                serialcomm.write(message.encode())

                # Wait for a response
                time.sleep(0.5)

                # Print the response from the serial device
                response = serialcomm.readline().decode('ascii').strip()
                if response:
                    print(f"Response: {response}")
                    print("Response received. Closing serial communication.")
                    break  # Exit the loop once a response is received

        except KeyboardInterrupt:
            # Graceful exit on keyboard interrupt
            print("\nProgram terminated by user.")

        finally:
            # Close the serial connection
            serialcomm.close()
            print("Serial communication closed.")
        image_placeholder.empty()
        run = True

    if right.button("💡 Back Lighting", use_container_width=True):
        image_placeholder.image("backlighting.png")
        print("hello3")
        text_to_speech("Setting up Back Lighting, Please wait for the lights to turn on")
                # Initialize the serial connection
        serialcomm = serial.Serial('COM12', 9600)
        serialcomm.timeout = 1

        try:
            while True:
                # Message to be sent
                message = "lightsetup3"

                # Send the message
                serialcomm.write(message.encode())

                # Wait for a response
                time.sleep(0.5)

                # Print the response from the serial device
                response = serialcomm.readline().decode('ascii').strip()
                if response:
                    print(f"Response: {response}")
                    print("Response received. Closing serial communication.")
                    break  # Exit the loop once a response is received

        except KeyboardInterrupt:
            # Graceful exit on keyboard interrupt
            print("\nProgram terminated by user.")

        finally:
            # Close the serial connection
            serialcomm.close()
            print("Serial communication closed.")
        image_placeholder.empty()
        run = True

    

    if run:
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        with mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.9,
            model_complexity=1) as hands:

            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    st.error("Failed to capture image from camera.")
                    break

                image = cv2.flip(image, 2)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image_rgb)

                if results.multi_hand_landmarks and results.multi_handedness:
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                        hand_label = handedness.classification[0].label  # "Right" or "Left"

                        if hand_label != "Right":
                            continue  # Skip processing if the hand is not the right hand

                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                        landmarks = [hand_landmarks.landmark[i] for i in range(len(hand_landmarks.landmark))]

                        if is_peace_sign(landmarks):
                            image_placeholder.image("LOOK.png")
                            cv2.putText(image, "Peace Sign Detected", (50, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            text_to_speech("Taking photo in 3 seconds")

                            for i in range(3, 0, -1):
                                text_to_speech(str(i))
                                

                            pyautogui.click()
                            st.toast('Photo Done!', icon='📸')
                            text_to_speech("Photo Done")
                            time.sleep(2)
                            image_placeholder.empty()

                        if is_five_fingers_open_right_hand(landmarks, hand_label):
                            image_placeholder.image("LOOK.png")
                            cv2.putText(image, "Five Fingers Open Detected (Right Hand)", (50, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            text_to_speech("Taking photo in 10 seconds")

                            for i in range(10, 0, -1):
                                text_to_speech(str(i))
                                

                            pyautogui.click()
                            st.toast('Photo Done!', icon='📸')
                            text_to_speech("Photo Done")
                            time.sleep(2)
                            image_placeholder.empty()

                stframe.image(image, channels='BGR')

                if cv2.waitKey(5) & 0xFF == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
