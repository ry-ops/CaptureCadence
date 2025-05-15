from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
from .snapshot import take_snapshots
from .clip import capture_clips
import os, json, asyncio
from dotenv import load_dotenv