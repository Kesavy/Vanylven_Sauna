import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shared

ROOT = sys.argv[1]

# Where the sauna is (from the Google Maps place "Vanylven Sauna")
LAT, LON = 62.0973003, 5.5577698
PLACE = 'https://maps.app.goo.gl/YxkPj1qFpbwp8hvf6'
DIRECTIONS = f'https://www.google.com/maps/dir/?api=1&destination={LAT},{LON}'
APPLE = f'https://maps.apple.com/?daddr={LAT},{LON}&q=Vanylven%20Sauna'
# OpenStreetMap: no cookies or tracking, unlike an embedded Google map
OSM = f'https://www.openstreetmap.org/export/embed.html?bbox={LON-.012:.5f},{LAT-.0045:.5f},{LON+.012:.5f},{LAT+.0045:.5f}&layer=mapnik&marker={LAT},{LON}'
REVIEW = 'https://g.page/r/CasW7u5nZ30fEBM/review'

T = r'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="dark">
{seo}
{icons}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:ital,wght@0,400..900;1,400..700&display=swap" rel="stylesheet">
<script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>
<style>
  /* Find us: map, address, how to reach us. Same tokens and shapes as the main site. */
  :root {{
    --night: #0b1012; --night-2: #121a1d; --ink: #eef2f1; --muted: #a7b4b4; --faint: #6b7a7b;
    --line: rgb(238 242 241 / .12); --heat: #ef6a32; --heat-soft: #ffb48f; --on-heat: #1a1310;
    --brand: #5a4d44; --radius: 16px; --max: 1180px; --ease: cubic-bezier(.16, 1, .3, 1);
  }}
  *, *::before, *::after {{ box-sizing: border-box; }}
  html {{ background: var(--night); }}
  body {{
    margin: 0; color: var(--ink); font-family: "Schibsted Grotesk", system-ui, sans-serif; font-size: 17px; line-height: 1.6;
    -webkit-font-smoothing: antialiased; overflow-x: clip;
    background: radial-gradient(60% 50% at 85% 0%, rgb(143 208 224 / .1), transparent 70%), var(--night);
    min-height: 100dvh; display: flex; flex-direction: column;
  }}
  img {{ display: block; max-width: 100%; height: auto; }}
  a {{ color: inherit; }}
  button {{ font: inherit; color: inherit; }}
  :focus-visible {{ outline: 3px solid var(--heat); outline-offset: 3px; }}
  .wrap {{ max-width: var(--max); margin: 0 auto; padding: 0 32px; }}
  h1, h2, h3 {{ margin: 0; font-weight: 800; letter-spacing: -0.035em; line-height: 1; }}
  p {{ margin: 0; }}
  .pebble {{ display: inline-grid; place-items: center; border-radius: 58% 42% 55% 45% / 47% 58% 42% 53%; }}
  .btn {{
    display: inline-flex; align-items: center; gap: 10px; padding: 16px 26px; border-radius: 999px; border: 0; cursor: pointer;
    font-weight: 700; font-size: 1rem; line-height: 1; text-decoration: none; white-space: nowrap; transition: transform .25s var(--ease), background-color .25s;
  }}
  .btn:active {{ transform: scale(.97); }}
  .btn-heat {{ background: var(--heat); color: var(--on-heat); }}
  .btn-heat:hover {{ background: #ff7a42; }}
  .btn-glass {{ background: rgb(255 255 255 / .08); box-shadow: inset 0 0 0 1px rgb(255 255 255 / .22); }}
  .btn-glass:hover {{ background: rgb(255 255 255 / .14); }}

  main {{ flex: 1; padding: 136px 0 120px; }}
  .layout {{ display: grid; grid-template-columns: 1fr 1.25fr; gap: 64px; align-items: start; }}
  .head h1 {{ font-size: clamp(2.6rem, 6vw, 4.6rem); max-width: 12ch; }}
  .head p {{ margin-top: 20px; color: var(--muted); font-size: 1.15rem; max-width: 40ch; }}
  .go {{ margin-top: 32px; display: flex; flex-wrap: wrap; gap: 12px; }}

  .info {{ margin-top: 56px; display: grid; gap: 36px; }}
  .info h2 {{ font-size: .9rem; font-weight: 600; letter-spacing: 0; color: var(--muted); margin-bottom: 10px; }}
  address {{ font-style: normal; font-size: 1.1rem; line-height: 1.55; }}
  address small {{ display: block; margin-top: 8px; color: var(--muted); font-size: .9rem; }}
  .contact {{ list-style: none; margin: 0; padding: 0; display: grid; border-radius: var(--radius); box-shadow: inset 0 0 0 1px var(--line); overflow: hidden; }}
  .contact li + li {{ border-top: 1px solid var(--line); }}
  .contact a {{ display: grid; grid-template-columns: 28px 1fr auto; gap: 14px; align-items: center; padding: 16px 20px; text-decoration: none; transition: background-color .2s; }}
  .contact a:hover {{ background: rgb(255 255 255 / .05); }}
  .contact i {{ font-size: 1.35rem; color: var(--heat-soft); }}
  .contact span small {{ display: block; color: var(--muted); font-size: .85rem; }}
  .contact .ph-arrow-up-right {{ font-size: 1rem; color: var(--faint); }}
  .note {{ color: var(--muted); font-size: .95rem; max-width: 46ch; }}
  .note a {{ color: var(--heat-soft); }}

  /* The map: OpenStreetMap, darkened to sit in the night palette */
  .map {{ position: sticky; top: 104px; border-radius: var(--radius); overflow: hidden; box-shadow: inset 0 0 0 1px var(--line), 0 40px 80px -40px rgb(0 0 0 / .8); background: var(--night-2); }}
  .map iframe {{ display: block; width: 100%; height: min(72vh, 640px); border: 0; filter: invert(.92) hue-rotate(180deg) saturate(.7) brightness(.95); }}
  .map figcaption {{ display: flex; justify-content: space-between; gap: 12px; padding: 12px 16px; font-size: .82rem; color: var(--faint); border-top: 1px solid var(--line); }}
  .map figcaption a {{ color: var(--muted); }}

  .review {{ margin-top: 80px; padding: 30px; border-radius: var(--radius); display: flex; flex-wrap: wrap; gap: 20px; align-items: center; justify-content: space-between;
    background: rgb(239 106 50 / .07); box-shadow: inset 0 0 0 1px rgb(239 106 50 / .25); }}
  .review h2 {{ font-size: 1.4rem; letter-spacing: -0.02em; }}
  .review p {{ margin-top: 6px; color: var(--muted); }}

  @media (max-width: 900px) {{
    .wrap {{ padding: 0 18px; }}
    main {{ padding-top: 96px; }}
    .layout {{ grid-template-columns: 1fr; gap: 40px; }}
    .map {{ position: static; }}
    .map iframe {{ height: 360px; }}
    .go .btn {{ flex: 1 1 auto; justify-content: center; }}
  }}
  @media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
{shell_css}</style>
</head>
<body>

{shell_header}

<main>
  <div class="wrap">
    <div class="layout">
      <div>
        <div class="head">
          <h1>{h1}</h1>
          <p>{lead}</p>
        </div>
        <div class="go">
          <a class="btn btn-heat" href="{directions}" target="_blank" rel="noopener"><i class="ph ph-navigation-arrow" aria-hidden="true"></i>{go_google}</a>
          <a class="btn btn-glass" href="{apple}" target="_blank" rel="noopener"><i class="ph ph-apple-logo" aria-hidden="true"></i>{go_apple}</a>
        </div>

        <div class="info">
          <section>
            <h2>{addr_h}</h2>
            <address>Vanylven Sauna<br>{addr_line}<br>6143 Fiskå, {country}<small>{coords} {lat:.5f}, {lon:.5f}</small></address>
          </section>
          <section>
            <h2>{contact_h}</h2>
            <ul class="contact">
              <li><a href="mailto:vanylvensauna@gmail.com"><i class="ph ph-envelope-simple" aria-hidden="true"></i><span>vanylvensauna@gmail.com<small>{email_note}</small></span><i class="ph ph-arrow-up-right" aria-hidden="true"></i></a></li>
              <li><a href="https://www.facebook.com/profile.php?id=61570144756846" target="_blank" rel="noopener"><i class="ph ph-messenger-logo" aria-hidden="true"></i><span>Messenger<small>{messenger_note}</small></span><i class="ph ph-arrow-up-right" aria-hidden="true"></i></a></li>
              <li><a href="https://www.instagram.com/vanylvensauna/" target="_blank" rel="noopener"><i class="ph ph-instagram-logo" aria-hidden="true"></i><span>Instagram<small>@vanylvensauna</small></span><i class="ph ph-arrow-up-right" aria-hidden="true"></i></a></li>
            </ul>
          </section>
          <p class="note">{note}</p>
        </div>
      </div>

      <figure class="map" style="margin:0">
        <iframe src="{osm}" title="{map_title}" loading="lazy" referrerpolicy="no-referrer"></iframe>
        <figcaption><span>© OpenStreetMap</span><a href="{place}" target="_blank" rel="noopener">{open_google}</a></figcaption>
      </figure>
    </div>

    <section class="review">
      <div>
        <h2>{review_h}</h2>
        <p>{review_p}</p>
      </div>
      <a class="btn btn-glass" href="{review}" target="_blank" rel="noopener"><i class="ph ph-star" aria-hidden="true"></i>{review_btn}</a>
    </section>
  </div>
</main>

{shell_footer}

<script>
{shell_js}</script>
</body>
</html>
'''

en = dict(
  lang='en', title='Find us | Vanylven Sauna',
  desc='Vanylven Sauna is on the shore below Fiskå Brygge Gjestgiveri in Fiskå, Vanylven. Map, directions and contact.',
  h1='Find us in Fiskå', lead='On the shore below Fiskå Brygge Gjestgiveri, right by the Vanylvsfjord.',
  go_google='Directions in Google Maps', go_apple='Apple Maps',
  addr_h='Address', addr_line='Below Fiskå Brygge Gjestgiveri', country='Norway', coords='GPS',
  contact_h='Get in touch', email_note='Questions, bookings outside opening hours, gift cards', messenger_note='Message us on Facebook',
  note='We have no phone, but we answer email and messages quickly. Booked a session? Your door code comes the day before. <a href="https://calendly.com/vanylvensauna/sauna" target="_blank" rel="noopener">Book a session</a>',
  map_title='Map showing Vanylven Sauna in Fiskå', open_google='Open in Google Maps',
  review_h='Been with us?', review_p='A few words on Google help other people find the sauna.', review_btn='Leave a review on Google',
)
nn = dict(
  lang='nn', title='Finn oss | Vanylven Sauna',
  desc='Vanylven Sauna ligg i sjøkanten nedanfor Fiskå Brygge Gjestgiveri på Fiskå i Vanylven. Kart, vegbeskriving og kontakt.',
  h1='Finn oss på Fiskå', lead='I sjøkanten nedanfor Fiskå Brygge Gjestgiveri, rett ved Vanylvsfjorden.',
  go_google='Vegbeskriving i Google Maps', go_apple='Apple Kart',
  addr_h='Adresse', addr_line='Nedanfor Fiskå Brygge Gjestgiveri', country='Noreg', coords='GPS',
  contact_h='Ta kontakt', email_note='Spørsmål, booking utanom opningstidene, gåvekort', messenger_note='Send oss ei melding på Facebook',
  note='Vi har ikkje telefon, men vi svarar raskt på e-post og meldingar. Har du booka? Koden til døra kjem dagen før. <a href="https://calendly.com/vanylvensauna/sauna" target="_blank" rel="noopener">Book ei økt</a>',
  map_title='Kart som viser Vanylven Sauna på Fiskå', open_google='Opne i Google Maps',
  review_h='Har du vore hos oss?', review_p='Nokre ord på Google hjelper andre å finne badstua.', review_btn='Skriv ei omtale på Google',
)

for d, path, img, alt_href in [
    (en, 'find/index.html', '../img/', '../nn/find/'),
    (nn, 'nn/find/index.html', '../../img/', '../../find/'),
]:
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='') as f:
        sh, sf = shared.parts(d['lang'], '../', img, alt_href, here='find')
        f.write(T.format(shell_header=sh, shell_footer=sf, shell_css=shared.CSS, shell_js=shared.JS,
                         seo=shared.seo('find/', d['lang'], d['title'], d['desc'], 'img/harbour-reflection.jpg'), icons=shared.icons(img),
                         directions=DIRECTIONS, apple=APPLE, osm=OSM, place=PLACE, review=REVIEW, lat=LAT, lon=LON, **d))
    print('wrote', path)
