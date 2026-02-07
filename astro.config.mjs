import { defineConfig } from "astro/config";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import react from "@astrojs/react";
import sitemap from "@astrojs/sitemap";

export default defineConfig({
  site: "https://enguerrand.dev",
  integrations: [tailwind({ applyBaseStyles: false }), mdx(), react(), sitemap()],
});
