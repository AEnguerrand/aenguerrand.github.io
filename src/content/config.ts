import { defineCollection, z } from "astro:content";

const talks = defineCollection({
  type: "content",
  schema: z
    .object({
      title: z.string(),
      date: z.string(),
      author: z.array(z.string()).optional(),
      event: z.string().optional(),
      location: z.string().optional(),
      summary: z.string().optional(),
      language: z.array(z.string()).optional(),
      sessionType: z.string().optional(),
      tags: z.array(z.string()).optional(),
      resources: z
        .array(
          z.object({
            label: z.string(),
            url: z.string().url(),
          })
        )
        .optional(),
    })
    .passthrough(),
});

const pages = defineCollection({
  type: "content",
  schema: z
    .object({
      title: z.string().optional(),
      layout: z.string().optional(),
      currentExploringTitle: z.string().optional(),
      currentExploringDescription: z.string().optional(),
      currentExploring: z
        .array(
          z.object({
            title: z.string(),
            description: z.string(),
          })
        )
        .optional(),
    })
    .passthrough(),
});

export const collections = { talks, pages };
