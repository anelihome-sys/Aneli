# Certificates — Aneli Interiors

Print-ready A4 certificate for the interior design practicum.

```
certificates/
├── template.html   # layout + type + seal (one source for all languages)
├── build.py        # fills the template, renders PDF + preview PNG
├── seal_bumps.svg.frag / grain.png / grain.b64   # seal scallops + paper texture
├── aneli-certificate-ayana-akhan-ru.html   # editable source (fonts via Google CDN)
├── aneli-certificate-ayana-akhan-en.html
└── dist/*.pdf      # print-ready, A4 portrait, fonts embedded
```

**Type:** Playfair Display (title, roles), Montserrat (tracked micro-labels),
Pinyon Script (recipient name), Allura (signature), Cormorant Garamond (duration line).
**Palette:** cream paper `#FCFAF4`, near-black ink `#17171A`, bronze gradient frame
`#8E5A1B → #CE9C55`.

## Issuing it to someone else

Edit the `DATA` dict in `build.py` — name, certificate number, city, year, duration,
signature roles — then:

```bash
python3 build.py --html
```

PDFs land in `dist/`. Rendering uses headless Chromium; without it, open the
`.html` file in a browser and print to PDF at A4, margins **none**,
background graphics **on**.

## Printing

A4, 100% scale, no fit-to-page. On 250–300 g/m² uncoated warm white the
hairline frame and the seal hold up; avoid glossy stock.
