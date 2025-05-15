import os
import subprocess
from datetime import datetime
from fastapi.responses import JSONResponse

def record_clip(ip, user, password, output_dir):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ip.replace('.', '_')}_{now}.mp4"
    output_path = os.path.join(output_dir, filename)

    try:
        stream_url = f"rtsp://{user}:{password}@{ip}:7447/stream"
        os.makedirs(output_dir, exist_ok=True)
        cmd = [
            "ffmpeg", "-y", "-i", stream_url,
            "-t", "00:00:10",
            "-c:v", "copy", "-an", output_path
        ]
        subprocess.run(cmd, check=True)
        return JSONResponse(content={"message": f"Clip saved: {filename}"})
    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
