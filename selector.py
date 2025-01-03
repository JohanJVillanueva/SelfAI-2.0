import tkinter as tk
import subprocess
import sys  # To determine the Python executable
import pyautogui  # To automate key presses
import time  # To add delay for ensuring the process starts

# Function to open the Python script for hand recognition
def open_hand_recognition():
    hand_recognition = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\arduinotalker.py"  # Path to arduinotalker.py
    root.destroy()  # Close the Tkinter window
    subprocess.Popen(["streamlit", "run", hand_recognition])
    time.sleep(5)  # Wait for 5 seconds to ensure the Streamlit window is open
    pyautogui.press("f11")  # Press F11 to enter fullscreen mode

# Function to open the Python script for voice recognition
def open_voice_recognition():
    voice_recognition = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\extra.py"  # Path to extra.py for voice recognition
    root.destroy()  # Close the Tkinter window
    subprocess.Popen(["streamlit", "run", voice_recognition])
    time.sleep(5)  # Wait for 5 seconds to ensure the Streamlit window is open
    pyautogui.press("f11")  # Press F11 to enter fullscreen mode

# Function to open the lightroom.py script directly
def setup_lightroom():
    lightroom = "C:\\Users\\liljo\\Desktop\\SelfAI Version 2\\lightroom.py"  # Path to lightroom.py
    #root.destroy()  # Close the Tkinter window
    subprocess.Popen([sys.executable, lightroom])  # Run the script with the Python interpreter
    time.sleep(5)  # Wait for 5 seconds (if needed for GUI or related setup)
    open_hand_recognition()


# Create the main Tkinter window
root = tk.Tk()
root.title("SelfAI Setup")
root.geometry("300x250")

# Add a label
label = tk.Label(root, text="Select an option to open the application:")
label.pack(pady=20)

# Add a button for hand recognition
button1 = tk.Button(root, text="Hand Recognition", command=open_hand_recognition, bg="blue", fg="white")
button1.pack(pady=10)

# Add a button for voice recognition
button2 = tk.Button(root, text="Voice Recognition", command=open_voice_recognition, bg="green", fg="white")
button2.pack(pady=10)

# Add a button for lightroom setup
button3 = tk.Button(root, text="Setup Lightroom", command=setup_lightroom, bg="orange", fg="white")
button3.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
