#!/usr/bin/env python3
"""Convert a Joomla 5 export (mysql --xml dumps) into a Hugo content tree."""
import xml.etree.ElementTree as ET
import re, os, json, html, urllib.parse, collections, datetime, pathlib, sys

SRC = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else 'site')

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter


def rows(path):
    r = ET.parse(SRC / path).getroot()
    return [{f.get('name'): (f.text or '') for f in row} for row in r.iter('row')]


# ---------------------------------------------------------------- source data
articles = rows('content.xml')
cats = {c['id']: c for c in rows('categories.xml')}
menus = rows('menu.xml')
users = {u['id']: u for u in rows('users.xml')}

tagmap = collections.defaultdict(list)
for t in rows('tags.xml'):
    if t.get('content_item_id'):
        tagmap[t['content_item_id']].append(t['title'])

# catid -> old url prefix, taken from the real menu items rather than guessed
CAT_ROUTE = {}
for m in menus:
    mo = re.search(r'view=category.*?id=(\d+)', m['link'] or '')
    if mo and m['published'] == '1':
        CAT_ROUTE[mo.group(1)] = m['path']

HOME_ID = None
for m in menus:
    mo = re.search(r'view=article&id=(\d+)', m['link'] or '')
    if mo and m['path'] == 'home':
        HOME_ID = mo.group(1)

# old URLs actually observed in two years of access logs
hits = {}
for line in (SRC / 'url-hits.txt').read_text(errors='replace').splitlines():
    mo = re.match(r'\s*(\d+)\s+(/\S+)', line)
    if mo:
        hits[mo.group(2)] = int(mo.group(1))


# ------------------------------------------------------------- html cleaning
def flatten_confluence_code(soup):
    """Confluence pastes wrap every token in a <span class=prismjs>. Collapse
    each code block down to its text and re-emit as a real <pre><code>."""
    for div in soup.select('div.code-block'):
        text = div.get_text()
        text = text.replace('\xa0', ' ').strip('\n')
        pre = soup.new_tag('pre')
        code = soup.new_tag('code')
        code.string = text
        pre.append(code)
        div.replace_with(pre)
    # breakout wrappers left behind by Confluence
    for div in soup.select('div.fabric-editor-breakout-mark'):
        div.unwrap()


IMAGE_MAP = {}


def slug_seg(seg):
    """Filenames with spaces or non-ascii break Markdown links. Normalise."""
    stem, dot, ext = seg.rpartition('.')
    if not dot:
        stem, ext = seg, ''
    stem = re.sub(r'[^A-Za-z0-9._-]+', '-', stem).strip('-') or 'image'
    stem = re.sub(r'-{2,}', '-', stem)
    return (stem + ('.' + ext.lower() if ext else '')).lower()


def fix_img(src):
    if not src or src.startswith(('http://', 'https://', 'data:', '//')):
        return src
    raw = urllib.parse.unquote(src.split('#')[0])   # drop #joomlaImage:// suffix
    rel = re.sub(r'^/?images/', '', raw)
    new = '/'.join(slug_seg(s) for s in rel.split('/') if s)
    IMAGE_MAP[rel] = new
    return '/images/' + new


def clean(html_in):
    soup = BeautifulSoup(html_in, 'html.parser')
    flatten_confluence_code(soup)

    for tag in soup.find_all(True):
        for attr in list(tag.attrs):
            if attr.startswith('data-') or attr in ('style', 'class', 'id', 'dir', 'lang'):
                del tag[attr]

    for img in soup.find_all('img'):
        img['src'] = fix_img(img.get('src', ''))
        img.attrs = {k: v for k, v in img.attrs.items() if k in ('src', 'alt', 'title')}

    for a in soup.find_all('a'):
        href = a.get('href', '')
        if href.startswith('/index.php/'):
            a['href'] = href.replace('/index.php', '', 1)

    # spans carry nothing once classes are gone
    for span in soup.find_all(['span', 'font']):
        span.unwrap()

    # Joomla/TinyMCE leaves a lot of <p>&nbsp;</p>
    for p in soup.find_all('p'):
        if not p.get_text(strip=True).replace('\xa0', ''):
            if not p.find(['img', 'br', 'iframe']):
                p.decompose()

    return str(soup)


class Conv(MarkdownConverter):
    def convert_img(self, el, text, parent_tags=None):
        alt = el.attrs.get('alt', '') or ''
        src = el.attrs.get('src', '') or ''
        return f'![{alt}]({src})'


def to_md(html_in):
    md = Conv(heading_style='ATX', bullets='-', code_language='').convert(clean(html_in))
    md = md.replace('\xa0', ' ')
    md = re.sub(r'[ \t]+\n', '\n', md)
    # Confluence emits one code container per LINE, which becomes one fence per
    # line. Weld consecutive fenced blocks back into a single block.
    prev = None
    while prev != md:
        prev = md
        md = re.sub(r'\n```\n{1,2}```\n', '\n', md)
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip() + '\n'


# ------------------------------------------------------------------ emitting
def yaml_str(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def dt(s):
    if not s or s.startswith('0000'):
        return None
    try:
        return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        return None


STATE = {'1': 'published', '0': 'unpublished', '-2': 'trashed'}
report = []

for a in articles:
    state = STATE.get(a['state'], a['state'])
    cat = cats.get(a['catid'], {})
    route = CAT_ROUTE.get(a['catid'])
    slug = a['alias']

    if state == 'trashed':
        dest = OUT / 'archive' / f'{slug}.md'
        section = 'archive'
    elif a['id'] == HOME_ID:
        dest = OUT / 'content' / '_index.md'
        section = 'home'
    elif route:
        section = route.split('/')[-1]
        dest = OUT / 'content' / route / f'{slug}.md'
    else:
        section = 'unfiled'
        dest = OUT / 'content' / 'unfiled' / f'{slug}.md'

    aliases = []
    if route:
        old = f'/index.php/{route}/{slug}'
        if old in hits:
            aliases.append(old)

    fm = ['---']
    fm.append(f'title: {yaml_str(html.unescape(a["title"]))}')
    d = dt(a['created'])
    if d:
        fm.append(f'date: {d}')
    m = dt(a['modified'])
    if m and m != d:
        fm.append(f'lastmod: {m}')
    fm.append(f'draft: {"true" if state != "published" else "false"}')
    fm.append(f'slug: {yaml_str(slug)}')
    if cat.get('title') and cat['title'] != 'Uncategorised':
        fm.append(f'categories: [{yaml_str(cat["title"])}]')
    if tagmap.get(a['id']):
        fm.append('tags: [' + ', '.join(yaml_str(t) for t in tagmap[a['id']]) + ']')
    if a['metadesc'].strip():
        fm.append(f'description: {yaml_str(html.unescape(a["metadesc"]).strip())}')
    if a['featured'] == '1':
        fm.append('featured: true')

    # Helix Ultimate kept "post media" in the article's attribs blob, not in
    # Joomla's own images column.
    try:
        att = json.loads(a['attribs'] or '{}')
    except ValueError:
        att = {}

    cover = (att.get('helix_ultimate_image') or '').strip()
    if cover:
        fm.append(f'cover: {yaml_str(fix_img(cover))}')
        alt = (att.get('helix_ultimate_image_alt_txt') or '').strip()
        if alt:
            fm.append(f'cover_alt: {yaml_str(alt)}')

    gal = att.get('helix_ultimate_gallery')
    if gal:
        try:
            imgs = json.loads(gal).get('helix_ultimate_gallery_images') or []
        except (ValueError, AttributeError):
            imgs = []
        imgs = [fix_img(i) for i in imgs if i and i.strip()]
        if imgs:
            fm.append('gallery:')
            for i in imgs:
                fm.append(f'  - {yaml_str(i)}')

    vid = (att.get('helix_ultimate_video') or '').strip()
    if vid:
        fm.append(f'video: {yaml_str(vid)}')
    author = users.get(a['created_by'], {}).get('name', '')
    if a['created_by_alias'].strip():
        author = a['created_by_alias'].strip()
    if author:
        fm.append(f'author: {yaml_str(author)}')
    if aliases:
        fm.append('aliases:')
        for al in aliases:
            fm.append(f'  - {al}')
    fm.append(f'joomla_id: {a["id"]}')
    fm.append('---')

    body = to_md(a['introtext'])
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text('\n'.join(fm) + '\n\n' + body, encoding='utf-8')

    report.append({
        'id': a['id'], 'slug': slug, 'section': section, 'state': state,
        'src_chars': len(a['introtext']), 'md_chars': len(body),
        'hits': hits.get(f'/index.php/{route}/{slug}', 0) if route else 0,
        'path': str(dest.relative_to(OUT)),
    })

(OUT / 'convert-report.json').write_text(json.dumps(report, indent=1))

# Only a handful of the images/ tree is actually referenced. Emit a script that
# copies just those in, under their normalised names.
import shlex

lines = [
    '#!/bin/sh',
    '# Copies the images actually referenced by the posts out of the Joomla',
    '# images/ tree into static/images/ under web-safe names.',
    '#',
    '# Joomla accumulated years of renames, so some database references point at',
    '# files that no longer exist. Those are reported at the end rather than',
    '# aborting the run; anything findable by basename is recovered.',
    '#',
    '# Usage: sh collect-images.sh /path/to/extracted/images',
    '',
    'SRC="${1:?usage: collect-images.sh <extracted images dir>}"',
    '[ -d "$SRC" ] || { echo "not a directory: $SRC" >&2; exit 1; }',
    ': > missing-images.txt',
    'MISSING=0',
    'RECOVERED=0',
    '',
    'copy() {',
    '  dest="static/images/$2"',
    '  if [ -f "$SRC/$1" ]; then',
    '    mkdir -p "$(dirname "$dest")" && cp "$SRC/$1" "$dest"',
    '    return',
    '  fi',
    '  hit=$(find "$SRC" -type f -iname "$(basename "$1")" 2>/dev/null | head -1)',
    '  if [ -n "$hit" ]; then',
    '    mkdir -p "$(dirname "$dest")" && cp "$hit" "$dest"',
    '    echo "  recovered: $1"',
    '    RECOVERED=$((RECOVERED+1))',
    '    return',
    '  fi',
    '  echo "$1" >> missing-images.txt',
    '  MISSING=$((MISSING+1))',
    '}',
    '',
]
for old, new in sorted(IMAGE_MAP.items()):
    lines.append(f'copy {shlex.quote(old)} {shlex.quote(new)}')
lines += [
    '',
    f'echo "collected {len(IMAGE_MAP)} references: $((({len(IMAGE_MAP)} - MISSING))) present, '
    '$RECOVERED recovered by search, $MISSING missing"',
    '[ "$MISSING" -gt 0 ] && echo "see missing-images.txt" || rm -f missing-images.txt',
    'exit 0',
]
(OUT / 'collect-images.sh').write_text('\n'.join(lines) + '\n')
print(f'{len(IMAGE_MAP)} referenced images -> collect-images.sh')

# ------------------------------------------------------------------ redirects
static = OUT / 'static'
static.mkdir(parents=True, exist_ok=True)
(static / '_redirects').write_text(
    "# Joomla SEF URLs carried /index.php/ in the path; strip it.\n"
    "/index.php/*  /:splat  301\n"
    "/index.php    /        301\n"
)

print(f'wrote {len(report)} files to {OUT}')
by = collections.Counter(r['section'] for r in report)
for k, v in sorted(by.items()):
    print(f'  {k:<12} {v}')
