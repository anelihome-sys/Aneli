#!/usr/bin/env python3
"""Build the Aneli Interiors practicum certificate (A4 portrait) as print-ready PDF.

Usage:  python3 build.py            -> dist/*.pdf  (fonts embedded)
        python3 build.py --html     -> also refresh the editable HTML sources
Edit DATA below to issue the certificate to someone else.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
SCRATCH = "/tmp/claude-0/-home-user-Aneli/a244e91c-c710-500a-a65f-806389f7b48f/scratchpad"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CDN_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Playfair+Display:ital,wght@0,400;0,500;0,700;1,400'
    '&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,400'
    '&family=Montserrat:wght@200;300;400;500'
    '&family=Pinyon+Script&family=Marck+Script&display=swap" rel="stylesheet">'
)

NAME = "Akhan Ayana Sherekhanqyzy"

COMMON = {
    "NAME": NAME,
    "SEAL_TOP": "ANELI INTERIORS",
    "SEAL_BOTTOM": "ALMATY · KAZAKHSTAN",
    "SEAL_YEAR": "2026",
}

DATA = {
  "ru": dict(COMMON,
    LANG="ru",
    TITLE_TAG="Сертификат — практикум по дизайну интерьера",
    H1="СЕРТИФИКАТ",
    H2="о прохождении практикума",
    PRESENTED="торжественно вручается",
    REASON="за успешное прохождение практикума по дизайну интерьера длительностью полтора месяца",
    SIG_INK="Анель Ташбаева",
    SIG_WHO="Анель Ташбаева",
    SIG_ROLE="Основатель и куратор практикума",
    PLACE="Алматы, 2026",
    file="aneli-certificate-ayana-akhan-ru",
  ),
  "en": dict(COMMON,
    LANG="en",
    TITLE_TAG="Certificate — Interior Design Practicum",
    H1="CERTIFICATE",
    H2="of completion",
    PRESENTED="proudly presented to",
    REASON="for successfully completing the six-week interior design practicum",
    SIG_INK="Anel Tashbayeva",
    SIG_WHO="Anel Tashbayeva",
    SIG_ROLE="Founder & Practicum Lead",
    PLACE="Almaty, 2026",
    file="aneli-certificate-ayana-akhan-en",
  ),
}

def render(tpl, data, fonts, bumps, grain):
    out = (tpl.replace("{{FONTS}}", fonts)
              .replace("{{SEAL_BUMPS}}", bumps)
              .replace("{{GRAIN}}", grain))
    for k, v in data.items():
        if k != "file":
            out = out.replace("{{%s}}" % k, v)
    left = re.findall(r"\{\{[A-Z_0-9]+\}\}", out)
    assert not left, "unresolved placeholders: %s" % set(left)
    return out

def main():
    tpl = open(os.path.join(HERE, "template.html")).read()
    bumps = open(os.path.join(HERE, "seal_bumps.svg.frag")).read()
    grain = open(os.path.join(HERE, "grain.b64")).read().strip()
    css = os.path.join(SCRATCH, "fonts.css")
    inline = "<style>\n%s\n</style>" % open(css).read() if os.path.exists(css) else CDN_LINK
    os.makedirs(DIST, exist_ok=True)
    for d in DATA.values():
        src = os.path.join(SCRATCH, d["file"] + ".html")
        open(src, "w").write(render(tpl, d, inline, bumps, grain))
        if "--html" in sys.argv:
            open(os.path.join(HERE, d["file"] + ".html"), "w").write(
                render(tpl, d, CDN_LINK, bumps, grain))
        pdf = os.path.join(DIST, d["file"] + ".pdf")
        png = os.path.join(SCRATCH, d["file"] + ".png")
        base = [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                "--run-all-compositor-stages-before-draw", "--virtual-time-budget=6000"]
        subprocess.run(base + ["--no-pdf-header-footer", "--print-to-pdf=" + pdf,
                               "file://" + src], check=True, capture_output=True)
        subprocess.run(base + ["--force-device-scale-factor=2", "--hide-scrollbars",
                               "--window-size=1123,794", "--screenshot=" + png,
                               "file://" + src], check=True, capture_output=True)
        print(pdf, os.path.getsize(pdf), "bytes")

if __name__ == "__main__":
    main()
