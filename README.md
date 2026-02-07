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
