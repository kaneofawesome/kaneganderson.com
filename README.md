# kaneganderson.com

Static site built with [Hugo](https://gohugo.io). Migrated off Joomla in
September 2026.

## Build

```sh
hugo server -D      # local preview at http://localhost:1313, drafts included
hugo --gc --minify  # production build into public/
```

No theme submodule, no npm. Templates live in `layouts/`, styles in
`assets/css/main.css`. Hugo extended is the only dependency.

## Layout

```
content/blog/{articles,books,journal,poetry,quotes,recipes}/  posts
content/unfiled/         posts that had no menu route in Joomla
archive/                 posts trashed in Joomla, kept out of the build
static/_redirects        strips the old /index.php/ URL prefix
static/images/           only the images actually referenced by posts
layouts/                 the whole theme
```

## Front matter

Each post carries `joomla_id` (its old `jos_content` row) and, where the old URL
appeared in the server access logs, an `aliases` entry so the previous link
still resolves.

## Deployment

Pushes to `main` trigger `.github/workflows/hugo.yml`, which builds with a
pinned Hugo version and publishes to GitHub Pages. `static/CNAME` holds the
custom domain so it survives every deploy.

## Redirects

Joomla served SEF URLs with `/index.php/` in the path. Every one of them is
handled by Hugo `aliases` in front matter, which emit meta-refresh pages at the
old paths. That is deliberately **host-independent** — it works on GitHub
Pages, Netlify, Cloudflare Pages, or S3, so moving hosts later costs nothing
but a DNS change.

Coverage: 81 posts, the six section listings, Joomla's `featured` view, and
`/index.php/` itself. The remainder of the old URLs in the access logs were
bot noise (`/phpinfo`, `/node/add`, injection probes) and are intentionally
left to 404.

`static/_redirects` is kept as a one-line wildcard for hosts that support it.
It is redundant on GitHub Pages and harmless there.

## Provenance

Content was exported from the Joomla 5.4.1 database (`jos_content`,
`jos_categories`, `jos_menu`, `jos_tags`) as XML, converted to Markdown, and
image paths normalised to web-safe names. `convert.py` is kept for reference;
it is not part of the build.

The full database dump from the migration is `lightsail-rescue/` — kept out of
git via `.gitignore` because of its size. Store it somewhere durable.

## Why the move

The Joomla site went down on 2026-08-11 when an unauthenticated attacker
deleted `configuration.php` through Helix Ultimate's `delete-media` AJAX
endpoint (CVE-2026-57830, fixed in Helix Ultimate 2.2.7). No login was
compromised and no shell was obtained, but the underlying Bitnami stack was
also deprecated by AWS. A static site removes the entire attack surface.
