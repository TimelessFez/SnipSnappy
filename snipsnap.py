# DISCLAIMER: This program runs in the background to detect key presses (re: lines 29-40) until the user ends the program.

# Imports
import os
import time
from pynput import keyboard
import subprocess

# Create directory to store the screenshots. Directory name is based on the date and time
directory = time.strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs("problem_steps/" + directory)

# Define function to capture a screenshot of the active window
def capture_screenshot():
    # Get ID of the active window
    active_window_id = subprocess.check_output(['xdotool', 'getactivewindow']).strip().decode()

    # Get the geometry of the active window
    geometry = subprocess.check_output(['xwininfo', '-id', active_window_id]).decode()

    # Parse the geometry string to get window position and size
    x, y = int(geometry.split('Absolute upper-left X:')[1].split('\n')[0]), int(geometry.split('Absolute upper-left Y:')[1].split('\n')[0])
    
    # Extracts width and height of the active window by splitting the output of the xwininfo. Extracts values from width and height labels
    width, height = int(geometry.split('Width:')[1].split('\n')[0]), int(geometry.split('Height:')[1].split('\n')[0])

    # Capture a screenshot of the active window using imagemagick. Save image as "step<incremented number>.png" under a directory within a folder named "problem_steps".
    subprocess.run(['import', '-window', active_window_id, '-frame', f'problem_steps/{directory}/step{len(os.listdir("problem_steps/" + directory)) + 1}.png'])

# Define a function to handle key presses
def on_press(key):
    try:
        # Default key: f3
        # Replace f3 with any key you want to use (e.g. shift_r, alt_l, ctrl_r, esc, backspace, enter, down, up, esc, etc.)
        if key == keyboard.Key.f3:
            capture_screenshot()
    except AttributeError:
        pass

# Create a listener for key presses
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
