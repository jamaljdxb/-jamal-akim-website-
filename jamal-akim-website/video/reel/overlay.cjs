// Streams overlay.html frames as PNGs (with alpha) to stdout.
//   node video/reel/overlay.cjs v|h | ffmpeg -f image2pipe -c:v png -i - ...
const path = require('path');
const { chromium } = require('playwright');

const mode = process.argv[2] || 'v', fps = 30;
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'overlay.html'));
  await page.evaluate(() => window.fontsReady);
  const dur = await page.evaluate(m => window.setup(m), mode);
  const frames = Math.round(dur * fps);
  for (let f = 0; f < frames; f += 10) {
    const imgs = await page.evaluate(([f0, n, fps]) => {
      const c = document.getElementById('c'), r = [];
      for (let i = 0; i < n; i++) { window.renderFrame((f0 + i) / fps); r.push(c.toDataURL('image/png')); }
      return r;
    }, [f, Math.min(10, frames - f), fps]);
    for (const d of imgs) {
      if (!process.stdout.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => process.stdout.once('drain', r));
    }
  }
  await browser.close();
})();
