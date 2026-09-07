// Отдельный .docx на каждый вариант. Данные берутся из variants.json (см. export_json.py).
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Tab, PageBreak,
  AlignmentType, BorderStyle, TabStopType, HeadingLevel, LevelFormat,
} = require("docx");

const ACCENT = "8A7F6D";
const INK = "1C1A17";
const MUTED = "6F6A62";
const SERIF = "Georgia";
const SANS = "Arial";
const LETTERS = ["А", "Б", "В", "Г"];
// A4 = 11906 dxa; поля 850 + 850 -> полоса набора 10206 dxa
const RIGHT_EDGE = 10206;

const hairline = (color, size) => ({
  bottom: { style: BorderStyle.SINGLE, size, color, space: 4 },
});

function head(variant, eyebrow) {
  return [
    new Paragraph({
      spacing: { after: 40 },
      children: [new TextRun({
        text: eyebrow.toUpperCase(), font: SANS, size: 13,
        color: ACCENT, characterSpacing: 30,
      })],
    }),
    new Paragraph({
      border: hairline(INK, 6),
      spacing: { after: 120 },
      tabStops: [{ type: TabStopType.RIGHT, position: RIGHT_EDGE }],
      children: [
        new TextRun({ text: "Экзаменационный тест", font: SERIF, size: 26, color: INK }),
        new TextRun({ font: SERIF, size: 22, color: INK,
          children: [new Tab(), `Вариант ${variant}`] }),
      ],
    }),
    new Paragraph({
      border: hairline("DDD8CF", 4),
      spacing: { after: 220 },
      tabStops: [
        { type: TabStopType.CENTER, position: Math.round(RIGHT_EDGE / 2) },
        { type: TabStopType.RIGHT, position: RIGHT_EDGE },
      ],
      children: [new TextRun({
        font: SANS, size: 14, color: MUTED,
        children: [
          "Ф. И. О. ______________________________________",
          new Tab(), "Дата ______________",
          new Tab(), "Один правильный ответ · 15 вопросов",
        ],
      })],
    }),
  ];
}

function question(i, item) {
  const opts = [];
  item.opts.forEach((text, k) => {
    if (k > 0) opts.push(new TextRun({ text: "   ", font: SANS, size: 17 }));
    opts.push(new TextRun({ text: `${LETTERS[k]}) `, font: SANS, size: 17, color: ACCENT }));
    opts.push(new TextRun({ text, font: SANS, size: 17, color: "2C2926" }));
  });
  return [
    new Paragraph({
      spacing: { before: 120, after: 20 },
      indent: { left: 300, hanging: 300 },
      children: [
        new TextRun({ text: `${i}. `, font: SERIF, size: 17, color: ACCENT }),
        new TextRun({ text: item.q, font: SANS, size: 17, bold: true, color: INK }),
      ],
    }),
    new Paragraph({ indent: { left: 300 }, children: opts }),
  ];
}

function key(variant, questions) {
  const rows = questions.map((item, i) => new Paragraph({
    spacing: { after: 20 },
    tabStops: [{ type: TabStopType.RIGHT, position: 1400 }],
    children: [
      new TextRun({ text: `${i + 1}`, font: SANS, size: 18, color: MUTED }),
      new TextRun({ font: SANS, size: 18, bold: true, color: INK,
        children: [new Tab(), LETTERS[item.correct]] }),
    ],
  }));
  return [
    new Paragraph({ children: [new PageBreak()] }),
    new Paragraph({
      spacing: { after: 40 },
      children: [new TextRun({ text: "Ключ ответов", font: SERIF, size: 30, color: INK })],
    }),
    new Paragraph({
      spacing: { after: 240 },
      border: hairline("DDD8CF", 4),
      children: [new TextRun({
        text: `ВАРИАНТ ${variant} · ДЛЯ ПРЕПОДАВАТЕЛЯ`,
        font: SANS, size: 13, color: ACCENT, characterSpacing: 30,
      })],
    }),
    ...rows,
    new Paragraph({
      spacing: { before: 300 },
      children: [new TextRun({
        text: "Эту страницу удаляют перед выдачей бланка. Оценка: 13–15 верных ответов — "
            + "уровень уверенный; 10–12 — база есть, слабые места чаще в этапности работ "
            + "и инженерии; менее 10 — требуется повторное прохождение блоков «Эргономика», "
            + "«Этапы проекта» и «Санузлы».",
        font: SANS, size: 15, color: MUTED, italics: true,
      })],
    }),
  ];
}

const data = JSON.parse(fs.readFileSync(path.join(__dirname, "variants.json"), "utf8"));
const outDir = path.join(__dirname, "docx");
fs.mkdirSync(outDir, { recursive: true });

(async () => {
  for (const v of data) {
    const eyebrow = `Дизайн интерьера · базовый уровень · комплект ${v.set}`;
    const doc = new Document({
      creator: "Aneli",
      title: `Экзаменационный тест · вариант ${v.number}`,
      styles: { default: { document: { run: { font: SANS, size: 17 }, paragraph: { spacing: { line: 230 } } } } },
      sections: [{
        properties: { page: { margin: { top: 800, right: 850, bottom: 800, left: 850 } } },
        children: [
          ...head(v.number, eyebrow),
          ...v.questions.flatMap((item, i) => question(i + 1, item)),
          ...key(v.number, v.questions),
        ],
      }],
    });
    const file = path.join(outDir, `Экзамен_Вариант-${String(v.number).padStart(2, "0")}.docx`);
    fs.writeFileSync(file, await Packer.toBuffer(doc));
    console.log("→", path.basename(file));
  }
})();
