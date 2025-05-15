from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .snapshot.py import take_snapshot
from .clip import record_clip

import json
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/snapshot")
async def snapshot(ip: str = Form(...), user: str = Form(...), password: str = Form(...), output: str = Form(...)):
    return take_snapshot(ip, user, password, output)

@app.post("/clip")
async def clip(ip: str = Form(...), user: str = Form(...), password: str = Form(...), output: str = Form(...)):
    return record_clip(ip, user, password, output)
