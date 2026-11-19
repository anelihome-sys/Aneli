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

SCALE = 8.4        # px per cm
BASELINE = 1430    # y where every item stands
GAP = 360          # default horizontal gap between items (override per item: gap)
MARGIN = 180

# span_cm = real-world size of the cut-out's full width (usually the item's length)
# or height_cm = real-world height of the cut-out (when width is unknown / perspective)
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
    dict(no="03", file="03-office-chair.png", height_cm=125, gap=110, cap_w=560,
         name="Офисное кресло",
         spec=[("Размеры", "уточнить")],
         notes=["Спинка — сетка, чёрная", "Подголовник, 3D-подлокотники",
                "Крестовина — хром, на колёсах"]),
]


def shadow(w, h):
    """Soft contact shadow under the object footprint."""
    sh = Image.new("L", (w, h), 0)
    ImageDraw.Draw(sh).ellipse([w * 0.06, h * 0.91, w * 0.94, h * 1.0], fill=38)
    return sh.filter(ImageFilter.GaussianBlur(h * 0.03))


def caption(d, it, x, y):
    cw = it.get("cap_w", 780)
    d.text((x, y), it["no"], font=font("Light", 40), fill=MUTED)
    if tag := it.get("tag"):
        f = font("Medium", 26)
        tw = d.textlength(tag, font=f)
        d.rounded_rectangle([x + 90, y + 2, x + 90 + tw + 44, y + 50], radius=24, outline=INK, width=2)
        d.text((x + 112, y + 12), tag, font=f, fill=INK)
    d.text((x, y + 66), it["name"], font=font("Regular", 58), fill=INK)
    y += 170
    d.line([x, y, x + cw, y], fill=LINE, width=3)
    y += 36
    for k, v in it["spec"]:
        d.text((x, y + 6), k.upper(), font=font("Regular", 28), fill=MUTED)
        d.text((x + 300, y), v, font=font("Light", 40), fill=INK)
        y += 62
    y += 14
    d.line([x, y, x + cw, y], fill=LINE, width=3)
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
        if "height_cm" in it:
            h = round(it["height_cm"] * SCALE); w = round(img.width * h / img.height)
        else:
            w = round(it["span_cm"] * SCALE); h = round(img.height * w / img.width)
        imgs.append(img.resize((w, h), Image.LANCZOS))
    col_w = [max(i.width, it.get("cap_w", 780)) for it, i in zip(ITEMS, imgs)]
    gaps = [it.get("gap", GAP) for it in ITEMS[1:]]
    x = (W - sum(col_w) - sum(gaps)) // 2
    for n, (it, img, cw) in enumerate(zip(ITEMS, imgs, col_w)):
        if n:
            x += it.get("gap", GAP)
        ix, iy = x + (cw - img.width) // 2, BASELINE - img.height
        sheet.paste((120, 116, 110), (ix, iy), shadow(img.width, img.height))
        sheet.paste(img, (ix, iy), img)
        caption(d, it, x, BASELINE + 110)
        x += cw

    sheet.save(HERE / "moodboard.png", dpi=(300, 300))
    sheet.save(HERE / "moodboard.pdf", resolution=300)


if __name__ == "__main__":
    build()
