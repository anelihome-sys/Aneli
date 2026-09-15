# Certificates — Aneli Interiors

Print-ready A4 landscape certificate for the interior design practicum.

```
certificates/
├── template.html   # layout + type + seal (one source for all languages)
├── build.py        # fills the template, renders PDF + preview PNG
├── seal_bumps.svg.frag   # generated seal scallops
├── aneli-certificate-ayana-akhan-ru.html   # editable source (fonts via Google CDN)
├── aneli-certificate-ayana-akhan-en.html
└── dist/           # print-ready PDFs (+ optional 600 dpi PNGs)
```

**Type:** Playfair Display (title, roles), Montserrat (tracked micro-labels),
Pinyon Script (recipient name), Marck Script (signature).
**Palette:** cream paper `#FCFAF4`, near-black ink `#17171A`, bronze gradient frame
`#8E5A1B → #CE9C55`.

## Issuing it to someone else

Edit the `DATA` dict in `build.py` — recipient, copy line, city, year, signatory — then:

```bash
python3 build.py --html        # PDFs + editable HTML
python3 build.py --png         # also 600 dpi PNGs (7019 × 4963 px)
```

PDFs land in `dist/`. Rendering uses headless Chromium; without it, open the
`.html` file in a browser and print to PDF at A4 landscape, margins **none**,
background graphics **on**.

## Output quality

The PDF is **100% vector** — type, frame and seal are all curves, with the fonts
subset and embedded. It stays sharp at any size and on any RIP; there is no
raster layer and no paper-texture overlay (texture should come from the stock,
not from the file). `--png` adds a 600 dpi flattened export, tagged with real
`pHYs` metadata so print software opens it at 297 × 210 mm — only for shops that
insist on an image.

## Printing

A4 landscape, 100% scale, no fit-to-page. On 250–300 g/m² uncoated warm white the
hairline frame and the seal hold up; avoid glossy stock.
