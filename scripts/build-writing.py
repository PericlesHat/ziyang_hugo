"""Render the authored Markdown into the existing buildless static website.

Run locally with Python and Markdown installed. Vercel serves the committed
public/ files directly; it does not execute this script.
"""
from pathlib import Path
import re
import json
import html
import markdown

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
SLUG = 'the-paper-is-just-a-view'
TITLE = 'The Paper Is Just a View'
DOMAIN = 'https://ziyang-emory.vercel.app'
SUMMARY = 'On research agents, the cost of understanding their output, and a future where papers are generated for readers who want them.'
source = (ROOT/'writing'/f'{SLUG}.md').read_text(encoding='utf-8')
source = source.removeprefix('# '+TITLE+'\n\n')
subtitle = 'Toward agent-native scientific communication'
source = source.replace('*'+subtitle+'*\n\n', '', 1)
source = re.sub(r'^\*Draft · [^\n]+\*\n\n', '', source, count=1)
count_text = re.sub(r'!\[[^]]*\]\([^)]*\)', '', source)
count_text = re.sub(r'\[([^]]*)\]\([^)]*\)', r'\1', count_text)
minutes = max(1, round(len(count_text.split()) / 225))
body = markdown.markdown(source, extensions=['extra', 'toc'], output_format='html')
alts = iter([
    'A man with glasses and a woman consider a complicated research figure they cannot immediately explain.',
    'Above, computers communicate through two researchers. Below, computers communicate directly as the researchers look up.',
    'A versioned research record connects claims, evidence, runs, code and open questions to papers, dialogue and further experiments.',
    'Two surprised researchers beside a fictional Agent Native Conference poster reading no paper accepted.',
])
def figure(m):
    tag = m.group(1)
    alt = html.escape(next(alts), quote=True)
    tag = tag.replace('alt=""', f'alt="{alt}"')
    tag = tag.replace(' />', ' width="1536" height="1024" loading="lazy" decoding="async" />')
    src = re.search(r'src="([^"]+)"', tag).group(1)
    return f'<figure><a class="figure-link" href="{src}" target="_blank" rel="noopener" aria-label="Open illustration at full size">{tag}</a></figure>'
body, image_count = re.subn(r'<p>(<img [^>]+>)</p>', figure, body)
assert image_count == 4, f'Expected 4 figures, found {image_count}'

def head(title, description, url, is_post=False):
    schema = {
        '@context':'https://schema.org', '@type':'BlogPosting' if is_post else 'CollectionPage',
        'headline':TITLE if is_post else 'Writing', 'description':description,
        'url':url, 'inLanguage':'en',
        'author':{'@type':'Person','name':'Ziyang Zhang','url':DOMAIN+'/'},
    }
    if is_post:
        schema.update(dateCreated='2026-11-08',dateModified='2026-11-12',mainEntityOfPage=url)
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark"><meta name="theme-color" content="#ffffff">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(description,quote=True)}">
<link rel="canonical" href="{url}"><meta property="og:type" content="{'article' if is_post else 'website'}">
<meta property="og:site_name" content="Ziyang Zhang"><meta property="og:title" content="{html.escape(title,quote=True)}">
<meta property="og:description" content="{html.escape(description,quote=True)}"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary"><link rel="icon" href="/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/writing.css"><script src="/js/writing-theme.js"></script>
<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>
</head><body><a class="skip-link" href="#main">Skip to article</a>
<button id="theme-toggle" class="theme-toggle" type="button" role="switch" aria-label="Dark mode" aria-checked="false" title="Switch to dark mode">
<span class="theme-toggle__moon" aria-hidden="true"><i data-feather="moon"></i></span><span class="theme-toggle__sun" aria-hidden="true"><i data-feather="sun"></i></span>
</button>
<nav class="site-nav" aria-label="Site navigation"><a href="/">← Ziyang Zhang</a><a href="/blog/">Writing</a></nav>'''

footer='''<script src="/js/feather.min.js"></script><script>feather.replace();</script></body></html>'''
post_dir=PUBLIC/'blog'/SLUG
post_dir.mkdir(parents=True,exist_ok=True)
post = head(TITLE+' | Ziyang Zhang',SUMMARY,DOMAIN+'/blog/'+SLUG+'/',True)
post += f'''<main id="main"><article>
<header class="article-header"><p class="article-meta">November 2026 · {minutes} min read</p>
<h1>{TITLE}</h1><p class="subtitle">{subtitle}</p></header>
<div class="article-body">{body}</div>
</article><nav class="end-nav" aria-label="More writing"><a href="/blog/">← All writing</a><a href="#main">Back to top ↑</a></nav></main>'''+footer
(post_dir/'index.html').write_text(post,encoding='utf-8')
index=head('Writing | Ziyang Zhang','Writing on research and AI.',DOMAIN+'/blog/')
index+=f'''<main id="main" class="writing-index"><h1>Writing</h1>
<article class="post-entry"><p class="article-meta">November 2026 · {minutes} min read</p><h2><a href="/blog/{SLUG}/">{TITLE}</a></h2><p>{SUMMARY}</p></article>
</main>'''+footer
(PUBLIC/'blog'/'index.html').write_text(index,encoding='utf-8')
# Only list real authored pages; old template/example URLs remain accessible.
sitemap = '<?xml version="1.0" encoding="utf-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for route in ['/', '/blog/', '/blog/'+SLUG+'/']:
    sitemap += f'  <url><loc>{DOMAIN}{route}</loc></url>\n'
sitemap += '</urlset>\n'
(PUBLIC/'sitemap.xml').write_text(sitemap,encoding='utf-8')
print(f'Rendered /blog/ and /blog/{SLUG}/; {minutes} min read, {image_count} illustrations.')
