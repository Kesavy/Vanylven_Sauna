import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shared

ROOT = sys.argv[1]

# Where the sauna is (from the Google Maps place "Vanylven Sauna")
LAT, LON = 62.0973003, 5.5577698
PLACE = 'https://maps.app.goo.gl/YxkPj1qFpbwp8hvf6'
DIRECTIONS = f'https://www.google.com/maps/dir/?api=1&destination={LAT},{LON}'
APPLE = f'https://maps.apple.com/?daddr={LAT},{LON}&q=Vanylven%20Sauna'
# Embedded Google map, zoomed in on Fiskå harbour (no API key needed)
GMAP = f'https://maps.google.com/maps?q=Vanylven%20Sauna&ll={LAT+.0009:.7f},{LON}&z=16&hl={{hl}}&output=embed'
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

  main {{ flex: 1; padding: 128px 0 120px; }}
  .eyebrow {{ display: inline-flex; gap: 8px; align-items: center; font-size: .9rem; font-weight: 600; color: var(--cold, #8fd0e0); }}
  .sec-h {{ font-size: clamp(1.8rem, 3.4vw, 2.6rem); letter-spacing: -0.035em; }}
  .sec-lead {{ margin-top: 12px; color: var(--muted); font-size: 1.05rem; max-width: 52ch; }}

  /* 1. Where: the answer first, map beside it */
  .where {{ display: grid; grid-template-columns: 5fr 7fr; gap: 56px; align-items: stretch; }}
  .where .text {{ display: flex; flex-direction: column; padding: 8px 0; }}
  .where h1 {{ margin-top: 14px; font-size: clamp(2.8rem, 6vw, 4.8rem); max-width: 10ch; }}
  .where .lead {{ margin-top: 20px; color: var(--muted); font-size: 1.15rem; max-width: 34ch; }}
  .go {{ margin-top: 32px; display: flex; flex-wrap: wrap; gap: 12px; }}
  address {{ margin-top: auto; padding-top: 40px; font-style: normal; display: grid; gap: 4px; }}
  address .label {{ font-size: .85rem; color: var(--faint); font-weight: 600; margin-bottom: 4px; }}
  address .gps {{ margin-top: 6px; color: var(--muted); font-size: .9rem; }}

  /* The map: embedded Google Maps */
  .map {{ margin: 0; border-radius: var(--radius); overflow: hidden; display: flex; flex-direction: column; background: var(--night-2);
    box-shadow: inset 0 0 0 1px var(--line), 0 40px 80px -40px rgb(0 0 0 / .8); }}
  .map iframe {{ display: block; width: 100%; flex: 1; min-height: 540px; border: 0; }}
  .map figcaption {{ display: flex; justify-content: space-between; gap: 12px; padding: 12px 16px; font-size: .82rem; color: var(--faint); border-top: 1px solid var(--line); }}
  .map figcaption a {{ color: var(--muted); }}

  /* 2. Getting here: three steps in order */
  .arrive {{ margin-top: 120px; padding-top: 56px; border-top: 1px solid var(--line); }}
  .steps {{ list-style: none; margin: 40px 0 0; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
  .steps li {{ padding: 28px; border-radius: var(--radius); background: var(--night-2); box-shadow: inset 0 0 0 1px var(--line); display: grid; gap: 12px; align-content: start; }}
  .steps .pebble {{ width: 44px; height: 40px; background: var(--ink); color: var(--night); font-weight: 800; }}
  .steps h3 {{ font-size: 1.2rem; letter-spacing: -0.02em; line-height: 1.2; margin-top: 6px; }}
  .steps p {{ color: var(--muted); font-size: .98rem; }}

  /* 3. Contact: one card per channel */
  .contact {{ margin-top: 120px; padding-top: 56px; border-top: 1px solid var(--line); }}
  .channels {{ list-style: none; margin: 40px 0 0; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }}
  .channels a {{ height: 100%; display: grid; grid-template-columns: auto 1fr auto; gap: 16px; align-items: start; padding: 24px; border-radius: var(--radius); text-decoration: none;
    box-shadow: inset 0 0 0 1px var(--line); transition: background-color .2s, box-shadow .2s; }}
  .channels a:hover {{ background: rgb(255 255 255 / .04); box-shadow: inset 0 0 0 1px rgb(255 255 255 / .25); }}
  .channels .ico {{ font-size: 1.6rem; color: var(--heat-soft); line-height: 1; }}
  .channels strong {{ display: block; font-size: 1.05rem; overflow-wrap: anywhere; }}
  .channels small {{ display: block; margin-top: 4px; color: var(--muted); font-size: .9rem; line-height: 1.45; }}
  .channels .ph-arrow-up-right {{ color: var(--faint); }}

  /* 4. Review */
  .review {{ margin-top: 96px; padding: 32px; border-radius: var(--radius); display: flex; flex-wrap: wrap; gap: 20px; align-items: center; justify-content: space-between;
    background: rgb(239 106 50 / .07); box-shadow: inset 0 0 0 1px rgb(239 106 50 / .25); }}
  .review h2 {{ font-size: 1.4rem; letter-spacing: -0.02em; }}
  .review p {{ margin-top: 6px; color: var(--muted); }}

  @media (max-width: 960px) {{
    .wrap {{ padding: 0 18px; }}
    main {{ padding-top: 96px; }}
    .where {{ grid-template-columns: 1fr; gap: 32px; }}
    .map iframe {{ min-height: 340px; }}
    .go .btn {{ flex: 1 1 auto; justify-content: center; }}
    .steps, .channels {{ grid-template-columns: 1fr; }}
    .arrive, .contact {{ margin-top: 80px; padding-top: 44px; }}
  }}
  @media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
{shell_css}</style>
</head>
<body>

{shell_header}

<main>
  <div class="wrap">
    <section class="where" aria-labelledby="where-h">
      <div class="text">
        <span class="eyebrow"><i class="ph ph-map-pin" aria-hidden="true"></i>{eyebrow}</span>
        <h1 id="where-h">{h1}</h1>
        <p class="lead">{lead}</p>
        <div class="go">
          <a class="btn btn-heat" href="{directions}" target="_blank" rel="noopener"><i class="ph ph-navigation-arrow" aria-hidden="true"></i>{go_google}</a>
          <a class="btn btn-glass" href="{apple}" target="_blank" rel="noopener"><i class="ph ph-apple-logo" aria-hidden="true"></i>{go_apple}</a>
        </div>
        <address>
          <span class="label">{addr_h}</span>
          <span>Vanylven Sauna</span>
          <span>{addr_line}</span>
          <span>6143 Fiskå, {country}</span>
          <span class="gps">{coords} {lat:.5f}, {lon:.5f}</span>
        </address>
      </div>
      <figure class="map">
        <iframe src="{gmap}" title="{map_title}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        <figcaption><span>Google Maps</span><a href="{place}" target="_blank" rel="noopener">{open_google}</a></figcaption>
      </figure>
    </section>

    <section class="arrive" aria-labelledby="arrive-h">
      <h2 class="sec-h" id="arrive-h">{arrive_h}</h2>
      <ol class="steps">
        <li><span class="pebble" aria-hidden="true">1</span><h3>{s1_h}</h3><p>{s1_p}</p></li>
        <li><span class="pebble p2" aria-hidden="true">2</span><h3>{s2_h}</h3><p>{s2_p}</p></li>
        <li><span class="pebble p3" aria-hidden="true">3</span><h3>{s3_h}</h3><p>{s3_p}</p></li>
      </ol>
    </section>

    <section class="contact" aria-labelledby="contact-h">
      <h2 class="sec-h" id="contact-h">{contact_h}</h2>
      <p class="sec-lead">{contact_lead}</p>
      <ul class="channels">
        <li><a href="mailto:vanylvensauna@gmail.com"><i class="ph ph-envelope-simple ico" aria-hidden="true"></i><span><strong>{email_h}</strong><small>vanylvensauna@gmail.com<br>{email_note}</small></span><i class="ph ph-arrow-up-right" aria-hidden="true"></i></a></li>
        <li><a href="https://www.facebook.com/profile.php?id=61570144756846" target="_blank" rel="noopener"><i class="ph ph-messenger-logo ico" aria-hidden="true"></i><span><strong>Messenger</strong><small>{messenger_note}</small></span><i class="ph ph-arrow-up-right" aria-hidden="true"></i></a></li>
        <li><a href="https://www.instagram.com/vanylvensauna/" target="_blank" rel="noopener"><i class="ph ph-instagram-logo ico" aria-hidden="true"></i><span><strong>Instagram</strong><small>@vanylvensauna<br>{insta_note}</small></span><i class="ph ph-arrow-up-right" aria-hidden="true"></i></a></li>
      </ul>
    </section>

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
  eyebrow='Fiskå, Vanylven', h1='Find us in Fiskå', lead='On the shore below Fiskå Brygge Gjestgiveri, right by the Vanylvsfjord.',
  go_google='Directions in Google Maps', go_apple='Apple Maps',
  addr_h='Address', addr_line='Below Fiskå Brygge Gjestgiveri', country='Norway', coords='GPS',
  arrive_h='Getting here',
  s1_h='Head for Fiskå Brygge Gjestgiveri', s1_p='The sauna is in the centre of Fiskå, by the harbour. The directions buttons above take you there.',
  s2_h='Walk down to the shore', s2_p='The sauna sits on the rocks right below the guesthouse, at the water’s edge.',
  s3_h='Enter your door code', s3_p='For private sessions, the code comes by email the day before. Open sauna on Wednesdays needs no booking.',
  contact_h='Questions?', contact_lead='We have no phone, but we answer emails and messages quickly.',
  email_h='Email', email_note='Questions, sessions outside opening hours, gift cards', messenger_note='Message us on our Facebook page', insta_note='Photos and news from the shore',
  map_title='Map showing Vanylven Sauna in Fiskå', open_google='Open in Google Maps',
  review_h='Been with us?', review_p='A few words on Google help other people find the sauna.', review_btn='Leave a review on Google',
)
nn = dict(
  lang='nn', title='Finn oss | Vanylven Sauna',
  desc='Vanylven Sauna ligg i sjøkanten nedanfor Fiskå Brygge Gjestgiveri på Fiskå i Vanylven. Kart, vegbeskriving og kontakt.',
  eyebrow='Fiskå, Vanylven', h1='Finn oss på Fiskå', lead='I sjøkanten nedanfor Fiskå Brygge Gjestgiveri, rett ved Vanylvsfjorden.',
  go_google='Vegbeskriving i Google Maps', go_apple='Apple Kart',
  addr_h='Adresse', addr_line='Nedanfor Fiskå Brygge Gjestgiveri', country='Noreg', coords='GPS',
  arrive_h='Slik finn du fram',
  s1_h='Køyr eller gå til Fiskå Brygge Gjestgiveri', s1_p='Badstua ligg midt på Fiskå, ved hamna. Knappane for vegbeskriving over tek deg dit.',
  s2_h='Gå ned til sjøkanten', s2_p='Badstua står på svaberget rett nedanfor gjestgiveriet, heilt nede ved vatnet.',
  s3_h='Tast inn koden', s3_p='For privat badstue kjem koden på e-post dagen før. Open badstue på onsdagar treng ikkje booking.',
  contact_h='Spørsmål?', contact_lead='Vi har ikkje telefon, men vi svarar raskt på e-post og meldingar.',
  email_h='E-post', email_note='Spørsmål, økter utanom opningstidene, gåvekort', messenger_note='Send oss ei melding på Facebook-sida vår', insta_note='Bilete og nytt frå sjøkanten',
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
                         directions=DIRECTIONS, apple=APPLE, gmap=GMAP.replace('{hl}', 'no' if d['lang'] == 'nn' else 'en'), place=PLACE, review=REVIEW, lat=LAT, lon=LON, **d))
    print('wrote', path)
