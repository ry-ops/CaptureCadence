const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

exports.capture = async function (site) {
  const { url, savePath = 'screenshots', baseName } = site;
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle0' });

  const directory = path.resolve(savePath);
  if (!fs.existsSync(directory)) {
    fs.mkdirSync(directory, { recursive: true });
  }

  const filename = baseName ? `${baseName}.webp` :
    url.replace(/https?:\/\//, '').replace(/[^\w]/g, '_') +
    `_${new Date().toISOString().replace(/[:.]/g, '-')}.webp`;

  const filepath = path.join(directory, filename);
  await page.screenshot({ path: filepath, fullPage: true, type: 'webp' });
  await browser.close();
};
