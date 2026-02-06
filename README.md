# aenguerrand.github.io / enguerrand.tech

Personal website rebuilt with Astro + Tailwind (shadcn-style tokens).

## Quick Start

```bash
# Install dependencies
npm install

# Start local development server
npm run dev

# Build for production
npm run build
```

## Structure

- **Content**: Markdown in `src/content/`
- **Pages**: Astro pages in `src/pages/`
- **Layout & UI**: `src/layouts/` and `src/components/`
- **Styles**: `src/styles/global.css`
- **Static files**: `public/`

## Deployment

Build output is in `dist/` by default. Configure your GitHub Pages workflow to run `npm run build` and publish the `dist/` directory.
