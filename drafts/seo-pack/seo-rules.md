# Site-wide SEO and AI-crawler rules for every article

1. **Length.** At least 2,000 words of body copy.
2. **Meta.** Unique `<title>` of 60 characters or fewer, and a meta description of 155 to 160 characters, both given per article. Add `og:title`, `og:description`, `og:image` (1200x630, per article, not the site default), `og:type=article`, `article:published_time`, `article:modified_time` and `twitter:card=summary_large_image`.
3. **Structured data.** `Article` with author Person (Jamal Akim, with sameAs links to his real Instagram, LinkedIn, YouTube and TikTok), `datePublished`, `dateModified` and `image`. Add `FAQPage` from the FAQ block and `BreadcrumbList`. Use `speakable` on the Key takeaways block if your schema setup supports it.
4. **Key takeaways near the top.** Five short, factual bullets, each a complete sentence with a number and a date. These are the lines AI answer engines quote, so keep them plain text, not images.
5. **Charts must be readable without the picture.** Every chart and graphic gets a `<figcaption>` with the source, plus an accessible data table, which can be visually collapsed, holding the same numbers. Use inline SVG with `<title>` and `<desc>`, or `<img>` with full alt text.
6. **Images.** Descriptive file names (given per article), alt text written for a blind reader that includes the keyword naturally, captions where given, explicit width and height, `loading="lazy"` below the fold, `fetchpriority="high"` on the hero, WebP or AVIF through astro:assets. Include images in the sitemap (`image:image`).
7. **Headings.** One H1 (the title). H2s phrased the way people search ("Can a non-resident get a mortgage in Dubai?").
8. **Internal links.** At least 3 to related guides plus /mortgages/ and /book/. Every new article is linked from at least one existing hub page (/international/, /caribbean/, /mortgages/, /compare/ or /developers/).
9. **External sources.** A "Sources" section near the end with links to primary sources (central banks, ADGM, DLD, UNHCR, IMF, Savills, Global Branded Residences). Use normal links for sources, and rel="sponsored" for any gccmortgages.com link.
10. **Crawlability.** Server-rendered HTML, no content hidden behind JavaScript, a canonical on every page, the sitemap with `<lastmod>`, an IndexNow ping on deploy, and new URLs added to llms.txt with a one-line summary each. robots.txt already allows GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot, Google-Extended, Applebot-Extended and Bingbot, so keep it that way.
11. **Freshness.** Show "Updated" dates. When rates or prices change, update the figures and `dateModified` instead of publishing a duplicate post.
12. **Voice.** Jamal's: short lines, worldly, straight talk, numbers worked through, no dashes in the copy.
