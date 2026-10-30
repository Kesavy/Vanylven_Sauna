# One header, menu and footer for every page. The home page is the source of truth;
# subpages get the same markup with paths adjusted, and the header starts in its "solid" state.

CALENDLY = 'https://calendly.com/vanylvensauna/sauna'

# Public address of the site. Change this one line when the site moves to its own domain,
# then rerun all generators and update sitemap.xml and robots.txt.
SITE = 'https://www.vanylvensauna.no/'

TEXT = {
  'en': dict(book='Book a session', open='Open menu', close='Close menu', menu='Menu', main='Main', contact='Contact and social',
             email='Email', lang_name='Norsk', lang_code='nn', credit='Vanylven Sauna is built by Stad Kystbygg and run by volunteers from Vanylven.', design='Website design and coding by',
             links=[('ritual', 'The ritual', '#ritual'), ('plan', 'Prices and booking', '#plan'), ('pay', 'How to pay', 'pay/'),
                    ('gift', 'Gift cards', 'gift/'), ('rules', 'Before you come', '#rules'), ('find', 'Find us', '#find')]),
  'nn': dict(book='Book ei økt', open='Opne meny', close='Lukk meny', menu='Meny', main='Hovudmeny', contact='Kontakt og sosiale medium',
             email='E-post', lang_name='English', lang_code='en', credit='Vanylven Sauna er bygd av Stad Kystbygg og drifta av frivillige frå Vanylven.', design='Design og koding av nettsida:',
             links=[('ritual', 'Ritualet', '#ritual'), ('plan', 'Prisar og booking', '#plan'), ('pay', 'Slik betaler du', 'pay/'),
                    ('gift', 'Gåvekort', 'gift/'), ('rules', 'Før du kjem', '#rules'), ('find', 'Finn oss', '#find')]),
}


def seo(page, lang, title, desc, image):
    """Canonical, language alternates and share tags for one page.
    page: path below the language root ('' for home, 'gift/', 'pay/'). image: path below the site root."""
    en, nn = SITE + page, SITE + 'nn/' + page
    url = en if lang == 'en' else nn
    locale = 'en_GB' if lang == 'en' else 'nn_NO'
    return f'''<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{en}">
<link rel="alternate" hreflang="nn" href="{nn}">
<link rel="alternate" hreflang="x-default" href="{en}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Vanylven Sauna">
<meta property="og:locale" content="{locale}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}{image}">
<meta name="twitter:card" content="summary_large_image">'''


def place(lang, desc):
    """Structured data for the home pages: what the sauna is, where, when, and what it costs.
    Search engines and AI answers read this instead of guessing from the page design."""
    import json
    url = SITE if lang == 'en' else SITE + 'nn/'
    data = {
        '@context': 'https://schema.org',
        '@type': ['LocalBusiness', 'SportsActivityLocation'],
        '@id': SITE + '#sauna',
        'name': 'Vanylven Sauna',
        'url': url,
        'description': desc,
        'inLanguage': 'en' if lang == 'en' else 'nn',
        'image': [SITE + 'img/deck-fjord.jpg', SITE + 'img/interior-bench.jpg', SITE + 'img/exterior-dock.jpg'],
        'logo': SITE + 'img/logo-mark.png',
        'email': 'vanylvensauna@gmail.com',
        'address': {'@type': 'PostalAddress', 'addressLocality': 'Fiskå', 'postalCode': '6143',
                    'addressRegion': 'Møre og Romsdal', 'addressCountry': 'NO'},
        'hasMap': 'https://maps.app.goo.gl/YxkPj1qFpbwp8hvf6',
        'currenciesAccepted': 'NOK',
        'paymentAccepted': 'Vipps, bank transfer',
        'priceRange': 'NOK 100-600',
        'openingHoursSpecification': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '10:00', 'closes': '20:00'},
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Wednesday', 'opens': '17:00', 'closes': '20:00'},
        ],
        'makesOffer': [
            {'@type': 'Offer', 'name': 'Private sauna, 2 hours, up to 8 people' if lang == 'en' else 'Privat badstue, 2 timar, opptil 8 personar',
             'price': '600', 'priceCurrency': 'NOK', 'url': CALENDLY},
            {'@type': 'Offer', 'name': 'Open sauna, Wednesday 17:00 to 20:00, per person' if lang == 'en' else 'Open badstue, onsdag 17:00 til 20:00, per person',
             'price': '100', 'priceCurrency': 'NOK'},
        ],
        'sameAs': ['https://www.instagram.com/vanylvensauna/', 'https://www.facebook.com/profile.php?id=61570144756846'],
    }
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n</script>'


def parts(lang, home, img, lang_href, here=None):
    """home: path to this language's home ('' on the home page itself, '../' on a subpage).
    lang_href: link to the same page in the other language. here: id of the current page, marked aria-current."""
    t = TEXT[lang]
    brand_href = '#top' if home == '' else home
    def href(target):
        return target if home == '' else home + target
    cur = ' aria-current="page"'
    links = ''.join(
        f'      <a href="{href(u)}" style="--i:{i}" data-close{cur if k == here else ""}>{label}</a>\n'
        for i, (k, label, u) in enumerate(t['links']))
    lc = t['lang_code']
    header = f'''<header class="nav{"" if home == "" else " solid"}" id="nav">
  <div class="wrap">
    <a class="brand" href="{brand_href}"><img src="{img}logo-symbol.svg" alt="" width="35" height="44">Vanylven Sauna</a>
    <span class="spacer"></span>
    <a class="btn btn-heat book" href="{CALENDLY}" target="_blank" rel="noopener">{t['book']}</a>
    <button class="menu-btn pebble" type="button" aria-label="{t['open']}" aria-controls="fog" aria-expanded="false"><i class="ph ph-list" aria-hidden="true"></i></button>
  </div>
</header>

<div class="fog" id="fog" role="dialog" aria-modal="true" aria-label="{t['menu']}">
  <div class="wrap" style="display:flex;flex-direction:column;height:100%">
    <div class="top">
      <a class="brand" href="{brand_href}" data-close><img src="{img}logo-symbol.svg" alt="" width="35" height="44">Vanylven Sauna</a>
      <button class="menu-btn pebble p3" type="button" aria-label="{t['close']}" data-close><i class="ph ph-x" aria-hidden="true"></i></button>
    </div>
    <nav aria-label="{t['main']}">
{links}    </nav>
    <div class="foot">
      <a class="btn btn-heat book" href="{CALENDLY}" target="_blank" rel="noopener">{t['book']} <i class="ph ph-arrow-up-right" aria-hidden="true"></i></a>
      <a href="mailto:vanylvensauna@gmail.com">vanylvensauna@gmail.com</a>
      <a class="social" href="https://www.instagram.com/vanylvensauna/" target="_blank" rel="noopener" aria-label="Instagram"><i class="ph ph-instagram-logo" aria-hidden="true"></i></a>
      <a class="social" href="https://www.facebook.com/profile.php?id=61570144756846" target="_blank" rel="noopener" aria-label="Facebook"><i class="ph ph-facebook-logo" aria-hidden="true"></i></a>
      <a href="{lang_href}" hreflang="{lc}" lang="{lc}">{t['lang_name']}</a>
    </div>
  </div>
</div>'''
    footer = f'''<footer>
  <div class="wrap row">
    <a class="logo" href="{brand_href}"><img src="{img}logo-full.svg" alt="Vanylven Sauna" width="122" height="80"></a>
    <nav aria-label="{t['contact']}">
      <a href="mailto:vanylvensauna@gmail.com"><i class="ph ph-envelope-simple" aria-hidden="true"></i>{t['email']}</a>
      <a href="https://www.instagram.com/vanylvensauna/" target="_blank" rel="noopener"><i class="ph ph-instagram-logo" aria-hidden="true"></i>Instagram</a>
      <a href="https://www.facebook.com/profile.php?id=61570144756846" target="_blank" rel="noopener"><i class="ph ph-facebook-logo" aria-hidden="true"></i>Facebook</a>
      <a href="{lang_href}" hreflang="{lc}" lang="{lc}">{t['lang_name']}</a>
    </nav>
  </div>
  <p class="wrap credit"><span>{t['credit']}</span><span>{t['design']} <a href="https://lossless.cz" target="_blank" rel="noopener">Lossless</a>.</span></p>
</footer>'''
    return header, footer


# Same rules as the home page; the shell always uses the home page's 1280px width and 32/18px gutters.
CSS = '''
  /* ---- Shared shell: header, menu, footer (identical on every page) ---- */
  .nav .wrap, .fog .wrap, footer .wrap { max-width: 1280px; margin: 0 auto; padding: 0 32px; }
  .nav { position: fixed; inset: 0 0 auto; z-index: 60; transition: background-color .4s, backdrop-filter .4s; }
  .nav.solid { background: rgb(11 16 18 / .55); backdrop-filter: blur(18px) saturate(1.2); -webkit-backdrop-filter: blur(18px) saturate(1.2); }
  .nav .wrap { height: 72px; display: flex; align-items: center; gap: 16px; }
  .brand { display: flex; align-items: center; gap: 12px; text-decoration: none; font-weight: 700; letter-spacing: -0.01em; }
  .brand img { width: auto; height: 44px; }
  .nav .spacer { flex: 1; }
  .nav .btn { padding: 12px 20px; font-size: .95rem; }
  .menu-btn { width: 48px; height: 46px; border: 0; cursor: pointer; background: rgb(255 255 255 / .1); font-size: 1.35rem; display: inline-grid; place-items: center; }
  .menu-btn:hover { background: rgb(255 255 255 / .18); }
  body.locked { overflow: hidden; }
  .fog {
    position: fixed; inset: 0; z-index: 80; display: flex; flex-direction: column; padding: 0 0 40px;
    background: rgb(11 16 18 / .55); backdrop-filter: blur(28px) saturate(1.2); -webkit-backdrop-filter: blur(28px) saturate(1.2);
    opacity: 0; visibility: hidden; transition: opacity .5s var(--ease), visibility 0s .5s;
  }
  .fog.open { opacity: 1; visibility: visible; transition: opacity .5s var(--ease); }
  .fog > .wrap { width: 100%; }
  .fog .top { height: 72px; display: flex; align-items: center; justify-content: space-between; }
  .fog nav { display: grid; gap: 2px; margin-top: 6vh; }
  .fog nav a {
    font-size: clamp(2.2rem, 6vw, 4.2rem); font-weight: 800; letter-spacing: -0.04em; text-decoration: none; line-height: 1.15;
    opacity: 0; filter: blur(12px); transform: translateY(14px);
    transition: opacity .7s, filter .7s, transform .7s var(--ease), color .2s; transition-delay: calc(var(--i) * 60ms + 100ms);
  }
  .fog nav a:hover, .fog nav a[aria-current] { color: var(--heat-soft); }
  .fog.open nav a { opacity: 1; filter: blur(0); transform: none; }
  .fog .foot { margin-top: auto; padding-top: 36px; display: flex; flex-wrap: wrap; gap: 16px 28px; align-items: center; color: var(--muted); }
  .fog .foot .social { font-size: 1.5rem; line-height: 1; margin-right: -14px; text-decoration: none; transition: color .2s; }
  .fog .foot .social:hover { color: var(--heat-soft); }
  footer { background: var(--brand); color: #f3eee9; padding: 40px 0; }
  footer .credit { margin-top: 24px; font-size: .85rem; color: rgb(243 238 233 / .6); display: flex; flex-wrap: wrap; gap: 8px 24px; justify-content: space-between; }
  footer .credit a { display: inline; text-decoration: underline; text-underline-offset: 3px; }
  footer .row { display: flex; flex-wrap: wrap; gap: 28px; justify-content: space-between; align-items: center; }
  footer nav { display: flex; flex-wrap: wrap; gap: 24px; }
  footer a { text-decoration: none; display: inline-flex; align-items: center; gap: 8px; opacity: .9; }
  footer .logo { opacity: 1; }
  footer .logo img { width: auto; height: 80px; }
  footer a:hover { opacity: 1; text-decoration: underline; text-underline-offset: 4px; }
  @media (max-width: 767px) {
    .nav .wrap, .fog .wrap, footer .wrap { padding: 0 18px; }
    .nav .wrap { height: 64px; }
    .nav .btn { display: none; }
  }
'''

JS = '''
  // Shared shell: fogged menu
  (() => {
    const nav = document.getElementById('nav'), fog = document.getElementById('fog'), openBtn = nav.querySelector('.menu-btn');
    const setMenu = (open) => {
      fog.classList.toggle('open', open); document.body.classList.toggle('locked', open);
      openBtn.setAttribute('aria-expanded', open);
      (open ? fog.querySelector('nav a') : openBtn).focus({ preventScroll: true });
    };
    openBtn.addEventListener('click', () => setMenu(true));
    fog.querySelectorAll('[data-close]').forEach((el) => el.addEventListener('click', () => setMenu(false)));
    addEventListener('keydown', (e) => { if (e.key === 'Escape' && fog.classList.contains('open')) setMenu(false); });
  })();
'''
