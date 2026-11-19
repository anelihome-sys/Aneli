"""Furniture moodboard on a clean white sheet.
Add items to ITEMS (cut-out PNG in items/, position, size) and rerun:  python3 build.py
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

# x, y = top-left of image (px); w = image width (px); caption: "right" | "below"
ITEMS = [
    dict(no="01", file="01-coffee-table.png", x=260, y=640, w=1750, caption="right",
         name="Журнальный столик",
         spec=[("Длина", "120 см"), ("Ширина", "60 см"), ("Высота", "40 см"), ("Вес", "9 кг")],
         notes=["Столешница — чёрный шпон, текстура ясеня", "Каркас — металл, чёрный матовый",
                "Форма — овал / стадион, X-царга"]),
]


def shadow(img, w, h):
    """Soft contact shadow under the object footprint."""
    sh = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(sh)
    d.ellipse([w * 0.06, h * 0.90, w * 0.94, h * 1.0], fill=40)
    return sh.filter(ImageFilter.GaussianBlur(h * 0.03))


def caption(d, it, x, y):
    d.text((x, y), it["no"], font=font("Light", 44), fill=MUTED)
    d.text((x, y + 70), it["name"], font=font("Regular", 64), fill=INK)
    y += 190
    d.line([x, y, x + 620, y], fill=LINE, width=3)
    y += 45
    for k, v in it["spec"]:
        d.text((x, y), k.upper(), font=font("Regular", 30), fill=MUTED)
        d.text((x + 320, y - 6), v, font=font("Light", 42), fill=INK)
        y += 72
    y += 20
    d.line([x, y, x + 620, y], fill=LINE, width=3)
    y += 45
    for n in it.get("notes", []):
        d.text((x, y), n, font=font("Light", 32), fill=MUTED)
        y += 52


def build():
    sheet = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(sheet)
    # header
    d.text((180, 150), "MOODBOARD", font=font("Light", 40), fill=INK, spacing=0)
    d.text((180, 210), "Подбор мебели", font=font("Light", 34), fill=MUTED)
    d.line([180, 300, W - 180, 300], fill=LINE, width=3)
    d.line([180, H - 200, W - 180, H - 200], fill=LINE, width=3)
    d.text((180, H - 160), f"{len(ITEMS):02d} позиц.", font=font("Light", 30), fill=MUTED)

    for it in ITEMS:
        img = Image.open(HERE / "items" / it["file"]).convert("RGBA")
        w = it["w"]; h = round(img.height * w / img.width)
        img = img.resize((w, h), Image.LANCZOS)
        sheet.paste((120, 116, 110), (it["x"], it["y"]), shadow(img, w, h))
        sheet.paste(img, (it["x"], it["y"]), img)
        if it["caption"] == "right":
            caption(d, it, it["x"] + w + 160, it["y"] + h // 2 - 330)
        else:
            caption(d, it, it["x"], it["y"] + h + 80)

    sheet.save(HERE / "moodboard.png", dpi=(300, 300))
    sheet.save(HERE / "moodboard.pdf", resolution=300)


if __name__ == "__main__":
    build()
