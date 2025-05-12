require('dotenv').config();
const fs = require('fs');
const path = require('path');

// Check for .env and create if missing
const envFilePath = path.join(__dirname, '.env');
if (!fs.existsSync(envFilePath)) {
  console.log('.env file not found, creating a default one...');
  fs.writeFileSync(envFilePath, `
PORT=3000
SCREENSHOT_INTERVAL_MINUTES=15
SAVE_DIRECTORY=./screenshots
BASE_FILENAME=default
REPLACE_EXISTING=true
`.trim());
  console.log('.env file created with default values.');
}

// Rest of your server code here...

const express = require('express');
const bodyParser = require('body-parser');
const puppeteer = require('./puppeteer');
const fs = require('fs');
const app = express();
const port = 3000;

let sites = [];

app.use(bodyParser.json());
app.use(express.static('ui'));
app.use('/screenshots', express.static('screenshots'));

app.post('/add-site', (req, res) => {
  const { url, interval, savePath, baseName } = req.body;
  const site = { url, interval, savePath, baseName };
  sites.push(site);
  saveAndSchedule(site);
  res.sendStatus(200);
});

function saveAndSchedule(site) {
  fs.writeFileSync('urls.json', JSON.stringify(sites, null, 2));
  setInterval(() => puppeteer.capture(site), site.interval * 60000);
}

function loadAndScheduleAll() {
  if (fs.existsSync('urls.json')) {
    sites = JSON.parse(fs.readFileSync('urls.json'));
    for (const site of sites) {
      setInterval(() => puppeteer.capture(site), site.interval * 60000);
    }
  }
}

app.listen(port, () => {
  loadAndScheduleAll();
  console.log(`App running at http://localhost:${port}`);
});
