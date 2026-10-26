#!/usr/bin/env python3
"""Build the dependency-free portfolio. Edit content.json, then run python3 build.py."""
import json, html, pathlib, datetime, hashlib, shutil
SOURCE=pathlib.Path(__file__).resolve().parent
ROOT=SOURCE/'dist'
(ROOT/'assets/images').mkdir(parents=True,exist_ok=True)
(ROOT/'assets/fonts').mkdir(parents=True,exist_ok=True)
shutil.copy2(SOURCE/'content.json',ROOT/'content.json')
for name in ['styles.css','site.js','favicon.svg','social-cover.jpg','pluto-wordmark.svg']:
 shutil.copy2(SOURCE/name,ROOT/'assets'/name)
for asset in SOURCE.glob('cover-*.jpg'):
 shutil.copy2(asset,ROOT/'assets/images'/asset.name.removeprefix('cover-'))
for name in ['anton-0.ttf','manrope-0.ttf','manrope-2.ttf','plex-mono-0.ttf','anton-LICENSE.txt','manrope-LICENSE.txt','ibm-plex-mono-LICENSE.txt']:
 shutil.copy2(SOURCE/name,ROOT/'assets/fonts'/name)
DATA=json.loads((ROOT/'content.json').read_text())
PROJECTS=DATA['projects']
BY_SLUG={p['slug']:p for p in PROJECTS}
BASE='https://plutowang.netlify.app'
CSS_VERSION=hashlib.sha256((ROOT/'assets/styles.css').read_bytes()).hexdigest()[:10]
JS_VERSION=hashlib.sha256((ROOT/'assets/site.js').read_bytes()).hexdigest()[:10]
WORDMARK_VERSION=hashlib.sha256((ROOT/'assets/pluto-wordmark.svg').read_bytes()).hexdigest()[:10]
FAVICON_VERSION=hashlib.sha256((ROOT/'assets/favicon.svg').read_bytes()).hexdigest()[:10]
SOCIAL_VERSION=hashlib.sha256((ROOT/'assets/social-cover.jpg').read_bytes()).hexdigest()[:10]
LABELS={'commercial':'Commercial','narrative':'Narrative','music':'Music video','documentary':'Documentary','newmedia':'New media'}
PLAYLISTS={
 'commercial':'PLzVnmFjMEHZbn5Zfyc5xqTk__Ry2ro0wN',
 'narrative':'PLzVnmFjMEHZZZQftcO9QaftmcsqQrY6Gm',
 'music':'PLzVnmFjMEHZapxgpAKAYEH5OeMMwICAn5',
 'documentary':'PLzVnmFjMEHZbLsOP2uIgezYuw6CN6YR-s',
 'newmedia':'PLzVnmFjMEHZbheD7g7Xr9M-CWnD8_Zd1c'}
def e(s): return html.escape(str(s),quote=True)
def url(p):return '/projects/'+p['slug']+'/'
def img(p):return '/assets/images/'+p['id']+'.jpg'
def head(title,description,path='/',image='/assets/social-cover.jpg',preload=None,schema=None):
 if image=='/assets/social-cover.jpg':image+='?v='+SOCIAL_VERSION
 preload_tag=f'<link rel="preload" as="image" href="{e(preload)}" fetchpriority="high">' if preload else ''
 structured='<script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</','<\\/')+'</script>' if schema else ''
 return f'''<!doctype html>
<html lang="en" class="no-js"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#10110f">
<link rel="canonical" href="{BASE}{path}"><meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{BASE}{path}"><meta property="og:image" content="{BASE}{e(image)}"><meta property="og:site_name" content="PLUTO WANG"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg?v={FAVICON_VERSION}"><link rel="stylesheet" href="/assets/styles.css?v={CSS_VERSION}">
<link rel="preload" href="/assets/fonts/anton-0.ttf" as="font" type="font/ttf" crossorigin>{preload_tag}{structured}
<script defer src="/assets/site.js?v={JS_VERSION}"></script></head><body>
<a class="skip-link" href="#main">Skip to content</a>'''
def header(home=False):
 prefix='' if home else '/'
 return f'''<header class="site-header"><div class="container header-inner"><a class="wordmark" href="/" aria-label="Pluto Wang — home">PLUTO WANG<span class="dot" aria-hidden="true"></span></a>
<button class="menu-toggle" aria-expanded="false" aria-controls="main-nav"><span class="menu-label">Menu</span><span class="menu-icon" aria-hidden="true">+</span></button>
<nav class="main-nav" id="main-nav" aria-label="Main navigation"><a href="{prefix}#work">Work</a><a href="{prefix}#about">About</a><a href="{prefix}#contact">Contact <span class="arrow" aria-hidden="true">↗</span></a></nav></div></header>'''
def footer():
 return '''<section class="contact-section" id="contact" aria-labelledby="contact-title"><div class="container"><div class="contact-top mono"><span>03 / Start a conversation</span><span>Commercial projects<br>Film &amp; art collaborations</span></div>
<h2 class="contact-title" id="contact-title"><a href="mailto:pluto.cywang@gmail.com">Let’s talk.<span class="arrow" aria-hidden="true">↗</span></a></h2>
<div class="contact-bottom"><div class="contact-email"><a href="mailto:pluto.cywang@gmail.com">pluto.cywang@gmail.com</a><button class="copy-email" hidden aria-live="polite">Copy email</button></div><p>Have a brief, a story, or an idea that doesn’t quite fit a frame? I’d like to hear it.</p></div></div></section>
<footer class="container site-footer mono"><span>© <span data-year>2026</span> Chung-Yi Wang (Pluto)</span><span>Stories / Images / Other worlds</span><a href="#main">Back to top ↑</a></footer></body></html>'''
def card(p,attributes=True):
 attrs=f'data-category="{p["category"]}" data-selected="{str(p["selected"]).lower()}" data-slug="{p["slug"]}" data-order="{int(p["number"])}"' if attributes else ''
 return f'''<article class="project-card" {attrs}><a href="{url(p)}" aria-label="View {e(p['title'])}"><div class="project-image"><img src="{img(p)}" alt="" width="1280" height="720" loading="lazy" decoding="async"><span class="image-action" aria-hidden="true">↗</span></div><div class="card-meta mono"><span>{p['number']} / {LABELS[p['category']]}</span><span>{e(p['medium'])}</span></div><h3 class="card-title">{e(p['title'])}<span class="arrow" aria-hidden="true">↗</span></h3></a></article>'''
def home():
 hero=BY_SLUG[DATA['hero']]
 description='Chung-Yi Wang (Pluto), director and visual artist. Selected commercials, music videos, narrative films, documentaries and immersive new media projects.'
 schema={'@context':'https://schema.org','@type':'Person','name':'Chung-Yi Wang','alternateName':'Pluto Wang','url':BASE,'jobTitle':'Director / Visual Artist','email':'mailto:pluto.cywang@gmail.com'}
 out=head('PLUTO WANG — Director / Visual Artist',description,preload=img(hero),schema=schema)+header(True)
 out+=f'''<main id="main"><section class="container masthead" aria-label="Pluto Wang, director and visual artist"><h1 class="masthead-title"><img src="/assets/pluto-wordmark.svg?v={WORDMARK_VERSION}" alt="PLUTO" width="966" height="218" fetchpriority="high"></h1><div class="signal-line"><span class="mono"><span class="accent">Signal 001</span><span class="signal-extra"> / Selected transmissions</span></span><span class="cross" aria-hidden="true">+</span><span class="mono right">Director / Visual Artist</span></div>
<a class="hero-link" href="{url(hero)}" aria-label="Watch {e(hero['title'])}"><div class="hero-frame"><img src="{img(hero)}" alt="A figure facing the sea in Daughter K Babbling" width="1280" height="720" fetchpriority="high"><span class="corner tl" aria-hidden="true"></span><span class="corner tr" aria-hidden="true"></span><span class="corner bl" aria-hidden="true"></span><span class="corner br" aria-hidden="true"></span><div class="hero-overlay"><div><div class="hero-kicker mono"><span class="status-dot" aria-hidden="true"></span>Featured transmission / Music video</div><h2 class="hero-title">{e(hero['title'])}</h2></div><span class="play-link mono"><span class="play-circle" aria-hidden="true"></span>Watch film</span></div></div></a><div class="hero-caption mono"><span>Ling Yu × Lo Si-rong</span><span>Sound into image. Image into feeling.</span></div><div class="intro-line"><p>Stories that stay with you.<br>Images that take you somewhere else.</p><span class="mono muted">Commercials, cinema<br>&amp; immersive experiences</span></div></section>
<section id="work" class="container section" aria-labelledby="work-title"><div class="section-heading"><div><span class="mono accent">01 / The work</span><h2 id="work-title">Selected transmissions.</h2></div><p class="section-note mono">Across screens, genres<br>and ways of seeing.</p></div><div class="filter-bar" role="group" aria-label="Filter works" hidden>'''
 for value,label in [('selected','Selected'),('all','All work'),*LABELS.items()]:
  count=len(DATA['selected_order']) if value=='selected' else len(PROJECTS) if value=='all' else sum(p['category']==value for p in PROJECTS)
  out+=f'<button class="filter-button" data-filter="{value}" aria-pressed="false">{label}<sup>{count:02}</sup></button>'
 out+=f'''</div><div class="work-status mono"><span id="work-count" role="status" aria-live="polite">{len(PROJECTS)} projects / Complete archive</span><span>Image / Story / Space</span></div><noscript><p class="noscript-note">All works are shown below. Open any project to watch it on YouTube.</p></noscript><div class="project-grid" id="project-grid" data-selected-order="{','.join(DATA['selected_order'])}">'''
 out+=''.join(card(p) for p in PROJECTS)
 out+=f'''</div><div class="work-end"><span class="mono muted">An ongoing body of work.</span><button id="view-all" class="line-button mono" hidden>Explore all {len(PROJECTS)} projects ↗</button></div></section>
<section id="about" class="container section" aria-labelledby="about-title"><div class="section-heading"><div><span class="mono accent">02 / Behind the signal</span><h2 id="about-title">Chung-Yi Wang.</h2></div><p class="section-note mono">Also known as Pluto.<br>Director / Visual Artist</p></div><div class="about-grid"><p class="about-statement">One practice.<br>Many ways<br>of <em>seeing.</em></p><div class="about-copy"><p>I’m Chung-Yi Wang (Pluto), a director and visual artist working across commercials, narrative film, music videos, documentary and new media.</p><p>My practice connects visual storytelling with immersive experiences—from the intimacy of a single frame to the possibilities of VR and multi-screen installations.</p><p>Alongside filmmaking, my experience spans creative direction, post-production supervision and teaching film, VR and documentary production.</p><ul class="discipline-list mono"><li>Direction</li><li>Visual storytelling</li><li>Creative direction</li><li>Immersive media</li></ul></div></div>
<div class="about-columns"><div><h3 class="list-label mono">Selected recognition</h3><ul class="record-list">
<li><span class="record-year">2024</span><div><h4 class="record-title">Excellence Script</h4><p class="record-detail">Young Screenwriters Conference<br><em>Cross the River in Summer</em></p></div></li>
<li><span class="record-year">2020</span><div><h4 class="record-title">Best Experimental</h4><p class="record-detail">Golden Rooster Award · Mobile Short Film Project<br><a href="/projects/save-the-earth/">Save the Earth ↗</a></p></div></li>
<li><span class="record-year">2018</span><div><h4 class="record-title">Best Narrative Prize</h4><p class="record-detail">Taipei Film Festival VR Hackathon<br><a href="/projects/free-will/">Free Will ↗</a></p></div></li></ul></div>
<div><h3 class="list-label mono">Selected experience</h3><ul class="record-list">
<li><span class="record-year">2018–2025</span><div><h4 class="record-title">Lecturer &amp; Studio Head</h4><p class="record-detail">Xiamen University Tan Kah Kee College<br>Sirius Creative Media Studio</p></div></li>
<li><span class="record-year">2019–2024</span><div><h4 class="record-title">Founder &amp; Creative Director</h4><p class="record-detail">Xiamen Pluto Media Co., Ltd.</p></div></li>
<li><span class="record-year">2019–2022</span><div><h4 class="record-title">Content &amp; Social Media</h4><p class="record-detail">Food channel management, audience research,<br>content strategy and monetization.</p></div></li>
<li><span class="record-year">2017–2018</span><div><h4 class="record-title">Director &amp; Post-Production Supervisor</h4><p class="record-detail">Lambda Film Co., Ltd.</p></div></li></ul></div></div></section></main>'''
 return out+footer()
def project_page(p):
 description=p['title']+' — '+p['medium']+'. '+p['description']+' From the portfolio of Chung-Yi Wang (Pluto).'
 out=head(p['title']+' — PLUTO WANG',description,url(p),img(p),img(p))+header()
 out+=f'''<main id="main" class="container project-main"><div class="project-breadcrumb mono"><a class="text-link" href="/?view={p['category']}#work">← Back to {LABELS[p['category']]}</a><span class="accent">Transmission {p['number']} / {len(PROJECTS)}</span></div><h1 class="project-title">{e(p['title'])}</h1><p class="project-subtitle">{e(p['description'])}</p>
<div class="video-shell"><button class="video-poster" data-video-id="{p['id']}" data-video-title="{e(p['source_title'])}" aria-label="Play {e(p['title'])}"><img src="{img(p)}" alt="" width="1280" height="720" fetchpriority="high"><span class="play-circle" aria-hidden="true"></span><span class="play-label mono">Play film / YouTube</span></button></div><div class="video-fallback mono"><span>Hosted on YouTube</span><a href="https://www.youtube.com/watch?v={p['id']}" target="_blank" rel="noopener noreferrer">Open on YouTube ↗</a></div>
<div class="project-details"><div><p>{e(p['source_title'])}</p></div><dl class="project-facts"><div><dt>Collection</dt><dd>{LABELS[p['category']]}</dd></div><div><dt>Format</dt><dd>{e(p['medium'])}</dd></div>'''
 if p.get('recognition'):out+=f'<div><dt>Recognition</dt><dd class="recognition">{e(p["recognition"])}</dd></div>'
 out+=f'''<div><dt>More work</dt><dd><a class="text-link" href="https://www.youtube.com/playlist?list={PLAYLISTS[p['category']]}" target="_blank" rel="noopener noreferrer">View collection on YouTube <span aria-hidden="true">↗</span></a></dd></div></dl></div>'''
 idx=PROJECTS.index(p);prev=PROJECTS[(idx-1)%len(PROJECTS)];nxt=PROJECTS[(idx+1)%len(PROJECTS)]
 out+=f'''<nav class="project-navigation mono" aria-label="Project navigation"><a href="{url(prev)}">← Previous project</a><a href="/#work">All work</a><a href="{url(nxt)}">Next project →</a></nav>'''
 related=[x for x in PROJECTS if x['category']==p['category'] and x!=p][:2]
 if len(related)<2:related.extend(x for x in PROJECTS if x['selected'] and x!=p and x not in related)
 out+='<section class="related" aria-labelledby="related-title"><div class="section-heading"><div><span class="mono accent">Keep exploring</span><h2 id="related-title">Another transmission.</h2></div></div><div class="project-grid">'+''.join(card(x,False) for x in related[:2])+'</div></section></main>'
 return out+footer()
if __name__=='__main__':
 assert len(PROJECTS)==len(BY_SLUG)==len({p['id'] for p in PROJECTS}), 'Duplicate project identifier'
 for p in PROJECTS:assert (ROOT/img(p).lstrip('/')).is_file(),f'Missing image for {p["slug"]}'
 (ROOT/'index.html').write_text(home())
 for p in PROJECTS:
  folder=ROOT/'projects'/p['slug'];folder.mkdir(parents=True,exist_ok=True);(folder/'index.html').write_text(project_page(p))
 notfound=head('Signal not found — PLUTO WANG','This transmission could not be found.',path='/404.html')+header()+'<main id="main" class="container not-found"><span class="mono accent">Signal interrupted</span><h1>404</h1><p>This transmission is off the air. Return to the selected works to find another story.</p><a class="line-button" href="/#work">Back to the work ↗</a></main>'+footer()
 (ROOT/'404.html').write_text(notfound)
 urls=['/']+[url(p) for p in PROJECTS]
 (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{BASE}{u}</loc></url>' for u in urls)+'</urlset>\n')
 (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml\n')
 print(f'Built homepage, {len(PROJECTS)} project pages, 404 and sitemap.')
