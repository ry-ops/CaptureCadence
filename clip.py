import asyncio
import json, os

CONFIG_PATH = "capture_cadence/config.json"
CLIPS_DIR = "capture_cadence/clips"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump({}, f)
    with open(CONFIG_PATH) as f:
        return json.load(f)

async def capture_clips(duration):
    config = load_config()
    print(f"[Clip] Capturing video clips of {duration} seconds...")
    # TODO: Implement actual UniFi Protect API clip capture logic here
    # Save clip files to CLIPS_DIR
    await asyncio.sleep(1)  # simulate async operation
