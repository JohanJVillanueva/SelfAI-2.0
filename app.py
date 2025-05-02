from flask import Flask, render_template, request
from flaskwebgui import FlaskUI
import serial

app = Flask(__name__)

# Try to connect to serial
try:
    ser = serial.Serial('COM13', 9600, timeout=5)
    print("Connected to Arduino on COM13")
except serial.SerialException as e:
    ser = None
    print(f"Error: {e}. Serial port not available.")

# Function to read data from Arduino
def read_serial_data():
    if ser and ser.in_waiting > 0:
        return ser.readline().decode('utf-8').strip()
    return None

@app.route('/')
def index():
    return render_template('index.html')  # Your HTML should be inside a 'templates' folder

@app.route('/shutter', methods=['POST'])
def trigger_shutter():
    if ser:
        ser.write(b's')
        response = read_serial_data()
        if response:
            print(f"Arduino says: {response}")
        return 'Shutter triggered!'
    return 'Serial port unavailable', 500

@app.route('/lighting', methods=['POST'])
def control_lighting():
    data = request.json
    mode = data.get('mode')
    commands = {
        'backlighting': b'lightsetup1',
        'rembrandt': b'lightsetup2',
        'front': b'lightsetup3'
    }

    if mode in commands and ser:
        ser.write(commands[mode])
        response = read_serial_data()
        if response:
            print(f"Arduino says: {response}")
        return f'Lighting set to {mode}'
    return 'Invalid command or serial error', 400

# Launch the app with a GUI window using FlaskUI
if __name__ == '__main__':
    ui = FlaskUI(app=app, server="flask", width=1000, height=700)
    ui.run()
