from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .snapshot import take_snapshot
from .clip import create_clip

app = FastAPI(title="Capture Cadence")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/snapshot")
async def snapshot_endpoint():
    # Call the snapshot logic here
    success = take_snapshot()
    return {"success": success}


@app.post("/clip")
async def clip_endpoint():
    # Call the clip creation logic here
    success = create_clip()
    return {"success": success}
