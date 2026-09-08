import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// One entry per Dubai neighbourhood / investment area.
// Add a new .md file in src/content/areas/ to create a new page automatically
// at /areas/<filename> — no code changes needed.
const areas = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/areas' }),
  schema: z.object({
    title: z.string(),               // e.g. "Property in Dubai Marina"
    area: z.string(),                // e.g. "Dubai Marina"
    metaDescription: z.string(),     // shown in Google search results
    summary: z.string(),             // short intro shown at top of page
    highlights: z.array(z.string()).default([]), // bullet points: why invest here
    publishDate: z.date(),
    updatedDate: z.date().optional(),
  }),
});

// One entry per blog / insight article.
// Add a new .md file in src/content/blog/ to publish a new post automatically
// at /blog/<filename>.
const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    metaDescription: z.string(),
    category: z.enum(['Build', 'Grow', 'Connect']),
    publishDate: z.date(),
    updatedDate: z.date().optional(),
    draft: z.boolean().default(false),
  }),
});

// One entry per off-plan project you're presenting to investors.
// Add a new .md file in src/content/projects/ to create a new page automatically
// at /projects/<filename>.
const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),               // e.g. "Marina Vista by Emaar"
    developer: z.string(),           // e.g. "Emaar Properties"
    area: z.string(),                // e.g. "Dubai Marina"
    startingPrice: z.string(),       // display string, e.g. "AED 1.2M" — placeholder until real pricing confirmed
    handover: z.string(),            // e.g. "Q4 2027"
    paymentPlan: z.string().optional(), // e.g. "60/40 post-handover"
    metaDescription: z.string(),
    summary: z.string(),
    highlights: z.array(z.string()).default([]),
    publishDate: z.date(),
    updatedDate: z.date().optional(),
    featured: z.boolean().default(false),
  }),
});

export const collections = { areas, blog, projects };
