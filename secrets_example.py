# =============================================================================
# secrets.py - Local config file (DO NOT COMMIT TO GITHUB)
# =============================================================================

secrets = {
    "pin": "1234",  # Your unlock PIN
    
    "svc_0": {
        "service": "amazon",
        "seed": "YOUR_BASE32_SEED_HERE",
        "display_name": "amzn",
        "color": (255, 165, 0),  # Orange
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
    # Add svc_5 through svc_11 as needed...
}

# Physical key layout (4 rows x 3 columns)
layout = {
    "page_0": [
        ["svc_0", "svc_1", "svc_2"],       # Top Row 0 (Keys 0, 1, 2)
        ["svc_3", "svc_4", "svc_5"],       # Mid-Top Row 1 (Keys 3, 4, 5)
        ["svc_6", "svc_7", "svc_8"],       # Mid-Bottom Row 2 (Keys 6, 7, 8)
        ["svc_9", "svc_10", "svc_11"],     # Bottom Row 3 (Keys 9, 10, 11)
    ],
}
