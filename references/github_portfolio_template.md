# GitHub Portfolio & Honor Code Guide

Use this structure when publishing a Coursera course workspace to GitHub.

## 1. Honor Code & Copyright Rules
- **Keep `raw/` local only**: Add `**/raw/` and `raw/` to `.gitignore` **before** running `git add` so verbatim video transcripts, readings, JSON dumps, and quiz feedback never enter Git commit history.
- **Start Private, Go Public Later**: Create the GitHub repository as **Private** while actively working through the modules.
- **Before Switching to Public**:
  - Replace or redact verbatim graded/practice quiz questions and answers inside `.docx`/`.pdf` study guides with concept-only self-check takeaways.
  - Keep your original study summaries, custom diagrams, cleaned `.ipynb` lab implementations, and final capstone project (`Module N/`).
  - Verify Git commit email privacy if desired (`<id>+<username>@users.noreply.github.com`).

## 2. Recommended `.gitignore`
```gitignore
# Coursera raw transcripts, readings, JSON dumps & quiz backups (local study only)
**/raw/
raw/

# Office / Word temporary lock files
~$*.docx
~$*.pdf

# Python / Jupyter artifacts
__pycache__/
*.py[cod]
.ipynb_checkpoints/
.venv/
venv/
.DS_Store
Thumbs.db
```

## 3. Recommended Root `README.md` Sections
1. **Course Title & Link**: Official Coursera course link and provider.
2. **Privacy Note**: Mention that raw Coursera transcripts/quizzes are excluded locally via `.gitignore`.
3. **Module Progress Table**: Table of all modules with item counts, completion status (`✅`, `🔄`, `⏳`), and direct links to `.pdf` (renders inline on GitHub!), `.docx`, and `labs/*.ipynb`.
4. **Tech Stack**: Languages, libraries, algorithms, and deployment tools covered.
5. **Repository Structure Tree**: Clean ASCII directory diagram.
6. **Certificate Verification Link**: Placeholder to fill in upon course completion.
