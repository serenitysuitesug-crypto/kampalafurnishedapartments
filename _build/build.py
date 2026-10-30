#!/usr/bin/env python3
"""
Builds the whole website from data/apartments.json.

How to use (from the repository folder):
    python3 _build/build.py

To add or change an apartment, edit data/apartments.json (and add its photos
to images/ named like R-1.webp, R-2.webp ...), then run the command above.
It regenerates index.html, every page in apartments/, the neighbourhood
pages, sitemap.xml and robots.txt.

This folder starts with "_" so GitHub Pages does not publish it.
"""
import json, os, re, html, datetime
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://kampalafurnishedapartments.com"
BRAND = "Furnished Apartments Uganda"
WHATSAPP = "256704229100"
WHATSAPP_2 = "256780228391"
CALL = "+256778663411"
CALL_DISPLAY = "+256 778 663411"
ADS_ID = "AW-17287370504"
ADS_CONVERSION = "AW-17287370504/txkQCNKT0J8bEIiuobNA"
TODAY = datetime.date.today().isoformat()
CHECKIN, CHECKOUT = "1:00 PM", "11:00 AM"
WEEKLY_NIGHTS, WEEKLY_OFF = 7, 15     # 15% off stays of 7 nights or more
MONTHLY_NIGHTS, MONTHLY_OFF = 30, 30  # 30% off stays of 30 nights or more

def disc(price, pct):
    return int(round(price * (100 - pct) / 100 / 1000.0) * 1000)

STAY_FAQS = [
    ("What are the check-in and check-out times?",
     f"Check-in is from {CHECKIN} and check-out is by {CHECKOUT}. If you need an earlier check-in or later check-out, message us on WhatsApp and we will do our best to arrange it."),
    ("Do you offer discounts for weekly or monthly stays?",
     f"Yes. You get {WEEKLY_OFF}% off the nightly rate when you stay {WEEKLY_NIGHTS} nights or more, and {MONTHLY_OFF}% off when you stay {MONTHLY_NIGHTS} nights or more. For example, a studio at UGX 100,000 per night costs UGX {disc(100000, WEEKLY_OFF):,} per night on a weekly stay and UGX {disc(100000, MONTHLY_OFF):,} per night on a monthly stay."),
]

# Neighbourhood information. Coordinates are approximate neighbourhood centres.
AREAS = {
    "Ntinda": {
        "slug": "furnished-apartments-ntinda",
        "geo": (0.3540, 32.6150),
        "intro": "Ntinda is one of Kampala's busiest and best-connected suburbs, in Nakawa Division about 7 km north-east of the city centre. You have supermarkets, restaurants, cafés, banks, pharmacies and boda bodas within a short walk, which makes it an easy base whether you are here for work, family or a holiday.",
        "why": [
            "Shops, restaurants and banks close by, so day-to-day errands are easy",
            "Quick access to Bukoto, Naguru, Kiwatule and Kisaasi",
            "A practical base for business travellers working in north-east Kampala",
            "Plenty of transport: taxis, boda bodas and ride-hailing apps work well here",
        ],
        "around": "From Ntinda you can reach Kampala city centre by road, with travel time depending heavily on traffic, and the Kampala Northern Bypass is close for trips across the city. Entebbe International Airport is roughly 1 to 1.5 hours away by road.",
    },
    "Kisaasi": {
        "slug": "furnished-apartments-kisaasi",
        "geo": (0.3720, 32.5990),
        "intro": "Kisaasi is a growing residential area in north Kampala, between Bukoto, Kyanja and Kulambiro. It is calmer than the busier suburbs but still has shops, restaurants and supermarkets along its main roads, which suits families and longer stays.",
        "why": [
            "A quieter residential setting that still has shops and eateries nearby",
            "Good for families and groups who want more space",
            "Easy reach of Ntinda, Bukoto and Kyanja",
            "Well placed for longer stays and relocations",
        ],
        "around": "Kisaasi connects to Ntinda and Bukoto by road and to the Kampala Northern Bypass for trips across the city. Entebbe International Airport is roughly 1 to 1.5 hours away by road, depending on traffic.",
    },
    "Kiwatule": {
        "slug": "furnished-apartments-kiwatule",
        "geo": (0.3710, 32.6300),
        "intro": "Kiwatule is a residential neighbourhood right next to Ntinda and Najjera in north-east Kampala. It offers a calmer stay than central Kampala while keeping Ntinda's shops, restaurants and services a short ride away.",
        "why": [
            "Peaceful residential streets close to Ntinda's amenities",
            "Good value for couples and longer stays",
            "Close to the Kampala Northern Bypass for getting around the city",
            "Easy reach of Najjera, Kira and Kisaasi",
        ],
        "around": "From Kiwatule, Ntinda is a short ride away and the Kampala Northern Bypass makes cross-city trips easier. Entebbe International Airport is roughly 1 to 1.5 hours away by road, depending on traffic.",
    },
    "Kulambiro": {
        "slug": "furnished-apartments-kulambiro",
        "geo": (0.3810, 32.6140),
        "intro": "Kulambiro is a quiet, green residential area in north-east Kampala, between Kisaasi, Najjera and Kiwatule. It is a good choice if you want rest and privacy, with Ntinda and Kisaasi close enough for shopping and dining.",
        "why": [
            "Calm, green and residential, away from city noise",
            "Ideal for rest, remote work and longer stays",
            "Close to Kisaasi, Najjera and Ntinda for shops and restaurants",
            "Secure, private apartments with local hosts nearby",
        ],
        "around": "Kulambiro connects by road to Kisaasi, Ntinda and Najjera. Entebbe International Airport is roughly 1 to 1.5 hours away by road, depending on traffic.",
    },
}

TYPES = {
    "Studio apartment": {"short": "Studio", "label": "Furnished studio", "rooms": 1, "beds": 0,
                         "suits": "solo travellers, couples and business visitors"},
    "One bedroom apartment": {"short": "One-bedroom", "label": "One-bedroom apartment", "rooms": 2, "beds": 1,
                              "suits": "couples, remote workers and business travellers"},
    "Three bedroom apartment": {"short": "Three-bedroom", "label": "Three-bedroom apartment", "rooms": 4, "beds": 3,
                                "suits": "families, groups of friends, work teams and relocations"},
}

# Opening sentences rotate between units so that similar apartments
# do not have identical text.
OPENERS = [
    "This {short_l} apartment is a fully furnished home in {loc}, ready for you to move straight in.",
    "Stay in {loc} in this fully furnished {short_l} apartment, set up for comfortable short and long stays.",
    "This {short_l} apartment in {loc} gives you your own private, furnished space with everything you need for the day-to-day.",
    "Looking for a furnished place to stay in {loc}? This {short_l} apartment is a comfortable, self-contained option at a fair nightly price.",
    "Enjoy a private, fully furnished stay in {loc} in this {short_l} apartment, with a kitchen so you can cook for yourself.",
    "Book this furnished {short_l} apartment in {loc} directly with our local host team and skip platform fees.",
]

CSS = """
:root{--brand:#0d6efd;--brand-dark:#0a58ca;--ink:#1d2433;--muted:#5c6577;--bg:#f5f6fa;--card:#fff;--line:#e6e8ef;--ok:#198754}
*{box-sizing:border-box}
body{background:var(--bg);font-family:'Montserrat',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);font-size:1.02rem;line-height:1.65}
h1,h2,h3,h4,.navbar-brand,.btn{font-weight:700;letter-spacing:.2px}
a{color:var(--brand-dark)}
.navbar-brand .logo{width:42px;height:42px;font-size:1.1rem;font-weight:700;box-shadow:0 2px 6px rgba(0,0,0,.2)}
.hero{position:relative;background:#123 url('/images/hero.webp') center/cover no-repeat;min-height:440px}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.55))}
.hero .inner{position:relative;z-index:1;padding:6.5rem 0 4.5rem;text-align:center;color:#fff}
.hero h1{font-size:clamp(2rem,5vw,3.2rem)}
.price-pill{display:inline-block;margin-top:1rem;padding:.55rem 1.2rem;border-radius:50px;background:linear-gradient(135deg,#28a745,#20c997);font-weight:700;color:#fff;box-shadow:0 4px 12px rgba(40,167,69,.3)}
.form-availability{margin-top:-2.5rem;margin-bottom:2rem;background:#fff;border-radius:.6rem;box-shadow:0 .5rem 1rem rgba(0,0,0,.06);padding:1.25rem;position:relative;z-index:3}
.apt-card{background:var(--card);border:1px solid var(--line);border-radius:.75rem;overflow:hidden;height:100%;display:flex;flex-direction:column;transition:transform .2s,box-shadow .2s}
.apt-card:hover{transform:translateY(-3px);box-shadow:0 10px 24px rgba(20,30,60,.08)}
.apt-card img{width:100%;height:240px;object-fit:cover;display:block;background:#dde1ea}
.apt-card .body{padding:1rem 1.1rem 1.2rem;display:flex;flex-direction:column;flex:1}
.apt-card h3{font-size:1.08rem;margin:0 0 .25rem}
.apt-card h3 a{color:var(--ink);text-decoration:none}
.apt-card .loc{color:var(--muted);font-size:.93rem;margin-bottom:.35rem}
.apt-card .price{color:var(--ok);font-weight:700;font-size:1.05rem}
.apt-card ul{padding-left:1.1rem;margin:.5rem 0 1rem;color:var(--muted);font-size:.92rem}
.apt-card .actions{margin-top:auto;display:flex;gap:.5rem}
.section{padding:3.5rem 0}
.section h2{margin-bottom:1rem}
.lead-muted{color:var(--muted);max-width:760px}
.area-card{display:block;background:#fff;border:1px solid var(--line);border-radius:.75rem;padding:1.25rem;text-decoration:none;color:var(--ink);height:100%}
.area-card:hover{border-color:var(--brand)}
.area-card .count{color:var(--muted);font-size:.92rem}
.benefit{background:#fff;border-radius:.75rem;padding:1.5rem;height:100%;text-align:center;border:1px solid var(--line)}
.benefit i{font-size:1.8rem;color:var(--brand)}
.faq details{background:#fff;border:1px solid var(--line);border-radius:.6rem;padding:1rem 1.2rem;margin-bottom:.75rem}
.faq summary{font-weight:700;cursor:pointer}
.faq details p{margin:.75rem 0 0;color:var(--muted)}
.crumbs{font-size:.9rem;color:var(--muted);margin:1.25rem 0 .5rem}
.crumbs a{color:var(--muted)}
.main-photo{width:100%;max-height:520px;object-fit:cover;border-radius:.75rem;background:#dde1ea}
.thumbs{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:.5rem}
.thumbs button{border:0;padding:0;background:none;border-radius:.4rem;overflow:hidden;cursor:zoom-in}
.thumbs img{width:100%;height:110px;object-fit:cover;display:block}
.info-card{background:#fff;border:1px solid var(--line);border-radius:.75rem;padding:1.25rem;margin-bottom:1.25rem}
.info-card ul.check{list-style:none;padding:0;margin:0}
.info-card ul.check li{padding:.45rem 0;border-bottom:1px solid var(--line)}
.info-card ul.check li:last-child{border-bottom:0}
.sticky-book{position:sticky;top:90px}
dialog.viewer{border:0;padding:0;background:transparent;max-width:95vw;max-height:95vh}
dialog.viewer::backdrop{background:rgba(0,0,0,.85)}
dialog.viewer img{max-width:95vw;max-height:88vh;display:block;border-radius:.5rem}
dialog.viewer .bar{display:flex;justify-content:space-between;margin-top:.5rem}
dialog.viewer .bar button{background:#fff;border:0;border-radius:50px;padding:.4rem 1rem;font-weight:700}
footer a{color:#fff}
footer .small-links a{display:inline-block;margin:0 .6rem .4rem 0;opacity:.9}
.wa-float{position:fixed;right:16px;bottom:16px;z-index:50;background:#25d366;color:#fff;border-radius:50px;padding:.7rem 1.1rem;font-weight:700;text-decoration:none;box-shadow:0 6px 18px rgba(0,0,0,.2)}
.wa-float:hover{color:#fff;background:#1ebe57}
@media (max-width:576px){.apt-card img{height:220px}.hero .inner{padding-top:5.5rem}}
"""

def esc(s):
    return html.escape(str(s), quote=True)

def ugx(n):
    return f"UGX {n:,}"

def wa_link(text, number=WHATSAPP):
    from urllib.parse import quote
    return f"https://wa.me/{number}?text={quote(text)}"

_size_cache = {}
def img_size(path):
    if path not in _size_cache:
        with Image.open(os.path.join(ROOT, path.lstrip('/'))) as im:
            _size_cache[path] = im.size
    return _size_cache[path]

def thumb(path):
    return "/images/thumbs/" + os.path.basename(path)

def full(path):
    return "/" + path.lstrip('/')

def apt_slug(a):
    return f"/apartments/apartment-{a['ref'].lower()}.html"

def apt_name(a):
    t = TYPES[a['title']]
    return a['name']

def head(title, description, canonical, image, schema, extra=""):
    schema_json = json.dumps(schema, indent=2, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" type="image/png" href="/favicon.png">
  <meta name="google-site-verification" content="rLjEVKRM0qckd3z85iLLPBOh2bBnLd7H-qq3cSN0mAA" />
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{SITE}{image}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">
{schema_json}
  </script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css" rel="stylesheet">
  <style>{CSS}</style>
  {extra}
  <!-- Google Ads tag. A conversion is now recorded only when someone taps WhatsApp or Call. -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={ADS_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{ADS_ID}');
    document.addEventListener('click', function (e) {{
      var a = e.target.closest('a[href^="https://wa.me"], a[href^="tel:"], [data-conversion]');
      if (a) gtag('event', 'conversion', {{'send_to': '{ADS_CONVERSION}'}});
    }});
  </script>
</head>
<body>
"""

def navbar():
    area_links = "".join(
        f'<li><a class="dropdown-item" href="/{v["slug"]}/">{k}</a></li>' for k, v in AREAS.items())
    return f"""<nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
  <div class="container">
    <a class="navbar-brand d-flex align-items-center" href="/">
      <span class="logo rounded-circle bg-white text-primary d-flex align-items-center justify-content-center">FA</span>
      <span class="ms-2" style="font-size:.95rem;line-height:1.1">Furnished Apartments<br><small class="fw-normal opacity-75">Kampala</small></span>
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Open menu">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
      <ul class="navbar-nav align-items-lg-center">
        <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="/#apartments">Apartments</a></li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="/#areas" role="button" data-bs-toggle="dropdown" aria-expanded="false">Areas</a>
          <ul class="dropdown-menu">{area_links}</ul>
        </li>
        <li class="nav-item"><a class="nav-link" href="/#faq">FAQ</a></li>
        <li class="nav-item ms-lg-2"><a class="btn btn-success btn-sm px-3" href="{wa_link('Hello, I would like to check availability for a furnished apartment in Kampala.')}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> Book on WhatsApp</a></li>
      </ul>
    </div>
  </div>
</nav>
"""

def footer(counts):
    area_links = "".join(f'<a href="/{v["slug"]}/">Furnished apartments in {k} ({counts.get(k,0)})</a>' for k, v in AREAS.items())
    return f"""<footer class="bg-primary text-white mt-5">
  <div class="container py-4">
    <div class="row g-4">
      <div class="col-md-5">
        <div class="d-flex align-items-center mb-2">
          <span class="rounded-circle bg-white text-primary d-flex align-items-center justify-content-center me-3" style="width:52px;height:52px;font-weight:700">FA</span>
          <div><div class="fw-bold">{BRAND}</div><div class="opacity-75">Ntinda · Kisaasi · Kiwatule · Kulambiro, Kampala</div></div>
        </div>
        <p class="opacity-75 mb-0">Fully furnished, Airbnb-style apartments for short and long stays, booked directly with local Ugandan hosts.</p>
      </div>
      <div class="col-md-4 small-links">
        <div class="fw-bold mb-2">Areas</div>
        {area_links}
      </div>
      <div class="col-md-3">
        <div class="fw-bold mb-2">Contact</div>
        <div><i class="bi bi-whatsapp"></i> <a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">+256 704 229100</a></div>
        <div><i class="bi bi-whatsapp"></i> <a href="https://wa.me/{WHATSAPP_2}" target="_blank" rel="noopener">+256 780 228391</a></div>
        <div><i class="bi bi-telephone-fill"></i> <a href="tel:{CALL}">{CALL_DISPLAY}</a></div>
      </div>
    </div>
  </div>
  <div class="text-center text-white-50 py-2" style="background:rgba(0,0,0,.08);font-size:.92rem">&copy; {datetime.date.today().year} {BRAND}. All rights reserved.</div>
</footer>
<a class="wa-float" href="{wa_link('Hello, I would like to check availability for a furnished apartment in Kampala.')}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><i class="bi bi-whatsapp"></i> WhatsApp</a>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" defer></script>
"""

def card(a, eager=False):
    t = TYPES[a['title']]
    w, h = img_size(thumb(a['image']))
    feats = "".join(f"<li>{esc(s)}</li>" for s in a['services'][:4])
    msg = f"Hello, I'd like to book the {a['name']} ({ugx(a['price'])}/night): {SITE}{apt_slug(a)} Is it available?"
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return f"""<div class="col-sm-6 col-lg-4 mb-4 apt-item" data-type="{esc(a['title'])}" data-location="{esc(a['location'])}">
  <article class="apt-card">
    <a href="{apt_slug(a)}"><img src="{thumb(a['image'])}" width="{w}" height="{h}" {loading} decoding="async" alt="{esc(a['name'])}, Kampala"></a>
    <div class="body">
      <h3><a href="{apt_slug(a)}">{esc(a['name'])}</a></h3>
      <div class="loc"><i class="bi bi-geo-alt"></i> <a href="/{AREAS[a['location']]['slug']}/" class="text-reset">{esc(a['location'])}</a>, Kampala · {len(a['gallery'])} photos</div>
      <div class="price">{ugx(a['price'])} <span class="fw-normal text-muted">/ night</span></div>
      <div class="small text-success">Save {WEEKLY_OFF}% weekly · {MONTHLY_OFF}% monthly</div>
      <ul>{feats}</ul>
      <div class="actions">
        <a href="{apt_slug(a)}" class="btn btn-outline-primary flex-fill">View details</a>
        <a href="{wa_link(msg)}" target="_blank" rel="noopener" class="btn btn-success flex-fill"><i class="bi bi-whatsapp"></i> Book</a>
      </div>
    </div>
  </article>
</div>"""

def faq_html(items):
    return "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in items)

def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q,
         "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', a)}} for q, a in items]}

def business_schema(apts):
    prices = [a['price'] for a in apts]
    return {
        "@type": "LodgingBusiness",
        "@id": f"{SITE}/#business",
        "name": BRAND,
        "url": SITE + "/",
        "image": f"{SITE}/images/hero.webp",
        "telephone": CALL,
        "priceRange": f"UGX {min(prices):,} – {max(prices):,} per night",
        "currenciesAccepted": "UGX",
        "address": {"@type": "PostalAddress", "addressLocality": "Kampala",
                    "addressRegion": "Central Region", "addressCountry": "UG"},
        "areaServed": [{"@type": "Place", "name": f"{k}, Kampala"} for k in AREAS],
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": "Free WiFi", "value": True},
                           {"@type": "LocationFeatureSpecification", "name": "Fully equipped kitchen", "value": True}],
        "openingHours": "Mo-Su 00:00-23:59",
        "checkinTime": "13:00",
        "checkoutTime": "11:00",
    }

def breadcrumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

VIEWER = """<dialog class="viewer" id="viewer"><img id="viewer-img" alt=""><div class="bar"><button type="button" id="v-prev">‹ Prev</button><button type="button" id="v-close">Close ✕</button><button type="button" id="v-next">Next ›</button></div></dialog>
<script>
(function(){
  var btns=[].slice.call(document.querySelectorAll('[data-full]')),d=document.getElementById('viewer'),im=document.getElementById('viewer-img'),i=0;
  if(!btns.length||!d)return;
  function show(n){i=(n+btns.length)%btns.length;im.src=btns[i].dataset.full;im.alt=btns[i].querySelector('img').alt;}
  btns.forEach(function(b,n){b.addEventListener('click',function(){show(n);if(d.showModal){d.showModal();}else{window.open(b.dataset.full,'_blank');}});});
  document.getElementById('v-prev').onclick=function(){show(i-1)};
  document.getElementById('v-next').onclick=function(){show(i+1)};
  document.getElementById('v-close').onclick=function(){d.close()};
  d.addEventListener('click',function(e){if(e.target===d)d.close();});
  document.addEventListener('keydown',function(e){if(!d.open)return;if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1);});
})();
</script>"""

# ---------------------------------------------------------------- pages

def build_index(apts, counts):
    min_price = min(a['price'] for a in apts)
    by_type = {}
    for a in apts:
        by_type.setdefault(a['title'], []).append(a['price'])
    faqs = [
        ("How much does a furnished apartment in Kampala cost per night?",
         f"Our studios start from {ugx(min_price)} per night. One-bedroom apartments are from {ugx(min(by_type['One bedroom apartment']))} and three-bedroom apartments from {ugx(min(by_type['Three bedroom apartment']))} per night. There are no booking platform fees because you book directly with us."),
        ("Which areas of Kampala are your apartments in?",
         "All our apartments are in north-east Kampala: <a href='/furnished-apartments-ntinda/'>Ntinda</a>, <a href='/furnished-apartments-kisaasi/'>Kisaasi</a>, <a href='/furnished-apartments-kiwatule/'>Kiwatule</a> and <a href='/furnished-apartments-kulambiro/'>Kulambiro</a>."),
        ("What is included in the apartments?",
         "Every apartment has free WiFi and a fully equipped kitchen. Other amenities depend on the unit and include daily cleaning, balconies, parking, smart TVs, washing machines and, in one three-bedroom apartment, a swimming pool. Each apartment page lists exactly what it includes."),
        ("How do I book?",
         f"Send us a WhatsApp message on <a href='https://wa.me/{WHATSAPP}'>+256 704 229100</a> with your dates and the apartment you like, or call {CALL_DISPLAY}. A local host replies personally to confirm availability and arrange check-in."),
        *STAY_FAQS,
        ("How far are the apartments from Entebbe Airport?",
         "Entebbe International Airport is roughly 1 to 1.5 hours away by road, depending on traffic. Ask us on WhatsApp if you would like help arranging transport."),
    ]
    schema = {"@context": "https://schema.org", "@graph": [
        business_schema(apts),
        {"@type": "WebSite", "@id": f"{SITE}/#website", "url": SITE + "/", "name": BRAND,
         "publisher": {"@id": f"{SITE}/#business"}},
        faq_schema(faqs),
    ]}
    title = f"Airbnb-Style Apartments in Kampala | From UGX {min_price:,}/Night"
    desc = (f"Fully furnished apartments in Ntinda, Kisaasi, Kiwatule and Kulambiro, Kampala, from {ugx(min_price)} per night. "
            f"{WEEKLY_OFF}% off weekly and {MONTHLY_OFF}% off monthly stays. Book directly with local hosts on WhatsApp.")
    types = "".join(f'<option value="{esc(t)}">{esc(TYPES[t]["short"])}</option>' for t in TYPES if t in by_type)
    locs = "".join(f'<option value="{esc(k)}">{esc(k)}</option>' for k in AREAS if counts.get(k))
    cards = "\n".join(card(a, eager=i < 3) for i, a in enumerate(apts))
    area_cards = "".join(f"""<div class="col-sm-6 col-lg-3 mb-3"><a class="area-card" href="/{v['slug']}/">
      <h3 class="h5 mb-1">{k}</h3><div class="count">{counts.get(k,0)} apartment{'s' if counts.get(k,0)!=1 else ''} · from {ugx(min(a['price'] for a in apts if a['location']==k))}/night</div>
      <p class="mb-0 mt-2" style="color:var(--muted);font-size:.93rem">{esc(v['intro'].split('. ')[0])}.</p></a></div>""" for k, v in AREAS.items() if counts.get(k))

    page = head(title, desc, SITE + "/", "/images/hero.webp", schema,
                extra='<link rel="preload" as="image" href="/images/hero.webp">')
    page += navbar()
    page += f"""
<header class="hero">
  <div class="container inner">
    <h1 class="fw-bold mb-3">Airbnb-Style Furnished Apartments in Kampala</h1>
    <p class="lead mb-0">Studios, one- and three-bedroom apartments in Ntinda, Kisaasi, Kiwatule and Kulambiro.<br class="d-none d-md-inline"> Fully furnished · Local hosts · Book directly, no platform fees</p>
    <span class="price-pill"><i class="bi bi-tag-fill"></i> From {ugx(min_price)} per night</span>
    <p class="mt-2 mb-0"><small>Save {WEEKLY_OFF}% on weekly stays and {MONTHLY_OFF}% on monthly stays · Check-in {CHECKIN}, check-out {CHECKOUT}</small></p>
    <div class="d-flex flex-column flex-md-row justify-content-center gap-3 mt-4">
      <a href="#apartments" class="btn btn-success btn-lg shadow"><i class="bi bi-house-door"></i> See apartments</a>
      <a href="tel:{CALL}" class="btn btn-primary btn-lg shadow"><i class="bi bi-telephone-fill"></i> Call {CALL_DISPLAY}</a>
    </div>
  </div>
</header>

<div class="container form-availability" id="form">
  <form class="row g-2 align-items-end justify-content-center" onsubmit="sendWhatsApp();return false;">
    <div class="col-6 col-lg-2"><label for="checkin" class="form-label mb-1">Check-in</label><input type="date" class="form-control" id="checkin"></div>
    <div class="col-6 col-lg-2"><label for="checkout" class="form-label mb-1">Check-out</label><input type="date" class="form-control" id="checkout"></div>
    <div class="col-6 col-lg-3"><label for="filter-size" class="form-label mb-1">Apartment type</label><select id="filter-size" class="form-select"><option value="">All types</option>{types}</select></div>
    <div class="col-6 col-lg-3"><label for="filter-location" class="form-label mb-1">Area</label><select id="filter-location" class="form-select"><option value="">All areas</option>{locs}</select></div>
    <div class="col-12 col-lg-2 d-grid"><button type="submit" class="btn btn-success"><i class="bi bi-whatsapp"></i> Check availability</button></div>
  </form>
</div>

<main>
<section class="container pb-4" id="apartments">
  <h2 class="fw-bold">Our Furnished Apartments in Kampala</h2>
  <p class="lead-muted mb-4">{len(apts)} fully furnished apartments, each with free WiFi and a fully equipped kitchen. Tap an apartment to see all photos, amenities and the nightly price, then book on WhatsApp.</p>
  <div class="row" id="apartment-list">
{cards}
  </div>
  <p id="no-results" class="text-muted" hidden>No apartments match those filters. <a href="#" onclick="resetFilters();return false;">Show all apartments</a>.</p>
</section>

<section class="section bg-white" id="areas">
  <div class="container">
    <h2 class="fw-bold">Where to Stay in Kampala</h2>
    <p class="lead-muted mb-4">Our apartments are in four neighbourhoods in north-east Kampala, each with its own feel. Pick the one that suits your trip.</p>
    <div class="row">{area_cards}</div>
  </div>
</section>

<section class="section" id="why-us">
  <div class="container">
    <h2 class="fw-bold text-center mb-4">Why Book Directly With Us?</h2>
    <div class="row g-3">
      <div class="col-md-4"><div class="benefit"><i class="bi bi-cash-coin"></i><h3 class="h5 mt-2">Fair, clear prices</h3><p class="mb-0">Studios from <strong>{ugx(min_price)} per night</strong>, with <strong>{WEEKLY_OFF}% off weekly</strong> and <strong>{MONTHLY_OFF}% off monthly</strong> stays. No platform fees or hidden charges.</p></div></div>
      <div class="col-md-4"><div class="benefit"><i class="bi bi-person-check"></i><h3 class="h5 mt-2">Local hosts</h3><p class="mb-0">Ugandan hosts who know Kampala well and can help with directions, transport and local tips.</p></div></div>
      <div class="col-md-4"><div class="benefit"><i class="bi bi-chat-dots"></i><h3 class="h5 mt-2">Real people on WhatsApp</h3><p class="mb-0">Message the property managers directly. No bots, just quick, personal replies.</p></div></div>
    </div>
  </div>
</section>

<section class="section bg-white faq" id="faq">
  <div class="container" style="max-width:860px">
    <h2 class="fw-bold mb-4">Frequently Asked Questions</h2>
    {faq_html(faqs)}
  </div>
</section>
</main>
"""
    page += footer(counts)
    page += f"""<script>
  function filterApartments() {{
    var t = document.getElementById('filter-size').value, l = document.getElementById('filter-location').value, shown = 0;
    document.querySelectorAll('.apt-item').forEach(function (el) {{
      var ok = (!t || el.dataset.type === t) && (!l || el.dataset.location === l);
      el.hidden = !ok; if (ok) shown++;
    }});
    document.getElementById('no-results').hidden = shown > 0;
  }}
  function resetFilters() {{
    document.getElementById('filter-size').value = ''; document.getElementById('filter-location').value = ''; filterApartments();
  }}
  function sendWhatsApp() {{
    var v = function (id) {{ return document.getElementById(id).value; }};
    var msg = "Hello, I'd like to check availability for a furnished apartment in Kampala." +
      "\\nCheck-in: " + (v('checkin') || 'Not specified') +
      "\\nCheck-out: " + (v('checkout') || 'Not specified') +
      "\\nArea: " + (v('filter-location') || 'Any') +
      "\\nApartment type: " + (v('filter-size') || 'Any');
    gtag('event', 'conversion', {{'send_to': '{ADS_CONVERSION}'}});
    window.open('https://wa.me/{WHATSAPP}?text=' + encodeURIComponent(msg), '_blank');
  }}
  document.getElementById('filter-size').addEventListener('change', filterApartments);
  document.getElementById('filter-location').addEventListener('change', filterApartments);
</script>
</body>
</html>
"""
    return page

def build_apartment(a, idx, apts, counts):
    t = TYPES[a['title']]
    area = AREAS[a['location']]
    name = apt_name(a)
    url = SITE + apt_slug(a)
    opener = OPENERS[idx % len(OPENERS)].format(
        label=t['label'], short_l=t['short'].lower(), loc=a['location'])
    feats = a['services']
    # lower-case amenity names inside a sentence, but keep words like WiFi and TV
    lc = lambda f: " ".join(w if sum(c.isupper() for c in w) > 1 else w.lower() for w in f.split())
    feat_text = ", ".join(lc(f) for f in feats[:-1]) + f" and {lc(feats[-1])}"
    para2 = (f"It comes with {feat_text}, and is priced at {ugx(a['price'])} per night. "
             f"It suits {t['suits']}, and works well for both short visits and longer stays.")
    para3 = area['intro'].split('. ')[0] + ". " + area['around']
    title = f"{a['name']} – {ugx(a['price'])}/Night"
    desc = (f"{t['label']} in {a['location']}, Kampala for {ugx(a['price'])} per night. "
            f"{', '.join(feats[:3])}. See {len(a['gallery'])} photos and book directly on WhatsApp.")
    msg = f"Hello, I'd like to book the {a['name']} ({ugx(a['price'])}/night): {url} Is it available? My dates are: "
    lat, lng = area['geo']
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Apartment", "@id": url + "#apartment", "name": name, "url": url,
         "description": opener + " " + para2,
         "image": [SITE + full(g) for g in a['gallery']],
         "numberOfRooms": t['rooms'],
         **({"numberOfBedrooms": t['beds']} if t['beds'] else {}),
         "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": f, "value": True} for f in feats],
         "address": {"@type": "PostalAddress", "addressLocality": f"{a['location']}, Kampala",
                     "addressRegion": "Central Region", "addressCountry": "UG"},
         "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng},
         "containedInPlace": {"@id": f"{SITE}/#business"}},
        {**business_schema(apts)},
        breadcrumbs([("Home", SITE + "/"), (f"Furnished apartments in {a['location']}", f"{SITE}/{area['slug']}/"), (a['name'], url)]),
    ]}
    mw, mh = img_size(full(a['gallery'][0]))
    thumbs = "".join(
        f'<button type="button" data-full="{full(g)}"><img src="{thumb(g)}" width="{img_size(thumb(g))[0]}" height="{img_size(thumb(g))[1]}" loading="lazy" decoding="async" alt="{esc(a["name"])}, photo {n+1}"></button>'
        for n, g in enumerate(a['gallery']))
    others = [o for o in apts if o['location'] == a['location'] and o['ref'] != a['ref']][:3]
    if len(others) < 3:
        others += [o for o in apts if o['location'] != a['location'] and o['title'] == a['title']][:3 - len(others)]
    other_cards = "\n".join(card(o) for o in others)
    feat_list = "".join(f'<li><i class="bi bi-check-circle-fill text-success me-2"></i>{esc(f)}</li>' for f in feats)

    page = head(title, desc, url, full(a['gallery'][0]), schema)
    page += navbar()
    page += f"""<main class="container" style="padding-top:72px">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/{area['slug']}/">{a['location']}</a> › {esc(a['name'])}</nav>
  <div class="row g-4">
    <div class="col-lg-8">
      <h1 class="fw-bold h2 mb-2">{esc(name)}</h1>
      <p class="mb-3"><span class="badge bg-primary me-2">{a['location']}, Kampala</span><span class="fw-bold text-success fs-5">{ugx(a['price'])}</span> <span class="text-muted">/ night</span></p>
      <button type="button" data-full="{full(a['gallery'][0])}" class="border-0 p-0 bg-transparent w-100" style="cursor:zoom-in">
        <img class="main-photo" src="{full(a['gallery'][0])}" width="{mw}" height="{mh}" fetchpriority="high" alt="{esc(a['name'])}, Kampala">
      </button>
      <h2 class="h5 mt-4 mb-2">Photos ({len(a['gallery'])})</h2>
      <div class="thumbs mb-4">{thumbs}</div>
      <div class="info-card">
        <h2 class="h4">About this apartment</h2>
        <p>{esc(opener)}</p>
        <p>{esc(para2)}</p>
        <h3 class="h5 mt-3">The area: {a['location']}</h3>
        <p class="mb-0">{esc(para3)} <a href="/{area['slug']}/">More about staying in {a['location']}</a>.</p>
      </div>
      <div class="info-card">
        <h2 class="h4">Amenities</h2>
        <ul class="check">{feat_list}</ul>
      </div>
    </div>
    <aside class="col-lg-4">
      <div class="info-card sticky-book">
        <div class="fs-4 fw-bold text-success">{ugx(a['price'])} <span class="fs-6 fw-normal text-muted">/ night</span></div>
        <ul class="list-unstyled my-3">
          <li><strong>Type:</strong> {t['short']} apartment</li>
          <li><strong>Area:</strong> <a href="/{area['slug']}/">{a['location']}</a>, Kampala</li>
          <li><strong>Check-in:</strong> from {CHECKIN}</li>
          <li><strong>Check-out:</strong> by {CHECKOUT}</li>
        </ul>
        <div class="rounded p-2 mb-3" style="background:#eaf6ee">
          <div class="fw-bold mb-1"><i class="bi bi-percent"></i> Longer stays cost less</div>
          <div class="d-flex justify-content-between"><span>{WEEKLY_NIGHTS}+ nights ({WEEKLY_OFF}% off)</span><strong>{ugx(disc(a['price'], WEEKLY_OFF))}</strong></div>
          <div class="d-flex justify-content-between"><span>{MONTHLY_NIGHTS}+ nights ({MONTHLY_OFF}% off)</span><strong>{ugx(disc(a['price'], MONTHLY_OFF))}</strong></div>
          <div class="small text-muted">Price per night</div>
        </div>
        <a href="{wa_link(msg)}" target="_blank" rel="noopener" class="btn btn-success btn-lg w-100 mb-2"><i class="bi bi-whatsapp"></i> Book on WhatsApp</a>
        <a href="tel:{CALL}" class="btn btn-outline-primary w-100"><i class="bi bi-telephone"></i> Call {CALL_DISPLAY}</a>
        <p class="small text-muted mt-3 mb-0">Book directly with our local hosts. No platform fees.</p>
      </div>
    </aside>
  </div>
  <section class="mt-4">
    <h2 class="h4 fw-bold mb-3">More furnished apartments {"in " + a['location'] if any(o['location']==a['location'] for o in others) else "you may like"}</h2>
    <div class="row">{other_cards}</div>
    <p><a href="/#apartments">See all {len(apts)} apartments</a></p>
  </section>
</main>
{VIEWER}
"""
    page += footer(counts)
    page += "</body>\n</html>\n"
    return page

def build_area(name, area, apts, counts):
    here = [a for a in apts if a['location'] == name]
    url = f"{SITE}/{area['slug']}/"
    low = min(a['price'] for a in here)
    kinds = sorted({TYPES[a['title']]['short'].lower() for a in here}, key=lambda k: ["studio", "one-bedroom", "three-bedroom"].index(k))
    kinds_text = (", ".join(kinds[:-1]) + " and " + kinds[-1]) if len(kinds) > 1 else kinds[0]
    title = f"Furnished Apartments in {name}, Kampala | From UGX {low:,}/Night"
    desc = (f"{len(here)} fully furnished {kinds_text} apartment{'s' if len(here)>1 else ''} in {name}, Kampala, from {ugx(low)} per night. "
            "Free WiFi and kitchen. Book directly with local hosts on WhatsApp.")
    faqs = [
        (f"How much does a furnished apartment in {name} cost?",
         f"Our apartments in {name} start from {ugx(low)} per night. Prices for each unit are shown above."),
        (f"How far is {name} from Entebbe Airport?",
         "Entebbe International Airport is roughly 1 to 1.5 hours away by road, depending on traffic."),
        *STAY_FAQS,
    ]
    lat, lng = area['geo']
    schema = {"@context": "https://schema.org", "@graph": [
        {**business_schema(apts)},
        {"@type": "ItemList", "name": f"Furnished apartments in {name}, Kampala",
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + apt_slug(a), "name": apt_name(a)} for i, a in enumerate(here)]},
        {"@type": "Place", "name": f"{name}, Kampala", "geo": {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}},
        breadcrumbs([("Home", SITE + "/"), (f"Furnished apartments in {name}", url)]),
        faq_schema(faqs),
    ]}
    why = "".join(f'<li><i class="bi bi-check-circle-fill text-success me-2"></i>{esc(w)}</li>' for w in area['why'])
    cards = "\n".join(card(a, eager=i < 3) for i, a in enumerate(here))
    other = " · ".join(f'<a href="/{v["slug"]}/">{k}</a>' for k, v in AREAS.items() if k != name and counts.get(k))
    msg = f"Hello, I'm looking for a furnished apartment in {name}. My dates are: "
    page = head(title, desc, url, full(here[0]['image']), schema)
    page += navbar()
    page += f"""<main class="container" style="padding-top:72px">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › {name}</nav>
  <h1 class="fw-bold h2">Furnished Apartments in {name}, Kampala</h1>
  <p class="lead-muted">{esc(area['intro'])}</p>
  <p class="mb-4"><span class="fw-bold text-success">From {ugx(low)} per night</span> · {WEEKLY_OFF}% off weekly, {MONTHLY_OFF}% off monthly · {len(here)} apartment{'s' if len(here)>1 else ''} · Free WiFi and kitchen in every unit
    <a href="{wa_link(msg)}" target="_blank" rel="noopener" class="btn btn-success btn-sm ms-md-2 mt-2 mt-md-0"><i class="bi bi-whatsapp"></i> Ask about availability</a></p>
  <div class="row">{cards}</div>
  <div class="row g-4 mt-1">
    <div class="col-lg-6"><div class="info-card h-100"><h2 class="h4">Why stay in {name}?</h2><ul class="check">{why}</ul></div></div>
    <div class="col-lg-6"><div class="info-card h-100"><h2 class="h4">Getting around</h2><p class="mb-0">{esc(area['around'])}</p></div></div>
  </div>
  <section class="faq mt-2">
    <h2 class="h4 fw-bold mb-3">Questions about staying in {name}</h2>
    {faq_html(faqs)}
  </section>
  <p class="mt-4">Other areas: {other} · <a href="/#apartments">All apartments</a></p>
</main>
"""
    page += footer(counts)
    page += "</body>\n</html>\n"
    return page

def build_sitemap(apts, counts):
    urls = [(SITE + "/", "1.0")]
    urls += [(f"{SITE}/{v['slug']}/", "0.9") for k, v in AREAS.items() if counts.get(k)]
    urls += [(SITE + apt_slug(a), "0.8") for a in apts]
    body = "".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{p}</priority>\n  </url>\n" for u, p in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'

def main():
    apts = json.load(open(os.path.join(ROOT, "data/apartments.json")))
    counts = {}
    for a in apts:
        counts[a['location']] = counts.get(a['location'], 0) + 1
        if a['location'] not in AREAS:
            raise SystemExit(f"Add '{a['location']}' to AREAS in _build/build.py first.")
        if a['title'] not in TYPES:
            raise SystemExit(f"Add '{a['title']}' to TYPES in _build/build.py first.")

    def write(rel, text):
        p = os.path.join(ROOT, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)

    write("index.html", build_index(apts, counts))
    for i, a in enumerate(apts):
        write(apt_slug(a).lstrip('/'), build_apartment(a, i, apts, counts))
    for k, v in AREAS.items():
        if counts.get(k):
            write(f"{v['slug']}/index.html", build_area(k, v, apts, counts))
    write("sitemap.xml", build_sitemap(apts, counts))
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Built home page, {len(apts)} apartment pages, {sum(1 for k in AREAS if counts.get(k))} area pages, sitemap and robots.txt")

if __name__ == "__main__":
    main()
