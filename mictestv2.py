import sounddevice as sd
import queue
import json
import time
import pyttsx3
import win32gui
import win32con
import win32api
import pyautogui
from vosk import Model, KaldiRecognizer

# === TEXT TO SPEECH FUNCTION ===
engine = pyttsx3.init()
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# === FIND ADOBE WINDOW FUNCTION ===
def find_window_by_partial_title(partial_title):
    def enum_callback(hwnd, results):
        if win32gui.IsWindowVisible(hwnd) and partial_title.lower() in win32gui.GetWindowText(hwnd).lower():
            results.append(hwnd)
    results = []
    win32gui.EnumWindows(enum_callback, results)
    return results[0] if results else None

# === LIST MICROPHONES ===
print("Available Microphones:")
devices = sd.query_devices()
input_devices = []
for i, dev in enumerate(devices):
    if dev['max_input_channels'] > 0:
        try:
            sd.check_input_settings(device=i)
            input_devices.append(i)
            print(f"[{i}] {dev['name']}")
        except Exception:
            continue

device_index = int(input("\nSelect the microphone index: "))

# === VOSK SETUP ===
model_path = "models/vosk-model-small-en-us-0.15"
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)
q = queue.Queue()

def callback(indata, frames, time_info, status):
    if status:
        print("Status:", status)
    q.put(bytes(indata))

# === TRIGGER WORDS & COOLDOWN ===
trigger_words = [
    "cheese", "selfie", "capture", "catcher",
    "caption", "chapter", "rapture", "snap", "click"
]
cooldown_seconds = 3
last_trigger_time = 0
triggered_this_session = False  # To ensure only one action is triggered

# === MAIN LISTENING LOOP ===
with sd.RawInputStream(samplerate=16000, blocksize=4000, dtype='int16',
                       channels=1, callback=callback, device=device_index):
    print("\n🎤 Listening for trigger words...")

    while True:
        data = q.get()
        current_time = time.time()
        in_cooldown = (current_time - last_trigger_time) < cooldown_seconds

        trigger_detected = False
        spoken_text = ""

        # Process full recognition result only (no partial)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            spoken_text = result.get("text", "").lower()

            # Check if any trigger words are detected
            if any(word in spoken_text for word in trigger_words):
                trigger_detected = True

        # Trigger action only if not in cooldown and not previously triggered in this session
        if trigger_detected and not in_cooldown and not triggered_this_session:
            last_trigger_time = time.time()
            triggered_this_session = True  # Prevent further triggers until cooldown is over

            print(f"✅ Trigger word detected: {spoken_text}")

            # === SEND F12 TO ADOBE ===
            hwnd = find_window_by_partial_title("Adobe")
            if hwnd:
                # Ensure F12 is only sent once
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_F12, 0)
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_F12, 0)
            else:
                print("No window with 'Adobe' in the title found.")

            # === COUNTDOWN & CLICK ===
            text_to_speech("3...2...1..")

            pyautogui.click()
            text_to_speech("Photo done")

        # Reset session trigger after cooldown period
        if current_time - last_trigger_time >= cooldown_seconds:
            triggered_this_session = False
