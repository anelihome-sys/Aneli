# Certificates — Aneli Interiors

Print-ready A4 certificate for the interior design practicum.

```
certificates/
├── template.html   # layout + type + seal (one source for all languages)
├── build.py        # fills the template, renders PDF + preview PNG
├── aneli-certificate-ayana-akhan-ru.html   # editable source (fonts via Google CDN)
├── aneli-certificate-ayana-akhan-en.html
└── dist/*.pdf      # print-ready, A4 portrait, fonts embedded
```

**Type:** Cormorant Garamond (display + body), Montserrat (tracked micro-labels),
Great Vibes (signature). **Palette:** warm paper `#FAF7F2`, graphite ink `#2B2724`,
bronze `#8A6E4B`.

## Issuing it to someone else

Edit the `DATA` dict in `build.py` — name, certificate number, city, year, hours —
then:

```bash
python3 build.py --html
```

PDFs land in `dist/`. Rendering uses headless Chromium; without it, open the
`.html` file in a browser and print to PDF at A4, margins **none**,
background graphics **on**.

## Printing

A4, 100% scale, no fit-to-page. On 250–300 g/m² uncoated warm white the
hairline frame and the seal hold up; avoid glossy stock.
