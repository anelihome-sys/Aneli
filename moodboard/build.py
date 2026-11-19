"""Furniture moodboard on a clean white sheet.
Add items to ITEMS (cut-out PNG in items/) and rerun:  python3 build.py
Furniture is drawn at one common scale (SCALE px per cm) on one baseline,
so relative sizes read honestly. The rug sits in its own band at the bottom.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).parent
W, H = 3508, 2480            # A4 landscape @300dpi (A3 @150dpi)
INK = (34, 33, 31)
MUTED = (140, 136, 130)
LINE = (214, 210, 204)
F = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
font = lambda w, s: ImageFont.truetype(F.format(w), s)

MARGIN = 180
SCALE = 6.9        # px per cm (furniture)
BASELINE = 1215    # y where every furniture item stands
GAP = 380          # default horizontal gap between items (override per item: gap)
CAP_W = 700

# span_cm = real-world width of the cut-out, or height_cm = its real-world height
ITEMS = [
    dict(no="01", file="01-coffee-table.png", span_cm=120,
         name="Журнальный столик",
         spec=[("Д × Ш × В", "120 × 60 × 40 см"), ("Вес", "9 кг")],
         notes=["Столешница — чёрный шпон, текстура ясеня", "Каркас — металл, чёрный матовый"]),
    dict(no="02", file="02-desk.png", span_cm=120, tag="ADJUSTABLE",
         name="Рабочий стол",
         spec=[("Д × Ш × В", "120 × 60 × до 116 см"), ("Вес", "21 кг")],
         notes=["Регулируемая высота — сидя / стоя", "Дерево / металл, пульт под столешницей"]),
    dict(no="03", file="03-office-chair.png", height_cm=125, gap=110, cap_w=520,
         name="Офисное кресло",
         spec=[("Размеры", "уточнить")],
         notes=["Сетка, подголовник, 3D-подлокотники", "Крестовина — хром, на колёсах"]),
]

RUG = dict(no="04", file="04-rug.png", texture="04-rug-texture.jpg",
           name="Ковёр",
           spec=[("Д × Ш", "400 × 300 см"), ("Высота", "1 см"), ("Вес", "59 кг")],
           notes=["Длинный ворс (шегги), молочный / айвори",
                  "Основа — тканая, серая; окантовка «ёлочкой»"])


def shadow(w, h):
    """Soft contact shadow under the object footprint."""
    sh = Image.new("L", (w, h), 0)
    ImageDraw.Draw(sh).ellipse([w * 0.06, h * 0.91, w * 0.94, h * 1.0], fill=38)
    return sh.filter(ImageFilter.GaussianBlur(h * 0.03))


def caption(d, it, x, y, cw=CAP_W):
    d.text((x, y), it["no"], font=font("Light", 36), fill=MUTED)
    if tag := it.get("tag"):
        f = font("Medium", 24)
        tw = d.textlength(tag, font=f)
        d.rounded_rectangle([x + 82, y, x + 82 + tw + 40, y + 46], radius=23, outline=INK, width=2)
        d.text((x + 102, y + 11), tag, font=f, fill=INK)
    d.text((x, y + 58), it["name"], font=font("Regular", 52), fill=INK)
    y += 150
    d.line([x, y, x + cw, y], fill=LINE, width=3)
    y += 30
    for k, v in it["spec"]:
        d.text((x, y + 6), k.upper(), font=font("Regular", 26), fill=MUTED)
        d.text((x + 230, y), v, font=font("Light", 38), fill=INK)
        y += 58
    y += 10
    d.line([x, y, x + cw, y], fill=LINE, width=3)
    y += 30
    for n in it.get("notes", []):
        d.text((x, y), n, font=font("Light", 28), fill=MUTED)
        y += 44


def furniture(sheet, d):
    imgs = []
    for it in ITEMS:
        img = Image.open(HERE / "items" / it["file"]).convert("RGBA")
        if "height_cm" in it:
            h = round(it["height_cm"] * SCALE); w = round(img.width * h / img.height)
        else:
            w = round(it["span_cm"] * SCALE); h = round(img.height * w / img.width)
        imgs.append(img.resize((w, h), Image.LANCZOS))
    col_w = [max(i.width, it.get("cap_w", CAP_W)) for it, i in zip(ITEMS, imgs)]
    gaps = [it.get("gap", GAP) for it in ITEMS[1:]]
    x = (W - sum(col_w) - sum(gaps)) // 2
    for n, (it, img, cw) in enumerate(zip(ITEMS, imgs, col_w)):
        if n:
            x += it.get("gap", GAP)
        ix, iy = x + (cw - img.width) // 2, BASELINE - img.height
        sheet.paste((120, 116, 110), (ix, iy), shadow(img.width, img.height))
        sheet.paste(img, (ix, iy), img)
        caption(d, it, x, BASELINE + 70, it.get("cap_w", CAP_W))
        x += cw


def rug_band(sheet, d, top, bottom):
    """Rug: top-down product view + close-up texture swatch + specs."""
    h = bottom - top
    rug = Image.open(HERE / "items" / RUG["file"]).convert("RGBA")
    rw = round(rug.width * h / rug.height)
    rug = rug.resize((rw, h), Image.LANCZOS)
    x = MARGIN + 80
    # soft lift shadow so an ivory rug still reads on white
    pad = 60
    sh = Image.new("L", (rw + 2 * pad, h + 2 * pad), 0)
    sh.paste(rug.split()[3].point(lambda v: v * 60 // 255), (pad, pad + 14))
    sh = sh.filter(ImageFilter.GaussianBlur(26))
    sheet.paste((110, 104, 96), (x - pad, top - pad), sh)
    sheet.paste(rug, (x, top), rug)
    # texture swatch
    tx = x + rw + 70
    tw = round(h * 1.5)
    tex = ImageOps.fit(Image.open(HERE / "items" / RUG["texture"]).convert("RGB"), (tw, h),
                       Image.LANCZOS, centering=(0.5, 0.62))
    sheet.paste(tex, (tx, top))
    d.text((tx, bottom + 22), "ТЕКСТУРА ВОРСА И ОСНОВА", font=font("Regular", 24), fill=MUTED)
    caption(d, RUG, tx + tw + 140, top + 10, 760)


def build():
    sheet = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(sheet)
    d.text((MARGIN, 150), "MOODBOARD", font=font("Light", 40), fill=INK)
    d.text((MARGIN, 210), "Подбор мебели", font=font("Light", 34), fill=MUTED)
    d.line([MARGIN, 300, W - MARGIN, 300], fill=LINE, width=3)

    furniture(sheet, d)

    d.line([MARGIN, 1740, W - MARGIN, 1740], fill=LINE, width=3)
    rug_band(sheet, d, 1820, 2250)

    d.line([MARGIN, H - 150, W - MARGIN, H - 150], fill=LINE, width=3)
    d.text((MARGIN, H - 112), f"{len(ITEMS) + 1:02d} позиц.  ·  мебель показана в едином масштабе",
           font=font("Light", 28), fill=MUTED)

    sheet.save(HERE / "moodboard.png", dpi=(300, 300))
    sheet.save(HERE / "moodboard.pdf", resolution=300)


if __name__ == "__main__":
    build()
