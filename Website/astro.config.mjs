import { defineConfig } from 'astro/config';

// Site is published at https://chihun-lee.github.io (user site -> root).
export default defineConfig({
  site: 'https://chihun-lee.github.io',
  base: '/',
  trailingSlash: 'ignore',
  build: {
    format: 'directory',
  },
});
