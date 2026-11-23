# Files for search engines and AI assistants: sitemap.xml, llms.txt, and the 404 page.
# Run after the page builders. python tools/build_extras.py .
import datetime, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shared, faq

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
SITE = shared.SITE
TODAY = datetime.date.today().isoformat()

# Indexable pages, each in English and Nynorsk. The pay page is noindex and stays out.
PAGES = ['', 'gift/', 'find/', 'privacy/']


def sitemap():
    def alts(page):
        en, nn = SITE + 'en/' + page, SITE + page
        return ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{h}" href="{u}"/>'
                       for h, u in [('en', en), ('nn', nn), ('nb', nn), ('no', nn), ('x-default', en)])
    urls = ''.join(f'''
  <url>
    <loc>{SITE}{prefix}{page}</loc>
    <lastmod>{TODAY}</lastmod>{alts(page)}
  </url>''' for page in PAGES for prefix in ['', 'en/'])
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}
</urlset>
'''


def llms():
    """A plain summary for AI assistants (llmstxt.org): what the sauna is and where the facts live."""
    qa = '\n'.join(f'- **{q}** {faq.plain(a.replace("{root}", SITE + "en/"))}' for q, a in faq.FAQ['en']['items'])
    return f'''# Vanylven Sauna

> A small public sauna on the shore of the Vanylvsfjord in Fiskå, Vanylven municipality (Møre og Romsdal, Norway), below Fiskå Brygge Gjestgiveri. Built by Stad Kystbygg and run by local volunteers. Private sessions for up to 8 people, and an open sauna on Wednesday evenings. Sea swimming straight from the shore.

Key facts:

- Location: 6143 Fiskå, Vanylven, Norway. GPS 62.09730, 5.55777.
- Private session: NOK 600 for 2 hours for the whole group (up to 8 people). Thursday to Sunday, 10:00 to 20:00, last start 18:00. Book online.
- Open sauna: NOK 100 per person, every Wednesday 17:00 to 20:00. No booking, pay on arrival.
- Payment: Vipps (943550) or bank transfer.
- Contact: vanylvensauna@gmail.com, or Messenger on the Facebook page. No phone.
- Languages: English and Nynorsk.

## Pages

- [Heim (nynorsk)]({SITE}): the main version of the site, in Nynorsk
- [Home (English)]({SITE}en/): the sauna, a visit step by step, prices, booking, rules, questions and answers
- [Gift cards]({SITE}en/gift/): gift cards for 2, 4 or 6 hours, valid one year, ordered online
- [Find us]({SITE}en/find/): address, directions, contact
- [How to pay]({SITE}en/pay/): Vipps and bank transfer details
- [Privacy]({SITE}en/privacy/): how personal data is handled

## Questions and answers

{qa}

## Optional

- [Booking calendar]({faq.CALENDLY})
- [Instagram](https://www.instagram.com/vanylvensauna/)
- [Google Maps]( https://maps.app.goo.gl/YxkPj1qFpbwp8hvf6)
'''.replace('( https', '(https')


def notfound():
    """Shown for any unknown address. Absolute paths, since it can be served at any depth."""
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | Vanylven Sauna</title>
<meta name="robots" content="noindex">
{shared.assets('/')}
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<style>
  :root {{ --night: #0b1012; --ink: #eef2f1; --muted: #a7b4b4; --heat: #ef6a32; --on-heat: #1a1310; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; min-height: 100dvh; display: grid; place-items: center; padding: 32px; background: var(--night); color: var(--ink);
    font-family: "Schibsted Grotesk", system-ui, sans-serif; text-align: center; }}
  img {{ height: 80px; width: auto; }}
  h1 {{ font-size: clamp(2.2rem, 6vw, 3.6rem); margin: 28px 0 12px; letter-spacing: -0.02em; }}
  p {{ color: var(--muted); margin: 0 0 8px; }}
  nav {{ margin-top: 28px; display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }}
  a {{ display: inline-flex; align-items: center; gap: 8px; padding: 13px 22px; border-radius: 999px; text-decoration: none; font-weight: 700;
    background: rgb(255 255 255 / .1); color: var(--ink); }}
  a.main {{ background: var(--heat); color: var(--on-heat); }}
  a:focus-visible {{ outline: 3px solid var(--heat); outline-offset: 3px; }}
</style>
</head>
<body>
<main>
  <img src="/img/logo-full.svg" alt="Vanylven Sauna" width="122" height="80">
  <h1>This page is not here</h1>
  <p>The address may have changed. The sauna has not.</p>
  <p lang="nn">Denne sida finst ikkje. Badstua er der framleis.</p>
  <nav>
    <a class="main" href="/" lang="nn"><i class="ph ph-house" aria-hidden="true"></i>Heim</a>
    <a href="/en/">Home</a>
    <a href="/find/" lang="nn"><i class="ph ph-map-pin" aria-hidden="true"></i>Finn oss</a>
  </nav>
</main>
</body>
</html>
'''


for name, text in [('sitemap.xml', sitemap()), ('llms.txt', llms()), ('404.html', notfound())]:
    with open(os.path.join(ROOT, name), 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    print('wrote', name)
