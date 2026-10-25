# "How I See It": brand video kit

Motion-graphics videos for YouTube, Instagram and TikTok, built in the site's brand (ink, paper, brass, DM Serif Display and Inter).

## The videos (`video/out/`)

| File | Format | Length | Use it for |
|---|---|---|---|
| `jamal-akim-main.mp4` | 16:9, 1920×1080 | ~3:40 | **YouTube main video.** The full story |
| `jamal-akim-whatif.mp4` | 9:16, 1080×1920 | ~68s | Shorts / Reels / TikTok. The "move Saadiyat to your city" map game |
| `jamal-akim-motivate.mp4` | 9:16 | ~21s | Option 2. "Built different" |
| `jamal-akim-identity.mp4` | 9:16 | ~16s | Option 1. "That's my edge" |
| `jamal-akim-hook.mp4` | 9:16 | ~11s | Option 3. Punchy hook ("Try me.") |

**Voiced versions** (AI voiceover plus a soft music bed, scenes re-timed to the voice) are rendered by `mix.py` and saved to the Higgsfield library as `jamal-akim-<cut>-voiced.mp4`. The voiced main video runs about 4:17. Lines and timings are in `audio/lines.md` and `audio/timing.json`. To use your own voice instead, record each line in `audio/lines.md` and re-run `mix.py` with your files.

The files in `out/` are the **silent** versions. Record your own voice over the top (CapCut, Premiere or the in-app editor) using the script below. On IG and TikTok, add a trending sound from inside the app. The on-screen text already works as captions for people watching with the sound off.

## Voiceover script for the main video (read along with the timings)

| Time | On screen | Say |
|---|---|---|
| 0:00 | Hook | "I'm dyslexic. I can't spell. But I can create. I can build. I can out-think. Try me." |
| 0:08 | How I'm wired | "I'm ADHD. I'm dyslexic. And yeah… I can do things most people can't. Because I see things most people don't. That's not my weakness. That's my edge." |
| 0:22 | Title | "I'm Jamal Akim. Property, business, people. Let me show you how I see things." |
| 0:28 | Maths F / Finance A | "I failed maths… but got an A in finance. Same brain. The difference? Context. Give me a story or a picture and I see everything." |
| 0:42 | Context icons | "My brain runs on context: stories, visuals, graphs, maps. Not just words on a page." |
| 0:49 | Fundamentals | "Before the hype, the basics. The water, the rice, the staple. In property that's location, infrastructure, scarcity. Get those right and everything else is seasoning." |
| 1:02 | Seen it | "You've seen the news. You've seen the content. You've reviewed the numbers. Now let me show you how I see it." |
| 1:11 | Globe → Saadiyat | "Saadiyat Island, Abu Dhabi. The Louvre. The Guggenheim. Zayed National Museum. The Abrahamic Family House: a mosque, a church and a synagogue, side by side. The 19th best beach in the world. And one of the top three luxury hotel brands in the world, in negotiation to come." |
| 1:25 | Across Abu Dhabi | "And zoom out. ADGM: Wall Street is essentially moving in. BlackRock, J.P. Morgan, family offices. Formula 1 at Yas Marina. The Sphere is coming. A Disney park announced. Etihad Rail connecting it all." |
| 1:35 | What if… | "Now… what if I moved it? Put the Louvre and a top-20 beach in Hatfield, Hertfordshire: would prices go up? Put ADGM, Wall Street moving in, in Newcastle: what would that show? F1 and the Sphere in Paris: would the world fly in? A mosque, church and synagogue side by side in Madrid: what would it say about the city? BlackRock, J.P. Morgan and family offices in California: would capital follow? All of it in Bahrain: would the region change?" |
| 2:15 | Already here | "We don't have to imagine. It's already here." |
| 2:21 | Beach | "Number 19 in the world. Crisp blue water. But other top beaches don't have a museum next door, or a whole cultural district. That's why it's number one to me. Mo at Aldar made me see it this way." |
| 2:38 | Scarcity | "Eighteen thousand new homes planned. Fewer than eighteen hundred will be villas and mansions. The most premium land. The most premium location." |
| 2:52 | Aldar | "And then the developer moved. Aldar, government-backed, and they never do this: 50/50, 5% down, a waiver and strong incentives. SEI Saadiyat. Saadiyat Grove, The Designer. Baccarat." |
| 3:05 | Generational | "Real estate is generational. You, your kids, their kids. Location, infrastructure, scarcity. That's how I see it." |
| 3:13 | Built different | "They called it a disorder. I call it an advantage. ADHD means I think fast, build fast, move fast. Dyslexia means I see the picture when others only see the words. I'm not broken. I'm built different." |
| 3:32 | End card | "Subscribe, and let's talk." |

## Post copy

**YouTube title:** I Failed Maths, Got an A in Finance. Here's How I See Property
**YouTube description:**
> I'm ADHD and dyslexic, and it's my edge. My brain runs on context: stories, maps, visuals. So here's how I see Saadiyat Island, Abu Dhabi: what if you moved the Louvre, the Guggenheim, a top-19 beach and a top luxury hotel to Hatfield, Newcastle, Paris or Madrid? What would happen to prices? We don't have to imagine. It's already here.
> Not financial advice. Figures from developer and public sources at time of recording. Always verify.

**Shorts / Reels / TikTok caption (what-if cut):** What if I moved Abu Dhabi's best address to YOUR city? 🌍 Would prices go up? #RealEstate #AbuDhabi #Saadiyat #PropertyInvestment #ADHD #Dyslexia
**Caption (hook / motivate / identity):** Dyslexic. ADHD. Built different. #ADHD #Dyslexia #Entrepreneur #Mindset

## Check before posting

- Confirm Sphere Abu Dhabi and the Disney park are still on track (both announced for Yas Island), and confirm the payment plan, the waiver and incentives, the "#19 beach" ranking, the luxury-hotel negotiation and the 18,000 / 1,800 homes figures against Aldar's current broker material. Off-plan terms change with each release.
- Check the project chip names (SEI Saadiyat · Saadiyat Grove: The Designer · Baccarat).
- The end card carries a "not financial advice" line. Keep it on property content.

## Editing and re-rendering

All text lives in `composer.html` (search for the line you want to change). Preview it in a browser with `composer.html?cut=main` (or `hook`, `motivate`, `identity`, `whatif`), then render:

```
node video/render.cjs main          # → video/out/jamal-akim-main.mp4
node video/render.cjs whatif --stills 10,24   # PNG frames for checking
```

Needs Node, Playwright (Chromium) and ffmpeg.
