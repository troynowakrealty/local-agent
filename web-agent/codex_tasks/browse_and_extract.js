const { chromium } = require('playwright');
const fs = require('fs');

async function main() {
  const data = JSON.parse(fs.readFileSync('data/siteplan_metadata.json', 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + process.cwd() + '/static_form.html');
  await page.fill('#owner', data.owner || '');
  await page.fill('#address', data.address || '');
  try {
    await page.click('#submit');
    await page.waitForTimeout(500);
    await browser.close();
    console.log('success');
  } catch (e) {
    await page.screenshot({ path: 'last_screenshot.png' });
    await browser.close();
    console.log('failed');
  }
}

if (require.main === module) {
  main();
}

module.exports = main;
