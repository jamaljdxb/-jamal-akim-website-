# Jamal Akim — Website

Built with Astro for speed and SEO, ready to deploy on Cloudflare Pages.

## Run it locally

```
npm install
npm run dev
```

Then open http://localhost:4321

## Project structure

- `src/pages/index.astro` — homepage
- `src/pages/journey.astro` — the journey / about page
- `src/pages/areas/` — Dubai neighbourhood pages (auto-generated from `src/content/areas/`)
- `src/pages/blog/` — blog / insights pages (auto-generated from `src/content/blog/`)
- `src/layouts/BaseLayout.astro` — shared header, footer, SEO meta tags
- `src/styles/global.css` — all design tokens (colors, fonts, spacing)

## Adding a new Dubai area page

Add a new `.md` file to `src/content/areas/`, e.g. `src/content/areas/palm-jumeirah.md`:

```markdown
---
title: "Property in Palm Jumeirah"
area: "Palm Jumeirah"
metaDescription: "..."
summary: "..."
highlights:
  - "..."
  - "..."
publishDate: 2026-03-01
---

Your article content here, in Markdown.
```

A page at `/areas/palm-jumeirah` is created automatically — no code changes needed.

## Adding a new blog post

Same idea — add a `.md` file to `src/content/blog/` with `title`, `metaDescription`,
`category` (Build / Grow / Connect), and `publishDate` in the frontmatter, then write
the article below it. It appears automatically at `/blog/<filename>` and in the blog index.

## Before going live — replace these placeholders

- WhatsApp number: search for `wa.me/00000000000` across the project and replace with your real number
- Instagram / LinkedIn links in `src/layouts/BaseLayout.astro`
- `site` URL in `astro.config.mjs` if your final domain differs from jamaljoseph.com
- Favicon in `public/`

## Deploying

See the deployment guide provided alongside this project for step-by-step
GitHub + Cloudflare Pages instructions.
