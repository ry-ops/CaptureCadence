![Alt text](https://github.com/ry-ops/CaptureCadence/blob/main/CaptureCadence.jpg)

# 🎥✨ Capture-Cadence

> Automate UniFi Protect camera snapshots & clips — beautifully, simply, on your own terms.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/Powered%20by-FastAPI-009688?logo=fastapi)
![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🔧 What is Capture-Cadence?

**Capture-Cadence** is your ✨ personal UniFi Protect assistant ✨ — a Python-powered scheduler and admin portal for:

- 📸 **Taking camera snapshots** at regular intervals
- 🎞️ **Recording video clips** on a customizable schedule
- 🧠 **Managing settings via a clean web portal**
- 🧰 Built with `FastAPI`, `APScheduler`, and `httpx`

Perfect for Raspberry Pi, home labs, small businesses, or anyone with a UniFi camera system looking to automate time-based media capture!

---

## 🌟 Features

✅ Snapshot scheduler (e.g. every hour)  
✅ Video clip recorder (custom duration + interval)  
✅ Web-based Admin Portal for live config  
✅ Manual "snap now" / "record now" buttons  
✅ Stores snapshots and clips in organized folders  
✅ Runs on Pi, Linux, or inside Docker 🐳  
✅ Lightweight & local — no cloud required

---

## 🖥️ Admin Portal

> Accessible via `http://<your-device-ip>:8000`

Easily configure:

- 🌐 UniFi Host IP
- 👤 Username & 🔐 Password
- 🕒 Snapshot & Clip Frequency
- ⏱️ Clip Duration
- 📁 Output Directory

---

## 🚀 Getting Started

### 🧪 Requirements

- Python 3.9+ or Docker
- Raspberry Pi / Linux / Mac / WSL / etc.
- UniFi Protect cameras on the same network

---

### 🛠 Installation

```bash
git clone https://github.com/ry-ops/capture-cadence.git
cd capture-cadence
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
````

Update `.env` with your UniFi details and desired output location.

---

### ▶️ Run the App

```bash
python3 -m capture_cadence.app
```

Visit `http://localhost:8000` in your browser 🎉

---

### 🐳 Docker (optional)

```bash
docker build -t capture-cadence .
docker run -d -p 8000:8000 --name cadence capture-cadence
```

---

## 📂 Project Structure

```
capture-cadence/
├── .env
├── Dockerfile
├── README.md
├── requirements.txt
├── config.json
├── app/
│   ├── __init__.py
│   ├── main.py          # (formerly app.py)
│   ├── snapshot.py
│   ├── clip.py
│   ├── static/
│   │   └── style.css    # example static file
│   ├── templates/
│   │   └── index.html   # example Jinja2 template
│   ├── snapshots/       # stores snapshot images
│   └── clips/           # stores video clips
└── CaptureCadence.png

...


## 🔮 Coming Soon

* 🗃️ Multi-camera support
* 🧪 Health checks & logs in UI
* ⏰ More scheduling options (e.g. CRON)
* ☁️ Optional cloud upload targets

---

## 🤝 Contribute

Pull requests are welcome! If you'd like to add features or suggest ideas, open an issue or fork the project 🚀

---

## 📜 License

Licensed under the MIT License — free for personal or commercial use.

---

## 👋 Made with 🧡 by ry-ops.dev

Got feedback? Want to show off how you’re using Capture Cadence? Open a discussion or tag the repo ⭐

---
