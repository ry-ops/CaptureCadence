import asyncio
import json, os

CONFIG_PATH = "capture_cadence/config.json"
SNAPSHOTS_DIR = "capture_cadence/snapshots"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump({}, f)
    with open(CONFIG_PATH) as f:
        return json.load(f)

async def take_snapshots():
    config = load_config()
    print("[Snapshot] Capturing snapshots for configured cameras...")
    # TODO: Implement actual UniFi Protect API snapshot logic here
    # Save snapshot files to SNAPSHOTS_DIR
    await asyncio.sleep(1)  # simulate async operation
