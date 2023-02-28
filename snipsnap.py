# DISCLAIMER: This program runs in the background to detect key presses (re: lines 29-40) until the user ends the program.

# Imports
import os
import time
from pynput import keyboard
import subprocess

# Create directory to store the screenshots. Directory name is based on the date and time
directory = time.strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs("snapshots/" + directory)
key_path = os.path.exists("keylog.txt")

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

    # Capture a screenshot of the active window using imagemagick. Save image as "step<incremented number>.png" under a directory within a folder named "snapshots".
    subprocess.run(['import', '-window', active_window_id, '-frame', f'snapshots/{directory}/step{len(os.listdir("snapshots/" + directory)) + 1}.png'])

# Define a function to handle key presses
def on_press(key):
    try:       
        # Default key: f3
        # Replace f3 with any key you want to use (e.g. shift_r, alt_l, ctrl_r, esc, backspace, enter, down, up, esc, etc.)
        if(key_path):
            with open("key_compare", "w", encoding="utf-8") as f:
                f.write('{0}'.format(key))
            with open("keylog.txt", "r") as f:
                logged_key = f.read()
                with open("key_compare", "r") as f:
                    compare_key = f.read()
                    if(compare_key == logged_key):
                        #print("All good")
                        capture_screenshot()
                    else:
                        print("Please press ", logged_key)

                #print(logged_key)
                
        else:
            with open("keylog.txt", "w", encoding="utf-8") as f:
                f.write('{0}'.format(key))
        # if key == keyboard.Key.f3:
        #     capture_screenshot()
        #     #print(f'{key} pressed')
    except AttributeError:
        pass

# Create a listener for key presses
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
