const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

module.exports = async function takeScreenshot(url, directory, baseName, replace) {
  const browser = await puppeteer.launch({
    headless: true, // headless mode is now explicitly a boolean in recent Puppeteer versions
    args: ['--no-sandbox', '--disable-setuid-sandbox'] // good for Docker compatibility
  });

  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle0' });
  await page.setViewport({ width: 1920, height: 1080 });

  if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
  }

  const filePath = path.join(directory, `${baseName}.webp`);
  if (!replace && fs.existsSync(filePath)) {
    console.log(`Skipping ${filePath} (already exists and replace is false)`);
    await browser.close();
    return;
  }

  await page.screenshot({
    path: filePath,
    type: 'webp',
    fullPage: true
  });

  await browser.close();
};
