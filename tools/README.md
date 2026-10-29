# Page generators

The header, menu and footer are shared by every page and live in `shared.py`.
The payment and gift card pages are generated, in English and Nynorsk, from `build_pay.py` and `build_gift.py`.

Run from the repository root:

```
python tools/apply_shell.py .
python tools/build_pay.py .
python tools/build_gift.py .
```

- Change the menu, header or footer: edit `shared.py`, then run all three.
- Change payment or gift card text: edit the `en` / `nn` dictionaries in the build script, then run it.
- Do not edit `pay/`, `gift/`, `nn/pay/` or `nn/gift/` by hand; the next build overwrites them.
- The home pages (`index.html`, `nn/index.html`) are edited by hand, except the header, the footer and the `<!-- seo -->` block in the head.
- SEO tags and the structured data (address, opening hours, prices) come from `seo()` and `place()` in `shared.py`. If hours or prices change on the page, change them there too.
- The public address is `SITE` in `shared.py` (https://www.vanylvensauna.no/). If it ever changes, change it there, run all three, then replace the old address in `sitemap.xml`, `robots.txt` and `v2/`.
