"""here be secrets"""
# =============================================================================
# Adafruit MacroPad RP2040 - TOTP secrets
# =============================================================================
# These are base32 encoded seeds from your 2FA providers
# Populate this list by replacing "YOUR_BASE32_SEED_HERE" with your actual seed.
# Rename this file to "secrets.py" and fill in your actual values
from adafruit_macropad import MacroPad

macropad = MacroPad()

def update_key_leds(page_name="page_0"):
    key_idx = 0
    for row in layout[page_name]:
        for service_key in row:
            if is_service_defined(service_key):
                color = secrets[service_key]["color"]
                brightness = secrets[service_key]["brightness"] / 100.0 #scale 0-100 to 0.0-1.0

                # Scale RGB color by brightness factor
                scaled_color = (
                    int(color[0] * brightness),
                    int(color[1] * brightness),
                    int(color[2] * brightness)
                )
                macropad.pixels[key_idx] = scaled_color
            else:
                macropad.pixels[key_idx] = (0, 0, 0) # Turns off LED for undefined services on that page.

            key_idx += 1

secrets = {
    "svc_0": {
        "service": "amazon",
        "seed": "YOUR_BASE32_SEED_HERE",
        "display_name": "amzn",
#		"led_effect": "breathing", --phase 2 addition
        "color": (255, 165, 0),  # Orange
#		"color_2": (255, 255, 255), # RGB White --phase 2 addition        
        "brightness": 80,
    },
    "svc_1": {
        "service": "instagram",
        "seed": "YOUR_BASE32_SEED_HERE",
        "display_name": "insta",
        "color": (0, 255, 255),  # Cyan
        "brightness": 80,
    },
    "svc_2": {
        "service": "github",
        "seed": "YOUR_BASE32_SEED_HERE",
        "display_name": "github",
        "color": (255, 255, 255),  # White
        "brightness": 80,
    },
    "svc_3": {
        "service": "google",
        "seed": "YOUR_BASE32_SEED_HERE",
        "display_name": "google",
        "color": (74, 144, 226),  # Blue
        "brightness": 80,
    },
    "svc_4": {
        "service": "twitter",
        "seed": "YOUR_BASE32_SEED_HERE",
        "display_name": "x",
        "color": (0, 0, 0),  # Black
        "brightness": 80,
    },
    # ... continue svc_5 through svc_11 ...
    # "svc_11": {
    #     "service": "YOUR_SERVICE_HERE",
    #     "seed": "YOUR_BASE32_SEED_HERE",
    #     "display_name": "display",
    #     "color": (255, 0, 0),  # Red
    #     "brightness": 80,
    # },
}

# Physical key layout (Page 0) - 4 rows x 3 columns
layout = {
    "page_0": [
        ["svc_0", "svc_1", "svc_2"],       # Top Row 0 (Keys 0, 1, 2)
        ["svc_3", "svc_4", "svc_5"],       # Mid-Top Row 1 (Keys 3, 4, 5)
        ["svc_6", "svc_7", "svc_8"],       # Mid-Bottom Row 2 (Keys 6, 7, 8)
        ["svc_9", "svc_10", "svc_11"],     # Bottom Row 3 (Keys 9, 10, 11)
    ],
} 
# End-of-file (EOF)