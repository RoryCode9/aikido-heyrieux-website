# Aikido Club Hugo Website

This repository now uses a Hugo-only static site stack:

- **Hugo**
- **Markdown content**
- **Lightweight Hugo theme**: [Bear Cub](https://github.com/clente/hugo-bearcub)
- **GitHub Actions** for CI/CD
- **GitHub Pages** for hosting

## Language support

The site is bilingual:

- **French** is the default language at the root URL
- **English** is available under `/en/`
- A language switch button is shown in the navbar

## Project structure

- `content/` → French content
- `content.en/` → English content
- `themes/hugo-bearcub/` → lightweight Hugo theme (git submodule)
- `layouts/partials/nav.html` → navbar override with language switch
- `static/club.css` → small site-specific style adjustments
- `.github/workflows/hugo.yml` → build and deploy workflow

## Requirements

- Hugo Extended `v0.161.1` or newer
- Git (required to fetch the theme submodule)

## Local development

```bash
make dev
```

This runs:

```bash
hugo server --disableFastRender --bind 127.0.0.1 --baseURL http://127.0.0.1:1313/
```

Open <http://127.0.0.1:1313/>.

## Production build

```bash
make build
```

Equivalent command:

```bash
hugo --gc --minify
```

Generated output goes to `public/`.

## GitHub Pages deployment

The workflow in `.github/workflows/hugo.yml`:

- checks out the repository with theme submodules
- installs Hugo
- builds the site
- deploys `public/` to GitHub Pages on pushes to `main`

To enable deployment:

1. Push the repository to GitHub.
2. Open **Settings → Pages**.
3. Set **Source** to **GitHub Actions**.
4. Push to `main`.

## Content updates

To edit the French site, update files in `content/`.
To edit the English site, update matching files in `content.en/`.

Keep the same filenames across both directories so Hugo can link translations automatically.

## Remaining placeholders

Before launch, replace these placeholders with real club information:

- club email address
- exact dojo location
- final class schedule
- instructor biographies
