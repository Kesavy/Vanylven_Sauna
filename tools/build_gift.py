import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shared, json

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
<link href="https://fonts.googleapis.com/css2?family=Italiana&family=Schibsted+Grotesk:ital,wght@0,400..900;1,400..700&display=swap" rel="stylesheet">
<script src="https://unpkg.com/@phosphor-icons/web@2.1.1"></script>
<style>
  /*
    Gift card page: the buyer designs the card, sees it live, and sends the order from their own email app.
    Nothing is stored or sent by the site. The card face copies the printed card (taupe, thin display title, ruled fields).
  */
  :root {{
    --night: #0b1012; --night-2: #121a1d; --ink: #eef2f1; --muted: #a7b4b4; --faint: #7d8c8d;
    --line: rgb(238 242 241 / .12); --heat: #ef6a32; --heat-soft: #ffb48f; --on-heat: #1a1310;
    --brand: #5a4d44; --card: #716a64; --card-ink: #f3eee9; --radius: 16px; --max: 1180px; --ease: cubic-bezier(.16, 1, .3, 1);
  }}
  *, *::before, *::after {{ box-sizing: border-box; }}
  html {{ background: var(--night); }}
  body {{
    margin: 0; color: var(--ink); font-family: "Schibsted Grotesk", system-ui, sans-serif; font-size: 17px; line-height: 1.6;
    -webkit-font-smoothing: antialiased; overflow-x: clip; min-height: 100dvh; display: flex; flex-direction: column;
    background: radial-gradient(55% 45% at 80% 10%, rgb(113 106 100 / .35), transparent 70%), var(--night);
  }}
  img {{ display: block; max-width: 100%; height: auto; }}
  a {{ color: inherit; }}
  button, input, select, textarea {{ font: inherit; color: inherit; }}
  :focus-visible {{ outline: 3px solid var(--heat); outline-offset: 3px; }}
  .wrap {{ max-width: var(--max); margin: 0 auto; padding: 0 32px; }}
  h1, h2, h3 {{ margin: 0; font-weight: 800; letter-spacing: -0.035em; line-height: 1; }}
  p {{ margin: 0; }}
  .pebble {{ display: inline-grid; place-items: center; border-radius: 58% 42% 55% 45% / 47% 58% 42% 53%; }}
  .pebble.p2 {{ border-radius: 45% 55% 40% 60% / 60% 45% 55% 40%; }}
  .pebble.p3 {{ border-radius: 62% 38% 48% 52% / 52% 40% 60% 48%; }}
  .btn {{
    display: inline-flex; align-items: center; justify-content: center; gap: 10px; padding: 17px 28px; border-radius: 999px; border: 0; cursor: pointer;
    font-weight: 700; font-size: 1rem; line-height: 1; text-decoration: none; white-space: nowrap; transition: transform .25s var(--ease), background-color .25s;
  }}
  .btn:active {{ transform: scale(.97); }}
  .btn-heat {{ background: var(--heat); color: var(--on-heat); }}
  .btn-heat:hover {{ background: #ff7a42; }}


  main {{ flex: 1; padding: 128px 0 120px; }}
  .layout {{ display: grid; grid-template-columns: 1fr 1.1fr; gap: 72px; align-items: start; }}
  .head h1 {{ font-size: clamp(2.6rem, 5.5vw, 4.4rem); max-width: 12ch; }}
  .head p {{ margin-top: 18px; color: var(--muted); font-size: 1.12rem; max-width: 44ch; }}

  form {{ margin-top: 44px; display: grid; gap: 26px; }}
  .field {{ display: grid; gap: 10px; }}
  .field > span, .field legend {{ font-weight: 600; font-size: .95rem; padding: 0; }}
  .field small {{ color: var(--faint); font-weight: 400; }}
  fieldset {{ border: 0; margin: 0; padding: 0; }}
  input[type="text"], input[type="email"], textarea {{
    width: 100%; padding: 15px 18px; border-radius: 12px; border: 0; background: rgb(255 255 255 / .06);
    box-shadow: inset 0 0 0 1px var(--line); transition: box-shadow .2s, background-color .2s;
  }}
  input[type="text"]:hover, input[type="email"]:hover, textarea:hover {{ background: rgb(255 255 255 / .08); }}
  input[type="text"]:focus, input[type="email"]:focus, textarea:focus {{ outline: none; box-shadow: inset 0 0 0 2px var(--heat); }}
  textarea {{ resize: none; min-height: 92px; }}
  .field .count {{ justify-self: end; margin-top: -4px; color: var(--faint); font-size: .85rem; font-variant-numeric: tabular-nums; }}
  .field .count.near {{ color: var(--heat-soft); }}
  .two {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}

  .choices {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }}
  .choice {{ position: relative; }}
  .choice input {{ position: absolute; opacity: 0; inset: 0; cursor: pointer; }}
  .choice label {{
    display: grid; gap: 2px; padding: 16px 16px 14px; border-radius: 14px; cursor: pointer;
    box-shadow: inset 0 0 0 1px var(--line); transition: box-shadow .2s, background-color .2s;
  }}
  .choice label strong {{ font-size: 1.2rem; letter-spacing: -0.02em; }}
  .choice label span {{ color: var(--muted); font-size: .9rem; }}
  .choice input:checked + label {{ background: rgb(239 106 50 / .1); box-shadow: inset 0 0 0 2px var(--heat); }}
  .choice input:focus-visible + label {{ outline: 3px solid var(--heat); outline-offset: 3px; }}

  .send {{ display: grid; gap: 14px; padding-top: 8px; }}
  .send .btn {{ width: 100%; }}
  .send p {{ color: var(--faint); font-size: .88rem; }}
  .send p a {{ color: var(--muted); }}
  .send .err {{ color: #ffb48f; font-size: .92rem; font-weight: 600; }}
  .send .btn:disabled {{ opacity: .6; cursor: progress; }}
  [hidden] {{ display: none !important; }}
  .sr {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%); white-space: nowrap; }}
  .done h2:focus {{ outline: none; }}
  .hp {{ position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }}

  /* After a successful order: the number and what to do next */
  .done {{ margin-top: 44px; display: grid; gap: 16px; padding: 30px; border-radius: var(--radius); background: rgb(239 106 50 / .08); box-shadow: inset 0 0 0 1px rgb(239 106 50 / .35); }}
  .done h2 {{ font-size: 1.6rem; letter-spacing: -0.03em; }}
  .done p {{ color: var(--muted); line-height: 1.6; }}
  .done p strong {{ color: var(--ink); }}
  .done a {{ color: var(--heat-soft); }}
  .done .again {{ justify-self: start; border: 0; background: none; padding: 0; color: var(--heat-soft); font: inherit; text-decoration: underline; text-underline-offset: 3px; cursor: pointer; }}
  .card .no {{ position: absolute; top: 4.5%; right: 4%; font-size: 2.2cqi; letter-spacing: .08em; opacity: .8; }}

  /* Fallback when no email app opens: the order in the card's look, ready to copy */
  .copybox {{ border: 0; padding: 0; max-width: min(560px, calc(100vw - 32px)); width: 100%; background: none; color: var(--card-ink); }}
  .copybox::backdrop {{ background: rgb(8 13 15 / .75); backdrop-filter: blur(6px); -webkit-backdrop-filter: blur(6px); }}
  .copybox .face {{ position: relative; border-radius: 14px; padding: 30px 30px 26px; display: grid; gap: 18px;
    background: radial-gradient(120% 90% at 20% 0%, rgb(255 255 255 / .08), transparent 60%), var(--card); box-shadow: 0 40px 80px -30px rgb(0 0 0 / .8); }}
  .copybox .face > img {{ width: 52%; height: auto; justify-self: center; }}
  .copybox h2 {{ font-size: 1.35rem; letter-spacing: -0.02em; }}
  .copybox .lead {{ font-size: .98rem; line-height: 1.5; }}
  .copybox .lead strong {{ white-space: nowrap; }}
  .copybox .order {{ margin: 0; padding: 16px 18px; border-radius: 10px; background: rgb(0 0 0 / .18); box-shadow: inset 0 0 0 1px rgb(243 238 233 / .25);
    font-family: inherit; font-size: .92rem; line-height: 1.55; white-space: pre-wrap; overflow-wrap: anywhere; max-height: 40vh; overflow: auto; font-weight: 400; }}
  .copybox .order b {{ font-weight: 800; color: #fff; }}
  .copybox .actions {{ display: flex; flex-wrap: wrap; gap: 10px; }}
  .copybox .actions .btn {{ flex: 1 1 auto; }}
  .copybox .btn-light {{ background: rgb(243 238 233 / .14); color: var(--card-ink); box-shadow: inset 0 0 0 1px rgb(243 238 233 / .35); }}
  .copybox .btn-light:hover {{ background: rgb(243 238 233 / .22); }}
  .copybox .close {{ position: absolute; top: 12px; right: 12px; width: 40px; height: 40px; border: 0; border-radius: 50%; cursor: pointer; background: rgb(0 0 0 / .18); color: var(--card-ink); font-size: 1.2rem; display: grid; place-items: center; }}

  .side {{ position: sticky; top: 28px; display: grid; gap: 28px; }}

  /* The card face */
  .card {{
    container-type: inline-size; aspect-ratio: 1.55; border-radius: 10px; position: relative; overflow: hidden; color: var(--card-ink);
    background: radial-gradient(120% 90% at 20% 0%, rgb(255 255 255 / .08), transparent 60%), var(--card);
    box-shadow: 0 40px 80px -30px rgb(0 0 0 / .7), 0 2px 0 rgb(255 255 255 / .06) inset;
    transform: rotate(-2deg); transition: transform .6s var(--ease);
  }}
  .card:hover {{ transform: rotate(0); }}
  .card .title {{ position: absolute; top: 9%; left: 0; right: 0; display: flex; justify-content: center; }}
  .card .title img {{ width: 58cqi; height: auto; }}
  .card dl {{ position: absolute; left: 7%; top: 29%; width: 50%; margin: 0; display: grid; gap: 3.8cqi; }}
  .card dl div {{ display: grid; grid-template-columns: auto 1fr; align-items: end; gap: 2cqi; border-bottom: 1px solid rgb(243 238 233 / .55); padding-bottom: .6cqi; }}
  .card dt {{ font-family: "Italiana", serif; font-size: 3.4cqi; line-height: 1; opacity: .9; }}
  .card dd {{ margin: 0; font-size: 3.3cqi; font-weight: 700; line-height: 1.1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-height: 1.1em; }}
  .card .msg {{ position: absolute; left: 7%; bottom: 6%; width: 50%; font-size: 2.8cqi; font-style: italic; font-weight: 700; line-height: 1.35; opacity: .9; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; overflow-wrap: anywhere; }}
  .card .mark {{ position: absolute; right: 7%; bottom: 9%; }}
  .card .mark img {{ display: block; width: 25cqi; height: auto; }}

  .how {{ display: grid; gap: 16px; padding: 26px; border-radius: var(--radius); background: var(--night-2); box-shadow: inset 0 0 0 1px var(--line); }}
  .how h2 {{ font-size: 1.2rem; letter-spacing: -0.02em; }}
  .how ol {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 14px; }}
  .how li {{ display: grid; grid-template-columns: 38px 1fr; gap: 14px; color: var(--muted); font-size: .97rem; }}
  .how li strong {{ color: var(--ink); font-weight: 600; }}
  .how .pebble {{ width: 34px; height: 31px; background: var(--ink); color: var(--night); font-weight: 800; font-size: .85rem; }}
  .how a {{ color: var(--heat-soft); }}

  /* Steam: you fill in the card while sitting in the sauna. Faded behind the form so the text stays clean, fuller around the card. */
  canvas.steam {{
    position: fixed; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 0;
    -webkit-mask-image: linear-gradient(to right, rgb(0 0 0 / .18) 0%, rgb(0 0 0 / .18) 42%, #000 72%);
    mask-image: linear-gradient(to right, rgb(0 0 0 / .18) 0%, rgb(0 0 0 / .18) 42%, #000 72%);
  }}
  main, footer {{ position: relative; z-index: 1; }}
  input[type="text"], input[type="email"], textarea {{ background-color: rgb(18 26 29 / .72); }}
  .choice label {{ background-color: rgb(18 26 29 / .55); }}

  @media (max-width: 900px) {{
    .wrap {{ padding: 0 18px; }}
    main {{ padding-top: 92px; }}
    .layout {{ grid-template-columns: 1fr; gap: 40px; }}
    .side {{ position: static; order: -1; }}
    .card {{ transform: rotate(-1.5deg); }}
    .choices {{ grid-template-columns: 1fr 1fr 1fr; }}
    .choice label {{ padding: 14px 12px 12px; }}
    .two {{ grid-template-columns: 1fr; }}
    .how {{ display: none; }}
    .how.after {{ display: grid; }}
    canvas.steam {{ -webkit-mask-image: linear-gradient(to bottom, #000 0%, rgb(0 0 0 / .5) 30%, rgb(0 0 0 / .12) 55%); mask-image: linear-gradient(to bottom, #000 0%, rgb(0 0 0 / .5) 30%, rgb(0 0 0 / .12) 55%); }}
  }}
  @media (min-width: 901px) {{ .how.after {{ display: none; }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ transition: none !important; }} }}
{shell_css}</style>
</head>
<body>
<canvas class="steam" aria-hidden="true"></canvas>

{shell_header}

<main id="main">
  <div class="wrap layout">
    <div>
      <div class="head">
        <h1>{h1}</h1>
        <p>{lead}</p>
      </div>

      <form id="order" novalidate>
        <fieldset class="field">
          <legend>{l_gift}</legend>
          <div class="choices">
            <div class="choice"><input type="radio" name="hours" id="h2" value="2" checked><label for="h2"><strong>{h2}</strong><span>{p2}</span></label></div>
            <div class="choice"><input type="radio" name="hours" id="h4" value="4"><label for="h4"><strong>{h4}</strong><span>{p4}</span></label></div>
            <div class="choice"><input type="radio" name="hours" id="h6" value="6"><label for="h6"><strong>{h6}</strong><span>{p6}</span></label></div>
          </div>
        </fieldset>
        <div class="two">
          <label class="field"><span>{l_to}</span><input type="text" name="to" maxlength="40" autocomplete="off" placeholder="{p_to}"></label>
          <label class="field"><span>{l_from}</span><input type="text" name="from" maxlength="40" autocomplete="name" placeholder="{p_from}"></label>
        </div>
        <label class="field"><span>{l_email}</span><input type="email" name="email" maxlength="120" autocomplete="email" placeholder="{p_email}" required></label>
        <label class="hp" aria-hidden="true">Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
        <label class="field"><span>{l_msg} <small>{optional}</small></span><textarea name="msg" maxlength="70" placeholder="{p_msg}" aria-describedby="msg-count"></textarea><small class="count" id="msg-count">0 / 70</small><span class="sr" id="msg-limit" aria-live="polite"></span></label>
        <div class="send">
          <p class="err" role="alert" hidden></p>
          <button class="btn btn-heat" type="submit"><i class="ph ph-paper-plane-tilt" aria-hidden="true"></i><span>{send}</span></button>
          <p>{send_note}</p>
        </div>
      </form>

      <section class="done" aria-live="polite" hidden>
        <h2 tabindex="-1"></h2>
        <p></p>
        <button class="again" type="button">{again}</button>
      </section>

      <dialog class="copybox" aria-labelledby="copy-h">
        <div class="face">
          <button class="close" type="button" aria-label="{close}"><i class="ph ph-x" aria-hidden="true"></i></button>
          <img src="{img}gavekort.svg" alt="" width="273" height="44">
          <h2 id="copy-h">{pop_h}</h2>
          <p class="lead">{pop_p}</p>
          <pre class="order"></pre>
          <div class="actions">
            <button class="btn btn-heat" type="button" data-copy="order"><i class="ph ph-copy" aria-hidden="true"></i><span>{copy_order}</span></button>
            <button class="btn btn-light" type="button" data-copy="email"><i class="ph ph-at" aria-hidden="true"></i><span>{copy_email}</span></button>
          </div>
        </div>
      </dialog>

      <section class="how after" aria-label="{how_h}">
        <h2>{how_h}</h2>
        <ol>{how_items}</ol>
      </section>
    </div>

    <div class="side">
      <figure class="card" aria-label="{preview_label}" style="margin:0">
        <span class="no" data-out="no"></span>
        <div class="title"><img src="{img}gavekort.svg" alt="{card_title}" width="273" height="44"></div>
        <dl>
          <div><dt>{c_value}</dt><dd data-out="value"></dd></div>
          <div><dt>{c_to}</dt><dd data-out="to"></dd></div>
          <div><dt>{c_from}</dt><dd data-out="from"></dd></div>
          <div><dt>{c_valid}</dt><dd data-out="valid"></dd></div>
        </dl>
        <p class="msg" data-out="msg"></p>
        <div class="mark"><img src="{img}logo-full.svg" alt="Vanylven Sauna" width="278" height="182"></div>
      </figure>

      <section class="how" aria-label="{how_h}">
        <h2>{how_h}</h2>
        <ol>{how_items}</ol>
      </section>
    </div>
  </div>
</main>

{shell_footer}

<script>
  // Steam: soft sprites rising on a half-resolution canvas (same recipe as the main page, without the water mode)
  (() => {{
    const c = document.querySelector('canvas.steam');
    const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const sprite = document.createElement('canvas'); sprite.width = sprite.height = 128;
    const sg = sprite.getContext('2d'), rg = sg.createRadialGradient(64, 64, 0, 64, 64, 64);
    rg.addColorStop(0, 'rgba(240,244,244,1)'); rg.addColorStop(.45, 'rgba(240,244,244,.45)'); rg.addColorStop(1, 'rgba(240,244,244,0)');
    sg.fillStyle = rg; sg.fillRect(0, 0, 128, 128);
    const g = c.getContext('2d'); let w, h, parts = [], tick = 0;
    const size = () => {{ w = c.width = Math.round(innerWidth * .5); h = c.height = Math.round(innerHeight * .5); if (calm) still(); }};
    const spawn = (y) => parts.push({{ x: Math.random() * w, y: y ?? h + 40, seed: Math.random() * 1000, vy: -(.2 + Math.random() * .35) * (h / 500),
      r: 34 + Math.random() * 44, grow: .22 + Math.random() * .3, life: 0, max: 520 + Math.random() * 260, a: .26 + Math.random() * .16 }});
    function still() {{ g.clearRect(0, 0, w, h); g.globalAlpha = .3; for (let i = 0; i < 12; i++) {{ const r = 90 + i * 8; g.drawImage(sprite, (i / 12) * w - r, h * .45 + Math.sin(i) * 50 - r, r * 2, r * 2); }} g.globalAlpha = 1; }}
    function frame() {{
      tick++;
      if (parts.length < 46 && tick % 3 === 0) spawn();
      g.clearRect(0, 0, w, h);
      for (let i = parts.length - 1; i >= 0; i--) {{
        const p = parts[i]; p.life++; p.y += p.vy; p.r += p.grow;
        p.x += Math.sin(p.seed + p.life * .012) * .45 + Math.sin(p.seed * 2 + tick * .004) * .25;
        const k = p.life / p.max;
        if (k >= 1 || p.y + p.r < -20) {{ parts.splice(i, 1); continue; }}
        g.globalAlpha = Math.sin(Math.PI * k) * p.a; g.drawImage(sprite, p.x - p.r, p.y - p.r, p.r * 2, p.r * 2);
      }}
      g.globalAlpha = 1;
      if (!document.hidden) requestAnimationFrame(frame); else addEventListener('visibilitychange', () => requestAnimationFrame(frame), {{ once: true }});
    }}
    size(); addEventListener('resize', size);
    if (!calm) {{ for (let i = 0; i < 24; i++) {{ spawn(Math.random() * h * 1.1); parts[i].life = Math.random() * 300; }} requestAnimationFrame(frame); }}
  }})();

  const t = {strings};
  const group = (n) => String(n).replace(/\B(?=(\d{{3}})+(?!\d))/g, ' ');
  {money_js}
  const form = document.getElementById('order');
  const out = (k) => document.querySelector('[data-out="' + k + '"]');
  const val = (n) => form.elements[n].value.trim();
  const hours = () => form.querySelector('input[name="hours"]:checked').value;

  // Valid for one year from the day the card is filled in
  const until = new Date(); until.setFullYear(until.getFullYear() + 1);
  // Month names are spelled out here: browsers without Nynorsk would otherwise fall back to their own language
  const validText = t.date.replace('{{d}}', until.getDate()).replace('{{m}}', t.months[until.getMonth()]).replace('{{y}}', until.getFullYear());
  out('valid').textContent = validText;

  function render() {{
    out('value').textContent = t.value(hours());
    out('to').textContent = val('to');
    out('from').textContent = val('from');
    out('msg').textContent = val('msg') ? '“' + val('msg') + '”' : '';
    const n = form.elements.msg.value.length, cnt = document.getElementById('msg-count');
    cnt.textContent = n + ' / 70'; cnt.classList.toggle('near', n >= 60);
    // Screen readers hear the count only near the limit, not on every key
    const lim = document.getElementById('msg-limit'), say = n >= 60 ? n + ' / 70' : '';
    if (lim.textContent !== say) lim.textContent = say;
    // Shrink the message a little until it fits its two lines on the card
    const m = out('msg'); let size = 2.8; m.style.fontSize = '';
    while (m.scrollHeight > m.clientHeight + 1 && size > 1.9) {{ size -= .1; m.style.fontSize = size + 'cqi'; }}
  }}
  form.addEventListener('input', render);
  render();

  // The order as lines; [label, customer's own text] pairs are shown bold in the copy dialog
  const EMAIL = 'vanylvensauna@gmail.com';
  function order() {{
    const h = hours(), amount = money(h * 300);
    return [
      t.mailHello, '',
      [t.mailGift + ': ', t.value(h) + ' (' + amount + ')'],
      [t.mailTo + ': ', val('to') || '-'],
      [t.mailFrom + ': ', val('from') || '-'],
      [t.mailMsg + ': ', val('msg') || '-'],
      [t.mailEmail + ': ', val('email') || '-'], '',
      // No validity date here: we set it ourselves when we issue the card, so an edited email cannot change it
      t.mailPay.replace('{{amount}}', amount).replace('{{ref}}', t.refWord + ' ' + (val('to') || '')), '',
      t.mailThanks,
    ];
  }}
  const plain = () => order().map((l) => (Array.isArray(l) ? l.join('') : l)).join('\r\n');

  const box = document.querySelector('.copybox');
  const pre = box.querySelector('.order');
  function showCopy() {{
    pre.replaceChildren();
    order().forEach((l, i) => {{
      if (i) pre.append('\n');
      if (Array.isArray(l)) {{ const b = document.createElement('b'); b.textContent = l[1]; pre.append(l[0], b); }}
      else pre.append(l);
    }});
    if (!box.open) box.showModal();
  }}
  box.querySelector('.close').addEventListener('click', () => box.close());
  box.addEventListener('click', (e) => {{ if (e.target === box) box.close(); }});
  box.querySelectorAll('[data-copy]').forEach((b) => b.addEventListener('click', async () => {{
    const label = b.querySelector('span'), text = label.textContent;
    try {{ await navigator.clipboard.writeText(b.dataset.copy === 'order' ? plain() : EMAIL); }}
    catch (e) {{ const r = document.createRange(); r.selectNodeContents(b.dataset.copy === 'order' ? pre : label); getSelection().removeAllRanges(); getSelection().addRange(r); return; }}
    // Keep the button the same size while it says "Copied"
    b.style.flex = '0 0 ' + b.offsetWidth + 'px';
    label.textContent = t.copied;
    setTimeout(() => {{ label.textContent = text; b.style.flex = ''; }}, 1800);
  }}));

  // The order goes to our gift card service, which stores it and answers with its number.
  // If the service cannot be reached, the buyer's email app opens with the order instead.
  const API = '{api}';
  const err = form.querySelector('.err'), sendBtn = form.querySelector('button[type="submit"]'), done = document.querySelector('.done');
  const pad = (n) => String(n).padStart(4, '0');
  const fill = (s, v) => s.replace(/\{{(\w+)\}}/g, (m, k) => v[k] ?? m);
  const escape = (s) => s.replace(/[&<>"]/g, (c) => ({{ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }}[c]));
  const fail = (msg) => {{ err.textContent = msg; err.hidden = false; form.elements.email.focus(); }};

  form.addEventListener('submit', async (e) => {{
    e.preventDefault();
    err.hidden = true;
    const email = val('email');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return fail(t.errEmail);
    const label = sendBtn.querySelector('span'), text = label.textContent;
    sendBtn.disabled = true; label.textContent = t.sending;
    try {{
      const r = await fetch(API, {{ method: 'POST', headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ hours: Number(hours()), to: val('to'), from: val('from'), msg: val('msg'), email, lang: t.lang, website: form.elements.website.value }}) }});
      if (r.status === 400) return fail(t.errEmail);
      if (!r.ok) throw new Error(r.status);
      const d = await r.json();
      const v = {{ n: pad(d.number), amount: money(d.amount), ref: t.refWord + ' ' + pad(d.number), email: escape(email) }};
      done.querySelector('h2').textContent = fill(t.doneH, v);
      done.querySelector('p').innerHTML = fill(t.doneP, v);
      out('no').textContent = t.no + ' ' + v.n;
      form.hidden = true; done.hidden = false; done.querySelector('h2').focus();
      done.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
    }} catch (e2) {{
      mailFallback();
    }} finally {{
      sendBtn.disabled = false; label.textContent = text;
    }}
  }});
  done.querySelector('.again').addEventListener('click', () => {{
    form.reset(); render(); out('no').textContent = '';
    done.hidden = true; form.hidden = false; form.elements.to.focus();
  }});

  // Fallback: the buyer's own email app with the order filled in.
  // If no email app takes over either (the page keeps focus), the order is shown to copy instead.
  function mailFallback() {{
    let left = false;
    const away = () => {{ left = true; }};
    addEventListener('blur', away, {{ once: true }});
    document.addEventListener('visibilitychange', away, {{ once: true }});
    location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(t.subject) + '&body=' + encodeURIComponent(plain());
    setTimeout(() => {{
      removeEventListener('blur', away);
      document.removeEventListener('visibilitychange', away);
      if (!left && document.visibilityState === 'visible' && document.hasFocus()) showCopy();
    }}, 1600);
  }}
{shell_js}</script>
</body>
</html>
'''

def how(items):
    cls = ['', ' p2', ' p3', '']
    return ''.join(f'<li><span class="pebble{cls[i]}" aria-hidden="true">{i+1}</span><p>{x}</p></li>' for i, x in enumerate(items))

en = dict(
  lang='en', title='Gift cards | Vanylven Sauna',
  desc='Give a few quiet hours by the fjord. Design a Vanylven Sauna gift card and order it by email.',
  alt_lang='nn', alt_name='Norsk', nav_label='Page links', nav_prices='Prices',
  h1='Give a few quiet hours', lead='A gift card is something to do, not something to keep. Fill in the card and see it take shape, then send us the order.',
  l_gift='How long?', h2='2 hours', h4='4 hours', h6='6 hours',
  l_to='To', p_to='Who is it for?', l_from='From', p_from='Your name', l_msg='A short message', optional='(optional)', p_msg='Happy birthday! Time to slow down.',
  l_email='Your email', p_email='So we can send you the card',
  send='Send the order', send_note='We keep your name, email and the card details only to issue and redeem the gift card, and delete them once the card has expired. <a href="../privacy/">Privacy</a>',
  again='Order another gift card',
  pop_h='Copy your order and email it to us', pop_p='Your email app did not open, so the order is not sent yet. Copy the text below and send it by email to <strong>vanylvensauna@gmail.com</strong>.',
  copy_order='Copy the order', copy_email='Copy email address', close='Close',
  how_h='How it works',
  how_items=how(['<strong>Send the order</strong> here on the page. You get an order number straight away.', '<strong>Pay with Vipps or bank transfer.</strong> Our Vipps number is 943550. Put the order number in the message. <a href="../pay/">Payment details</a>', '<strong>We email you the gift card</strong> once the payment is in, with its own number and valid for one year, ready to print or forward.', '<strong>To use it,</strong> the recipient books a time as usual and emails us the gift card number instead of paying.']),
  preview_label='Preview of your gift card', card_title='GIFT CARD', c_value='Value:', c_to='To:', c_from='From:', c_valid='Valid until:',
  strings=dict(subject='Gift card order', mailHello='Hi, I would like to order a gift card.', mailGift='Gift', mailTo='To', mailFrom='From', mailMsg='Message on the card', mailEmail='My email', lang='en', no='No.', sending='Sending…',
    errEmail='Please enter your email, so we can send you the gift card.',
    doneH='Thank you! Your order number is {n}.',
    doneP='Pay <strong>{amount}</strong> with Vipps to 943550 or by <a href="../pay/#abroad">bank transfer</a>, and write <strong>{ref}</strong> in the message. Once the payment is in, we email the gift card to <strong>{email}</strong>.', copied='Copied', date='{d} {m} {y}', months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
    mailPay='I will pay {amount} with Vipps or bank transfer, with the message "{ref}".', refWord='Gift card', mailThanks='Thank you!'),
)
nn = dict(
  lang='nn', title='Gåvekort | Vanylven Sauna',
  desc='Gi nokre stille timar ved fjorden. Lag eit gåvekort frå Vanylven Sauna og bestill det på e-post.',
  alt_lang='en', alt_name='English', nav_label='Lenker', nav_prices='Prisar',
  h1='Gi nokre stille timar', lead='Eit gåvekort er noko å gjere, ikkje noko å ha. Fyll ut kortet og sjå det ta form, og send oss så bestillinga.',
  l_gift='Kor lenge?', h2='2 timar', h4='4 timar', h6='6 timar',
  l_to='Til', p_to='Kven er det til?', l_from='Frå', p_from='Namnet ditt', l_msg='Ei kort helsing', optional='(valfritt)', p_msg='Gratulerer med dagen! Tid for å senke skuldrane.',
  l_email='E-posten din', p_email='Så vi kan sende deg kortet',
  send='Send bestillinga', send_note='Vi tek vare på namn, e-post og opplysningane på kortet berre for å skrive ut og løyse inn gåvekortet, og slettar dei når kortet har gått ut. <a href="../privacy/">Personvern</a>',
  again='Bestill eit gåvekort til',
  pop_h='Kopier bestillinga og send ho til oss på e-post', pop_p='E-postprogrammet ditt opna seg ikkje, så bestillinga er ikkje send enno. Kopier teksten under og send han på e-post til <strong>vanylvensauna@gmail.com</strong>.',
  copy_order='Kopier bestillinga', copy_email='Kopier e-postadressa', close='Lukk',
  how_h='Slik gjer du',
  how_items=how(['<strong>Send bestillinga</strong> her på sida. Du får eit bestillingsnummer med ein gong.', '<strong>Betal med Vipps eller bankoverføring.</strong> Vipps-nummeret vårt er 943550. Skriv bestillingsnummeret i meldinga. <a href="../pay/">Betalingsinfo</a>', '<strong>Vi sender deg gåvekortet</strong> på e-post når betalinga er komen, med eige nummer og gyldig i eitt år, klart til å skrive ut eller sende vidare.', '<strong>For å bruke det</strong> bookar mottakaren ei tid som vanleg, og sender oss nummeret på gåvekortet på e-post i staden for å betale.']),
  preview_label='Førehandsvising av gåvekortet', card_title='GÅVEKORT', c_value='Beløp:', c_to='Til:', c_from='Frå:', c_valid='Gyldig til:',
  strings=dict(subject='Bestilling av gåvekort', mailHello='Hei, eg vil gjerne bestille eit gåvekort.', mailGift='Gåve', mailTo='Til', mailFrom='Frå', mailMsg='Helsing på kortet', mailEmail='E-posten min', lang='nn', no='Nr.', sending='Sender…',
    errEmail='Skriv inn e-posten din, så vi kan sende deg gåvekortet.',
    doneH='Takk! Bestillingsnummeret ditt er {n}.',
    doneP='Betal <strong>{amount}</strong> med Vipps til 943550 eller med <a href="../../pay/#abroad">bankoverføring</a>, og skriv <strong>{ref}</strong> i meldinga. Når betalinga er komen, sender vi gåvekortet til <strong>{email}</strong>.', copied='Kopiert', date='{d}. {m} {y}', months=['januar', 'februar', 'mars', 'april', 'mai', 'juni', 'juli', 'august', 'september', 'oktober', 'november', 'desember'],
    mailPay='Eg betaler {amount} med Vipps eller bankoverføring, med meldinga «{ref}».', refWord='Gåvekort', mailThanks='Takk!'),
)

def money(n, lang):
    # NOK 1 200 in English, 1 200 kr in Nynorsk, with a non-breaking space between thousands
    g = f'{n:,}'.replace(',', ' ')
    return 'NOK ' + g if lang == 'en' else g + ' kr'


for d, path, img, home, alt_href, unit in [
    (en, 'gift/index.html', '../img/', '../', '../nn/gift/', 'hours'),
    (nn, 'nn/gift/index.html', '../../img/', '../', '../../gift/', 'timar'),
]:
    s = dict(d['strings'])
    js = json.dumps(s, ensure_ascii=False)
    js = js[:-1] + ', value: (h) => h + " ' + unit + '"}'
    money_js = 'const money = (n) => ' + ('"NOK " + group(n)' if d['lang'] == 'en' else 'group(n) + " kr"') + ';'
    d2 = {k: v for k, v in d.items() if k != 'strings'}
    d2.update(p2=money(600, d['lang']), p4=money(1200, d['lang']), p6=money(1800, d['lang']))
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8', newline='') as f:
        sh, sf = shared.parts(d['lang'], '../', img, alt_href, here='gift')
        f.write(T.format(shell_header=sh, shell_footer=sf, shell_css=shared.CSS, shell_js=shared.JS, icons=shared.icons(img), seo=shared.seo('gift/', d['lang'], d['title'], d['desc'], 'img/gift-card.png'), img=img, home=home, alt_href=alt_href, strings=js, money_js=money_js, api=shared.VOUCHER_API, **d2))
    print('wrote', path)
