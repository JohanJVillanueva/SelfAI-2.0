import cv2
import mediapipe as mp
import streamlit as st
import pyttsx3
import pyautogui
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

st.sidebar.image("logo.png", use_column_width=True)
#st.image("logo.png", use_column_width=True)

original_title = '<h4 style="font-family: sans-serif; color:White; font-size: 20px; text-shadow: 2px 2px 4px #000000;">Please pick your lighting style: </h4>'
st.markdown(original_title, unsafe_allow_html=True)


# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://raw.githubusercontent.com/JohanJVillanueva/SelfAI-2.0/refs/heads/main/bg2.jpg");
    background-size: cover;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

def count_fingers(hand_landmarks):
    finger_tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[finger_tips_ids[0]].x < hand_landmarks.landmark[finger_tips_ids[0] - 2].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other four fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[finger_tips_ids[id]].y < hand_landmarks.landmark[finger_tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

def text_to_speech(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def main():
    
    st.sidebar.title("Settings")
    max_num_hands = st.sidebar.slider('Max number of hands:', 1, 4, 2, 1)
    min_detection_confidence = st.sidebar.slider('Minimum detection confidence:', 0.1, 1.0, 0.5, 0.1)
    
    run = st.sidebar.button('Start Hand Tracking')
    
    # Adding buttons to print "hello1" to "hello4" in the terminal
    left, middle, right = st.columns(3)
    if left.button("💡Double Bounce Lighting", use_container_width=True):
        print("hello1")
        text_to_speech("Setting up Double Bounce Lighting, Please wait for the lights to turn on")
        run = True
        
    if middle.button("💡 Rembrandt Lighting", use_container_width=True):
        print("hello2")
        text_to_speech("Setting up Double Remrandt Lighting, Please wait for the lights to turn on")
        run = True

    if right.button("💡 Back Lighting", use_container_width=True):
        print("hello3")
        text_to_speech("Setting up Back Lighting, Please wait for the lights to turn on")
        run = True


    if run:
        cap = cv2.VideoCapture(0)
        stframe = st.empty()
        
        with mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence) as hands:
            
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    st.error("Failed to capture image from camera.")
                    break
                
                # Flip the image horizontally for a later selfie-view display
                image = cv2.flip(image, 1)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Process the image and find hands
                results = hands.process(image_rgb)
                
                # Draw the hand annotations on the image and count fingers
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        
                        # Count the number of raised fingers
                        fingers_count = count_fingers(hand_landmarks)
                        
                        # Display the number of raised fingers and add text-to-speech and pyautogui
                        if fingers_count in [1, 2, 3,4,5]:
                            font_scale = 5 if fingers_count == 1 else 2
                            cv2.putText(image, str(fingers_count), (100, 200), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0, 255, 0), 10, cv2.LINE_AA)
                            
                            if fingers_count == 1 or fingers_count == 2:
                                print("1 Detected")
                                image_placeholder = st.empty() 
                                image_placeholder.image("LOOK.png") 
                                text_to_speech("Taking photo in 3 seconds")
                                text_to_speech("Please look at the Lens")
                                text_to_speech("3")
                                text_to_speech("2")
                                text_to_speech("1")
                                pyautogui.click()
                                text_to_speech("Photo Done")
                                image_placeholder.empty() 
                                
                                
                            elif fingers_count == 3 or fingers_count == 4:
                                print("3 Detected")
                                image_placeholder = st.empty() 
                                image_placeholder.image("LOOK.png") 
                                text_to_speech("Taking photo in 5 seconds")
                                text_to_speech("Please look at the Lens")
                                text_to_speech("5")
                                text_to_speech("4")
                                text_to_speech("3")
                                text_to_speech("2")
                                text_to_speech("1")
                                pyautogui.click()
                                text_to_speech("Photo Done")
                                image_placeholder.empty() 
                                
                                
                            elif fingers_count == 5:
                                print("5 Detected")
                                image_placeholder = st.empty() 
                                image_placeholder.image("LOOK.png") 
                                text_to_speech("Taking photo in 10 seconds")
                                text_to_speech("Please look at the Lens")
                                text_to_speech("10")
                                text_to_speech("9")
                                text_to_speech("8")
                                text_to_speech("7")
                                text_to_speech("6")
                                text_to_speech("5")
                                text_to_speech("4")
                                text_to_speech("3")
                                text_to_speech("2")
                                text_to_speech("1")
                                pyautogui.click()
                                text_to_speech("Photo Done")
                                image_placeholder.empty() 
                                
                
                stframe.image(image, channels='BGR')
                
                if cv2.waitKey(5) & 0xFF == 27:
                    break
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
