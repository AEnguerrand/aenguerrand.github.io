import { defineCollection, z } from "astro:content";

const talks = defineCollection({
  type: "content",
  schema: z
    .object({
      title: z.string(),
      date: z.string(),
      author: z.array(z.string()).optional(),
      tags: z.array(z.string()).optional(),
    })
    .passthrough(),
});

const pages = defineCollection({
  type: "content",
  schema: z
    .object({
      title: z.string().optional(),
      layout: z.string().optional(),
    })
    .passthrough(),
});

export const collections = { talks, pages };
