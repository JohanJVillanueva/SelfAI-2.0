import pyaudio
import audioop
import pyautogui
import time

# Initialize PyAudio
p = pyaudio.PyAudio()

# List all available audio devices
device_info = p.get_host_api_info_by_index(0)
device_count = device_info.get('deviceCount')

# Find the input device index (microphone)
for i in range(device_count):
    info = p.get_device_info_by_index(i)
    if info['maxInputChannels'] > 0:
        print(f"Device index {i}: {info['name']}")

# Assuming you're using the first available microphone (you can change the index)
mic_index = 0  # Change this index to the correct one from the list above

# Open the stream using the selected microphone
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                input_device_index=mic_index,
                frames_per_buffer=1024)

# Function to detect claps
def detect_claps(rms, threshold=2000):
    """Detect a single clap based on RMS threshold."""
    if rms > threshold:
        return True
    return False

# Variables to track clap detection
clap_count = 0
last_clap_time = time.time()

# Adjust the duration for detecting the second clap (now set to 2 seconds)
clap_duration = 2.0  # Time window between claps (seconds)

try:
    while True:
        data = stream.read(1024)
        rms = audioop.rms(data, 2)
        
        # Detect a clap
        if detect_claps(rms):
            current_time = time.time()
            
            # Check if the second clap is within the time frame (now 2 seconds)
            if current_time - last_clap_time < clap_duration:
                clap_count += 1
                if clap_count == 2:
                    print("Two claps detected! Clicking...")
                    pyautogui.click()  # Trigger click on the screen
                    clap_count = 0  # Reset clap count after clicking
            else:
                clap_count = 1  # Reset to 1 if the claps are too far apart
            last_clap_time = current_time

        max_n = 100
        n = min(int(rms // 2), max_n)
        blank = max_n - n
        print(f"RMS: {n * '█'}{blank * ' '}", end='\r')

except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print()
