import tkinter as tk
import subprocess
import sys  # To determine the Python executable
import pyautogui  # To automate key presses
import time  # To add delay for ensuring the process starts
from tkinter import PhotoImage  # To work with images
import pyttsx3  # For text-to-speech functionality

# Initialize the pyttsx3 engine

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say("Opening SelfAI")
engine.runAndWait()

# Function to speak the text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to open the Python script for hand recognition
def open_hand_recognition(number):
    hand_recognition = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\arduinotalker.py"  # Path to arduinotalker.py
    root.destroy()  # Close the Tkinter window
    subprocess.Popen(["streamlit", "run", hand_recognition])
    time.sleep(5)  # Wait for 5 seconds to ensure the Streamlit window is open
    pyautogui.press("f11")  # Press F11 to enter fullscreen mode
    time.sleep(8)
    for i in range(number):
        pyautogui.press('tab')
        time.sleep(0.1)  # Small delay between key presses
    pyautogui.press("enter")

# Additional functions for buttons "1", "2", and "3"
def open_script_1():
    speak("Welcome to Self AI, Let's start with Double Bounce Lighting")  # Speak the button text
    lightroom = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\lightroom.py"  # Path to lightroom.py
    subprocess.Popen([sys.executable, lightroom])  # Run the script with the Python interpreter
    time.sleep(5)  # Wait for 5 seconds (if needed for GUI or related setup)
    open_hand_recognition(7)

    # Wait for 20 seconds
    time.sleep(30)
    # Press Ctrl+W to close the application
    pyautogui.hotkey('ctrl', 'w')
    # Announce the time is up
    speak("Your time is up, thank you for using Self AI")

def open_script_2():
    speak("Welcome to Self AI, Let's start with Rembrandt Lighting")  # Speak the button text
    lightroom = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\lightroom.py"  # Path to lightroom.py
    subprocess.Popen([sys.executable, lightroom])  # Run the script with the Python interpreter
    time.sleep(5)  # Wait for 5 seconds (if needed for GUI or related setup)
    open_hand_recognition(8)

    # Wait for 20 seconds
    time.sleep(30)
    # Press Ctrl+W to close the application
    pyautogui.hotkey('ctrl', 'w')
    # Announce the time is up
    speak("Your time is up, thank you for using Self AI")

def open_script_3():
    speak("Welcome to Self AI, Let's start with Back Lighting")  # Speak the button text
    lightroom = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\lightroom.py"  # Path to lightroom.py
    subprocess.Popen([sys.executable, lightroom])  # Run the script with the Python interpreter
    time.sleep(5)  # Wait for 5 seconds (if needed for GUI or related setup)
    open_hand_recognition(9)

    # Wait for 20 seconds
    time.sleep(30)
    # Press Ctrl+W to close the application
    pyautogui.hotkey('ctrl', 'w')
    # Announce the time is up
    speak("Your time is up, thank you for using Self AI")

# Create the main Tkinter window
root = tk.Tk()
root.title("SelfAI Setup")
root.geometry("400x500")  # Make the window bigger (increased size)

# Prevent resizing
root.resizable(False, False)

# Load the logo image
logo = PhotoImage(file="logo.png")  # Make sure the logo is in the same directory as this script or provide the full path

# Resize the logo by scaling it down
logo = logo.subsample(5, 5)  # Adjust the scale as needed (for example, subsample by a factor of 3)

# Add the logo label
logo_label = tk.Label(root, image=logo)
logo_label.pack(pady=20)

# Add a label
label = tk.Label(root, text="Select an option to open the application:")
label.pack(pady=20)

# Add three additional buttons (1, 2, 3)
button4 = tk.Button(root, text="Start with Double Bounce Lighting", command=open_script_1, bg="red", fg="white")
button4.pack(pady=10)

button5 = tk.Button(root, text="Start with Rembrandt Lighting", command=open_script_2, bg="purple", fg="white")
button5.pack(pady=10)

button6 = tk.Button(root, text="Start with Back Lighting", command=open_script_3, bg="yellow", fg="black")
button6.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
