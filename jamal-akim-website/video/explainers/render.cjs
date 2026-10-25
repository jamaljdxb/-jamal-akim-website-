// Streams JPEG frames of an explainer page to stdout for ffmpeg.
//   node render.cjs <page.html> <v|sq|h> '<durations json>' [start end] | ffmpeg -f image2pipe -c:v mjpeg -framerate 30 -i - ...
const path = require('path');
const { chromium } = require('playwright');

const [page_, mode = 'v', dursJson = '[]', a, b] = process.argv.slice(2);
const fps = 30;
(async () => {
  const browser = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(page_));
  await page.evaluate(() => window.fontsReady);
  const dur = await page.evaluate(([m, d]) => window.setup(m, d), [mode, JSON.parse(dursJson)]);
  const f0 = a ? Math.round(+a * fps) : 0, f1 = b ? Math.min(Math.round(+b * fps), Math.round(dur * fps)) : Math.round(dur * fps);
  for (let f = f0; f < f1; f += 10) {
    const imgs = await page.evaluate(([f, n, fps]) => {
      const c = document.getElementById('c'), r = [];
      for (let i = 0; i < n; i++) { window.renderFrame((f + i) / fps); r.push(c.toDataURL('image/jpeg', 0.92)); }
      return r;
    }, [f, Math.min(10, f1 - f), fps]);
    for (const d of imgs) {
      if (!process.stdout.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => process.stdout.once('drain', r));
    }
  }
  await browser.close();
  process.stderr.write(`duration ${dur}\n`);
})();
