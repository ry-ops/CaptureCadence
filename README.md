# ShotClock 🕒

**ShotClock** is a lightweight web app and Dockerized service that takes full-page screenshots of websites on a schedule. It uses [Puppeteer](https://pptr.dev/) for browser automation and provides a simple web interface to add, customize, and manage screenshot jobs.

## 🚀 Features

- 📸 Full-page screenshots of any URL
- 🕓 Customizable screenshot interval per site (in minutes)
- 🗂️ Choose the destination folder for each image
- 📝 Set a custom base name for saved files
- 🔁 Overwrite images automatically with consistent filenames (e.g. `duluth.webp`)
- 💾 Images saved in `.webp` format for efficient storage
- 🧰 Docker-ready for easy deployment

## 📦 Requirements

- [Docker](https://www.docker.com/) (for containerized setup)
- Or: Node.js (v18+) and npm for local development

## 🛠️ Local Development

Clone this repository and install dependencies:

```bash
git clone https://github.com/yourusername/shotclock.git
cd shotclock
npm install
npm start
````

Then open your browser to:
`http://localhost:3000`

## 🐳 Docker Usage

To build and run the app in a container:

```bash
docker build -t shotclock .
docker run -p 3000:3000 -v $(pwd)/screenshots:/app/screenshots shotclock
```

Access the web UI at:
`http://localhost:3000`

## 📁 Project Structure

```
.
├── Dockerfile
├── puppeteer.js       # Screenshot logic
├── server.js          # Express server & scheduler
├── urls.json          # Saved job config
├── ui/
│   └── index.html     # Web interface
└── screenshots/       # Output directory for .webp files
```

## ✏️ Usage

1. Open the web interface.
2. Enter:

   * The website URL
   * Interval in minutes
   * Optional: folder name (relative to project root, e.g. `Photos`)
   * Optional: base filename (e.g. `duluth`)
3. Click **Add Website**.
4. Screenshots will be automatically taken and saved on schedule.

---

## 🌍 Deployment

### 🚀 Deploy to Fly.io

1. **Install Fly CLI**:

   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**:

   ```bash
   fly auth login
   ```

3. **Create App**:

   ```bash
   fly launch
   ```

4. **Deploy**:

   ```bash
   fly deploy
   ```

5. Visit your app at `https://your-app.fly.dev`.

💾 **Optional: Add persistent storage**:

```bash
fly volumes create shotclock_data --size 1 --region <your-region>
```

Update `fly.toml`:

```toml
[mounts]
  source = "shotclock_data"
  destination = "/app/screenshots"
```

---

### 🧪 Deploy to Render.com

1. Push this project to GitHub.
2. Log into [Render](https://render.com).
3. Click **New Web Service**.
4. Connect your repo and choose:

   * **Environment**: Docker
   * **Start Command**: `npm start`
   * **Port**: `3000`
5. Render will build and deploy automatically.

---

## 📄 License

MIT License

---

Made with ❤️ using Puppeteer + Node.js

```

---

```
