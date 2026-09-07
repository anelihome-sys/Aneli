# -*- coding: utf-8 -*-
"""Выгружает варианты обоих комплектов в variants.json для сборки .docx (build_docx.js)."""
import json, os, sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import build_exam as set1
import build_exam2 as set2

data = []
for first, mod in ((1, set1), (6, set2)):
    for i, variant in enumerate(mod.VARIANTS):
        data.append({
            "number": first + i,
            "set": 1 if first == 1 else 2,
            "questions": [{"q": q, "opts": o, "correct": c} for q, o, c in variant],
        })

out = os.path.join(here, "variants.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("json:", out, "| вариантов:", len(data))
