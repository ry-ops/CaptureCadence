import os
from datetime import datetime

def record_clip(duration_seconds: int = 10) -> bool:
    """
    Simulate recording a video clip from a camera.
    Saves a dummy video file to clips folder.
    """
    try:
        clips_dir = os.path.join("app", "static", "clips")
        os.makedirs(clips_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"clip_{timestamp}.mp4"
        filepath = os.path.join(clips_dir, filename)

        # For now, just create an empty file to simulate video clip
        with open(filepath, "wb") as f:
            f.write(b"")  # Replace with actual video data in real usage

        return True
    except Exception as e:
        print(f"Error recording clip: {e}")
        return False
