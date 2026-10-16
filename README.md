# Ziyang Zhang's Website

This repository serves prebuilt static files from `public/`. Edit
`public/index.html` directly to update the homepage. Hugo is not required.

## Vercel Deployment

Keep the Vercel project's Root Directory at the repository root so that it reads
`vercel.json` and `package.json`.

- Framework: Other (`framework: null`).
- Install command: empty; no dependencies are installed.
- Build command: empty; no site generation runs.
- Output directory: `public`.
- Node.js version: `24.x`, declared in `package.json` to override an outdated
  project setting. This is deployment metadata; the website has no Node.js
  runtime or package dependencies.

The deployment configuration preserves existing file and directory URLs. There
is no single-page-app fallback or catch-all rewrite.

## Local Preview

From the repository root, run:

```sh
python -m http.server 8000 --directory public
```

Visit `http://localhost:8000/`. No package installation or build is needed.
