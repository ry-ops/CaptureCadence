import os
from datetime import datetime
import requests
from fastapi.responses import JSONResponse

def take_snapshot(ip, user, password, output_dir):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{ip.replace('.', '_')}_{now}.jpg"
    filepath = os.path.join(output_dir, filename)

    try:
        url = f"http://{ip}/snap.jpeg"
        response = requests.get(url, auth=(user, password), timeout=10)
        response.raise_for_status()
        os.makedirs(output_dir, exist_ok=True)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return JSONResponse(content={"message": f"Snapshot saved: {filename}"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
