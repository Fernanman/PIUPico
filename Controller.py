import time

import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

def mapping():
    """
    Up Left      - Q - GP4  - Breadboard row 11 - White
    Up Right     - E - GP9  - Breadboard row 17 - Brown
    Middle       - S - GP8  - Breadboard row 16 - Black
    Bottom Left  - Z - GP5  - Breadboard row 12 - Red
    Bottom Right - C - GP13 - Breadboard row 22 - Orange
    """

    # Mapping for the keys. Using dictionaries because they are constant time O(1).
    key_map = {0 : Keycode.Q, 
            1 : Keycode.E,
            2 : Keycode.S,
            3 : Keycode.Z,
            4 : Keycode.C
            }
    
    return key_map

def status_map():
    # Maps of the status of the arrows. Start at 1 since they are pull up.
    arrow_status = {0 : 1,
                    1 : 1,
                    2 : 1,
                    3 : 1,
                    4 : 1
                    }
    arrow_prev_status = {0 : 1,
                        1 : 1,
                        2 : 1,
                        3 : 1,
                        4 : 1
                        }
    
    return arrow_status, arrow_prev_status

def setup():
    keypress_pins = [board.GP4, board.GP9, board.GP8, board.GP5, board.GP13]
    # Pins after they've been made pull up
    pull_up_pins = []

    time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems

    # Make all pin objects inputs with pullups
    for pin in keypress_pins:
        key_pin = digitalio.DigitalInOut(pin)
        key_pin.direction = digitalio.Direction.INPUT
        key_pin.pull = digitalio.Pull.UP
        pull_up_pins.append(key_pin)


    print("Setup complete.")

    return pull_up_pins

def main():
    keyboard = Keyboard(usb_hid.devices)
    key_map = mapping()
    arrow_status, arrow_prev_status = status_map()
    pull_up_pins = setup()

    while True:
        # Check each pin
        for i, key_pin in enumerate(pull_up_pins):
            # Updates the status us the key pin.
            arrow_status[i] = key_pin.value 

            # Checks if the arrow is pressed.
            if arrow_status[i] != arrow_prev_status[i] and not arrow_status[i]:
                keyboard.press(key_map[i])
                arrow_prev_status[i] = arrow_status[i]

            # Cheks if the arrow has been released
            if arrow_status[i] != arrow_prev_status[i] and arrow_status[i]:
                keyboard.release(key_map[i])
                arrow_prev_status[i] = arrow_status[i]
                

if __name__ == "__main__":
    main()

