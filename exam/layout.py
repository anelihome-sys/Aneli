# -*- coding: utf-8 -*-
"""Вёрстка экзаменационного бланка: HTML для печати в PDF (Chromium headless)."""
import html

LETTERS = ["А", "Б", "В", "Г"]

CSS_TPL = """
@page { size: A4; margin: 14mm 15mm 13mm 15mm; }
* { box-sizing: border-box; }
body { margin: 0; font-family: "Liberation Sans", Arial, sans-serif;
       color: #1c1a17; font-size: {fs}pt; line-height: {lh}; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
.head { display: flex; justify-content: space-between; align-items: baseline;
        border-bottom: 0.6pt solid #1c1a17; padding-bottom: 5pt; margin-bottom: 4pt; }
.head .t { font-family: "Liberation Serif", Georgia, serif; font-size: 12pt; letter-spacing: 0.02em; }
.head .t span { display: block; font-family: "Liberation Sans", Arial, sans-serif;
                font-size: 6.8pt; letter-spacing: 0.16em; text-transform: uppercase;
                color: #8a7f6d; margin-bottom: 2.5pt; }
.head .v { font-family: "Liberation Serif", Georgia, serif; font-size: 10.5pt; white-space: nowrap; }
.meta { display: flex; justify-content: space-between; font-size: 7pt; color: #6f6a62;
        letter-spacing: 0.03em; border-bottom: 0.4pt solid #ddd8cf;
        padding-bottom: 6pt; margin-bottom: 11pt; }
.q { margin-bottom: {gap}pt; padding-left: 15pt; position: relative; }
.q .n { position: absolute; left: 0; top: 0; font-family: "Liberation Serif", Georgia, serif;
        font-size: {fs}pt; color: #8a7f6d; }
.q .txt { font-weight: bold; }
.q .opts { margin-top: 1.5pt; color: #2c2926; }
.q .opts b { font-weight: normal; color: #8a7f6d; }
.keyhead { font-family: "Liberation Serif", Georgia, serif; font-size: 15pt; margin: 0 0 2pt; }
.keysub { font-size: 7pt; letter-spacing: 0.14em; text-transform: uppercase;
          color: #8a7f6d; margin-bottom: 12pt; }
.keygrid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 9pt; }
.keycol { border-top: 0.6pt solid #1c1a17; padding-top: 5pt; }
.keycol h3 { font-family: "Liberation Serif", Georgia, serif; font-weight: normal;
             font-size: 9.5pt; margin: 0 0 4pt; }
.keycol table { width: 100%; border-collapse: collapse; font-size: 7.6pt; }
.keycol td { padding: 1.6pt 0; border-bottom: 0.3pt solid #ece8e0; }
.keycol td.a { text-align: right; font-weight: bold; }
.note { margin-top: 14pt; padding-top: 7pt; border-top: 0.4pt solid #ddd8cf;
        font-size: 7.4pt; color: #6f6a62; line-height: 1.5; }
"""

NOTE = ("Оценка: 13–15 верных ответов — уровень уверенный, можно допускать к самостоятельному "
        "ведению проекта под наблюдением. 10–12 — база есть, слабые места чаще в этапности работ "
        "и инженерии. Менее 10 — требуется повторное прохождение блоков «Эргономика», "
        "«Этапы проекта» и «Санузлы».")


def _esc(s):
    return html.escape(s)


def render_variant(number, page, eyebrow):
    rows = []
    for i, (q, opts, _) in enumerate(page, 1):
        o = "&nbsp;&nbsp; ".join(
            f"<b>{LETTERS[k]})</b> {_esc(t)}" for k, t in enumerate(opts))
        rows.append(
            f'<div class="q"><span class="n">{i}.</span>'
            f'<div class="txt">{_esc(q)}</div><div class="opts">{o}</div></div>')
    return f"""<div class="page">
  <div class="head">
    <div class="t"><span>{_esc(eyebrow)}</span>Экзаменационный тест</div>
    <div class="v">Вариант {number}</div>
  </div>
  <div class="meta"><div>Ф. И. О. ________________________________________</div>
    <div>Дата ______________</div><div>Один правильный ответ · 15 вопросов</div></div>
  {''.join(rows)}
</div>"""


def render_key(variants, first_number):
    cols = []
    for v, page in enumerate(variants):
        trs = "".join(
            f'<tr><td>{i}</td><td class="a">{LETTERS[c]}</td></tr>'
            for i, (_, _, c) in enumerate(page, 1))
        cols.append(f'<div class="keycol"><h3>Вариант {first_number + v}</h3>'
                    f'<table>{trs}</table></div>')
    return f"""<div class="page">
  <h1 class="keyhead">Ключ ответов</h1>
  <div class="keysub">Для преподавателя · не выдаётся вместе с бланком</div>
  <div class="keygrid">{''.join(cols)}</div>
  <div class="note">{NOTE}</div>
</div>"""


def build_html(variants, title, eyebrow, first_number=1, fs=9.4, gap=7.6, lh=1.36):
    css = CSS_TPL.replace("{fs}", str(fs)).replace("{gap}", str(gap)).replace("{lh}", str(lh))
    pages = "".join(render_variant(first_number + i, p, eyebrow)
                    for i, p in enumerate(variants))
    pages += render_key(variants, first_number)
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8">'
            f'<title>{_esc(title)}</title><style>{css}</style></head>'
            f'<body>{pages}</body></html>')
