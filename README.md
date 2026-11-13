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

## Writing

The homepage book icon beside the shark control links directly to the essay.
`/blog/` lists the current essays. The research protocol essay lives at
`/blog/the-paper-is-just-a-view/` and includes its own
four transparent illustrations. Older template post URLs are preserved, but
they are not promoted in the new writing index.

The editable article source is `writing/the-paper-is-just-a-view.md`, exported
from the companion draft Page. Page edits are not synchronized automatically.
After updating the source, regenerate the two static writing pages locally:

```sh
python -m pip install Markdown
python scripts/build-writing.py
```

Only the local authoring command needs Python Markdown. Vercel still serves
the committed `public/` files with no install or build command. Writing pages
use the homepage's color palette and follow the system theme on fresh visits;
manual theme changes are temporary and are not saved to browser storage.
The generated sitemap lists the real homepage, writing index and essay; the
old example-domain/template entries are not included.
