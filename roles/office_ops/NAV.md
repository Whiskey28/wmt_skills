# 日常办公（PPT/PDF/Word/Excel）- Skills 导航

## NAV_DATA（结构化）

```yaml
role: office_ops
role_display: 日常办公（PPT/PDF/Word/Excel）
skill_packages:
  - id: document_skills
    type: local_family
    display: document-skills/*
    why: 办公文档格式（PPTX/DOCX/PDF/XLSX）通用工具箱
  - id: baoyu_slide_deck
    type: local_skill
    display: baoyu-slide-deck
    why: 文字内容快速转演示稿
    optional: true
skill_items_local:
  - id: document-skills/pptx
    package: document_skills
  - id: document-skills/docx
    package: document_skills
  - id: document-skills/pdf
    package: document_skills
  - id: document-skills/xlsx
    package: document_skills
  - id: baoyu-slide-deck
    package: baoyu_slide_deck
skill_items_external:
  - name: pdf-ocr
    url: https://skillshub.wtf/TerminalSkills/skills/pdf-ocr?format=md
    purpose: 扫描版 PDF OCR 提取
  - name: docx
    url: https://skillshub.wtf/anthropics/skills/docx?format=md
    purpose: Word（.docx）处理（官方 skills）
  - name: markitdown
    url: https://skillshub.wtf/K-Dense-AI/claude-scientific-skills/markitdown?format=md
    purpose: 多格式文件 → Markdown（含 OCR/转写）
  - name: markdown-converter
    url: https://skillshub.wtf/intellectronica/agent-skills/markdown-converter?format=md
    purpose: 文档/文件 → Markdown（markitdown 封装）
```

## 你常见的交付物 / 任务

- PPT：汇报稿、方案、复盘、演讲稿
- PDF：合并拆分、OCR、表格/文本抽取
- Word：报告/制度/合同类文书（如需要）、格式统一
- Excel：数据清洗、对账、报表、批量转换

## 建议你优先收集/沉淀的 Skills 类型

- **模板化生成**：提纲 → 成稿（PPT/Word）
- **批量处理**：多文件合并拆分、提取、统一格式
- **结构化抽取**：从 PDF/图片中提取表格与文本

## 推荐“大技能包”（先装一套，再挑工具）

- **`document-skills/*`**：办公文档格式（PPTX/DOCX/PDF/XLSX）的通用工具箱
- （可选）**`baoyu-slide-deck`**：当你想把文字内容快速转成演示稿

## Skillshub 推荐（外部可直接拉取）

- [pdf-ocr](https://skillshub.wtf/TerminalSkills/skills/pdf-ocr)：扫描版 PDF OCR 提取
- [docx](https://skillshub.wtf/anthropics/skills/docx)：Word（.docx）处理（官方 skills）
- [markitdown](https://skillshub.wtf/K-Dense-AI/claude-scientific-skills/markitdown)：多格式文件 → Markdown（含 OCR/转写等）
- [markdown-converter](https://skillshub.wtf/intellectronica/agent-skills/markdown-converter)：文档/文件 → Markdown（markitdown 封装）

## 你电脑里现有技能库（家族示例）

- **Office/PDF 工具链**：`document-skills/pptx`、`document-skills/docx`、`document-skills/pdf`、`document-skills/xlsx`
- **演示稿生成（偏内容）**：`baoyu-slide-deck`

