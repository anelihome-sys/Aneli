#!/usr/bin/env python3
"""Build the Aneli Interiors practicum certificate (A4) as print-ready PDF.

Usage:  python3 build.py            -> writes dist/*.pdf (fonts embedded)
        python3 build.py --html     -> also writes CDN-font HTML sources
Edit the DATA dict below to issue the certificate to someone else.
"""
import os, re, subprocess, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
SCRATCH = "/tmp/claude-0/-home-user-Aneli/a244e91c-c710-500a-a65f-806389f7b48f/scratchpad"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CDN_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400'
    '&family=Great+Vibes&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">'
)

NAME = "Akhan Ayana Sherekhanqyzy"

DATA = {
  "ru": {
    "LANG": "ru",
    "TITLE_TAG": "Сертификат — практикум по дизайну интерьера",
    "STUDIO_SUB": "студия дизайна интерьера · Алматы",
    "H1": "СЕРТИФИКАТ",
    "KICKER": "о прохождении практикума по дизайну интерьера",
    "ATTEST": "настоящим удостоверяется, что",
    "NAME": NAME,
    "BODY": ("успешно прошла практикум по дизайну интерьера в студии Aneli Interiors "
             "продолжительностью <em>шесть недель</em> — занятия три раза в неделю "
             "по 2 часа 30 минут, общим объёмом 45 часов практической работы."),
    "S1": "недель", "S2": "занятий", "S3": "часов",
    "PLACE": "г. Алматы · 2026",
    "CERT_NO": "сертификат № AI-2026-014",
    "SIG_LABEL": "Руководитель практикума",
    "SEAL_BOTTOM": "ALMATY · KAZAKHSTAN",
    "SEAL_YEAR": "2026",
    "file": "aneli-certificate-ayana-akhan-ru",
  },
  "en": {
    "LANG": "en",
    "TITLE_TAG": "Certificate — Interior Design Practicum",
    "STUDIO_SUB": "interior design studio · Almaty",
    "H1": "CERTIFICATE",
    "KICKER": "of completion — interior design practicum",
    "ATTEST": "this is to certify that",
    "NAME": NAME,
    "BODY": ("has successfully completed the Interior Design Practicum at Aneli Interiors — "
             "<em>six weeks</em> of studio work, three sessions per week of 2 hours 30 minutes, "
             "45 hours in total."),
    "S1": "weeks", "S2": "sessions", "S3": "hours",
    "PLACE": "Almaty · 2026",
    "CERT_NO": "certificate no. AI-2026-014",
    "SIG_LABEL": "Practicum Lead",
    "SEAL_BOTTOM": "ALMATY · KAZAKHSTAN",
    "SEAL_YEAR": "2026",
    "file": "aneli-certificate-ayana-akhan-en",
  },
}

def render(tpl, data, fonts):
    out = tpl.replace("{{FONTS}}", fonts)
    for k, v in data.items():
        if k == "file":
            continue
        out = out.replace("{{%s}}" % k, v)
    left = re.findall(r"\{\{[A-Z_0-9]+\}\}", out)
    assert not left, "unresolved placeholders: %s" % set(left)
    return out

def main():
    tpl = open(os.path.join(HERE, "template.html")).read()
    inline = "<style>\n%s\n</style>" % open(os.path.join(SCRATCH, "fonts.css")).read() \
        if os.path.exists(os.path.join(SCRATCH, "fonts.css")) else CDN_LINK
    os.makedirs(DIST, exist_ok=True)
    for key, d in DATA.items():
        src = os.path.join(SCRATCH, d["file"] + ".html")
        open(src, "w").write(render(tpl, d, inline))
        if "--html" in sys.argv:
            open(os.path.join(HERE, d["file"] + ".html"), "w").write(render(tpl, d, CDN_LINK))
        pdf = os.path.join(DIST, d["file"] + ".pdf")
        png = os.path.join(SCRATCH, d["file"] + ".png")
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                        "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
                        "--virtual-time-budget=6000",
                        "--print-to-pdf=" + pdf, "file://" + src],
                       check=True, capture_output=True)
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                        "--force-device-scale-factor=2", "--hide-scrollbars",
                        "--window-size=794,1123", "--virtual-time-budget=6000",
                        "--screenshot=" + png, "file://" + src],
                       check=True, capture_output=True)
        print(pdf, os.path.getsize(pdf), "bytes")

if __name__ == "__main__":
    main()
