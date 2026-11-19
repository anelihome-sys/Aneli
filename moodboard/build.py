"""Furniture moodboard on a clean white sheet.
Add items to ITEMS (cut-out PNG in items/) and rerun:  python3 build.py
All items are drawn at one common scale (SCALE px per cm of `span_cm`)
and stand on one baseline, so relative sizes read honestly.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).parent
W, H = 3508, 2480            # A4 landscape @300dpi (A3 @150dpi)
INK = (34, 33, 31)
MUTED = (140, 136, 130)
LINE = (214, 210, 204)
F = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
font = lambda w, s: ImageFont.truetype(F.format(w), s)

SCALE = 9.6        # px per cm
BASELINE = 1430    # y where every item stands
GAP = 420          # horizontal gap between items
MARGIN = 180

# span_cm = real-world size of the cut-out's full width (usually the item's length)
ITEMS = [
    dict(no="01", file="01-coffee-table.png", span_cm=120,
         name="Журнальный столик",
         spec=[("Длина", "120 см"), ("Ширина", "60 см"), ("Высота", "40 см"), ("Вес", "9 кг")],
         notes=["Столешница — чёрный шпон, текстура ясеня", "Каркас — металл, чёрный матовый",
                "Форма — овал / стадион, X-царга"]),
    dict(no="02", file="02-desk.png", span_cm=120, tag="ADJUSTABLE",
         name="Рабочий стол",
         spec=[("Длина", "120 см"), ("Ширина", "60 см"), ("Высота", "до 116 см"), ("Вес", "21 кг")],
         notes=["Регулируемая высота — сидя / стоя", "Столешница — дерево, тёмный тон",
                "Опоры — металл, чёрный; пульт под столешницей"]),
]


def shadow(w, h):
    """Soft contact shadow under the object footprint."""
    sh = Image.new("L", (w, h), 0)
    ImageDraw.Draw(sh).ellipse([w * 0.06, h * 0.91, w * 0.94, h * 1.0], fill=38)
    return sh.filter(ImageFilter.GaussianBlur(h * 0.03))


def caption(d, it, x, y):
    d.text((x, y), it["no"], font=font("Light", 40), fill=MUTED)
    if tag := it.get("tag"):
        f = font("Medium", 26)
        tw = d.textlength(tag, font=f)
        d.rounded_rectangle([x + 90, y + 2, x + 90 + tw + 44, y + 50], radius=24, outline=INK, width=2)
        d.text((x + 112, y + 12), tag, font=f, fill=INK)
    d.text((x, y + 66), it["name"], font=font("Regular", 58), fill=INK)
    y += 170
    d.line([x, y, x + 780, y], fill=LINE, width=3)
    y += 36
    for k, v in it["spec"]:
        d.text((x, y + 6), k.upper(), font=font("Regular", 28), fill=MUTED)
        d.text((x + 300, y), v, font=font("Light", 40), fill=INK)
        y += 62
    y += 14
    d.line([x, y, x + 780, y], fill=LINE, width=3)
    y += 36
    for n in it.get("notes", []):
        d.text((x, y), n, font=font("Light", 30), fill=MUTED)
        y += 48


def build():
    sheet = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(sheet)
    d.text((MARGIN, 150), "MOODBOARD", font=font("Light", 40), fill=INK)
    d.text((MARGIN, 210), "Подбор мебели", font=font("Light", 34), fill=MUTED)
    d.line([MARGIN, 300, W - MARGIN, 300], fill=LINE, width=3)
    d.line([MARGIN, H - 170, W - MARGIN, H - 170], fill=LINE, width=3)
    d.text((MARGIN, H - 130), f"{len(ITEMS):02d} позиц.  ·  предметы показаны в едином масштабе",
           font=font("Light", 30), fill=MUTED)

    imgs = []
    for it in ITEMS:
        img = Image.open(HERE / "items" / it["file"]).convert("RGBA")
        w = round(it["span_cm"] * SCALE); h = round(img.height * w / img.width)
        imgs.append(img.resize((w, h), Image.LANCZOS))
    col_w = [max(i.width, 780) for i in imgs]
    x = (W - sum(col_w) - GAP * (len(imgs) - 1)) // 2
    for it, img, cw in zip(ITEMS, imgs, col_w):
        ix, iy = x + (cw - img.width) // 2, BASELINE - img.height
        sheet.paste((120, 116, 110), (ix, iy), shadow(img.width, img.height))
        sheet.paste(img, (ix, iy), img)
        caption(d, it, x, BASELINE + 110)
        x += cw + GAP

    sheet.save(HERE / "moodboard.png", dpi=(300, 300))
    sheet.save(HERE / "moodboard.pdf", resolution=300)


if __name__ == "__main__":
    build()
