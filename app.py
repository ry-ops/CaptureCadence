from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
import os, json, asyncio
from dotenv import load_dotenv

import snapshot
import clip

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

CONFIG_PATH = "config.json"
CLIPS_DIR = "clips"
SNAPSHOTS_DIR = "snapshots"
scheduler = BackgroundScheduler()
scheduler.start()

os.makedirs(CLIPS_DIR, exist_ok=True)
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump({}, f)
    with open(CONFIG_PATH) as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def reschedule_tasks():
    scheduler.remove_all_jobs()
    config = load_config()
    if config.get("snapshot_interval"):
        scheduler.add_job(lambda: asyncio.create_task(snapshot.take_snapshots()), 'interval', hours=int(config["snapshot_interval"]))
    if config.get("clip_interval") and config.get("clip_duration"):
        scheduler.add_job(lambda: asyncio.create_task(clip.capture_clips(int(config["clip_duration"]))), 'interval', hours=int(config["clip_interval"]))

@app.on_event("startup")
async def startup_event():
    reschedule_tasks()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    config = load_config()
    return templates.TemplateResponse("index.html", {"request": request, "config": config})

@app.post("/save")
async def save_settings(
    request: Request,
    host: str = Form(...),
    user: str = Form(...),
    password: str = Form(...),
    snapshot_interval: int = Form(...),
    clip_interval: int = Form(...),
    clip_duration: int = Form(...),
    output_dir: str = Form(...)
):
    config = {
        "host": host,
        "user": user,
        "password": password,
        "snapshot_interval": snapshot_interval,
        "clip_interval": clip_interval,
        "clip_duration": clip_duration,
        "output_dir": output_dir
    }
    save_config(config)
    reschedule_tasks()
    return RedirectResponse(url="/", status_code=303)

@app.post("/snapshot-now")
async def manual_snapshot():
    await snapshot.take_snapshots()
    return RedirectResponse(url="/", status_code=303)

@app.post("/clip-now")
async def manual_clip():
    config = load_config()
    duration = int(config.get("clip_duration", 30))
    await clip.capture_clips(duration)
    return RedirectResponse(url="/", status_code=303)
