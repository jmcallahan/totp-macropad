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

failed_attempts = 0
lockout_until = 0
user_pin = ""

# --- Keypad Map ---
NUMPAD_MAP = [
    "1", "2", "3", # Keys 0, 1, 2
    "4", "5", "6", # Keys 3, 4, 5
    "7", "8", "9", # Keys 6, 7, 8
    "CLR", "0", "ABT" # Keys 9, 10, 11
]

# --- Helper Functions ---

def sync_time_from_serial():
    """Checks USB Serial for timestamp and updates internal RTC."""
    if usb_cdc.console.in_waiting > 0:
        try: # Read line and  clean up extra whitespace
            line = usb_cdc.console.readline().decode('utf-8').strip()

            # Looks for the 'T' prefix followed by the rest of the timestamp.
            if line.startswith('T') and line[1:].isdigit():
                epoch = int(line[1:])
                r.datetime = time.localtime(epoch)
                return True
        except Exception as e:
            print("Serial Sync Error:", e)

    return False

def set_locked_leds():
    """Sets all key pixels to solid red indicating locked state."""
    for i in range(12):
        macropad.pixels[i] = (255, 0, 0)

def access_denied_flash():
    """Flashes LEDS red and blue - three sets of 2 flashes"""
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    for _ in range(3):
        macropad.pixels.fill(RED)
        time.sleep(0.3)
        macropad.pixels.fill(0, 0, 0)
        time.sleep(0.2)
        macropad.pixels.fill(RED)
        time.sleep(0.3)
        macropad.pixels.fill(0, 0, 0)
        time.sleep(0.5)
        macropad.pixels.fill(BLUE)
        time.sleep(0.3)
        macropad.pixels.fill(0, 0, 0)
        time.sleep(0.2)
        macropad.pixels.fill(BLUE)
        time.sleep(0.3)
        macropad.pixels.fill(0, 0, 0)
        time.sleep(0.5)        

def is_service_defined(service_key):
    """Check if a service exists in secrets and has a valid seed configured."""
    if service_key in secrets:
        seed = secrets[service_key].get("seed", "")
        return seed not in ["YOUR_BASE32_SEED_HERE", "NULL", ""]
    return False

def update_key_leds(page_name="page_0"):
    """Applies individual color and brightness to physical key LEDs."""
    key_idx = 0
    for row in layout[page_name]:
        for service_key in row:
            if is_service_defined(service_key):
                color = secrets[service_key]["color"]
                # Scale brightness (0-100%) to a float factor (0.0 - 1.0)
                brightness_factor = secrets[service_key]["brightness"] / 100.0               
                scaled_color = (
                    int(color[0] * brightness_factor),
                    int(color[1] * brightness_factor),
                    int(color[2] * brightness_factor)
                )
                macropad.pixels[key_idx] = scaled_color
            else:
                macropad.pixels[key_idx] = (0, 0, 0)  # Off            
            key_idx += 1


# --- User Pin & Pin Processing Functions ---
def user_pin():
    """Returns the user-defined PIN from secrets."""
    return secrets.get("pin", "")

def process_pin_key(key_num):
    """Processes a key press in the context of PIN entry."""
    global user_pin, current_state, failed_attempts, lockout_until

    current_time = time.monotonic()

    # Check for lockout
    if current)time < lockout_until:
        remaining_seconds = int(lockout_until - current_time)
        macropad.display_text[0].text = "LOCKOUT ACTIVE"
        macropad.display_text[1].text = "TRY AGAIN IN {remaining_seconds}s"
        return

action = NUMPAD_MAP[key_num]

# --- Cancel & Clear / Abort & Sleep input actions ---
if action in ["CLR", "ABT"]:
    user_pin = ""
    macropad.display_text[)].text = "Enter PIN:"
    macropad.display_text[1].text = ""
    set_locked_leds()
    return

# --- Pin Digit Entry ---
target_pin = secrets.get("pin", "")
user_pin += action

# hide yo digits baby! ---
macropad.display_text[0].text = "Enter PIN:"
macropad.display_text[1].text = "*" * len(user_pin)

# --- Auto-accept PIN when it matches expected length ---
if len(user_pin) == len(target_pin):
    if user_pin == target_pin:
        # SUCCESS - you just unlocked your own shit!
        current_state = STATE_UNLOCKED
        failed_attempts = 0 # REset lockout counter and timer
        user_pin = ""
        update_key)leds()
        macropad.display_text[0].text = "UNLOCKED"
        macropad.display_text[1].text = ""
    else:
        # FAILURE - HAHA YOU SUCK AGAIN!!!
        failed_attempts += 1
        lockout_secs = get_lockout_duration(failed_attempts)
        lockout_until = current_time + lockout_secs

        access_denied_flash()
        user_pin = ""

        if lockout_secs > 0:
            macropad.display_text[0].text = "LOCKED OUT"
            macropad.display_text[1].text = f"WAIT  {lockout_secs // 60}m"
        else:
            macropad.display_text[0].text = "WRONG PIN"
            macropad.display_text[1].text = f"Attempts: {failed_attempts}"
            set_locked_leds()
