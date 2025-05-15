from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
import os
import uuid

from app.unifi_client import UniFiClient
from app.scheduler import scheduler, scheduled_jobs

router = APIRouter()

_settings = None  # Will be set by main app startup with config

class Settings(BaseModel):
    unifi_ip: str
    api_key: str
    username: str
    password: str
    output_folder: str

def set_settings(settings: Settings):
    global _settings
    _settings = settings

# Capture still endpoint
@router.post("/capture/still")
async def capture_still(camera_id: str, background_tasks: BackgroundTasks):
    if _settings is None:
        raise HTTPException(status_code=400, detail="Settings not configured")
    client = UniFiClient(
        _settings.unifi_ip, _settings.api_key, _settings.username, _settings.password
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{camera_id}_still_{timestamp}.jpg"
    output_path = os.path.join(_settings.output_folder, filename)

    background_tasks.add_task(client.capture_still, camera_id, output_path)
    return {"message": "Capture started", "filename": filename}

# Capture video endpoint
@router.post("/capture/video")
async def capture_video(camera_id: str, length_sec: int, background_tasks: BackgroundTasks):
    if _settings is None:
        raise HTTPException(status_code=400, detail="Settings not configured")
    client = UniFiClient(
        _settings.unifi_ip, _settings.api_key, _settings.username, _settings.password
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{camera_id}_video_{timestamp}.mp4"
    output_path = os.path.join(_settings.output_folder, filename)

    background_tasks.add_task(client.capture_video, camera_id, length_sec, output_path)
    return {"message": "Video capture started", "filename": filename}

# Schedule APIs
class ScheduleStillRequest(BaseModel):
    camera_id: str
    interval_minutes: int  # every X minutes

class ScheduleVideoRequest(BaseModel):
    camera_id: str
    cron: str  # cron expression
    length_sec: int

@router.post("/schedule/still")
async def schedule_still_capture(req: ScheduleStillRequest):
    if _settings is None:
        raise HTTPException(400, "Settings not configured")
    client = UniFiClient(
        _settings.unifi_ip, _settings.api_key, _settings.username, _settings.password
    )
    job_id = str(uuid.uuid4())

    def job():
        import asyncio
        asyncio.create_task(
            client.capture_still(req.camera_id, f"{_settings.output_folder}/{req.camera_id}_scheduled_still_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
        )

    scheduler.add_job(job, 'interval', minutes=req.interval_minutes, id=job_id)
    scheduled_jobs[job_id] = {
        "type": "still",
        "camera_id": req.camera_id,
        "interval_minutes": req.interval_minutes,
    }
    return {"message": "Scheduled still capture added", "job_id": job_id}

@router.post("/schedule/video")
async def schedule_video_capture(req: ScheduleVideoRequest):
    if _settings is None:
        raise HTTPException(400, "Settings not configured")
    client = UniFiClient(
        _settings.unifi_ip, _settings.api_key, _settings.username, _settings.password
    )
    job_id = str(uuid.uuid4())

    def job():
        import asyncio
        asyncio.create_task(
            client.capture_video(req.camera_id, req.length_sec, f"{_settings.output_folder}/{req.camera_id}_scheduled_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        )

    try:
        trigger = scheduler._create_trigger_from_cron(req.cron)
    except Exception as e:
        # Fallback to manual CronTrigger parse
        from apscheduler.triggers.cron import CronTrigger
        try:
            trigger = CronTrigger.from_crontab(req.cron)
        except Exception as e2:
            raise HTTPException(400, f"Invalid cron expression: {e2}")

    scheduler.add_job(job, trigger, id=job_id)
    scheduled_jobs[job_id] = {
        "type": "video",
        "camera_id": req.camera_id,
        "cron": req.cron,
        "length_sec": req.length_sec,
    }
    return {"message": "Scheduled video capture added", "job_id": job_id}

@router.get("/schedule/list")
async def list_schedules():
    return scheduled_jobs

@router.delete("/schedule/remove")
async def remove_schedule(job_id: str = Query(...)):
    if job_id not in scheduled_jobs:
        raise HTTPException(404, "Schedule not found")
    scheduler.remove_job(job_id)
    del scheduled_jobs[job_id]
    return {"message": "Schedule removed"}
