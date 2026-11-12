import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shared

ROOT = sys.argv[1]

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
  /* Privacy: plain reading page in the site's tokens */
  :root {{
    --night: #0b1012; --night-2: #121a1d; --ink: #eef2f1; --muted: #a7b4b4; --faint: #7d8c8d;
    --line: rgb(238 242 241 / .12); --heat: #ef6a32; --heat-soft: #ffb48f; --on-heat: #1a1310;
    --brand: #5a4d44; --radius: 16px; --max: 1080px; --ease: cubic-bezier(.16, 1, .3, 1);
  }}
  *, *::before, *::after {{ box-sizing: border-box; }}
  html {{ background: var(--night); }}
  body {{
    margin: 0; color: var(--ink); font-family: "Schibsted Grotesk", system-ui, sans-serif; font-size: 17px; line-height: 1.65;
    -webkit-font-smoothing: antialiased; overflow-x: clip; background: var(--night);
    min-height: 100dvh; display: flex; flex-direction: column;
  }}
  a {{ color: var(--heat-soft); }}
  button {{ font: inherit; color: inherit; }}
  :focus-visible {{ outline: 3px solid var(--heat); outline-offset: 3px; }}
  .wrap {{ max-width: var(--max); margin: 0 auto; padding: 0 32px; }}
  h1, h2 {{ margin: 0; font-weight: 800; letter-spacing: -0.035em; line-height: 1.05; }}
  p, ul {{ margin: 0; }}
  .pebble {{ display: inline-grid; place-items: center; border-radius: 58% 42% 55% 45% / 47% 58% 42% 53%; }}
  .btn {{ display: inline-flex; align-items: center; gap: 10px; padding: 16px 26px; border-radius: 999px; border: 0; font-weight: 700; line-height: 1; text-decoration: none; white-space: nowrap; }}
  .btn-heat {{ background: var(--heat); color: var(--on-heat); }}

  main {{ flex: 1; padding: 136px 0 120px; }}
  .doc {{ max-width: 68ch; }}
  .doc h1 {{ font-size: clamp(2.4rem, 5.5vw, 4rem); }}
  .doc .lead {{ margin-top: 20px; color: var(--muted); font-size: 1.12rem; }}
  .doc .updated {{ margin-top: 10px; color: var(--faint); font-size: .9rem; }}
  .doc section {{ margin-top: 44px; display: grid; gap: 12px; }}
  .doc h2 {{ font-size: 1.35rem; letter-spacing: -0.02em; }}
  .doc p, .doc li {{ color: #d3dcdb; }}
  .doc ul {{ padding-left: 1.2em; display: grid; gap: 6px; }}
  .doc strong {{ color: var(--ink); }}

  @media (max-width: 860px) {{
    .wrap {{ padding: 0 18px; }}
    main {{ padding-top: 96px; }}
  }}
{shell_css}</style>
</head>
<body>

{shell_header}

<main id="main">
  <div class="wrap">
    <article class="doc">
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
      <p class="updated">{updated}</p>
{sections}
    </article>
  </div>
</main>

{shell_footer}

<script>
{shell_js}</script>
</body>
</html>
'''

def sections(items):
    out = []
    for h, body in items:
        out.append(f'      <section>\n        <h2>{h}</h2>\n        {body}\n      </section>')
    return '\n'.join(out)

MAIL = '<a href="mailto:vanylvensauna@gmail.com">vanylvensauna@gmail.com</a>'

en = dict(
  lang='en', title='Privacy | Vanylven Sauna',
  desc='How Vanylven Sauna handles personal details: gift card orders, bookings and visits to the website.',
  h1='Privacy', lead='We collect as little as we can, and only what we need to run the sauna. Here is what that means.',
  updated='Last updated 11 November 2026',
  sections=sections([
    ('Who is responsible', f'<p>Vanylven Sauna in Fiskå, run by volunteers from Vanylven, is responsible for the personal details described here. Contact us at {MAIL}.</p>'),
    ('Gift card orders', '<p>When you order a gift card on this website, we receive your email address, the names you write on the card (to and from), the message, the number of hours and the time of the order.</p>'
      '<ul><li><strong>Why:</strong> to issue the gift card, send it to you and check it when it is used.</li>'
      '<li><strong>Legal basis:</strong> it is needed to deliver what you ordered (GDPR article 6 (1) b). We do not ask for consent and we do not use your email for anything else, such as newsletters.</li>'
      '<li><strong>How long:</strong> until the gift card has expired, one year after the order. Then we delete the order.</li></ul>'),
    ('Bookings and payments', '<p>Bookings are made in Calendly, which receives the name and email you enter there. Payments go through Vipps or your bank. We use these details only to handle your booking and match your payment, and we do not keep them longer than we need to.</p>'),
    ('Who else handles the data', '<ul><li><strong>Vercel</strong> stores gift card orders for us. The data is kept in Frankfurt, Germany. Vercel is an American company and follows the EU rules for transfers to the USA.</li>'
      '<li><strong>Calendly</strong> handles bookings, <strong>Vipps</strong> handles mobile payments.</li>'
      '<li>We never sell or share your details with anyone else.</li></ul>'),
    ('When you visit the website', '<p>The website itself has no analytics, no advertising and no tracking cookies. To show the page, your browser fetches fonts from Google Fonts and icons and scripts from public content networks (unpkg and cdnjs). These services see your IP address when your browser asks for the files, as any website does. The map on the Find us page is embedded from Google Maps; when it loads, Google receives your IP address and may set its own cookies, under <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">the Google privacy policy</a>. The weather line on the home and Find us pages comes from the server that also handles gift card orders (Vercel, Frankfurt), which gets it from MET Norway; MET Norway does not see visitors. The host of this website also keeps short technical logs.</p>'),
    ('Your rights', f'<p>You can ask to see the details we have about you, have them corrected or deleted, or object to how we use them. Write to {MAIL}. If you think we handle your details wrongly, you can complain to the Norwegian Data Protection Authority, <a href="https://www.datatilsynet.no/en/" target="_blank" rel="noopener">Datatilsynet</a>.</p>'),
  ]),
)
nn = dict(
  lang='nn', title='Personvern | Vanylven Sauna',
  desc='Korleis Vanylven Sauna handterer personopplysningar: bestilling av gåvekort, booking og besøk på nettsida.',
  h1='Personvern', lead='Vi samlar inn så lite som mogleg, og berre det vi treng for å drive badstua. Her er kva det tyder.',
  updated='Sist oppdatert 11. november 2026',
  sections=sections([
    ('Kven som er ansvarleg', f'<p>Vanylven Sauna på Fiskå, drifta av frivillige frå Vanylven, er ansvarleg for personopplysningane som er omtala her. Kontakt oss på {MAIL}.</p>'),
    ('Bestilling av gåvekort', '<p>Når du bestiller eit gåvekort på denne nettsida, får vi e-postadressa di, namna du skriv på kortet (til og frå), helsinga, talet på timar og tidspunktet for bestillinga.</p>'
      '<ul><li><strong>Kvifor:</strong> for å skrive ut gåvekortet, sende det til deg og sjekke det når det blir brukt.</li>'
      '<li><strong>Rettsleg grunnlag:</strong> det trengst for å levere det du har bestilt (personvernforordninga artikkel 6 nr. 1 bokstav b). Vi ber ikkje om samtykke, og vi brukar ikkje e-posten din til noko anna, til dømes nyheitsbrev.</li>'
      '<li><strong>Kor lenge:</strong> til gåvekortet har gått ut, eitt år etter bestillinga. Då slettar vi bestillinga.</li></ul>'),
    ('Booking og betaling', '<p>Booking skjer i Calendly, som får namnet og e-posten du skriv inn der. Betaling skjer med Vipps eller gjennom banken din. Vi brukar desse opplysningane berre for å handtere bookinga og finne betalinga di, og vi tek ikkje vare på dei lenger enn vi treng.</p>'),
    ('Kven andre som handterer opplysningane', '<ul><li><strong>Vercel</strong> lagrar gåvekortbestillingane for oss. Opplysningane ligg i Frankfurt i Tyskland. Vercel er eit amerikansk selskap og følgjer EU-reglane for overføring til USA.</li>'
      '<li><strong>Calendly</strong> handterer booking, <strong>Vipps</strong> handterer mobilbetaling.</li>'
      '<li>Vi sel aldri opplysningane dine og deler dei ikkje med andre.</li></ul>'),
    ('Når du besøkjer nettsida', '<p>Nettsida sjølv har ingen analyseverktøy, ingen reklame og ingen sporingscookies. For å vise sida hentar nettlesaren skrifter frå Google Fonts og ikon og skript frå offentlege innhaldsnettverk (unpkg og cdnjs). Desse tenestene ser IP-adressa di når nettlesaren ber om filene, slik det er for alle nettsider. Kartet på sida Finn oss er henta frå Google Maps. Når kartet lastar, får Google IP-adressa di og kan setje eigne informasjonskapslar, etter <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">personvernerklæringa til Google</a>. Vêrlinja på framsida og på sida Finn oss kjem frå den same tenaren som tek imot gåvekortbestillingar (Vercel, Frankfurt), som hentar ho frå Meteorologisk institutt; instituttet ser ikkje dei besøkande. Den som driftar nettsida, tek òg vare på korte tekniske loggar.</p>'),
    ('Rettane dine', f'<p>Du kan be om å få sjå opplysningane vi har om deg, få dei retta eller sletta, eller protestere mot korleis vi brukar dei. Skriv til {MAIL}. Om du meiner vi handterer opplysningane dine feil, kan du klage til <a href="https://www.datatilsynet.no/" target="_blank" rel="noopener">Datatilsynet</a>.</p>'),
  ]),
)

for d, path, img, alt_href in [
    (en, 'privacy/index.html', '../img/', '../nn/privacy/'),
    (nn, 'nn/privacy/index.html', '../../img/', '../../privacy/'),
]:
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='') as f:
        sh, sf = shared.parts(d['lang'], '../', img, alt_href, here='privacy')
        f.write(T.format(shell_header=sh, shell_footer=sf, shell_css=shared.CSS, shell_js=shared.JS,
                         seo=shared.seo('privacy/', d['lang'], d['title'], d['desc'], 'img/deck-fjord.jpg'), icons=shared.icons(img), **d))
    print('wrote', path)
