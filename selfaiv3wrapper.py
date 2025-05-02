import os
import threading
from flask import Flask
from flaskwebgui import FlaskUI

# Flask dummy app (just for flaskwebgui to attach to)
app = Flask(__name__)

# Path to your Streamlit app
STREAMLIT_APP = "selfaiv3.py"

def run_streamlit():
    # Start the Streamlit server
    os.system(f"streamlit run {STREAMLIT_APP} --server.headless true")

@app.route('/')
def index():
    # Automatically redirect to the local Streamlit server
    return '''
        <script>
            window.location.replace("http://localhost:8501");
        </script>
    '''

if __name__ == '__main__':
    threading.Thread(target=run_streamlit).start()
    ui = FlaskUI(app=app, server="flask", width=1000, height=700)
    ui.run()
