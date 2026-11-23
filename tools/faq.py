# Questions and answers for the home pages: a visible section plus FAQPage data for search engines and AI answers.
# Every answer repeats what the site already says elsewhere (prices, hours, rules, booking). Keep them in step.
import html, json, re

SITE = 'https://www.vanylvensauna.no/'
EMAIL = 'vanylvensauna@gmail.com'
CALENDLY = 'https://calendly.com/vanylvensauna/sauna'
MESSENGER = 'https://www.facebook.com/profile.php?id=61570144756846'

FAQ = {
    'en': dict(
        eyebrow='Questions and answers', h='Good to know', lead='The short answers to what people ask us most.',
        items=[
            ('How much does the sauna cost?',
             'A private session costs NOK 600 for 2 hours, for the whole group of up to 8 people. Open sauna on Wednesday evenings costs NOK 100 per person.'),
            ('When is the sauna open?',
             f'Private sessions run Thursday to Sunday, 10:00 to 20:00, with the last start at 18:00. Open sauna is every Wednesday, 17:00 to 20:00. For other times, email <a href="mailto:{EMAIL}">{EMAIL}</a> or message us on <a href="{MESSENGER}" target="_blank" rel="noopener">Messenger</a>.'),
            ('How do I book?',
             f'Pick a free time in our <a href="{CALENDLY}" target="_blank" rel="noopener">booking calendar</a>, then pay with Vipps or bank transfer. Open sauna on Wednesdays needs no booking: just come.'),
            ('How do I pay?',
             'With Vipps (943550) or by bank transfer. Write the date and your name in the message so we can find your booking. <a href="{root}pay/">How to pay, step by step</a>.'),
            ('How do I get in?',
             'When your payment is in, we email you the door code the day before your visit.'),
            ('Can I swim in the sea?',
             'Yes. The sauna sits on the shore of the Vanylvsfjord in Fiskå, so you can cool off in the sea between rounds. Sauna and swimming are at your own risk.'),
            ('What should I bring?',
             'Swimwear, your own towel to sit or lie on, and plenty of water to drink. No alcohol, inside or outside.'),
            ('Can children come?',
             'Yes. Children under 16 come with an adult.'),
            ('Can I cancel?',
             'Cancel by email or Messenger at least 24 hours before your session and it costs nothing. Later cancellations cost NOK 300.'),
            ('Do you sell gift cards?',
             'Yes, for 2, 4 or 6 hours, valid for one year. <a href="{root}gift/">Design the card online</a>, pay with Vipps or bank transfer, and we send it to you. To use one, book as usual and email us the card number instead of paying.'),
            ('Where is the sauna?',
             'On the shore below Fiskå Brygge Gjestgiveri in Fiskå, Vanylven, in Møre og Romsdal, not far from Stad. <a href="{root}find/">Map and directions</a>.'),
            ('Who runs the sauna?',
             'Vanylven Sauna was built by Stad Kystbygg and is run by volunteers from Vanylven.'),
        ]),
    'nn': dict(
        eyebrow='Spørsmål og svar', h='Greitt å vite', lead='Korte svar på det folk oftast spør oss om.',
        items=[
            ('Kva kostar badstua?',
             'Ei privat økt kostar 600 kr for 2 timar, for heile gruppa på opptil 8 personar. Open badstue onsdagskveldar kostar 100 kr per person.'),
            ('Når er badstua open?',
             f'Privat badstue torsdag til søndag, 10:00 til 20:00, med siste start 18:00. Open badstue kvar onsdag, 17:00 til 20:00. Vil du kome på andre tider, send e-post til <a href="mailto:{EMAIL}">{EMAIL}</a> eller ei melding på <a href="{MESSENGER}" target="_blank" rel="noopener">Messenger</a>.'),
            ('Korleis bookar eg?',
             f'Finn ei ledig tid i <a href="{CALENDLY}" target="_blank" rel="noopener">bookingkalenderen</a> vår, og betal med Vipps eller bankoverføring. Til open badstue på onsdagar treng du ikkje booke: berre kom.'),
            ('Korleis betaler eg?',
             'Med Vipps (943550) eller bankoverføring. Skriv datoen og namnet ditt i meldinga, så finn vi bookinga di. <a href="{root}pay/">Slik betaler du, steg for steg</a>.'),
            ('Korleis kjem eg inn?',
             'Når betalinga er komen inn, sender vi deg koden til døra på e-post dagen før besøket.'),
            ('Kan eg bade i sjøen?',
             'Ja. Badstua ligg i sjøkanten ved Vanylvsfjorden på Fiskå, så du kan kjøle deg ned i sjøen mellom rundane. Badstue og bading skjer på eige ansvar.'),
            ('Kva skal eg ta med?',
             'Badetøy, eige handkle å sitje eller liggje på, og rikeleg med vatn å drikke. Ikkje alkohol, verken inne eller ute.'),
            ('Kan born vere med?',
             'Ja. Born under 16 år kjem saman med ein vaksen.'),
            ('Kan eg avbestille?',
             'Avbestill på e-post eller Messenger seinast 24 timar før økta, så kostar det ingenting. Ved seinare avbestilling er gebyret 300 kr.'),
            ('Sel de gåvekort?',
             'Ja, for 2, 4 eller 6 timar, gyldige i eitt år. <a href="{root}gift/">Lag kortet på nettsida</a>, betal med Vipps eller bankoverføring, så sender vi det til deg. Book som vanleg og send oss nummeret på gåvekortet i staden for å betale.'),
            ('Kvar ligg badstua?',
             'I sjøkanten nedanfor Fiskå Brygge Gjestgiveri på Fiskå i Vanylven, i Møre og Romsdal, ikkje langt frå Stad. <a href="{root}find/">Kart og vegbeskriving</a>.'),
            ('Kven driv badstua?',
             'Vanylven Sauna er bygd av Stad Kystbygg og blir driven av frivillige frå Vanylven.'),
        ]),
}

CSS = '''
  /* Questions and answers */
  .faq { padding: 140px 0; }
  .faq .head { max-width: 760px; margin-bottom: 48px; }
  .faq .eyebrow { display: inline-flex; gap: 8px; align-items: center; color: var(--heat-soft, var(--heat)); font-weight: 700; font-size: .9rem; }
  .faq h2 { margin-top: 14px; font-size: clamp(2.6rem, 5.4vw, 4.8rem); }
  .faq .head p { margin-top: 20px; color: var(--muted); font-size: 1.15rem; max-width: 52ch; }
  .faq .list { display: grid; grid-template-columns: 1fr 1fr; gap: 0 48px; }
  .faq details { border-top: 1px solid rgb(255 255 255 / .1); }
  .faq summary { list-style: none; cursor: pointer; display: flex; justify-content: space-between; gap: 16px; align-items: center; padding: 22px 0; font-weight: 700; font-size: 1.08rem; }
  .faq summary::-webkit-details-marker { display: none; }
  .faq summary i { flex: none; transition: transform .3s; color: var(--muted); }
  .faq details[open] summary i { transform: rotate(45deg); }
  .faq details p { margin: -6px 0 24px; color: var(--muted); max-width: 60ch; }
  .faq details a { color: var(--ink); }
  @media (max-width: 767px) { .faq { padding: 90px 0; } .faq .list { grid-template-columns: 1fr; } }
  @media (prefers-reduced-motion: reduce) { .faq summary i { transition: none; } }
'''


def section(lang, root):
    """The visible section. root: '' on the English home page, '../' on the Nynorsk one."""
    f = FAQ[lang]
    items = ''.join(
        f'''        <details>
          <summary>{q}<i class="ph ph-plus" aria-hidden="true"></i></summary>
          <p>{a.replace('{root}', root)}</p>
        </details>
''' for q, a in f['items'])
    return f'''  <section class="faq" id="faq" aria-labelledby="faq-h">
    <div class="wrap">
      <div class="head reveal">
        <span class="eyebrow"><i class="ph ph-question" aria-hidden="true"></i>{f['eyebrow']}</span>
        <h2 id="faq-h">{f['h']}</h2>
        <p>{f['lead']}</p>
      </div>
      <div class="list">
{items}      </div>
    </div>
  </section>'''


def plain(text):
    return html.unescape(re.sub(r'<[^>]+>', '', text))


def data(lang):
    """FAQPage structured data, same words as the visible section."""
    f = FAQ[lang]
    d = {
        '@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': lang,
        'about': {'@id': SITE + '#sauna'},
        'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': plain(a.replace('{root}', ''))}}
                       for q, a in f['items']],
    }
    return '<script type="application/ld+json">\n' + json.dumps(d, ensure_ascii=False, indent=2) + '\n</script>'
