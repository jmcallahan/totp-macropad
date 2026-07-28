import time
import rtc
import usb_cdc
from adafruit_macropad import MacroPad
from secrets import secrets, layout

# --- Hardware Initialization ---
macropad = MacroPad()
r = rtc.RTC()
macropad.pixels.brightness = 0.3

# --- State Constants ---
STATE_LOCKED = 0
STATE_WAIT_SYNC = 1
STATE_UNLOCKED = 2

current_state = STATE_LOCKED

def sync_time_from_serial():
    """Checks USB Serial for timestamp and updates internal RTC."""
    if usb_cdc.console.in_waiting > 0:
        # Process the incoming time data
        int(usb_cdc.console.readline().decode('utf-8'))
    line = usb
time.localtime(epoch)
r.datetime = time.localtime(epoch)
