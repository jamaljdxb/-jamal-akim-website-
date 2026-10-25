# Go-live plan (when Jamal says "logged in")

## Step 1: on the work laptop (Jamal)
1. Open Terminal and type `claude`, then `/login`.
2. Say: "Commit everything in the jamal-akim-website folder and push master to GitHub (jamaljdxb/jamal-akim-website). Don't delete anything."
3. Come back to this phone session and say "logged in".

## Step 2: Cloudflare (any browser, phone is fine)
Workers & Pages → jamal-akim-website → Settings → Build → Connect GitHub:
- Branch `master`
- Build command `npm run build`
- Deploy command `npx wrangler deploy`
- Variable `NODE_VERSION` = `22`
- Preview builds: on

## Step 3: Claude (this session)
1. Check GitHub master is the six-week-newer copy, not the 14 September one.
2. Add on a preview branch:
   - Latin America (5 articles plus the SEO pack)
   - mortgages (4)
   - branded residences
   - UK CGT
   - ADGM
   - the explainer videos (leverage, CGT, ADGM, branded)
   - SEO fixes (sitemap lastmod, IndexNow, og images, workers.dev 301)
3. Jamal checks the preview link, then merge. Cloudflare deploys automatically.
4. Ping IndexNow and submit the sitemap.

## After this: updating from the phone
- GitHub becomes the master copy, and every change deploys automatically.
- To change anything, open the Claude app → Code → this repo and describe the change.
- Claude edits on a branch and you get a preview link. Say "ship it" and it goes live.
- The work laptop is no longer needed. Its copy is just a backup; on it, always `git pull` before editing.
