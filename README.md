# Aikido Club Hugo Website

A clean, modern Hugo static website for an Aikido club. The project uses idiomatic Hugo templates, Hugo Pipes for styling, local static assets, semantic HTML, responsive CSS, and no custom backend.

## Pages

- Home
- About the Club
- Classes / Schedule
- Instructors
- Contact

## Requirements

- Hugo Extended `v0.161.1` or newer compatible version
- Make
- Python 3 for the local validation script

No Hugo Modules are used, so `hugo mod tidy` is not required.

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

Generated output goes to `public/`, which is intentionally ignored by Git.

## Validation

```bash
make check
```

This performs a production Hugo build and runs `scripts/check_site.py` against `public/` to validate internal links, local assets, required contact form fields, honeypot field, and configured FormSubmit endpoint visibility.

Manual checks before launch:

1. `hugo version`
2. `hugo --gc --minify`
3. `hugo server --disableFastRender`
4. Check all internal links
5. Check responsive layout on mobile and desktop widths
6. Confirm contact form renders and validates client-side
7. Confirm images load locally
8. Confirm README instructions remain accurate

## Contact form endpoint

Hugo is static and cannot process form submissions by itself. The contact form posts to FormSubmit, which forwards submissions to `rory.chat@tutamail.com`:

```toml
[params]
  formEndpoint = "https://formsubmit.co/rory.chat@tutamail.com"
```

Important: FormSubmit normally sends an activation email to the recipient on the first submission. Confirm that email from `rory.chat@tutamail.com` before relying on live contact messages.

The form includes HTML5 validation and a honeypot anti-spam field.

## GitHub Pages deployment

A GitHub Actions workflow is included at `.github/workflows/hugo.yml`.

It:

- builds the Hugo site on push and pull request
- fails if the build fails
- can deploy to GitHub Pages on pushes to `main` when Pages is configured for GitHub Actions in repository settings

To deploy:

1. Push this repository to `https://github.com/RoryCode9/aikido-heyrieux-website`.
2. Open repository **Settings → Pages**.
3. Set **Source** to **GitHub Actions**.
4. Push to `main` and wait for the `Hugo` workflow to complete.

## Image attribution

Temporary images are stored locally and not hotlinked. See [`ATTRIBUTION.md`](ATTRIBUTION.md).

| File | Source | License |
| --- | --- | --- |
| `assets/images/aikido-training.jpg` | Wikimedia Commons: Aikido lesson in Turku Aikikai’s dojo 2016 | CC BY-SA 4.0 |
| `assets/images/aikido-keyhole.jpg` | Wikimedia Commons: Aikido keyhole | CC BY-SA 3.0 |

## Remaining TODOs

- Replace placeholder club name, location, email, schedule, and instructor bios with real content.
- Replace the placeholder contact form endpoint with a production form provider or backend.
- Replace temporary Wikimedia images with final club-approved photography if available.
- GitHub Pages URL is expected to be `https://rorycode9.github.io/aikido-heyrieux-website/` unless a custom domain is configured.
