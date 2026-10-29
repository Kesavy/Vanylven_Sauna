# Writes the shared header, menu and footer from shared.py into the two home pages.
# The pay and gift pages get theirs when build_pay.py / build_gift.py run.
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shared

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'

for path, lang, img, lang_href in [('index.html', 'en', 'img/', 'nn/'), ('nn/index.html', 'nn', '../img/', '../')]:
    p = os.path.join(ROOT, path)
    s = open(p, encoding='utf-8').read()
    header, footer = shared.parts(lang, '', img, lang_href)
    s, n1 = re.subn(r'<header class="nav" id="nav">.*?(?=\n\n<main)', lambda m: header, s, count=1, flags=re.S)
    s, n2 = re.subn(r'<footer>.*?</footer>', lambda m: footer, s, count=1, flags=re.S)
    assert (n1, n2) == (1, 1), (path, n1, n2)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        f.write(s)
    print('updated', path)
