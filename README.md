# enguerrand.dev

Personal website built with Astro + Tailwind.

## Run

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## Deploy (Cloudflare Workers - Static Assets)

This site is deployed as static assets through Cloudflare Workers using `wrangler.toml`.

### Workers Builds (recommended)

Connect this repository in Cloudflare Workers Builds and use:

- Root directory: `.`
- Build command: `npm ci && npm run build`
- Deploy command: `npx wrangler deploy`

`wrangler.toml` defines the static assets directory (`dist`) and HTML/404 handling.

### Local deploy (optional)

```bash
npm run deploy:cf
```

## Content

- Pages: `src/pages/`
- Talks and page content: `src/content/`
- Components: `src/components/`

## GitHub Stars

The `/github-stars` page is generated from:

- `data/starred-lists.json`
- `public/data/starred-groups.json`

Refresh data:

```bash
npm run stars:refresh
```

Stars scripts use `uv`. Optional env vars: `GITHUB_TOKEN`, `GITHUB_COOKIE`.
