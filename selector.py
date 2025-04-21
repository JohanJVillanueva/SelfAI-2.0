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
    
    hand_recognition = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\arduinotalker.py"
    subprocess.Popen(["streamlit", "run", hand_recognition])
    
    time.sleep(8)
    
    for i in range(number):
        pyautogui.press('tab')
        time.sleep(0.1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.hotkey("ctrl", "t")
    
    time.sleep(1)
    url = "file:///C:/Users/liljo/Desktop/SelfAI%20Version%202/SelfAI%20Tutorial.mp4"
    pyautogui.write(url)
    pyautogui.press("enter")
    time.sleep(2)
    pyautogui.press("F11")
    time.sleep(78)
    pyautogui.hotkey("ctrl", "w")
    engine = pyttsx3.init()
    message = "Please wait for the webcam to show up. Once shown, you can start using SelfAI."
    engine.say(message)
    engine.runAndWait()
    pyautogui.hotkey("alt", "tab")
    root.destroy()

def open_script_1():
    speak("Welcome to Self AI, Let's start with Double Bounce Lighting")
    lightroom = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\lightroom.py"
    subprocess.Popen([sys.executable, lightroom])
    time.sleep(5)
    open_hand_recognition(8)

def open_script_2():
    speak("Welcome to Self AI, Let's start with Rembrandt Lighting")
    lightroom = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\lightroom.py"
    subprocess.Popen([sys.executable, lightroom])
    time.sleep(5)
    open_hand_recognition(9)

def open_script_3():
    speak("Welcome to Self AI, Let's start with Back Lighting")
    lightroom = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\lightroom.py"
    subprocess.Popen([sys.executable, lightroom])
    time.sleep(5)
    open_hand_recognition(10)

def export_photos():
    speak("Exporting photos. Please wait.")
    time.sleep(2)
    pyautogui.hotkey('win', '1')
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(2)
    pyautogui.hotkey('win', '8')
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(2)
    pyautogui.hotkey('ctrl', 'shift', 'e')
    time.sleep(2)
    pyautogui.press('enter')
    speak("Photos will be exported, thank you for using SelfAI.")

root = tk.Tk()
root.title("SelfAI Setup")
root.attributes('-fullscreen', True)  # Enable full-screen mode
#root.geometry("1920x1080")  # Set the window size to 1920x1080
root.configure(bg="white")  # Set background color

# Load the logo image
logo = PhotoImage(file="logo.png")
logo = logo.subsample(5, 5)

# Add a container frame for centering the layout
container = tk.Frame(root, bg="white")
container.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

# Add the logo label to the container frame
logo_label = tk.Label(container, image=logo, bg="white")
logo_label.grid(row=0, column=0, columnspan=2, pady=20)

# Configure grid layout within the container frame
for i in range(2):
    container.grid_rowconfigure(i, weight=1)
    container.grid_columnconfigure(i, weight=1)

# Add buttons in a 2x2 grid
button1 = tk.Button(
    container, text="Double Bounce Lighting", command=open_script_1, bg="red", fg="white",
    font=("Arial", 20), height=3, width=20
)
button1.grid(row=1, column=0, padx=20, pady=20)

button2 = tk.Button(
    container, text="Rembrandt Lighting", command=open_script_2, bg="purple", fg="white",
    font=("Arial", 20), height=3, width=20
)
button2.grid(row=1, column=1, padx=20, pady=20)

button3 = tk.Button(
    container, text="Back Lighting", command=open_script_3, bg="yellow", fg="black",
    font=("Arial", 20), height=3, width=20
)
button3.grid(row=2, column=0, padx=20, pady=20)

button4 = tk.Button(
    container, text="Export Photos", command=export_photos, bg="blue", fg="white",
    font=("Arial", 20), height=3, width=20
)
button4.grid(row=2, column=1, padx=20, pady=20)

# Start the Tkinter event loop
root.mainloop()