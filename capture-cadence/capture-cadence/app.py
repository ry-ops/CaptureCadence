from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
import httpx, json, os
from dotenv import load_dotenv
import asyncio

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="capture_cadence/static"), name="static")
templates = Jinja2Templates(directory="capture_cadence/templates")

CONFIG_PATH = "capture_cadence/config.json"
scheduler = BackgroundScheduler()
scheduler.start()

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            json.dump({}, f)
    with open(CONFIG_PATH) as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

# Placeholder for UniFi Protect API interaction
async def take_snapshots():
    config = load_config()
    print("[Snapshot] Capturing snapshots for configured cameras...")
    # TODO: Insert UniFi Protect API snapshot logic here
    await asyncio.sleep(1)  # simulate async operation

async def capture_clips(duration):
    config = load_config()
    print(f"[Clip] Capturing video clips of {duration} seconds...")
    # TODO: Insert UniFi Protect API video clip recording logic here
    await asyncio.sleep(1)  # simulate async operation

def reschedule_tasks():
    scheduler.remove_all_jobs()
    config = load_config()
    if config.get("snapshot_interval"):
        scheduler.add_job(lambda: asyncio.create_task(take_snapshots()), 'interval', hours=int(config["snapshot_interval"]))
    if config.get("clip_interval") and config.get("clip_duration"):
        scheduler.add_job(lambda: asyncio.create_task(capture_clips(int(config["clip_duration"]))), 'interval', hours=int(config["clip_interval"]))

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
    await take_snapshots()
    return RedirectResponse(url="/", status_code=303)

@app.post("/clip-now")
async def manual_clip():
    config = load_config()
    duration = int(config.get("clip_duration", 30))
    await capture_clips(duration)
    return RedirectResponse(url="/", status_code=303)
