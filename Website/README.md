# Website

Static academic site for Chihun Lee, built with [Astro](https://astro.build/).
Deploys to **https://chihun-lee.github.io** via GitHub Pages.

## Data flow

Single source of truth: `/Users/chihun/Code/SNS/data/*.yaml`.

`src/lib/data.ts` reads those YAML files at build time and exposes typed objects to Astro pages. **Do not edit content inside `src/pages/` — edit the YAML.**

## Local development

```bash
cd Website
npm install
npm run dev      # http://localhost:4321
npm run build    # outputs to ./dist
npm run preview
```

## CV PDF

The CV agent writes `/Users/chihun/Code/SNS/CV/build/cv.pdf`. The deploy workflow copies it to `Website/public/cv.pdf` before `astro build`. For local dev with the PDF, manually copy:

```bash
cp ../CV/build/cv.pdf public/cv.pdf
```

If `cv.pdf` is absent, the `/cv` page still renders but the embedded PDF will 404.

## Deployment

`.github/workflows/deploy-website.yml` at the **repo root** builds `Website/` on every push to `main` and deploys `Website/dist/` to GitHub Pages.

Because the site lives at the user-site root (`chihun-lee.github.io`), `astro.config.mjs` uses `base: '/'`.

## File tree

```
Website/
├── astro.config.mjs
├── package.json
├── tsconfig.json
├── README.md
├── public/
│   ├── favicon.svg
│   └── cv.pdf            # injected at deploy time
└── src/
    ├── layouts/Base.astro
    ├── components/PubItem.astro
    ├── lib/data.ts       # YAML loader (build-time)
    ├── styles/tokens.css
    └── pages/
        ├── index.astro
        ├── research.astro
        ├── publications.astro
        ├── talks.astro
        ├── people.astro
        └── cv.astro
```
