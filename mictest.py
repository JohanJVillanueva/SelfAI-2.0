import pyaudio
import audioop
import time
import win32gui
import win32con
import win32api
import speech_recognition as sr
import threading
from multiprocessing import Process
import pyttsx3

# --- TTS Setup (using multiprocessing to avoid blocking) ---
def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def text_to_speech(text):
    p = Process(target=speak, args=(text,))
    p.start()
    p.join()

# --- Window Targeting ---
def find_window_by_partial_title(partial_title):
    def callback(hwnd, titles):
        if partial_title.lower() in win32gui.GetWindowText(hwnd).lower():
            titles.append(hwnd)
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows[0] if windows else None

# --- Photo Trigger Sequence ---
def trigger_photo():
    print("📸 Triggering photo sequence...")
    text_to_speech("Taking photo in 5 seconds")
    text_to_speech("5. . 4. . 3.")
    hwnd = find_window_by_partial_title("Adobe")
    if hwnd:
        text_to_speech("2. . 1. .")
        win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F12, 0)
        win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F12, 0)
        print("✅ Sent F12 to Adobe window.")
        text_to_speech("Photo Done")
    else:
        print("⚠️ No Adobe window found.")

# --- Clap Detection Thread ---
def clap_listener():
    p = pyaudio.PyAudio()
    mic_index = 0  # Change if needed

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    input_device_index=mic_index,
                    frames_per_buffer=1024)

    def detect_claps(rms, threshold=2000):
        return rms > threshold

    clap_count = 0
    last_clap_time = 0
    clap_duration = 2.0
    clap_cooldown = 0.3

    print("🎤 Listening for claps...")

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            rms = audioop.rms(data, 2)
            current_time = time.time()

            if detect_claps(rms) and (current_time - last_clap_time > clap_cooldown):
                if current_time - last_clap_time < clap_duration:
                    clap_count += 1
                    if clap_count == 2:
                        print("👏 Two claps detected!")
                        trigger_photo()
                        clap_count = 0
                else:
                    clap_count = 1
                last_clap_time = current_time

            # Optional RMS bar visual
            max_n = 100
            n = min(int(rms // 2), max_n)
            blank = max_n - n
            print(f"RMS: {n * '█'}{blank * ' '}", end='\r')

    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()

# --- Voice Detection Thread ---
def voice_listener():
    recognizer = sr.Recognizer()
    mic = sr.Microphone(device_index=0)  # Change if needed

    print("🗣️ Listening for keyword 'cheese'...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        while True:
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=2)
                command = recognizer.recognize_google(audio, language="en-US", show_all=False).lower()
                print(f"🧠 Heard: {command}")
                
                # Add a tolerance level to recognize 'cheese' in noisy conditions
                if "cheese" in command:
                    print("🔑 Keyword 'cheese' detected!")
                    trigger_photo()
                
                if "capture" in command:
                    print("🔑 Keyword 'capture' detected!")
                    trigger_photo()


                if "camera" in command:
                    print("🔑 Keyword 'camera' detected!")
                    trigger_photo()

                
                if "record" in command:
                    print("🔑 Keyword 'record' detected!")
                    trigger_photo()

                if "five" in command:
                    print("🔑 Keyword 'five' detected!")
                    trigger_photo()
            
            except sr.UnknownValueError:
                # If the speech was not understood, continue listening
                pass
            except sr.RequestError:
                print("⚠️ Speech recognition service error.")
            except Exception as e:
                print(f"⚠️ Voice detection error: {e}")

# --- Main ---
if __name__ == "__main__":
    # Start the clap and voice listener in separate threads
    threading.Thread(target=clap_listener, daemon=True).start()
    threading.Thread(target=voice_listener, daemon=True).start()

    print("🟢 System is running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:  
        print("\nShutting down...") 