# Adds the "Follow the fundamentals" cut (money / moneyv) to studio.html.
#   python3 video/patches/money.py video/studio.html
import sys

p = sys.argv[1]
s = open(p).read()


def R(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)


# new places on the globe
R("""  bahrain: { name: 'Bahrain', c: [50.56, 26.07] },
};""", """  bahrain: { name: 'Bahrain', c: [50.56, 26.07] },
  rak: { name: 'Ras Al Khaimah', c: [55.94, 25.79] },
  fujairah: { name: 'Fujairah', c: [56.33, 25.12] },
  dubai: { name: 'Dubai', c: [55.27, 25.2] },
  lagos: { name: 'Lagos', c: [3.38, 6.52] },
  panama: { name: 'Panama City', c: [-79.52, 8.98] },
  mexico: { name: 'Mexico City', c: [-99.13, 19.43] },
  manila: { name: 'Manila', c: [120.98, 14.6] },
  sydney: { name: 'Sydney', c: [151.21, -33.87] },
};""")

# GlobeMove: configurable intro lines
R("""      headline(['What if', 'I *moved* it?'], portrait ? M : W * .6,""",
  """      headline(o.introLines || ['What if', 'I *moved* it?'], portrait ? M : W * .6,""")

# new scenes, inserted before the copy section
R("""// ---------- copy ----------""", """// ---------- "follow the fundamentals" scenes ----------
const KIT = [
  ['Culture', 'Louvre · Guggenheim · Zayed National Museum'],
  ['Faith', 'Abrahamic Family House'],
  ['Beach', '#19 in the world'],
  ['Capital', 'ADGM · BlackRock · J.P. Morgan'],
  ['Play', 'F1 · Sphere · Disney'],
  ['Move', 'Etihad Rail'],
];

function Kit(dur) {
  return { dur, bg: 'paper', draw(t) {
    headline(['Take', '*Abu Dhabi*.'], M, portrait ? H * .17 : H * .5, { size: (portrait ? 130 : 150) * s, anchor: portrait ? 'top' : undefined }, t);
    mono('The kit', M, portrait ? H * .15 : H * .5 - 190 * s, { color: P.orange, alpha: eo(seg(t, .2, .6)) });
    const x0 = portrait ? M : W * .45, x1 = W - M, top = portrait ? H * .42 : H * .2, rh = (portrait ? 118 : 116) * s;
    KIT.forEach(([cat, items], i) => {
      const at = .8 + i * (dur - 3) / KIT.length, a = eo(seg(t, at, at + .45)); if (a <= 0) return;
      const y = top + i * rh;
      ctx.globalAlpha = a;
      hair(x0, y, x0 + (x1 - x0) * eo(seg(t, at, at + .6)), y, P.ink, 1);
      mono(`0${i + 1}  ${cat}`, x0, y + 30 * s, { color: P.orange, size: 16 * s });
      head(items, x0, y + rh * .78, { size: (portrait ? 34 : 40) * s, weight: 700 });
      ctx.globalAlpha = 1;
    });
  } };
}

function Noise(dur) {
  const words = ['CRASH?', 'BUBBLE?', 'SLOWDOWN?', 'RATES?', 'PANIC?', 'SELL?'];
  // illustrative long run: drift up, two dips; not a forecast
  const r = rng(7), series = []; let v = 1;
  for (let i = 0; i < 300; i++) {
    v *= 1 + .0035 + (r() - .5) * .028 - (i >= 110 && i < 130 ? .013 : 0) - (i >= 268 && i < 288 ? .016 : 0);
    series.push(v);
  }
  return { dur, bg: 'paper', draw(t) {
    if (t < 4.6) {
      const rr = rng(3);
      words.forEach((w, i) => {
        const at = i * .45, a = eback(seg(t, at, at + .3)); if (a <= 0) return;
        const x = M + rr() * (W - 2 * M - 360 * s), y = H * .18 + rr() * H * .6, rot = (rr() - .5) * .3;
        ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(a, a);
        ctx.globalAlpha = clamp(a) * (t > 3.3 ? .18 : 1);
        setFont('mono', 44 * s, 500); const tw = ctx.measureText(w).width;
        ctx.fillStyle = P.orange; ctx.fillRect(-16 * s, -40 * s, tw + 32 * s, 64 * s);
        ctx.fillStyle = P.ink; ctx.textBaseline = 'middle'; ctx.fillText(w, 0, -8 * s);
        ctx.restore();
      });
      if (t > 3.3) headline(['That’s', '*noise*.'], M, H * .5, { size: (portrait ? 170 : 200) * s, out: eio(seg(t, 4.3, 4.6)) }, t - 3.3);
      return;
    }
    const lt = t - 4.6;
    const x0 = M, x1 = W - M, yb = portrait ? H * .72 : H * .8, yt = portrait ? H * .4 : H * .36;
    const z = eio(seg(lt, .8, 3.2)), a0 = lerp(.89, 0, z);
    const i0 = Math.floor(a0 * 299), win = series.slice(i0);
    const lo = lerp(Math.min(...win), Math.min(...series), z), hi = lerp(Math.max(...win), Math.max(...series), z);
    ctx.save(); ctx.strokeStyle = P.ink; ctx.lineWidth = 3.5 * s; ctx.beginPath();
    win.forEach((v, k) => { const x = lerp(x0, x1, k / (win.length - 1)), y = lerp(yb, yt, (v - lo) / (hi - lo)); k ? ctx.lineTo(x, y) : ctx.moveTo(x, y); });
    ctx.stroke(); ctx.restore();
    hair(x0, yb + 20 * s, x1, yb + 20 * s, P.ink, 1.5);
    mono(z < .5 ? 'Short term' : 'Mid to long term', x0, yb + 50 * s, { color: z < .5 ? P.orange : P.blue });
    mono('Illustrative. Not a forecast.', x1, yb + 50 * s, { align: 'right', size: 13 * s });
    const hs = (portrait ? 96 : 110) * s, hy = portrait ? H * .17 : H * .14;
    if (lt < 3.6) headline(['Zoom out.'], M, hy, { size: hs, anchor: 'top', out: eio(seg(lt, 3.3, 3.6)) }, lt);
    else headline(['Hold mid to long.', 'Let the *fundamentals* work.'], M, hy, { size: hs * .72, anchor: 'top' }, lt - 3.6);
  } };
}

// ---------- copy ----------""")

# copy + cut definitions
R("""const CUTS = {""", """const RIGHT = [
  { t: 0, lines: ['I’m *right brain*.'], kicker: 'How I see it' },
  { t: 1.6, lines: ['I think in', 'pictures.'] },
  { t: 3.2, lines: ['But numbers?'] },
  { t: 4.3, lines: ['_Vital_.'], size: 240 },
  { t: 5.4, lines: ['Parting with', 'cash?', 'You need', '*context*.'] },
  { t: 8, lines: ['That’s my *edge*.'], bg: 'ink', circle: 0 },
];
const FUND = [
  { t: 0, lines: ['Every time.'] },
  { t: 1.4, lines: ['*Fundamentals*', 'first.'] },
  { t: 3.1, lines: ['Money', '_follows_.'], bg: 'blue', size: 220 },
];
const MONEY = ['rak', 'fujairah', 'dubai', 'lagos', 'panama', 'mexico', 'manila', 'sydney'].map(k => [k, 'Would money|follow?', 'The whole kit']);
const moneyCut = v => () => [
  Beats(RIGHT, 10, { size: 170 }),
  Kit(12),
  GlobeMove(34, { intro: 2.4, moves: MONEY, introLines: ['Now', '*move* it.'] }),
  Beats(FUND, 5, { size: 190 }),
  Noise(12),
  Generational(8),
  Beats([{ t: 0, lines: ['Follow the', '*fundamentals*.'] }], 3.5, { bg: 'blue', size: 170 }),
  CTA(5, v ? { msg: 'Follow' } : {}),
];

const CUTS = {
  money: { w: 1920, h: 1080, scenes: moneyCut(false) },
  moneyv: { w: 1080, h: 1920, scenes: moneyCut(true) },""")

open(p, 'w').write(s)
print('patched', p)
