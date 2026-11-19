"""Editorial moodboard on light beige — English, dark-brown type.
Run:  python3 build_beige.py   ->  moodboard-beige.png / .pdf
Furniture shares one scale (S px per cm); the rug is laid as a floor plane.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = Path(__file__).parent
IT = HERE / "items"
W, H = 3508, 2480
BG = (238, 230, 218)          # light warm beige
BROWN = (74, 52, 38)          # dark brown ink
SOFT = (128, 104, 86)         # secondary brown
HAIR = (196, 182, 164)        # hairlines
S = 5.0                       # px per cm

INTER = "/usr/share/fonts/opentype/inter/Inter-{}.otf"
def sans(w, s): return ImageFont.truetype(INTER.format(w), s)
def serif(s, w=b"Light", italic=False):
    f = ImageFont.truetype(str(HERE / "fonts" / ("CormorantGaramond-Italic.ttf" if italic else "CormorantGaramond.ttf")), s)
    f.set_variation_by_name(w)
    return f


def tracked(d, xy, text, f, fill, track=0.12):
    """Letter-spaced text; returns end x."""
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + f.size * track
    return x


def load(name, w=None, h=None):
    im = Image.open(IT / name).convert("RGBA")
    if w: h = round(im.height * w / im.width)
    else: w = round(im.width * h / im.height)
    return im.resize((w, h), Image.LANCZOS)


def place(sheet, im, x, bottom, shadow=0.9):
    """Paste cut-out standing on `bottom`, with a soft contact shadow."""
    y = bottom - im.height
    if shadow:
        p = 120
        sh = Image.new("L", (im.width + 2 * p, im.height + 2 * p), 0)
        ImageDraw.Draw(sh).ellipse([p + im.width * .05, p + im.height * .93,
                                    p + im.width * .95, p + im.height * 1.01], fill=int(70 * shadow))
        sheet.paste((92, 70, 52), (x - p, y - p), sh.filter(ImageFilter.GaussianBlur(im.height * .025)))
    sheet.paste(im, (x, y), im)
    return x, y


def perspective_coeffs(dst, src):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def rug_floor(sheet, quad):
    rug = Image.open(IT / "04-rug.png").convert("RGBA")
    w, h = rug.size
    co = perspective_coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)])
    plane = rug.transform(sheet.size, Image.PERSPECTIVE, co, Image.BICUBIC)
    a = plane.split()[3]
    sh = a.point(lambda v: v * 55 // 255).filter(ImageFilter.GaussianBlur(18))
    sheet.paste((92, 70, 52), (0, 10), sh)
    sheet.paste(plane, (0, 0), plane)


def swatch(sheet, d, src, box, cx, cy, r, label):
    im = Image.open(IT / src).convert("RGB")
    if box: im = im.crop(box)
    im = ImageOps.fit(im, (2 * r, 2 * r), Image.LANCZOS)
    m = Image.new("L", (8 * r, 8 * r), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 8 * r - 1, 8 * r - 1], fill=255)
    m = m.resize((2 * r, 2 * r), Image.LANCZOS)
    sh = Image.new("L", (2 * r + 80, 2 * r + 80), 0)
    sh.paste(m.point(lambda v: v * 60 // 255), (40, 52))
    sheet.paste((92, 70, 52), (cx - r - 40, cy - r - 40), sh.filter(ImageFilter.GaussianBlur(16)))
    sheet.paste(im, (cx - r, cy - r), m)
    f = sans("Regular", 22)
    tw = sum(d.textlength(c, font=f) + 22 * .18 for c in label)
    tracked(d, (cx - tw / 2, cy + r + 34), label, f, SOFT, .18)


def marker(d, x, y, n):
    d.ellipse([x - 26, y - 26, x + 26, y + 26], outline=BROWN, width=2)
    f = sans("Regular", 22)
    tw = d.textlength(n, font=f)
    d.text((x - tw / 2, y - 14), n, font=f, fill=BROWN)


LEGEND = [
    ("01", "SOFA", ["212 × 95 × 90 cm", "64 kg"], ["Leather, dark chocolate", "Piped seams · black metal legs"]),
    ("02", "COFFEE TABLE", ["120 × 60 × 40 cm", "9 kg"], ["Black ash veneer top", "Matte black steel frame"]),
    ("03", "SHAG RUG", ["400 × 300 × 1 cm", "59 kg"], ["Long pile, ivory", "Woven grey backing"]),
    ("04", "ADJUSTABLE DESK", ["120 × 60 × up to 116 cm", "21 kg"], ["Height adjustable · sit / stand", "Wood top · black steel frame"]),
    ("05", "OFFICE CHAIR", ["Dimensions TBC", ""], ["Mesh back · adjustable headrest", "3D armrests · chrome base"]),
]


def legend(d, top):
    x0, x1 = 200, W - 200
    col = (x1 - x0) / len(LEGEND)
    d.line([x0, top, x1, top], fill=HAIR, width=2)
    for i, (n, name, dims, notes) in enumerate(LEGEND):
        x = round(x0 + i * col)
        y = top + 48
        d.text((x, y + 6), n, font=sans("Light", 30), fill=SOFT)
        tracked(d, (x + 70, y + 8), name, sans("Medium", 25), BROWN, .2)
        y += 78
        for t in dims:
            if t: d.text((x, y), t, font=sans("Light", 29), fill=BROWN)
            y += 42
        y += 12
        for t in notes:
            d.text((x, y), t, font=sans("Light", 24), fill=SOFT)
            y += 36


def build():
    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)

    # ---- header
    d.text((200, 120), "Living & Workspace", font=serif(118, b"Light"), fill=BROWN)
    tracked(d, (206, 285), "FURNITURE SELECTION  —  MOODBOARD", sans("Regular", 24), SOFT, .28)
    f = sans("Regular", 24); txt = "ALL DIMENSIONS L × W × H"
    tw = sum(d.textlength(c, font=f) + 24 * .28 for c in txt)
    tracked(d, (W - 200 - tw, 285), txt, f, SOFT, .28)

    # ---- living group: rug floor, sofa, coffee table
    rug_floor(sheet, [(520, 1420), (2060, 1420), (2300, 1850), (260, 1850)])
    sofa = load("05-sofa.png", w=round(212 * S))
    sx, sy = place(sheet, sofa, 640, 1560)
    table = load("01-coffee-table.png", w=round(120 * S))
    tx, ty = place(sheet, table, 1280, 1790)

    # ---- workspace: desk + chair
    desk = load("02-desk.png", w=round(120 * S))
    dx, dy = place(sheet, desk, 2640, 1730)
    chair = load("03-office-chair.png", h=round(125 * S))
    cx, cy = place(sheet, chair, 2400, 1850)

    # ---- material swatches
    swatch(sheet, d, "05-sofa-texture.jpg", (230, 40, 690, 500), 2330, 760, 165, "LEATHER")
    swatch(sheet, d, "01-coffee-table-detail.jpg", (230, 110, 560, 380), 2730, 760, 165, "BLACK ASH")
    swatch(sheet, d, "04-rug-texture.jpg", (0, 0, 380, 380), 3130, 760, 165, "SHAG PILE")

    # ---- palette
    tracked(d, (200, 470), "PALETTE", sans("Regular", 22), SOFT, .28)
    pal = [((60, 42, 34), "CHOCOLATE"), ((30, 29, 28), "BLACK"), ((236, 230, 220), "IVORY"),
           ((196, 176, 150), "SAND"), ((168, 168, 166), "CHROME")]
    for i, (c, n) in enumerate(pal):
        x = 200 + i * 190
        d.rectangle([x, 530, x + 150, 680], fill=c, outline=HAIR, width=1)
        tracked(d, (x, 702), n, sans("Regular", 18), SOFT, .2)

    # ---- number markers
    marker(d, sx + 40, sy - 30, "01")
    marker(d, tx + table.width - 30, ty + 170, "02")
    marker(d, 300, 1730, "03")
    marker(d, dx + desk.width - 10, dy + 30, "04")
    marker(d, cx + 30, cy + 60, "05")

    legend(d, 2000)
    sheet.save(HERE / "moodboard-beige.png", dpi=(300, 300))
    sheet.save(HERE / "moodboard-beige.pdf", resolution=300)


if __name__ == "__main__":
    build()
