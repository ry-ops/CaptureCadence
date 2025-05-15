from fastapi import FastAPI
from app.api import router, set_settings
from app.models import Settings  # create this if needed

app = FastAPI()

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Capture Cadence backend is running"}
    
@app.on_event("startup")
async def startup_event():
    # Load your config however you want — environment variables, file, etc.
    settings = Settings(
        unifi_ip="192.168.1.100",
        api_key="your_api_key_here",
        username="admin",
        password="your_password",
        output_folder="/data",
    )
    set_settings(settings)
