import cv2
import mediapipe as mp
import streamlit as st
import pyttsx3
import pyautogui
import time
#import serial
from streamlit_modal import Modal
import win32gui
import win32con
import win32api

st.set_page_config(
    page_title="SelfAI",
    page_icon="📸",
    initial_sidebar_state="collapsed"  # Options: 'auto', 'expanded', 'collapsed'
)


def find_window_by_partial_title(partial_title):
    def enum_windows_callback(hwnd, results):
        if partial_title.lower() in win32gui.GetWindowText(hwnd).lower():
            results.append(hwnd)
    results = []
    win32gui.EnumWindows(enum_windows_callback, results)
    return results[0] if results else None

import streamlit.components.v1 as components

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

st.sidebar.image("logo.png", use_column_width=True)

logo = "logo.png"
col1, col2, col3 = st.columns(3)
col2.image(logo, width=250)

#original_title = '<h4 style="font-family: sans-serif; color:White; font-size: 20px; text-shadow: 2px 2px 4px #000000;">Please pick your lighting style: </h4>'
#st.markdown(original_title, unsafe_allow_html=True)

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
    thumb_facing_camera = thumb_tip.z < landmarks[3].z  # Thumb closer to the camera

    ring_finger_bent = landmarks[16].y > landmarks[14].y
    pinky_bent = landmarks[20].y > landmarks[18].y

    return index_raised and middle_raised and thumb_facing_camera and ring_finger_bent and pinky_bent

def main():
    image_placeholder = st.empty()
    run = st.sidebar.button('Start Hand Tracking')

    # start area for lighting
    # end area for lighting

    if run:
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        with mp_hands.Hands(
            max_num_hands=2,  # Allow detection of up to two hands
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

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                        landmarks = [hand_landmarks.landmark[i] for i in range(len(hand_landmarks.landmark))]

                        if is_peace_sign(landmarks):
                            image_placeholder.image("LOOK.png")
                            cv2.putText(image, "Peace Sign Detected", (50, 50),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            #text_to_speech("Taking photo in 5 seconds")
                            text_to_speech("5")
                            text_to_speech("4")
                            text_to_speech("3")

                            hwnd = find_window_by_partial_title("Adobe")
                            if hwnd:
                                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F12, 0)
                                win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F12, 0)
                            else:
                                print("No window with 'Adobe' in the title found.")

                            text_to_speech("2")
                            text_to_speech("1")


                            pyautogui.click()
                            st.toast('Photo Done!', icon='📸')
            
                            time.sleep(1)
                            image_placeholder.empty()
                            text_to_speech("Photo Done")

                stframe.image(image, channels='BGR')

                if cv2.waitKey(5) & 0xFF == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
