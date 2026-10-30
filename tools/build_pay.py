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
<meta name="robots" content="noindex">
{seo}
<link rel="icon" href="{img}logo-mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:ital,wght@0,400..900;1,400..700&display=swap" rel="stylesheet">
<script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>
<style>
  /* Payment page: same tokens and shapes as the main site, kept short and calm. */
  :root {{
    --night: #0b1012; --night-2: #121a1d; --ink: #eef2f1; --muted: #a7b4b4; --faint: #6b7a7b;
    --line: rgb(238 242 241 / .12); --heat: #ef6a32; --heat-soft: #ffb48f; --on-heat: #1a1310;
    --brand: #5a4d44; --radius: 16px; --max: 1080px; --ease: cubic-bezier(.16, 1, .3, 1);
  }}
  *, *::before, *::after {{ box-sizing: border-box; }}
  html {{ background: var(--night); }}
  body {{
    margin: 0; color: var(--ink); font-family: "Schibsted Grotesk", system-ui, sans-serif; font-size: 17px; line-height: 1.6;
    -webkit-font-smoothing: antialiased; overflow-x: clip;
    background: radial-gradient(60% 50% at 85% 0%, rgb(239 106 50 / .16), transparent 70%), var(--night);
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
  .pebble.p2 {{ border-radius: 45% 55% 40% 60% / 60% 45% 55% 40%; }}
  .pebble.p3 {{ border-radius: 62% 38% 48% 52% / 52% 40% 60% 48%; }}
  .pebble.p4 {{ border-radius: 50% 50% 62% 38% / 40% 56% 44% 60%; }}
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
  .head h1 {{ font-size: clamp(2.6rem, 6vw, 4.6rem); max-width: 14ch; }}
  .head p {{ margin-top: 20px; color: var(--muted); font-size: 1.15rem; max-width: 52ch; }}
  .head p.pre {{ margin-top: 14px; font-size: .98rem; }}
  .head p.pre a {{ color: var(--heat-soft); }}

  /* Prices read as a plain list (not pills), so nothing looks selectable */
  .prices {{ margin: 44px 0 0; max-width: 520px; }}
  .prices h2 {{ font-size: .9rem; font-weight: 600; letter-spacing: 0; color: var(--muted); margin-bottom: 6px; }}
  .prices dl {{ margin: 0; }}
  .prices div {{ display: flex; align-items: baseline; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--line); }}
  .prices dt {{ color: var(--ink); }}
  .prices dt span {{ color: var(--muted); }}
  .prices dd {{ margin: 0 0 0 auto; font-weight: 700; font-size: 1.15rem; letter-spacing: -0.01em; white-space: nowrap; font-variant-numeric: tabular-nums; }}

  .switch {{ margin-top: 64px; display: inline-flex; padding: 5px; border-radius: 999px; background: rgb(255 255 255 / .06); box-shadow: inset 0 0 0 1px var(--line); }}
  .switch button {{ border: 0; background: none; cursor: pointer; padding: 12px 22px; border-radius: 999px; font-weight: 600; color: var(--muted); display: inline-flex; gap: 8px; align-items: center; transition: background-color .3s var(--ease), color .3s; }}
  .switch button[aria-selected="true"] {{ background: var(--ink); color: var(--night); }}

  .panel {{ margin-top: 36px; display: grid; grid-template-columns: 1.25fr 1fr; gap: 56px; align-items: start; }}
  .panel[hidden] {{ display: none; }}
  .panel h2 {{ font-size: 1.7rem; letter-spacing: -0.025em; margin-bottom: 26px; }}

  .steps {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 22px; counter-reset: s; }}
  .steps li {{ display: grid; grid-template-columns: 44px 1fr; gap: 18px; align-items: start; }}
  .steps .pebble {{ width: 40px; height: 37px; background: var(--ink); color: var(--night); font-weight: 800; font-size: .95rem; }}
  .steps p {{ padding-top: 6px; }}
  .steps p em {{ font-style: normal; color: var(--muted); }}

  .rows {{ display: grid; border-radius: var(--radius); box-shadow: inset 0 0 0 1px var(--line); overflow: hidden; }}
  .row {{ display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 16px; padding: 16px 16px 16px 22px; }}
  .row + .row {{ border-top: 1px solid var(--line); }}
  .row dt {{ color: var(--muted); font-size: .88rem; }}
  .row dd {{ margin: 2px 0 0; font-size: 1.2rem; font-weight: 600; letter-spacing: .01em; font-variant-numeric: tabular-nums; }}
  .copy {{ border: 0; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; padding: 10px 16px; border-radius: 999px; background: rgb(255 255 255 / .08); font-size: .9rem; font-weight: 600; transition: background-color .25s; }}
  .copy:hover {{ background: rgb(255 255 255 / .15); }}
  .copy.done {{ background: var(--ink); color: var(--night); }}
  .copy i {{ font-size: 1.1em; }}

  .note {{ margin-top: 22px; display: flex; gap: 14px; padding: 18px 20px; border-radius: var(--radius); background: rgb(239 106 50 / .08); box-shadow: inset 0 0 0 1px rgb(239 106 50 / .22); }}
  .note i {{ font-size: 1.4rem; color: var(--heat-soft); flex: none; }}
  .note p {{ color: var(--ink); font-size: .98rem; }}
  .note p span {{ color: var(--muted); }}

  /* QR for Vipps number 943550 (from the Vipps portal). Shown on wide screens only: you scan it with the phone you pay from. */
  .qr {{ position: sticky; top: 32px; border-radius: var(--radius); padding: 28px; background: var(--night-2); box-shadow: inset 0 0 0 1px var(--line); text-align: center; }}
  .qr .slot {{ aspect-ratio: 1; display: grid; place-items: center; border-radius: 12px; background: repeating-linear-gradient(45deg, rgb(255 255 255 / .03) 0 10px, transparent 10px 20px); box-shadow: inset 0 0 0 1px rgb(255 255 255 / .16); color: var(--faint); }}
  .qr .slot i {{ font-size: 4rem; }}
  .qr .slot {{ background: none; box-shadow: none; }}
  .qr .slot img {{ display: block; width: 100%; height: auto; border-radius: 6.5%; }}
  .qr h3 {{ margin-top: 22px; font-size: 1.15rem; letter-spacing: -0.02em; }}
  .qr p {{ margin-top: 6px; color: var(--muted); font-size: .92rem; }}
  .side p.small {{ color: var(--muted); font-size: .95rem; }}

  .after {{ margin-top: 96px; padding-top: 40px; border-top: 1px solid var(--line); display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }}
  .after h3 {{ font-size: 1.2rem; letter-spacing: -0.02em; display: flex; gap: 10px; align-items: center; }}
  .after p {{ margin-top: 8px; color: var(--muted); max-width: 46ch; }}
  .after .btn {{ margin-top: 18px; }}


  .sr {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}

  @media (max-width: 860px) {{
    .wrap {{ padding: 0 18px; }}
    main {{ padding-top: 96px; }}
    .panel {{ grid-template-columns: 1fr; gap: 32px; }}
    .qr {{ display: none; }}
    .after {{ grid-template-columns: 1fr; }}
    .switch {{ display: flex; }}
    .switch button {{ flex: 1; justify-content: center; padding: 12px 10px; }}
  }}
  @media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
{shell_css}</style>
</head>
<body>

{shell_header}

<main>
  <div class="wrap">
    <div class="head">
      <h1>{h1}</h1>
      <p>{lead}</p>
      <p class="pre">{pre}</p>
    </div>

    <section class="prices" aria-labelledby="prices-h">
      <h2 id="prices-h">{prices_h}</h2>
      <dl>
        <div><dt>{private_name} <span>{private_unit}</span></dt><dd>{private_price}</dd></div>
        <div><dt>{open_name} <span>{open_unit}</span></dt><dd>{open_price}</dd></div>
      </dl>
    </section>

    <div class="switch" role="tablist" aria-label="{switch_label}">
      <button type="button" role="tab" id="tab-vipps" aria-controls="vipps" aria-selected="true"><i class="ph ph-device-mobile" aria-hidden="true"></i>{tab_vipps}</button>
      <button type="button" role="tab" id="tab-abroad" aria-controls="abroad" aria-selected="false" tabindex="-1"><i class="ph ph-globe-hemisphere-west" aria-hidden="true"></i>{tab_abroad}</button>
    </div>

    <section class="panel" id="vipps" role="tabpanel" aria-labelledby="tab-vipps">
      <div>
        <h2>{vipps_h}</h2>
        <ol class="steps">
          <li><span class="pebble" aria-hidden="true">1</span><p>{v1}</p></li>
          <li><span class="pebble p2" aria-hidden="true">2</span><p>{v2}</p></li>
          <li><span class="pebble p3" aria-hidden="true">3</span><p>{v3}</p></li>
          <li><span class="pebble p4" aria-hidden="true">4</span><p>{v4}</p></li>
        </ol>
        <dl class="rows" style="margin-top:32px">
          <div class="row"><div><dt>{l_vipps}</dt><dd>943550</dd></div><button class="copy" type="button" data-copy="943550"><i class="ph ph-copy" aria-hidden="true"></i><span>{copy}</span></button></div>
        </dl>
        <div class="note"><i class="ph ph-chat-text" aria-hidden="true"></i><p>{msg_note}</p></div>
      </div>
      <aside class="qr">
        <div class="slot"><img src="{img}vipps-qr.jpg" alt="{qr_alt}" width="800" height="800"></div>
        <h3>{qr_h}</h3>
        <p>{qr_p}</p>
      </aside>
    </section>

    <section class="panel" id="abroad" role="tabpanel" aria-labelledby="tab-abroad" hidden>
      <div>
        <h2>{abroad_h}</h2>
        <dl class="rows">
          <div class="row"><div><dt>{l_name}</dt><dd>Sauna</dd></div><button class="copy" type="button" data-copy="Sauna"><i class="ph ph-copy" aria-hidden="true"></i><span>{copy}</span></button></div>
          <div class="row"><div><dt>IBAN</dt><dd>NO84 3905 3414 714</dd></div><button class="copy" type="button" data-copy="NO8439053414714"><i class="ph ph-copy" aria-hidden="true"></i><span>{copy}</span></button></div>
          <div class="row"><div><dt>SWIFT / BIC</dt><dd>SPARNO22XXX</dd></div><button class="copy" type="button" data-copy="SPARNO22XXX"><i class="ph ph-copy" aria-hidden="true"></i><span>{copy}</span></button></div>
          <div class="row"><div><dt>{l_amount}</dt><dd>{amount_value}</dd></div></div>
        </dl>
        <div class="note"><i class="ph ph-chat-text" aria-hidden="true"></i><p>{ref_note}</p></div>
      </div>
      <aside class="side">
        <p class="small">{abroad_side}</p>
      </aside>
    </section>

    <div class="after">
      <div>
        <h3><i class="ph ph-key" aria-hidden="true"></i>{after_h}</h3>
        <p>{after_p}</p>
      </div>
      <div>
        <h3><i class="ph ph-calendar-blank" aria-hidden="true"></i>{book_h}</h3>
        <p>{book_p}</p>
        <a class="btn btn-heat" href="https://calendly.com/vanylvensauna/sauna" target="_blank" rel="noopener">{book_btn} <i class="ph ph-arrow-up-right" aria-hidden="true"></i></a>
      </div>
    </div>
  </div>
</main>

{shell_footer}

<p class="sr" aria-live="polite" id="live"></p>

<script>
  // Tabs: Vipps or bank transfer. #abroad in the URL opens the bank tab, so the link can be shared.
  const tabs = [...document.querySelectorAll('[role="tab"]')];
  function show(id, focus) {{
    tabs.forEach((t) => {{
      const on = t.getAttribute('aria-controls') === id;
      t.setAttribute('aria-selected', on); t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      if (on && focus) t.focus();
    }});
  }}
  tabs.forEach((t, i) => {{
    t.addEventListener('click', () => {{ show(t.getAttribute('aria-controls')); history.replaceState(null, '', '#' + t.getAttribute('aria-controls')); }});
    t.addEventListener('keydown', (e) => {{
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const next = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      show(next.getAttribute('aria-controls'), true);
    }});
  }});
  if (location.hash === '#abroad') show('abroad');

  // Copy buttons
  const live = document.getElementById('live');
  document.querySelectorAll('.copy').forEach((b) => {{
    const label = b.querySelector('span'), icon = b.querySelector('i'), text = label.textContent;
    b.addEventListener('click', async () => {{
      try {{ await navigator.clipboard.writeText(b.dataset.copy); }} catch (e) {{ return; }}
      b.classList.add('done'); label.textContent = '{copied}'; icon.className = 'ph ph-check';
      live.textContent = '{copied}: ' + b.dataset.copy;
      setTimeout(() => {{ b.classList.remove('done'); label.textContent = text; icon.className = 'ph ph-copy'; }}, 1800);
    }});
  }});
{shell_js}</script>
</body>
</html>
'''

en = dict(
  lang='en', title='Pay for your sauna | Vanylven Sauna',
  desc='How to pay for your session at Vanylven Sauna, with Vipps or by bank transfer from abroad.',
  alt_lang='nn', alt_name='Norsk', nav_label='Page links', nav_prices='Prices',
  pre='Not booked yet? <a href="https://calendly.com/vanylvensauna/sauna" target="_blank" rel="noopener">Pick a time first</a>. Have a gift card? No need to pay, just <a href="mailto:vanylvensauna@gmail.com">email us</a> the number of your gift card.',
  h1='Pay for your session', lead='Pay before you come. Once your payment is in, we send you the door code the day before your visit.',
  private_price='NOK 600', prices_h='What to pay', private_name='Private sauna', private_unit='2 hours, up to 8 people', open_name='Open sauna', open_unit='per person, paid when you arrive', open_price='NOK 100',
  switch_label='How do you want to pay?', tab_vipps='I have Vipps', tab_abroad='From abroad',
  vipps_h='Pay with Vipps',
  v1='Open Vipps and tap <strong>Pay</strong>.',
  v2='Search for <strong>943550</strong>. <em>That is our Vipps number.</em>',
  v3='Enter the amount: <strong>600 kr</strong> for a private session, <strong>100 kr</strong> per person for open sauna.',
  v4='Add a message (see below) and confirm.',
  l_vipps='Vipps number', copy='Copy', copied='Copied',
  msg_note='In the message, write <strong>the date of your session and your name</strong>, for example <em>12 June, Kari Nordmann</em>. <span>That is how we match your payment to your booking.</span>',
  qr_alt='QR code for Vipps number 943550', qr_h='Scan to pay', qr_p='Point your phone camera at the code and Vipps opens with our number filled in.',
  abroad_h='Pay by bank transfer', l_name='Account name', l_amount='Amount', amount_value='NOK 600 (Private Sauna) or NOK 100 per person (Open Sauna)',
  ref_note='In the payment reference, write <strong>the date of your session and your name</strong>. <span>That is how we match your payment to your booking.</span>',
  abroad_side='Most visitors from abroad do not have Vipps, so a bank transfer is the way to go. International transfers can take a few working days, so pay as soon as you have booked. Questions? Email <a href="mailto:vanylvensauna@gmail.com">vanylvensauna@gmail.com</a>.',
  after_h='What happens next', after_p='When your payment has come in, we send you the code to the sauna door the day before your visit.',
  book_h='Not booked yet?', book_p='Pick a free time in the calendar first, then pay here.', book_btn='Book a session',
)
nn = dict(
  lang='nn', title='Betal for badstua | Vanylven Sauna',
  desc='Slik betaler du for økta i Vanylven Sauna, med Vipps eller med bankoverføring frå utlandet.',
  alt_lang='en', alt_name='English', nav_label='Lenker', nav_prices='Prisar',
  pre='Ikkje booka enno? <a href="https://calendly.com/vanylvensauna/sauna" target="_blank" rel="noopener">Vel ei tid først</a>. Har du gåvekort? Då treng du ikkje betale, berre <a href="mailto:vanylvensauna@gmail.com">send oss</a> nummeret på gåvekortet.',
  h1='Betal for økta', lead='Betal før du kjem. Når betalinga er komen inn, sender vi deg koden til døra dagen før besøket.',
  private_price='600 kr', prices_h='Kva du betaler', private_name='Privat badstue', private_unit='2 timar, opptil 8 personar', open_name='Open badstue', open_unit='per person, betal når du kjem', open_price='100 kr',
  switch_label='Korleis vil du betale?', tab_vipps='Eg har Vipps', tab_abroad='Frå utlandet',
  vipps_h='Betal med Vipps',
  v1='Opne Vipps og trykk på <strong>Betal</strong>.',
  v2='Søk opp <strong>943550</strong>. <em>Det er Vipps-nummeret vårt.</em>',
  v3='Skriv inn beløpet: <strong>600 kr</strong> for privat økt, <strong>100 kr</strong> per person for open badstue.',
  v4='Skriv ei melding (sjå under) og stadfest.',
  l_vipps='Vipps-nummer', copy='Kopier', copied='Kopiert',
  msg_note='I meldinga skriv du <strong>datoen for økta og namnet ditt</strong>, til dømes <em>12. juni, Kari Nordmann</em>. <span>Slik finn vi ut kva booking betalinga høyrer til.</span>',
  qr_alt='QR-kode for Vipps-nummer 943550', qr_h='Skann og betal', qr_p='Hald kameraet på telefonen mot koden, så opnar Vipps seg med nummeret vårt.',
  abroad_h='Betal med bankoverføring', l_name='Kontonamn', l_amount='Beløp', amount_value='600 kr (privat badstue) eller 100 kr per person (open badstue)',
  ref_note='I referansefeltet skriv du <strong>datoen for økta og namnet ditt</strong>. <span>Slik finn vi ut kva booking betalinga høyrer til.</span>',
  abroad_side='Dei fleste som kjem frå utlandet har ikkje Vipps, så då er bankoverføring vegen å gå. Utanlandske overføringar kan ta nokre arbeidsdagar, så betal så snart du har booka. Spørsmål? Send e-post til <a href="mailto:vanylvensauna@gmail.com">vanylvensauna@gmail.com</a>.',
  after_h='Kva skjer så', after_p='Når betalinga er komen inn, sender vi deg koden til badstudøra dagen før besøket.',
  book_h='Ikkje booka enno?', book_p='Vel ei ledig tid i kalenderen først, og betal så her.', book_btn='Book ei økt',
)
for d, path, img, home, alt_href in [
    (en, 'pay/index.html', '../img/', '../', '../nn/pay/'),
    (nn, 'nn/pay/index.html', '../../img/', '../', '../../pay/'),
]:
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='') as f:
        sh, sf = shared.parts(d['lang'], '../', img, alt_href, here='pay')
        f.write(T.format(shell_header=sh, shell_footer=sf, shell_css=shared.CSS, shell_js=shared.JS, seo=shared.seo('pay/', d['lang'], d['title'], d['desc'], 'img/deck-fjord.jpg'), img=img, home=home, alt_href=alt_href, **d))
    print('wrote', path)
