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
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guides import GUIDES

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
GOOGLE_PROFILE = "https://www.google.com/maps?cid=17499836862195176242"  # Google Business Profile
BUSINESS_GEO = (0.3675737, 32.6198788)
REVIEWS = json.load(open(os.path.join(ROOT, "data/reviews.json")))

def stars_html(n):
    n = round(n * 2) / 2
    return "".join('<i class="bi bi-star-fill"></i>' if i + 1 <= n else ('<i class="bi bi-star-half"></i>' if i + 0.5 == n else '<i class="bi bi-star"></i>') for i in range(5))

def reviews_block(limit=4, heading="What Our Guests Say", wrap=True):
    items = REVIEWS["reviews"][:limit]
    cards = "".join(f"""<div class="col-md-6 {'col-lg-3' if limit >= 4 else ''} mb-3"><figure class="review h-100">
        <div class="review-stars" aria-label="{r['stars']} out of 5 stars">{stars_html(r['stars'])}</div>
        <blockquote class="mb-2">{esc(r['text'])}</blockquote>
        <figcaption>{esc(r['name'])} <span class="text-muted">· Google review</span></figcaption>
      </figure></div>""" for r in items)
    inner = f"""<div class="d-flex flex-wrap align-items-end justify-content-between gap-2 mb-3">
      <div><h2 class="fw-bold {'h4' if not wrap else ''} mb-1">{heading}</h2>
      <div><span class="review-stars">{stars_html(REVIEWS['rating'])}</span> <strong>{REVIEWS['rating']}</strong> on Google from {REVIEWS['count']} reviews</div></div>
      <a class="btn btn-outline-primary btn-sm" href="{GOOGLE_PROFILE}" target="_blank" rel="noopener">Read all reviews on Google</a>
    </div>
    <div class="row">{cards}</div>"""
    return f'<section class="section" id="reviews"><div class="container">{inner}</div></section>' if wrap else f'<section class="mt-4" id="reviews">{inner}</section>'

def map_block(lat, lng, heading, profile=None):
    profile = profile or GOOGLE_PROFILE
    return f"""<div class="info-card">
        <h2 class="h4">{heading}</h2>
        <div class="ratio ratio-16x9 rounded overflow-hidden mb-3" style="background:#dde1ea">
          <iframe src="https://www.google.com/maps?q={lat},{lng}&z=16&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map showing the apartment location" style="border:0" allowfullscreen></iframe>
        </div>
        <div class="d-flex flex-wrap gap-2">
          <a class="btn btn-outline-primary btn-sm" href="https://www.google.com/maps/dir/?api=1&destination={lat},{lng}" target="_blank" rel="noopener"><i class="bi bi-sign-turn-right"></i> Get directions</a>
          <a class="btn btn-outline-secondary btn-sm" href="{profile}" target="_blank" rel="noopener"><i class="bi bi-star-fill text-warning"></i> See our Google reviews</a>
        </div>
      </div>"""
CHECKIN, CHECKOUT = "1:00 PM", "11:00 AM"
PICKUP_PRICE = 180000  # airport pickup, per trip
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
    "Two bedroom apartment": {"short": "Two-bedroom", "label": "Two-bedroom apartment", "rooms": 3, "beds": 2,
                              "suits": "families, small groups and colleagues travelling together"},
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
:root{--brand:#1b2a41;--brand-dark:#8a6420;--navy:#1b2a41;--navy-2:#2a3d5c;--gold:#b8892e;--gold-light:#e3c27a;--ink:#1d2433;--muted:#5c6577;--bg:#f5f6fa;--card:#fff;--line:#e6e8ef;--ok:#198754}
*{box-sizing:border-box}
body{background:var(--bg);font-family:'Montserrat',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--ink);font-size:1.02rem;line-height:1.65}
h1,h2,h3,h4,.navbar-brand,.btn{font-weight:700;letter-spacing:.2px}
a{color:var(--brand-dark)}
:root{--bs-primary:#1b2a41;--bs-primary-rgb:27,42,65;--bs-link-color:#8a6420;--bs-link-color-rgb:138,100,32;--bs-link-hover-color:#6b4c14;--bs-link-hover-color-rgb:107,76,20}
.btn-primary{--bs-btn-bg:#1b2a41;--bs-btn-border-color:#1b2a41;--bs-btn-hover-bg:#2a3d5c;--bs-btn-hover-border-color:#2a3d5c;--bs-btn-active-bg:#142033;--bs-btn-active-border-color:#142033}
.btn-outline-primary{--bs-btn-color:#1b2a41;--bs-btn-border-color:#1b2a41;--bs-btn-hover-bg:#1b2a41;--bs-btn-hover-border-color:#1b2a41;--bs-btn-active-bg:#142033;--bs-btn-active-border-color:#142033}
.navbar.bg-primary{border-bottom:2px solid var(--gold)}
footer.bg-primary{border-top:3px solid var(--gold)}
footer a:hover,.navbar-dark .nav-link:hover{color:var(--gold-light)!important}
.dropdown-item:active{background:var(--navy)}
.logo-mark{display:block;flex:none;filter:drop-shadow(0 2px 4px rgba(0,0,0,.18))}
.brand-text{font-size:1rem;line-height:1.1;display:flex;flex-direction:column}
.brand-text small{font-weight:400;opacity:.8;font-size:.75rem;letter-spacing:.5px;margin-top:2px}
.hero{position:relative;background:#123 url('/images/hero.webp') center/cover no-repeat;min-height:440px}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.35),rgba(0,0,0,.55))}
.hero .inner{position:relative;z-index:1;padding:6.5rem 0 4.5rem;text-align:center;color:#fff}
.hero h1{font-size:clamp(2rem,5vw,3.2rem)}
.price-pill{display:inline-block;margin-top:1rem;padding:.55rem 1.2rem;border-radius:50px;background:var(--gold);font-weight:700;color:#fff;box-shadow:0 4px 12px rgba(184,137,46,.35)}
.form-availability{background:#fff;border:1px solid var(--line);border-radius:.75rem;box-shadow:0 .5rem 1rem rgba(0,0,0,.04);padding:1.25rem}
.apt-card{background:var(--card);border:1px solid var(--line);border-radius:.85rem;overflow:hidden;height:100%;display:flex;flex-direction:column;transition:box-shadow .2s}
.apt-card:hover{box-shadow:0 10px 24px rgba(20,30,60,.09)}
.ph{position:relative;overflow:hidden;aspect-ratio:4/3;background:#dde1ea}
.ph-track{display:flex;height:100%;transition:transform .3s ease}
.ph-track img{flex:0 0 100%;width:100%;height:100%;object-fit:cover;display:block}
.ph-prev,.ph-next{position:absolute;top:50%;transform:translateY(-50%);width:32px;height:32px;border-radius:50%;border:0;background:rgba(255,255,255,.92);color:#222;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 4px rgba(0,0,0,.25);font-size:.9rem}
.ph-prev{left:8px}.ph-next{right:8px}
@media (hover:hover){.ph-prev,.ph-next{opacity:0;transition:opacity .2s}.apt-card:hover .ph-prev,.apt-card:hover .ph-next{opacity:1}}
.ph-count{position:absolute;right:8px;bottom:8px;background:rgba(0,0,0,.6);color:#fff;font-size:.75rem;padding:.1rem .5rem;border-radius:50px}
.apt-card .body{padding:.8rem .9rem .9rem;display:flex;flex-direction:column;flex:1}
.apt-card h3{font-size:1rem;margin:0 0 .15rem;line-height:1.3}
.apt-card h3 a{color:var(--ink);text-decoration:none}
.apt-card .meta{color:var(--muted);font-size:.85rem}
.apt-card .price{font-weight:700;font-size:1.02rem;margin-top:.35rem}
.apt-card .price span{font-weight:400;color:var(--muted);font-size:.88rem}
.apt-card .deal{color:var(--ok);font-size:.8rem;margin-bottom:.7rem}
.chips-bar{position:sticky;top:66px;z-index:20;background:var(--bg);padding:.5rem 0;margin:0 -12px .5rem;padding-left:12px;padding-right:12px}
.chips{display:flex;gap:.45rem;overflow-x:auto;scrollbar-width:none;padding-bottom:.35rem}
.chips::-webkit-scrollbar{display:none}
.chip{flex:none;border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:50px;padding:.38rem .9rem;font-size:.9rem;font-weight:600;white-space:nowrap}
.chip span{color:var(--muted);font-weight:400;margin-left:.15rem}
.chip.active{background:var(--navy);border-color:var(--navy);color:#fff}
.chip.active span{color:#c9cfdb}
.apt-group{margin-top:1.25rem}
.group-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:.6rem}
.group-head h3 span{font-weight:400;color:var(--muted);font-size:.88rem;margin-left:.3rem}
.row-nav{gap:.4rem}
.row-nav button{width:34px;height:34px;border-radius:50%;border:1px solid var(--line);background:#fff}
.row-nav button:hover{border-color:var(--ink)}
.apt-row{display:grid;grid-auto-flow:column;grid-auto-columns:min(80%,290px);gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-left:2px;padding:2px 2px 10px;scrollbar-width:thin;overscroll-behavior-x:contain}
.apt-row>.apt-card{scroll-snap-align:start}
@media (min-width:992px){.apt-row{grid-auto-columns:calc((100% - 42px)/4);scrollbar-width:none}.apt-row::-webkit-scrollbar{display:none}}
.see-area{display:inline-block;font-size:.9rem;font-weight:600;text-decoration:none;margin-top:.1rem}
.article{background:#fff;border:1px solid var(--line);border-radius:.85rem;padding:1.5rem 1.4rem}
.article h2{font-size:1.35rem;margin-top:1.8rem}
.article h3{font-size:1.08rem;margin-top:1.3rem}
.article .lead{font-size:1.12rem;color:var(--ink)}
.article li{margin-bottom:.35rem}
table.compare{table-layout:fixed;width:100%}table.compare th{font-weight:700}table.compare th:first-child{width:28%}
@media (max-width:576px){table.compare{font-size:.85rem}table.compare td,table.compare th{padding:.45rem .4rem!important}.article{padding:1.1rem .9rem}}
table.compare td,table.compare th{padding:.6rem .7rem;vertical-align:top}
table.compare thead th{background:var(--navy);color:#fff}
.guide-card{display:flex;gap:.9rem;background:#fff;border:1px solid var(--line);border-radius:.75rem;padding:1.1rem;text-decoration:none;color:var(--ink);height:100%}
.guide-card:hover{border-color:var(--gold)}
.guide-card i{font-size:1.6rem;color:var(--gold);flex:none}
.guide-card p{color:var(--muted);font-size:.92rem;margin:0}
.mobile-bar{position:fixed;left:0;right:0;bottom:0;z-index:60;display:flex;gap:.6rem;padding:.6rem 12px calc(.6rem + env(safe-area-inset-bottom));background:#fff;border-top:1px solid var(--line);box-shadow:0 -4px 16px rgba(0,0,0,.06)}
.mobile-bar .btn{flex:1;font-weight:700;padding:.6rem}
.mobile-bar .btn-success{flex:1.6}
@media (max-width:991.98px){body{padding-bottom:76px}}
.section{padding:3.5rem 0}
.section h2{margin-bottom:1rem}
.lead-muted{color:var(--muted);max-width:760px}
.area-card{display:block;background:#fff;border:1px solid var(--line);border-radius:.75rem;padding:1.25rem;text-decoration:none;color:var(--ink);height:100%}
.area-card:hover{border-color:var(--gold)}
.area-card .count{color:var(--muted);font-size:.92rem}
.benefit{background:#fff;border-radius:.75rem;padding:1.5rem;height:100%;text-align:center;border:1px solid var(--line)}
.benefit i{font-size:1.8rem;color:var(--gold)}
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
.review{background:#fff;border:1px solid var(--line);border-radius:.75rem;padding:1.1rem;margin:0;display:flex;flex-direction:column}
.review blockquote{font-size:.95rem;color:var(--ink);flex:1}
.review figcaption{font-weight:700;font-size:.9rem}
.review-stars{color:#f5a623;letter-spacing:1px}
@media (max-width:767.98px){.hero{min-height:0}.hero .inner{padding:5.2rem 0 1.6rem}.hero h1{font-size:1.65rem;margin-bottom:.6rem!important}.hero .lead{font-size:1rem}.price-pill{margin-top:.7rem;font-size:.95rem;padding:.4rem 1rem}.chips-bar{top:62px}.brand-text{font-size:.92rem}}
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

LOGO_MARK = """<svg class="logo-mark" viewBox="0 0 48 48" width="40" height="40" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#fff"/><path d="M10 24 24 12l14 12" fill="none" stroke="#1b2a41" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 22v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V22" fill="none" stroke="#1b2a41" stroke-width="4" stroke-linejoin="round"/><rect x="21" y="28" width="6" height="10" rx="1.5" fill="#b8892e"/></svg>"""

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
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="icon" type="image/png" href="/favicon.png">
  <link rel="apple-touch-icon" href="/favicon.png">
  <meta name="theme-color" content="#1b2a41">
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
      {LOGO_MARK}
      <span class="ms-2 brand-text">Furnished Apartments<small>Kampala · Uganda</small></span>
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
        <li class="nav-item"><a class="nav-link" href="/guides/">Guides</a></li>
        <li class="nav-item"><a class="nav-link" href="/#faq">FAQ</a></li>
        <li class="nav-item ms-lg-2"><a class="btn btn-success btn-sm px-3" href="{wa_link('Hello, I would like to check availability for a furnished apartment in Kampala.')}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> Book on WhatsApp</a></li>
      </ul>
    </div>
  </div>
</nav>
"""

def footer(counts, wa_msg="Hello, I would like to check availability for a furnished apartment in Kampala."):
    area_links = "".join(f'<a href="/{v["slug"]}/">Furnished apartments in {k} ({counts.get(k,0)})</a>' for k, v in AREAS.items())
    return f"""<footer class="bg-primary text-white mt-5">
  <div class="container py-4">
    <div class="row g-4">
      <div class="col-md-5">
        <div class="d-flex align-items-center mb-2">
          <span class="me-3">{LOGO_MARK}</span>
          <div><div class="fw-bold">{BRAND}</div><div class="opacity-75">Ntinda · Kisaasi · Kiwatule · Kulambiro, Kampala</div></div>
        </div>
        <p class="opacity-75 mb-0">Fully furnished, Airbnb-style apartments for short and long stays, booked directly with local Ugandan hosts.</p>
      </div>
      <div class="col-md-4 small-links">
        <div class="fw-bold mb-2">Areas</div>
        {area_links}
        <div class="fw-bold mb-2 mt-3">Travel guides</div>
        {"".join(f'<a href="/guides/{g["slug"]}/">{esc(g["title"])}</a>' for g in GUIDES)}
      </div>
      <div class="col-md-3">
        <div class="fw-bold mb-2">Contact</div>
        <div><i class="bi bi-whatsapp"></i> <a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">+256 704 229100</a></div>
        <div><i class="bi bi-whatsapp"></i> <a href="https://wa.me/{WHATSAPP_2}" target="_blank" rel="noopener">+256 780 228391</a></div>
        <div><i class="bi bi-telephone-fill"></i> <a href="tel:{CALL}">{CALL_DISPLAY}</a></div>
        <div class="mt-2"><i class="bi bi-star-fill text-warning"></i> <a href="{GOOGLE_PROFILE}" target="_blank" rel="noopener">Our reviews on Google</a></div>
      </div>
    </div>
  </div>
  <div class="text-center text-white-50 py-2" style="background:rgba(0,0,0,.08);font-size:.92rem">&copy; {datetime.date.today().year} {BRAND}. All rights reserved.</div>
</footer>
<a class="wa-float d-none d-lg-inline-block" href="{wa_link(wa_msg)}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><i class="bi bi-whatsapp"></i> WhatsApp</a>
<div class="mobile-bar d-lg-none">
  <a class="btn btn-success" href="{wa_link(wa_msg)}" target="_blank" rel="noopener"><i class="bi bi-whatsapp"></i> WhatsApp</a>
  <a class="btn btn-outline-primary" href="tel:{CALL}"><i class="bi bi-telephone-fill"></i> Call</a>
</div>
<script>
  // photo arrows on apartment cards
  document.addEventListener('click', function (e) {{
    var b = e.target.closest('.ph-prev, .ph-next'); if (!b) return;
    e.preventDefault();
    var ph = b.closest('.ph'), imgs = ph.querySelectorAll('img'), n = imgs.length;
    var i = ((+ph.dataset.i || 0) + (b.classList.contains('ph-next') ? 1 : -1) + n) % n;
    [i, (i + 1) % n].forEach(function (k) {{ var im = imgs[k]; if (im.dataset.src) {{ im.src = im.dataset.src; im.removeAttribute('data-src'); }} }});
    ph.dataset.i = i; ph.querySelector('.ph-track').style.transform = 'translateX(' + (-100 * i) + '%)';
    ph.querySelector('.ph-count').textContent = (i + 1) + ' / ' + n;
  }});
</script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" defer></script>
"""

TYPE_SHORT = {"Studio apartment": "Studio", "One bedroom apartment": "1-Bedroom", "Two bedroom apartment": "2-Bedroom", "Three bedroom apartment": "3-Bedroom"}

def card(a, eager=False, wrap=True):
    msg = f"Hello, I'd like to book the {a['name']} ({ugx(a['price'])}/night): {SITE}{apt_slug(a)} Is it available?"
    pics = a['gallery'][:5]
    w, h = img_size(thumb(pics[0]))
    imgs = []
    for k, g in enumerate(pics):
        alt = f"{esc(a['name'])}, Kampala" + (f" – photo {k+1}" if k else "")
        if k == 0:
            load = 'fetchpriority="high"' if eager else 'loading="lazy"'
            imgs.append(f'<img src="{thumb(g)}" width="{w}" height="{h}" {load} decoding="async" alt="{alt}">')
        else:
            imgs.append(f'<img data-src="{thumb(g)}" width="{w}" height="{h}" decoding="async" alt="{alt}">')
    arrows = (f'<button type="button" class="ph-prev" aria-label="Previous photo"><i class="bi bi-chevron-left"></i></button>'
              f'<button type="button" class="ph-next" aria-label="Next photo"><i class="bi bi-chevron-right"></i></button>'
              f'<span class="ph-count">1 / {len(pics)}</span>') if len(pics) > 1 else ""
    inner = f"""<article class="apt-card apt-item" data-type="{esc(a['title'])}" data-location="{esc(a['location'])}">
    <div class="ph"><a class="ph-track" href="{apt_slug(a)}">{''.join(imgs)}</a>{arrows}</div>
    <div class="body">
      <h3><a href="{apt_slug(a)}">{esc(a['name'])}</a></h3>
      <div class="meta">{TYPE_SHORT[a['title']]} · {esc(a['location'])}, Kampala</div>
      <div class="price">{ugx(a['price'])} <span>/ night</span></div>
      <div class="deal">{WEEKLY_OFF}% off weekly · {MONTHLY_OFF}% off monthly</div>
      <a href="{wa_link(msg)}" target="_blank" rel="noopener" class="btn btn-success btn-sm w-100 mt-auto"><i class="bi bi-whatsapp"></i> Book on WhatsApp</a>
    </div>
  </article>"""
    return f'<div class="col-sm-6 col-lg-4 col-xl-3 mb-4">{inner}</div>' if wrap else inner

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
        "hasMap": GOOGLE_PROFILE,
        "sameAs": [GOOGLE_PROFILE],
        "geo": {"@type": "GeoCoordinates", "latitude": BUSINESS_GEO[0], "longitude": BUSINESS_GEO[1]},
        "image": f"{SITE}/images/hero.webp",
        "telephone": CALL,
        "priceRange": f"UGX {min(prices):,} – {max(prices):,} per night",
        "currenciesAccepted": "UGX",
        "address": {"@type": "PostalAddress", "streetAddress": "Namuganza Road, Ntinda", "addressLocality": "Kampala",
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
         f"Our studios start from {ugx(min_price)} per night. " + " ".join(f"{TYPES[t]['short']} apartments are from {ugx(min(by_type[t]))} per night." for t in TYPES if t in by_type and t != 'Studio apartment') + " There are no booking platform fees because you book directly with us."),
        ("Which areas of Kampala are your apartments in?",
         "All our apartments are in north-east Kampala: <a href='/furnished-apartments-ntinda/'>Ntinda</a>, <a href='/furnished-apartments-kisaasi/'>Kisaasi</a>, <a href='/furnished-apartments-kiwatule/'>Kiwatule</a> and <a href='/furnished-apartments-kulambiro/'>Kulambiro</a>."),
        ("What is included in the apartments?",
         "Every apartment has free WiFi and a fully equipped kitchen. Other amenities depend on the unit and include daily cleaning, balconies, parking, smart TVs, washing machines and, in one three-bedroom apartment, a swimming pool. Each apartment page lists exactly what it includes."),
        ("How do I book?",
         f"Send us a WhatsApp message on <a href='https://wa.me/{WHATSAPP}'>+256 704 229100</a> with your dates and the apartment you like, or call {CALL_DISPLAY}. A local host replies personally to confirm availability and arrange check-in."),
        *STAY_FAQS,
        ("How far are the apartments from Entebbe Airport? Do you offer airport pickup?",
         f"Entebbe International Airport is roughly 1 to 1.5 hours away by road, depending on traffic. We offer airport pickup for {ugx(PICKUP_PRICE)} per trip; send your flight number and arrival time on WhatsApp to book it. Read our <a href='/guides/entebbe-airport-to-ntinda/'>airport transfer guide</a> for all the options."),
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
    locs = "".join(f'<option value="{esc(k)}">{esc(k)}</option>' for k in AREAS if counts.get(k))
    kinds_present = [TYPES[t]['short'].lower().replace('-bedroom', '') for t in TYPES if t in by_type and t != 'Studio apartment']
    hero_kinds = "Studios, " + (", ".join(k + "-" for k in kinds_present[:-1]) + " and " + kinds_present[-1] + "-bedroom apartments" if len(kinds_present) > 1 else kinds_present[0] + "-bedroom apartments")
    order = sorted([k for k in AREAS if counts.get(k)], key=lambda k: -counts[k])
    area_chips = '<button type="button" class="chip active" data-area="">All areas</button>' + "".join(
        f'<button type="button" class="chip" data-area="{esc(k)}">{k} <span>{counts[k]}</span></button>' for k in order)
    type_chips = '<button type="button" class="chip active" data-kind="">All types</button>' + "".join(
        f'<button type="button" class="chip" data-kind="{esc(t)}">{TYPE_SHORT[t]}</button>' for t in TYPES if t in by_type)
    groups, n = [], 0
    for k in order:
        here = sorted([a for a in apts if a['location'] == k], key=lambda a: not a.get('featured'))
        row = "".join(card(a, eager=(n + i) < 2, wrap=False) for i, a in enumerate(here))
        n += len(here)
        groups.append(f"""<div class="apt-group" data-location="{esc(k)}">
    <div class="group-head">
      <h3 class="h5 fw-bold mb-0"><a href="/{AREAS[k]['slug']}/" class="text-reset text-decoration-none">{k}</a> <span>{len(here)} apartment{'s' if len(here) != 1 else ''} · from {ugx(min(a['price'] for a in here))}</span></h3>
      <div class="row-nav d-none d-lg-flex"><button type="button" class="row-prev" aria-label="Scroll left"><i class="bi bi-chevron-left"></i></button><button type="button" class="row-next" aria-label="Scroll right"><i class="bi bi-chevron-right"></i></button></div>
    </div>
    <div class="apt-row">{row}</div>
    <a class="see-area" href="/{AREAS[k]['slug']}/">About staying in {k} <i class="bi bi-arrow-right"></i></a>
  </div>""")
    groups = "\n".join(groups)
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
    <p class="lead mb-0">{hero_kinds} in Ntinda, Kisaasi, Kiwatule and Kulambiro.<span class="d-none d-md-inline"><br> Fully furnished · Local hosts · Book directly, no platform fees</span></p>
    <span class="price-pill"><i class="bi bi-tag-fill"></i> From {ugx(min_price)} per night</span>
    <a href="#reviews" class="d-inline-block mt-2 ms-md-2 text-white text-decoration-none"><span class="review-stars">{stars_html(REVIEWS['rating'])}</span> <strong>{REVIEWS['rating']}</strong> on Google · {REVIEWS['count']} reviews</a>
    <p class="mt-2 mb-0 d-none d-md-block"><small>Save {WEEKLY_OFF}% on weekly stays and {MONTHLY_OFF}% on monthly stays · Check-in {CHECKIN}, check-out {CHECKOUT}</small></p>
    <div class="d-none d-md-flex justify-content-center gap-3 mt-4">
      <a href="#apartments" class="btn btn-success btn-lg shadow"><i class="bi bi-house-door"></i> See apartments</a>
      <a href="tel:{CALL}" class="btn btn-outline-light btn-lg shadow"><i class="bi bi-telephone-fill"></i> Call {CALL_DISPLAY}</a>
    </div>
  </div>
</header>

<main>
<section class="container pt-4 pb-2" id="apartments">
  <h2 class="fw-bold mb-1">Our Furnished Apartments</h2>
  <p class="lead-muted mb-3">{len(apts)} apartments with free WiFi and a full kitchen. Tap one for all photos and details.</p>
  <div class="chips-bar">
    <div class="chips" role="group" aria-label="Filter by area">{area_chips}</div>
    <div class="chips" role="group" aria-label="Filter by type">{type_chips}</div>
  </div>
  {groups}
  <p id="no-results" class="text-muted mt-3" hidden>No apartments match those filters. <a href="#" onclick="resetFilters();return false;">Show all apartments</a>.</p>
</section>


<section class="section bg-white" id="areas">
  <div class="container">
    <h2 class="fw-bold">Where to Stay in Kampala</h2>
    <p class="lead-muted mb-4">Our apartments are in four neighbourhoods in north-east Kampala, each with its own feel. Pick the one that suits your trip.</p>
    <div class="row">{area_cards}</div>
  </div>
</section>

{reviews_block()}

<section class="section bg-white" id="why-us">
  <div class="container">
    <h2 class="fw-bold text-center mb-4">Why Book Directly With Us?</h2>
    <div class="row g-3">
      <div class="col-md-4"><div class="benefit"><i class="bi bi-cash-coin"></i><h3 class="h5 mt-2">Fair, clear prices</h3><p class="mb-0">Studios from <strong>{ugx(min_price)} per night</strong>, with <strong>{WEEKLY_OFF}% off weekly</strong> and <strong>{MONTHLY_OFF}% off monthly</strong> stays. No platform fees or hidden charges.</p></div></div>
      <div class="col-md-4"><div class="benefit"><i class="bi bi-person-check"></i><h3 class="h5 mt-2">Local hosts</h3><p class="mb-0">Ugandan hosts who know Kampala well and can help with directions, transport and local tips.</p></div></div>
      <div class="col-md-4"><div class="benefit"><i class="bi bi-chat-dots"></i><h3 class="h5 mt-2">Real people on WhatsApp</h3><p class="mb-0">Message the property managers directly. No bots, just quick, personal replies.</p></div></div>
    </div>
  </div>
</section>

<section class="section" id="guides">
  <div class="container">
    <h2 class="fw-bold mb-1">Kampala Travel Guides</h2>
    <p class="lead-muted mb-3">Practical tips to help you plan your stay.</p>
    <div class="row g-3">{guide_cards()}</div>
  </div>
</section>

<section class="section faq" id="faq">
  <div class="container" style="max-width:860px">
    <h2 class="fw-bold mb-4">Frequently Asked Questions</h2>
    {faq_html(faqs)}
  </div>
</section>
</main>
"""
    page += footer(counts)
    page += f"""<script>
  var state = {{area: '', kind: ''}};
  function filterApartments() {{
    var total = 0;
    document.querySelectorAll('.apt-group').forEach(function (g) {{
      var shown = 0, areaOk = !state.area || g.dataset.location === state.area;
      g.querySelectorAll('.apt-item').forEach(function (el) {{
        var ok = areaOk && (!state.kind || el.dataset.type === state.kind);
        el.hidden = !ok; if (ok) shown++;
      }});
      g.hidden = shown === 0; total += shown;
      g.querySelector('.apt-row').scrollLeft = 0;
    }});
    document.getElementById('no-results').hidden = total > 0;
  }}
  function setChip(attr, value) {{
    document.querySelectorAll('.chip[data-' + attr + ']').forEach(function (c) {{ c.classList.toggle('active', c.dataset[attr] === value); }});
  }}
  function resetFilters() {{ state = {{area: '', kind: ''}}; setChip('area', ''); setChip('kind', ''); filterApartments(); }}
  document.querySelectorAll('.chip').forEach(function (c) {{
    c.addEventListener('click', function () {{
      if ('area' in c.dataset) {{ state.area = c.dataset.area; setChip('area', state.area); }}
      else {{ state.kind = c.dataset.kind; setChip('kind', state.kind); }}
      filterApartments();
    }});
  }});
  document.querySelectorAll('.apt-group').forEach(function (g) {{
    var row = g.querySelector('.apt-row');
    g.querySelector('.row-prev').onclick = function () {{ row.scrollBy({{left: -row.clientWidth * 0.9, behavior: 'smooth'}}); }};
    g.querySelector('.row-next').onclick = function () {{ row.scrollBy({{left: row.clientWidth * 0.9, behavior: 'smooth'}}); }};
  }});
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
    keep = {"Netflix", "DSTV", "Kampala"}
    lc = lambda f: " ".join(w if sum(c.isupper() for c in w) > 1 or w in keep else w.lower() for w in f.split())
    feat_text = ", ".join(lc(f) for f in feats[:-1]) + f" and {lc(feats[-1])}"
    para2 = (f"It comes with {feat_text}, and is priced at {ugx(a['price'])} per night. "
             f"It suits {t['suits']}, and works well for both short visits and longer stays.")
    para3 = area['intro'].split('. ')[0] + ". " + area['around']
    title = f"{a['name']} – {ugx(a['price'])}/Night"
    desc = (f"{t['label']} in {a['location']}, Kampala for {ugx(a['price'])} per night. "
            f"{', '.join(feats[:3])}. See {len(a['gallery'])} photos and book directly on WhatsApp.")
    msg = f"Hello, I'd like to book the {a['name']} ({ugx(a['price'])}/night): {url} Is it available? My dates are: "
    lat, lng = a.get('geo') or area['geo']
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
      {map_block(lat, lng, "Location", a.get('profile')) if a.get('geo') else ""}
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
  {reviews_block(limit=2, heading="What Guests Say", wrap=False) if a.get('geo') else ""}
  <section class="mt-4">
    <h2 class="h4 fw-bold mb-3">More furnished apartments {"in " + a['location'] if any(o['location']==a['location'] for o in others) else "you may like"}</h2>
    <div class="row">{other_cards}</div>
    <p><a href="/#apartments">See all {len(apts)} apartments</a></p>
  </section>
</main>
{VIEWER}
"""
    page += footer(counts, wa_msg=msg)
    page += "</body>\n</html>\n"
    return page

def build_area(name, area, apts, counts):
    here = sorted([a for a in apts if a['location'] == name], key=lambda a: not a.get('featured'))
    pinned = [a for a in here if a.get('geo')]
    url = f"{SITE}/{area['slug']}/"
    low = min(a['price'] for a in here)
    kinds = sorted({TYPES[a['title']]['short'].lower() for a in here}, key=lambda k: ["studio", "one-bedroom", "two-bedroom", "three-bedroom"].index(k))
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
  {map_block(*(BUSINESS_GEO if any(tuple(a['geo']) == BUSINESS_GEO for a in pinned) else pinned[0]['geo']), f"Our {name} location", None if any(tuple(a['geo']) == BUSINESS_GEO for a in pinned) else pinned[0].get('profile')) if pinned else ""}
  {reviews_block(limit=4, heading="What Our Guests Say", wrap=False) if pinned else ""}
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

def guide_cards():
    return "".join(f"""<div class="col-md-6"><a class="guide-card" href="/guides/{g['slug']}/"><i class="bi {g['icon']}"></i>
      <div><h3 class="h6 fw-bold mb-1">{esc(g['title'])}</h3><p>{esc(g['summary'])}</p></div></a></div>""" for g in GUIDES)

def fill_guide(text, apts, counts):
    def low(area):
        ps = [a['price'] for a in apts if a['location'] == area]
        return ugx(min(ps)) if ps else ""
    vals = {"ntinda_from": low("Ntinda"), "kisaasi_from": low("Kisaasi"),
            "ntinda_count": str(counts.get("Ntinda", 0)), "kisaasi_count": str(counts.get("Kisaasi", 0)),
            "whatsapp_link": esc(wa_link("Hello, I'm planning a stay in Kampala and have a question.")),
            "call": CALL_DISPLAY, "checkin": CHECKIN, "checkout": CHECKOUT,
            "weekly_off": str(WEEKLY_OFF), "monthly_off": str(MONTHLY_OFF), "pickup_price": ugx(PICKUP_PRICE)}
    for k, v in vals.items():
        text = text.replace("{" + k + "}", v)
    return text

def build_guide(g, apts, counts):
    url = f"{SITE}/guides/{g['slug']}/"
    body = fill_guide(g['body'], apts, counts)
    faqs = [(q, fill_guide(a, apts, counts)) for q, a in g['faqs']]
    if g.get('area'):
        picks = sorted([a for a in apts if a['location'] == g['area']], key=lambda a: not a.get('featured'))[:3]
    else:
        picks = [a for a in apts if a['location'] == "Ntinda" and a.get('featured')][:1] + [a for a in apts if a['location'] == "Kisaasi"][:2]
    image = full(picks[0]['image']) if picks else "/images/hero.webp"
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": g['title'], "description": g['description'], "url": url,
         "image": SITE + image, "datePublished": g['updated'], "dateModified": g['updated'],
         "author": {"@type": "Organization", "name": BRAND, "url": SITE + "/"},
         "publisher": {"@id": f"{SITE}/#business"}, "mainEntityOfPage": url},
        {**business_schema(apts)},
        breadcrumbs([("Home", SITE + "/"), ("Guides", f"{SITE}/guides/"), (g['title'], url)]),
        faq_schema(faqs),
    ]}
    side = "\n".join(card(a) .replace('col-sm-6 col-lg-4 col-xl-3 mb-4', 'mb-3') for a in picks)
    others = "".join(f'<li><a href="/guides/{o["slug"]}/">{esc(o["title"])}</a></li>' for o in GUIDES if o['slug'] != g['slug'])
    page = head(g['seo_title'], g['description'], url, image, schema)
    page += navbar()
    page += f"""<main class="container" style="padding-top:72px">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/guides/">Guides</a> › {esc(g['title'])}</nav>
  <div class="row g-4">
    <div class="col-lg-8">
      <article class="article">
        <h1 class="fw-bold h2 mb-1">{esc(g['title'])}</h1>
        <p class="small text-muted mb-3">Updated {datetime.date.fromisoformat(g['updated']).strftime('%-d %B %Y')} · {BRAND}</p>
        {body}
        <h2>Frequently asked questions</h2>
        <div class="faq">{faq_html(faqs)}</div>
      </article>
      {f'<div class="info-card mt-4"><h2 class="h5">More guides</h2><ul class="mb-0">{others}</ul></div>' if others else ''}
    </div>
    <aside class="col-lg-4">
      <div class="info-card">
        <h2 class="h5 fw-bold">Need a place to stay?</h2>
        <p class="mb-3">Fully furnished apartments from {ugx(min(a['price'] for a in apts))} per night. {WEEKLY_OFF}% off weekly, {MONTHLY_OFF}% off monthly.</p>
        <a href="{wa_link('Hello, I read your guide and would like to check availability.')}" target="_blank" rel="noopener" class="btn btn-success w-100 mb-2"><i class="bi bi-whatsapp"></i> Ask on WhatsApp</a>
        <a href="/#apartments" class="btn btn-outline-primary w-100">See all apartments</a>
      </div>
      {side}
    </aside>
  </div>
</main>
"""
    page += footer(counts)
    page += "</body>\n</html>\n"
    return page

def build_guides_index(apts, counts):
    url = f"{SITE}/guides/"
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Kampala travel guides", "url": url,
         "hasPart": [{"@type": "Article", "headline": g['title'], "url": f"{SITE}/guides/{g['slug']}/"} for g in GUIDES]},
        breadcrumbs([("Home", SITE + "/"), ("Guides", url)]),
    ]}
    page = head("Kampala Travel Guides | Furnished Apartments Uganda",
                "Practical guides for visitors to Kampala: getting from Entebbe Airport, choosing a neighbourhood and planning your stay.",
                url, "/images/hero.webp", schema)
    page += navbar()
    page += f"""<main class="container" style="padding-top:72px">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › Guides</nav>
  <h1 class="fw-bold h2">Kampala Travel Guides</h1>
  <p class="lead-muted mb-4">Practical tips from our local hosts to help you plan your stay in Kampala.</p>
  <div class="row g-3">{guide_cards()}</div>
</main>
"""
    page += footer(counts)
    page += "</body>\n</html>\n"
    return page

def build_sitemap(apts, counts):
    urls = [(SITE + "/", "1.0")]
    urls += [(f"{SITE}/{v['slug']}/", "0.9") for k, v in AREAS.items() if counts.get(k)]
    urls += [(SITE + apt_slug(a), "0.8") for a in apts]
    urls += [(f"{SITE}/guides/", "0.6")] + [(f"{SITE}/guides/{g['slug']}/", "0.7") for g in GUIDES]
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
    write("guides/index.html", build_guides_index(apts, counts))
    for g in GUIDES:
        write(f"guides/{g['slug']}/index.html", build_guide(g, apts, counts))
    write("sitemap.xml", build_sitemap(apts, counts))
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Built home page, {len(apts)} apartment pages, {sum(1 for k in AREAS if counts.get(k))} area pages, sitemap and robots.txt")

if __name__ == "__main__":
    main()
