# Coursera Study Guide Skill (`coursera-study-guide`)

A reusable AI agent skill that turns any completed Coursera module into:
1. A clean, read-only local archive of transcripts, readings, labs/notebooks, and quiz feedback (`raw/`).
2. High-DPI technical diagrams (`300 DPI`) tailored to each subsection.
3. A professionally formatted `.docx` study guide + companion `.pdf` verified page-by-page.
4. A GitHub-ready portfolio repository that keeps raw Coursera transcripts and quiz answers out of Git history.

---

## Repository Contents

```text
coursera-study-guide/
├── SKILL.md                              # Agent workflow, frontmatter & guardrails (root)
├── README.md                             # Installation & usage documentation
├── LICENSE                               # MIT License
├── requirements.txt                      # Python dependencies
├── .gitignore
├── scripts/
│   ├── json_to_markdown.py               # Converts browser-extracted Coursera JSON -> clean Markdown
│   ├── docx_helpers.py                   # Reusable python-docx styling, tables, callouts, code blocks & PDF export
│   └── verify_docx_pages.py              # Renders .docx -> .pdf -> page PNGs for visual layout QA
└── references/
    ├── browser_extraction_guide.md       # Read-only Coursera extraction playbook
    ├── diagram_design_checklist.md       # Matplotlib/Pillow diagram standards & pitfall checks
    └── github_portfolio_template.md      # .gitignore, README template & Honor Code checklist
```

---

## Installation

### Option 1: Clone into Personal Global Skills (Recommended)
Works automatically across every Coursera course and workspace:

- **Windows (PowerShell):**
  ```powershell
  git clone https://github.com/emon4075/coursera-study-guide.git "$env:USERPROFILE\.gemini\skills\coursera-study-guide"
  ```
- **macOS / Linux:**
  ```bash
  git clone https://github.com/emon4075/coursera-study-guide.git ~/.gemini/skills/coursera-study-guide
  ```

### Option 2: Per-Workspace / Team Install
```bash
git clone https://github.com/emon4075/coursera-study-guide.git .agents/skills/coursera-study-guide
```

### Option 3: Import into MCP Market Hub
You can import `https://github.com/emon4075/coursera-study-guide` via **MCP Market Hub -> Add skill -> Import from GitHub (Public repo)**.

---

## Python Dependencies

```bash
pip install -r requirements.txt
```

*(For `.docx` → `.pdf` export and page verification: Microsoft Word on Windows via `pywin32`, or LibreOffice `soffice` on macOS/Linux/Windows.)*

---

## Quick Usage Prompt

Once installed, open your completed Coursera module in Google Chrome (with browser access enabled) and prompt your agent:

> `/browser Use the coursera-study-guide skill to extract Module <N> of my open Coursera course in read-only mode and build a complete study guide (.docx and .pdf) with custom diagrams per subsection.`

---

## Honor Code & Copyright Notice
This skill enforces strict read-only Coursera interaction (never submitting quizzes or altering progress) and puts `**/raw/` in `.gitignore` so copyrighted transcripts and graded quiz answers remain strictly local on your machine. When making a course repository public after graduation, verify that no verbatim quiz questions or answers remain in tracked files.
