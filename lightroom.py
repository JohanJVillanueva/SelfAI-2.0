import pyautogui
import time
from datetime import datetime

# Brief delay to allow you to switch to the desired window
time.sleep(1)  # Gives you 3 seconds to prepare

# Press Win + 8
pyautogui.hotkey('win', '8')
time.sleep(.5)  # Small delay to ensure the command is processed

# Press Alt + F
pyautogui.hotkey('alt', 'f')
time.sleep(.5)

# Press the Down arrow 8 times
for i in range(7):
    pyautogui.press('down')
    time.sleep(0.1)  # Small delay between key presses

# Press the Right arrow 1 time
pyautogui.press('right')
time.sleep(0.2)

# Press Enter 2 times
pyautogui.press('enter')

# Enter the current date with a period as the separator
current_date = datetime.now().strftime('%d.%m.%Y')  # Format as DD.MM.YYYY
pyautogui.typewrite(current_date)
time.sleep(1)  # Delay to ensure the date is entered

# Press Enter 2 times
pyautogui.press('enter')
time.sleep(2)

