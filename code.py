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
last_activity_time = time.monotonic()

# --- Keypad Map ---
NUMPAD_MAP = [
    "1", "2", "3",    # Keys 0, 1, 2
    "4", "5", "6",    # Keys 3, 4, 5
    "7", "8", "9",    # Keys 6, 7, 8
    "CLR", "0", "ABT" # Keys 9, 10, 11
]

# --- User Preferences ---
ENABLE_AUTO_LOCK = True  # Toggles idle timeout auto-lock
AUTO_LOCK_DELAY = 60 

# --- Helper Functions ---

def sync_time_from_serial():
    """Checks USB Serial for timestamp and updates internal RTC."""
    if usb_cdc.console.in_waiting > 0:
        try:
            line = usb_cdc.console.readline().decode('utf-8').strip()
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
    """Flashes LEDS red and blue - three sets of 2 flashes."""
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    for _ in range(3):
        macropad.pixels.fill(RED)
        time.sleep(0.1)
        macropad.pixels.fill(BLACK)
        time.sleep(0.05)
        macropad.pixels.fill(BLUE)
        time.sleep(0.1)
        macropad.pixels.fill(BLACK)
        time.sleep(0.05)

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

def get_lockout_duration(attempts):
    """Calculates progressive lockout duration in seconds."""
    if attempts < 3:
        return 0
    elif attempts == 3:
        return 60    # 1 Minute
    elif attempts == 4:
        return 300   # 5 Minutes
    else:
        return 900   # 15 Minutes

def active_totp_code():
    """Placeholder: Returns current 6-digit TOTP code."""
    if current_state != STATE_UNLOCKED:
        return "LOCKED"
    # Placeholder code until TOTP math engine is linked
    return "123456"

def process_pin_key(key_num):
    """Processes a key press in the context of PIN entry."""
    global user_pin, current_state, failed_attempts, lockout_until

    current_time = time.monotonic()

    # 1. Check for active lockout
    if current_time < lockout_until:
        remaining_seconds = int(lockout_until - current_time)
        macropad.display_text[0].text = "LOCKOUT ACTIVE"
        macropad.display_text[1].text = f"TRY AGAIN IN {remaining_seconds}s"
        return

    action = NUMPAD_MAP[key_num]

    # 2. Cancel / Clear input actions
    if action in ["CLR", "ABT"]:
        user_pin = ""
        macropad.display_text[0].text = "Enter PIN:"
        macropad.display_text[1].text = ""
        set_locked_leds()
        return

    # 3. Digit Entry
    target_pin = secrets.get("pin", "1234")
    user_pin += action

    # Hide digits on OLED
    macropad.display_text[0].text = "Enter PIN:"
    macropad.display_text[1].text = "*" * len(user_pin)

    # 4. Auto-accept PIN when length matches target
    if len(user_pin) == len(target_pin):
        if user_pin == target_pin:
            # SUCCESS
            current_state = STATE_UNLOCKED
            failed_attempts = 0
            user_pin = ""
            update_key_leds()
            macropad.display_text[0].text = "UNLOCKED"
            macropad.display_text[1].text = ""
        else:
            # FAILURE
            failed_attempts += 1
            lockout_secs = get_lockout_duration(failed_attempts)
            lockout_until = current_time + lockout_secs

            access_denied_flash()
            user_pin = ""

            if lockout_secs > 0:
                macropad.display_text[0].text = "LOCKED OUT"
                macropad.display_text[1].text = f"WAIT {lockout_secs // 60}m"
            else:
                macropad.display_text[0].text = "WRONG PIN"
                macropad.display_text[1].text = f"Attempts: {failed_attempts}"
                set_locked_leds()

# --- Boot Initialization ---
set_locked_leds()
macropad.display_text[0].text = "LOCKED"
macropad.display_text[1].text = "Enter PIN"

keys_held = set()

# =============================================================================
# MAIN RUNTIME LOOP
# =============================================================================
while True:
    # 1. Background USB Serial Time Sync
    sync_time_from_serial()

    # 2. Idle Timeout Auto-Lock Check
    if ENABLE_AUTO_LOCK and current_state == STATE_UNLOCKED:
        if time.monotonic() - last_activity_time >= AUTO_LOCK_DELAY:
            current_state = STATE_LOCKED
            set_locked_leds()
            macropad.display_text[0].text = "LOCKED"
            macropad.display_text[1].text = ""
            user_pin = ""

    # 3. Handle Key Events
    key_event = macropad.keys.events.get()
    if key_event:
        last_activity_time = time.monotonic()
        
        if key_event.pressed:
            keys_held.add(key_event.key_number)
            
            # Check for Dual-Key Lock Combo (Keys 9 and 11 held together)
            if 9 in keys_held and 11 in keys_held:
                current_state = STATE_LOCKED
                set_locked_leds()
                macropad.display_text[0].text = "LOCKED"
                macropad.display_text[1].text = ""
                user_pin = ""
                keys_held.clear()
                continue

            # Handle normal single keypresses based on State
            if current_state == STATE_LOCKED:
                process_pin_key(key_event.key_number)
            elif current_state == STATE_UNLOCKED:
                # Keypress in unlocked state (Displays account details)
                macropad.display_text[0].text = f"Key {key_event.key_number}"

        elif key_event.released:
            keys_held.discard(key_event.key_number)

    # 4. Handle Rotary Encoder Press (Type TOTP into browser)
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        last_activity_time = time.monotonic()
        if current_state == STATE_UNLOCKED:
            code = active_totp_code()
            macropad.keyboard_layout.write(code)
            macropad.keyboard.send(macropad.Keycode.ENTER)
            macropad.display_text[1].text = "Sent to PC!"
        elif current_state == STATE_LOCKED:
            # Reset PIN entry on click if locked
            user_pin = ""
            macropad.display_text[1].text = ""
