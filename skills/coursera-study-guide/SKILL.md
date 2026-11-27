---
name: coursera-study-guide
description: >-
  Extract completed Coursera modules in strict read-only mode via browser and
  compile formatted, diagram-rich study guides (.docx and .pdf) with code
  walkthroughs, quiz rationales, and GitHub-safe repository setup. Use when the
  user asks to document a Coursera course or module from their browser, convert
  Coursera transcripts/labs/quizzes into study notes, or organize a Coursera
  portfolio repository on GitHub.
license: MIT
compatibility: >-
  Compatible with Antigravity, Claude Code, and OpenCode. Requires Python 3.10+
  (python-docx, matplotlib, pillow, numpy, pymupdf), Microsoft Word (Windows)
  or LibreOffice for PDF verification, and an optional browser MCP (e.g.,
  chrome-devtools-mcp or Playwright MCP) for automated Coursera extraction.
---

# Coursera Study Guide Pipeline

End-to-end workflow for turning any completed Coursera module into a clean local raw archive, a richly illustrated `.docx` + `.pdf` study guide, and a privacy-safe GitHub portfolio repository.

## Core Guardrails

1. **Strict Read-Only on Coursera**: Never click `Submit`, `Retake`, `Try again`, `Mark as Completed`, `Reset`, or alter course progress. Only read completed quizzes via `view-feedback`.
2. **Respect Auth & Anti-Bot Gates**: Never bypass login screens, 2FA, passkeys, or CAPTCHAs. If Coursera or GitHub requires sign-in or verification, stop and ask the user to complete it directly in the browser UI.
3. **Never Guess Course Structure**: Always inspect the Coursera course/module outline first so folder names and item ordering match what Coursera actually renders.
4. **Protect Honor Code & Copyright on GitHub**: Never commit `raw/` directories (verbatim transcripts, readings, or quiz dumps) to a Git repository.

---

## Workflow

### Phase 1: Course & Module Structure Inspection

Before creating folders or extracting items, use your browser agent or configured browser MCP (e.g., `/browser` in Antigravity, or `chrome-devtools-mcp` / Playwright MCP in Claude Code or OpenCode) to inspect the open course. *(If no browser tool is connected, ask the user to save/export transcripts, `.ipynb` labs, and quiz text into `Module N/raw/` and start at Phase 2.)* Inspect:

1. All modules in the course (`Module 1` .. `Module N`) and exact titles.
2. Whether the target module renders a **flat sequential item list** or **grouped lesson sections** in the UI (`nav[aria-label="Lessons"]`). Do not invent artificial `Lesson 1` subfolders when Coursera displays a flat list.
3. Exact item sequence (videos, readings, Jupyter/Skills Network labs, practice quizzes, graded quizzes).

Use this workspace layout:

```text
<Course Root>/
├── .gitignore
├── README.md
├── COURSE_INDEX.md
└── Module N/
    ├── Module_N_<Module_Title>.docx
    ├── Module_N_<Module_Title>.pdf
    └── raw/                    # Ignored by Git!
        ├── MODULE_N_INDEX.md
        ├── 01_<item>.md .. NN_<item>.md
        └── _json/              # Raw browser extraction backups
```

See [Browser Extraction Guide](./references/browser_extraction_guide.md) for exact DOM/extraction instructions per item type.

### Phase 2: Raw Extraction & Markdown Materialization

1. Have the browser agent/MCP (or manual export) save every item in `Module N` sequentially into `<Course Root>/Module N/raw/` (saving `MODULE_N_INDEX.json` and `01_*.json` .. `NN_*.json`, plus downloading or extracting `.ipynb`/`.py` lab files and noting key on-screen visual slides/timestamps).
2. Convert the extracted JSON payloads into clean Markdown files and archive the JSONs under `_json/` using [json_to_markdown.py](./scripts/json_to_markdown.py):

   ```bash
   python scripts/json_to_markdown.py --raw-dir "<Course Root>/Module N/raw"
   ```

3. Verify that every item in `MODULE_N_INDEX.md` is present and complete (note any external readings or container-gated labs clearly).

### Phase 3: Visual Diagrams (One Roadmap + One Visual Per Subsection)

1. Generate **1 Module Roadmap diagram** (`fig_00_...png`) plus **1 dedicated 300-DPI technical diagram per subsection** (`fig_01_...png` .. `fig_NN_...png`) using `matplotlib` / `Pillow` / `numpy` stored in scratch space.
2. Follow [Diagram Design Checklist](./references/diagram_design_checklist.md):
   - Always use `ax.inset_axes(..., transform=ax.transData)` for embedded grids/images (never `fig.add_axes`).
   - Use explicit `zorder` layers and generous margins so labels never collide with borders.
   - **Visually inspect every generated PNG** with your file/image-reading tool and fix any overlaps before building the document.

### Phase 4: Build `.docx`, Export `.pdf`, and Visually Verify Every Page

1. Build `Module_N_<Title>.docx` using the reusable primitives in [docx_helpers.py](./scripts/docx_helpers.py):
   - Cover banner, metadata table, official description & learning objectives, and roadmap visual.
   - Per-subsection banner (`TYPE`, `DURATION`, `STATUS`), concept explanations, slide/demo notes, code & lab cell-by-cell walkthroughs (when labs exist), quiz question/option/feedback tables, and embedded diagrams with `keep_with_next`.
   - End-of-module quick-reference glossary and bridge to the next module.
2. Export a companion `.pdf` (for inline GitHub viewing) and render every page to PNG using [verify_docx_pages.py](./scripts/verify_docx_pages.py):

   ```bash
   python scripts/verify_docx_pages.py "<Course Root>/Module N/Module_N_Title.docx" --export-pdf "<Course Root>/Module N/Module_N_Title.pdf" --pages-dir "<scratch>/pages"
   ```

3. Inspect the rendered page PNGs with your file/image-reading tool to confirm zero blank trailing pages, zero orphan headings, and crisp table pagination.

### Phase 5: GitHub Setup & Honor-Code-Safe Sharing

Follow [GitHub Portfolio Template](./references/github_portfolio_template.md):

1. Ensure `.gitignore` excludes `**/raw/`, `raw/`, Office lock files (`~$*.docx`, `~$*.pdf`), and Python/Jupyter caches **before** `git add`.
2. Verify commit authorship matches the user (`git config user.name` and `git config user.email` aligned with their GitHub account).
3. Start the GitHub repository as **Private** while completing modules. Before switching to **Public** after course completion, ensure no verbatim graded quiz answers or copyrighted transcripts remain in tracked files.
