# Coursera Study Guide Skill (`coursera-study-guide`)

A reusable, cross-agent skill (compatible with **Antigravity**, **Claude Code**, **OpenCode**, and **MCP Market Hub**) that turns any completed Coursera module into:
1. A clean, read-only local archive of transcripts, readings, labs/notebooks, and quiz feedback (`raw/`).
2. High-DPI technical diagrams (`300 DPI`) tailored to each subsection.
3. A professionally formatted `.docx` study guide + companion `.pdf` verified page-by-page.
4. A GitHub-ready portfolio repository that keeps raw Coursera transcripts and quiz answers out of Git history.

---

## Repository Contents

```text
coursera-study-guide/
├── README.md
├── LICENSE                                   # MIT License
├── requirements.txt                          # Python dependencies
├── .gitignore
└── skills/
    └── coursera-study-guide/
        ├── SKILL.md                          # Agent workflow, frontmatter & guardrails
        ├── scripts/
        │   ├── json_to_markdown.py           # Coursera JSON -> clean Markdown + _json archive
        │   ├── docx_helpers.py               # Reusable python-docx styling, code blocks & PDF export
        │   └── verify_docx_pages.py          # Renders .docx -> .pdf -> page PNGs for visual QA
        └── references/
            ├── browser_extraction_guide.md   # Read-only Coursera extraction playbook
            ├── diagram_design_checklist.md   # Matplotlib/Pillow diagram standards & pitfall checks
            └── github_portfolio_template.md  # .gitignore, README template & Honor Code checklist
```

---

## Installation

Clone the repository and copy `skills/coursera-study-guide` into your agent's skill directory:

### 1. Antigravity
- **Global (all courses):**
  - Windows (PowerShell):
    ```powershell
    git clone https://github.com/emon4075/coursera-study-guide.git "$env:TEMP\coursera-skill-repo"
    Copy-Item -Recurse "$env:TEMP\coursera-skill-repo\skills\coursera-study-guide" "$env:USERPROFILE\.gemini\skills\coursera-study-guide"
    ```
  - macOS / Linux:
    ```bash
    git clone https://github.com/emon4075/coursera-study-guide.git /tmp/coursera-skill-repo
    cp -r /tmp/coursera-skill-repo/skills/coursera-study-guide ~/.gemini/skills/coursera-study-guide
    ```
- **Project-level:** Copy `skills/coursera-study-guide` into `.agents/skills/coursera-study-guide`.

### 2. Claude Code
- **Personal / Global (also available as `/coursera-study-guide`):**
  - Windows (PowerShell):
    ```powershell
    Copy-Item -Recurse "$env:TEMP\coursera-skill-repo\skills\coursera-study-guide" "$env:USERPROFILE\.claude\skills\coursera-study-guide"
    ```
  - macOS / Linux:
    ```bash
    cp -r /tmp/coursera-skill-repo/skills/coursera-study-guide ~/.claude/skills/coursera-study-guide
    ```
- **Project-level:** Copy `skills/coursera-study-guide` into `.claude/skills/coursera-study-guide`.

### 3. OpenCode
- **Project-level (native):** Copy `skills/coursera-study-guide` into `.opencode/skills/coursera-study-guide`.
- **Cross-agent shared path:** Copy `skills/coursera-study-guide` into `.agents/skills/coursera-study-guide`.

### 4. MCP Market Hub
Import directly via **MCP Market Hub -> Add skill -> Import from GitHub (Public repo)** using the skill folder URL:
```text
https://github.com/emon4075/coursera-study-guide/tree/main/skills/coursera-study-guide
```

---

## Python & Browser Prerequisites

```bash
pip install -r requirements.txt
```

- **PDF Export & Page Verification:** Microsoft Word on Windows (`pywin32`), or LibreOffice (`soffice`) on macOS/Linux/Windows.
- **Automated Coursera Extraction (Phase 1):**
  - **Antigravity:** Run `/browser` with Chrome remote debugging enabled.
  - **Claude Code / OpenCode:** Attach a browser MCP server such as `chrome-devtools-mcp` or Playwright MCP, **or** export raw transcripts, `.ipynb` labs, and quiz text into `Module N/raw/` and run Phases 2–5 directly.

---

## Quick Usage Prompt

Once installed, prompt your agent in your course workspace:

> Use the `coursera-study-guide` skill to extract Module `<N>` of my open Coursera course in read-only mode and build a complete study guide (`.docx` and `.pdf`) with custom diagrams per subsection.

*(In Antigravity, prefix with `/browser` to activate the browser subagent; in Claude Code, you can also invoke `/coursera-study-guide`.)*

---

## Honor Code & Copyright Notice
This skill enforces strict read-only Coursera interaction (never submitting quizzes or altering progress) and puts `**/raw/` in `.gitignore` so copyrighted transcripts and graded quiz answers remain strictly local on your machine. When making a course repository public after graduation, verify that no verbatim quiz questions or answers remain in tracked files.
