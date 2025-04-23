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

# Change this index if needed
mic_index = 0

# Open the stream using the selected microphone
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                input_device_index=mic_index,
                frames_per_buffer=1024)

# Function to detect claps
def detect_claps(rms, threshold=2000):
    return rms > threshold

# Variables to track clap detection
clap_count = 0
last_clap_time = 0
clap_duration = 2.0      # Time window between claps (seconds)
clap_cooldown = 0.3      # Cooldown after a clap to avoid double detection

try:
    while True:
        data = stream.read(1024, exception_on_overflow=False)
        rms = audioop.rms(data, 2)
        current_time = time.time()

        if detect_claps(rms) and (current_time - last_clap_time > clap_cooldown):
            if current_time - last_clap_time < clap_duration:
                clap_count += 1
                if clap_count == 2:
                    print("Two claps detected! Clicking...")
                    pyautogui.click()
                    clap_count = 0
            else:
                clap_count = 1
            last_clap_time = current_time

        max_n = 100
        n = min(int(rms // 2), max_n)
        blank = max_n - n
        print(f"RMS: {n * '█'}{blank * ' '}", end='\r')

except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("\nStream closed.")
