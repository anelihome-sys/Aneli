"""Sunlit version of the beige moodboard: warm light, window shafts, palm-frond
shadows, long cast shadows, brand mark.   python3 build_sunlit.py
"""
import math
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
from build_beige import (HERE, W, H, S, BROWN, SOFT, HAIR, sans, serif, tracked, load,
                         perspective_coeffs, swatch, marker, legend, IT)

BG = (241, 229, 211)
SUN = (255, 238, 205)
SHADE = (118, 88, 60)


# ---------------------------------------------------------------- light
def sunlit_background():
    """Warm daylight: glow from upper left, soft window shafts, fall-off to lower right."""
    import numpy as np
    sc = 4
    h, w = H // sc, W // sc
    y, x = np.mgrid[0:h, 0:w].astype(float)
    xn, yn = x / w, y / h
    glow = np.exp(-(((xn + .05) / .75) ** 2 + ((yn + .1) / .7) ** 2))          # sun from upper left
    u = (x * math.cos(math.radians(-58)) + y * math.sin(math.radians(-58))) / w  # shaft direction
    pane = (np.sin(u * 2 * math.pi * 3.2) > -0.35).astype(float)               # panes + mullions
    shaft_zone = np.clip(1.2 - (xn * .9 + yn * .6), 0, 1)                     # shafts fade out
    light = 0.93 + 0.10 * glow + 0.055 * pane * shaft_zone - 0.05 * np.clip(xn + yn - 1, 0, 1)
    base = np.array(BG, float)
    warm = np.array([1.0, 0.985, 0.95])
    img = np.clip(base * light[..., None] * (1 + (warm - 1) * glow[..., None]), 0, 255).astype("uint8")
    im = Image.fromarray(img).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(28))
    return im


def palm_frond(mask, base, angle, length, leaf=210):
    d = ImageDraw.Draw(mask)
    pts = []
    for i in range(61):
        t = i / 60
        a = math.radians(angle + 28 * t)            # gentle arc
        pts.append((base[0] + math.cos(a) * length * t, base[1] + math.sin(a) * length * t))
    d.line(pts, fill=255, width=14)
    for i in range(4, 58, 2):
        t = i / 60
        (x, y), (x2, y2) = pts[i], pts[i + 1]
        a = math.atan2(y2 - y, x2 - x)
        L = leaf * math.sin(math.pi * min(1, t * 1.15)) + 40
        for side in (-1, 1):
            b = a + side * math.radians(52)
            tip = (x + math.cos(b) * L, y + math.sin(b) * L)
            n = (math.cos(b + math.pi / 2) * 9, math.sin(b + math.pi / 2) * 9)
            d.polygon([(x - n[0], y - n[1]), (tip[0], tip[1]), (x + n[0], y + n[1])], fill=255)


def palm_shadows(sheet):
    m = Image.new("L", (W, H), 0)
    palm_frond(m, (W + 120, -80), 150, 1500)
    palm_frond(m, (W + 60, 260), 175, 1150, leaf=170)
    palm_frond(m, (W - 380, -160), 112, 900, leaf=150)
    m = m.filter(ImageFilter.GaussianBlur(8)).point(lambda p: p * 58 // 255)
    sheet.paste(SHADE, (0, 0), m)


# ---------------------------------------------------------------- objects
def sun_grade(im, warmth=1.0):
    """Warm, slightly richer colour with light falling from the left."""
    rgb, a = im.convert("RGB"), im.split()[3]
    rgb = ImageEnhance.Color(rgb).enhance(1.18)
    rgb = ImageEnhance.Brightness(rgb).enhance(1.05)
    r, g, b = rgb.split()
    r = r.point(lambda v: min(255, int(v * (1 + .05 * warmth) + 4)))
    b = b.point(lambda v: int(v * (1 - .08 * warmth)))
    rgb = Image.merge("RGB", (r, g, b))
    # left-to-right light gradient
    grad = Image.linear_gradient("L").rotate(90).resize(im.size)        # 255 left -> 0 right
    hi = ImageEnhance.Brightness(rgb).enhance(1.16)
    lo = ImageEnhance.Brightness(rgb).enhance(0.92)
    rgb = Image.composite(hi, lo, grad)
    out = rgb.convert("RGBA"); out.putalpha(a)
    return out


def cast_shadow(sheet, im, x, bottom, k=0.32, shift=0.55, opacity=85):
    """Long sun shadow thrown back-right from the object's footprint."""
    w, h = im.size
    hs = max(1, int(h * k)); s = int(h * shift)
    a = im.split()[3]
    sh = a.transform((w + s, hs), Image.AFFINE, (1, s / hs, -s, 0, 1 / k, 0), Image.BILINEAR)
    fade = Image.linear_gradient("L").resize((w + s, hs))               # darker near base
    sh = Image.composite(sh, Image.new("L", sh.size, 0), fade)
    sh = sh.point(lambda p: p * opacity // 255).filter(ImageFilter.GaussianBlur(10))
    sheet.paste(SHADE, (x, bottom - hs), sh)


def place_sun(sheet, im, x, bottom):
    cast_shadow(sheet, im, x, bottom)
    y = bottom - im.height
    p = 120
    c = Image.new("L", (im.width + 2 * p, im.height + 2 * p), 0)
    ImageDraw.Draw(c).ellipse([p + im.width * .05, p + im.height * .93,
                               p + im.width * .95, p + im.height * 1.01], fill=80)
    sheet.paste((80, 58, 40), (x - p, y - p), c.filter(ImageFilter.GaussianBlur(im.height * .022)))
    sheet.paste(im, (x, y), im)
    return x, y


def rug_floor_sun(sheet, quad):
    rug = sun_grade(Image.open(IT / "04-rug.png").convert("RGBA"), warmth=0.6)
    w, h = rug.size
    co = perspective_coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)])
    plane = rug.transform(sheet.size, Image.PERSPECTIVE, co, Image.BICUBIC)
    a = plane.split()[3]
    sheet.paste(SHADE, (0, 12), a.point(lambda v: v * 50 // 255).filter(ImageFilter.GaussianBlur(18)))
    sheet.paste(plane, (0, 0), plane)


# ---------------------------------------------------------------- swatches
def swatch_sun(sheet, d, src, box, cx, cy, r, label, gloss=1.0):
    from PIL import ImageOps
    im = Image.open(IT / src).convert("RGB")
    if box: im = im.crop(box)
    im = ImageOps.fit(im, (2 * r, 2 * r), Image.LANCZOS).convert("RGBA")
    im = ImageEnhance.Contrast(ImageEnhance.Color(im.convert("RGB")).enhance(1.08)).enhance(1.15).convert("RGBA")
    # sun glint: soft hotspot upper-left + faint diagonal window streak
    g = Image.new("L", im.size, 0)
    gd = ImageDraw.Draw(g)
    gd.ellipse([r * .28, r * .22, r * .98, r * .78], fill=int(105 * gloss))
    g = g.filter(ImageFilter.GaussianBlur(r * .2))
    st = Image.new("L", im.size, 0)
    ImageDraw.Draw(st).polygon([(r * .55, 0), (r * .95, 0), (r * .15, 2 * r), (-r * .25, 2 * r)],
                               fill=int(38 * gloss))
    g = Image.composite(Image.new("L", im.size, 255), g, st.filter(ImageFilter.GaussianBlur(r * .12))) \
        if False else Image.fromarray(__import__("numpy").clip(
            __import__("numpy").array(g, int) + __import__("numpy").array(
                st.filter(ImageFilter.GaussianBlur(r * .12)), int), 0, 255).astype("uint8"))
    im.paste((255, 247, 228), (0, 0), g)
    # circle mask + shadow
    m = Image.new("L", (8 * r, 8 * r), 0)
    ImageDraw.Draw(m).ellipse([0, 0, 8 * r - 1, 8 * r - 1], fill=255)
    m = m.resize((2 * r, 2 * r), Image.LANCZOS)
    sh = Image.new("L", (2 * r + 160, 2 * r + 160), 0)
    sh.paste(m.point(lambda v: v * 75 // 255), (95, 100))
    sheet.paste(SHADE, (cx - r - 80, cy - r - 80), sh.filter(ImageFilter.GaussianBlur(22)))
    sheet.paste(im.convert("RGB"), (cx - r, cy - r), m)
    f = sans("Regular", 24)
    tw = sum(d.textlength(c, font=f) + 24 * .2 for c in label)
    tracked(d, (cx - tw / 2, cy + r + 36), label, f, SOFT, .2)


# ---------------------------------------------------------------- brand
def brand(d, x, y):
    s = 58
    d.rounded_rectangle([x, y, x + s, y + s], radius=17, outline=BROWN, width=4)
    d.ellipse([x + s / 2 - 14, y + s / 2 - 14, x + s / 2 + 14, y + s / 2 + 14], outline=BROWN, width=4)
    d.ellipse([x + s - 15, y + 9, x + s - 8, y + 16], fill=BROWN)
    d.text((x + s + 26, y + 2), "aneli.interiors.dubai", font=sans("Regular", 40), fill=BROWN)


def build():
    sheet = sunlit_background()
    palm_shadows(sheet)
    d = ImageDraw.Draw(sheet)

    # header
    brand(d, 200, 150)
    t1 = "Moodboard for The Palm Jumeirah, Villa C124"
    f1 = serif(96, b"Light")
    d.text(((W - d.textlength(t1, font=f1, features=["lnum"])) / 2, 112), t1, font=f1, fill=BROWN, features=["lnum"])
    t2 = "Home Office on the Ground Floor"
    f2 = serif(62, b"Light Italic", italic=True)
    d.text(((W - d.textlength(t2, font=f2)) / 2, 240), t2, font=f2, fill=SOFT)
    d.line([W / 2 - 60, 352, W / 2 + 60, 352], fill=HAIR, width=2)

    # living group
    rug_floor_sun(sheet, [(520, 1420), (2060, 1420), (2300, 1850), (260, 1850)])
    sofa = sun_grade(load("05-sofa.png", w=round(212 * S)))
    sx, sy = place_sun(sheet, sofa, 640, 1560)
    table = sun_grade(load("01-coffee-table.png", w=round(120 * S)))
    tx, ty = place_sun(sheet, table, 1280, 1790)

    # workspace
    desk = sun_grade(load("02-desk.png", w=round(120 * S)))
    dx, dy = place_sun(sheet, desk, 2640, 1730)
    chair = sun_grade(load("03-office-chair.png", h=round(125 * S)))
    cx, cy = place_sun(sheet, chair, 2400, 1850)

    # swatches
    swatch_sun(sheet, d, "05-sofa-texture.jpg", (230, 40, 690, 500), 2170, 740, 205, "LEATHER", 1.0)
    swatch_sun(sheet, d, "01-coffee-table-detail.jpg", (300, 130, 520, 350), 2635, 740, 205, "BLACK ASH", .7)
    swatch_sun(sheet, d, "04-rug-texture.jpg", (0, 0, 380, 380), 3100, 740, 205, "SHAG PILE", .3)

    # palette
    tracked(d, (200, 470), "PALETTE", sans("Regular", 22), SOFT, .28)
    pal = [((60, 42, 34), "CHOCOLATE"), ((30, 29, 28), "BLACK"), ((240, 233, 220), "IVORY")]
    for i, (c, n) in enumerate(pal):
        x = 200 + i * 190
        d.rectangle([x, 530, x + 150, 680], fill=c, outline=HAIR, width=1)
        tracked(d, (x, 702), n, sans("Regular", 18), SOFT, .2)

    marker(d, sx + 40, sy - 30, "01")
    marker(d, tx + table.width - 30, ty + 170, "02")
    marker(d, 300, 1730, "03")
    marker(d, dx + desk.width - 10, dy + 30, "04")
    marker(d, cx + 30, cy + 60, "05")

    legend(d, 2000)
    sheet.save(HERE / "moodboard-sunlit.png", dpi=(300, 300))
    sheet.save(HERE / "moodboard-sunlit.pdf", resolution=300)


if __name__ == "__main__":
    build()
