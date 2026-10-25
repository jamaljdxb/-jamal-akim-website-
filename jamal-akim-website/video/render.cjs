// Renders composer.html to MP4 frame by frame.
//   node video/render.cjs <cut> [out.mp4] [--fps 30]
//   node video/render.cjs <cut> --stills 3,12.5,40   (PNG frames for checking)
// Cuts: main (16:9 YouTube), hook, motivate, whatif, identity (9:16 Shorts/Reels/TikTok)
const http = require('http');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const { chromium } = require('playwright');

const args = process.argv.slice(2);
const cut = args[0] || 'main';
const flag = (name, def) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : def; };
const fps = +flag('--fps', 30);
const stills = flag('--stills');
const outDir = path.join(__dirname, 'out');
const out = args[1] && !args[1].startsWith('--') ? args[1] : path.join(outDir, `jamal-akim-${cut}.mp4`);

const types = { '.html': 'text/html', '.js': 'text/javascript', '.woff2': 'font/woff2' };
const server = http.createServer((req, res) => {
  const file = path.join(__dirname, decodeURIComponent(req.url.split('?')[0]));
  if (!file.startsWith(__dirname) || !fs.existsSync(file)) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': types[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

(async () => {
  await new Promise(r => server.listen(0, r));
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('pageerror', e => console.error('page error:', e.message));
  await page.goto(`http://localhost:${server.address().port}/composer.html`);
  await page.evaluate(() => window.fontsReady);
  const duration = await page.evaluate(c => window.setup(c), cut);
  fs.mkdirSync(outDir, { recursive: true });

  if (stills) {
    for (const t of stills.split(',').map(Number)) {
      const data = await page.evaluate(t => { window.renderFrame(t); return document.getElementById('c').toDataURL('image/png'); }, t);
      const f = path.join(outDir, `still-${cut}-${t}.png`);
      fs.writeFileSync(f, Buffer.from(data.split(',')[1], 'base64'));
      console.log(f);
    }
  } else {
    const frames = Math.round(duration * fps);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error',
      '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p',
      '-c:a', 'aac', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const batch = 15;
    for (let f = 0; f < frames; f += batch) {
      const imgs = await page.evaluate(([f0, n, fps]) => {
        const c = document.getElementById('c'), r = [];
        for (let i = 0; i < n; i++) { window.renderFrame((f0 + i) / fps); r.push(c.toDataURL('image/jpeg', 0.93)); }
        return r;
      }, [f, Math.min(batch, frames - f), fps]);
      for (const d of imgs) {
        if (!ff.stdin.write(Buffer.from(d.split(',')[1], 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
      }
      if (f % (fps * 10) < batch) process.stdout.write(`\r${cut}: ${Math.round(100 * f / frames)}%`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
    console.log(`\n${out} (${duration.toFixed(1)}s)`);
  }
  await browser.close();
  server.close();
})();
