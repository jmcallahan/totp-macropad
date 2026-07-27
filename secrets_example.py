# =============================================================================
# Adafruit MacroPad RP2040 - TOTP secrets
# =============================================================================
# These are base32 encoded seeds from your 2FA providers
# Populate this list by replacing "YOUR_BASE32_SEED_HERE" with your actual seed.
# Rename this file to "secrets.py" and fill in your actual values

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

# Physical key layout (Page 0)
layout = {
    "page_0": [
        ["svc_0", "svc_1", "svc_2", "svc_3"],       # Row 0 (top)
        ["svc_4", "svc_5", "svc_6", "svc_7"],       # Row 1 (middle)
        ["svc_8", "svc_9", "svc_10", "svc_11"],     # Row 2 (bottom)
    ],
}