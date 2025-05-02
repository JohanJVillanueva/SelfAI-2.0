from flaskwebgui import FlaskUI
import os
import threading
import subprocess
import time

# --- Start Streamlit as a subprocess ---
def run_streamlit():
    os.system("streamlit run mictest.py")

# --- Run FlaskWebGUI pointing to Streamlit URL ---
if __name__ == "__main__":
    threading.Thread(target=run_streamlit, daemon=True).start()
    time.sleep(2)  # Let Streamlit boot

    # Launch the GUI browser window
    FlaskUI(server="streamlit", port=8501).run()
