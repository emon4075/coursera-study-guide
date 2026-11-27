# Browser Extraction Guide for Coursera (Read-Only)

Follow this playbook when instructing a browser subagent or configured browser MCP (e.g., Antigravity `/browser`, `chrome-devtools-mcp`, or Playwright MCP) to inspect and extract a Coursera course module. *(If running without a browser MCP, ask the user to export transcripts, readings, `.ipynb` notebooks, and quiz reviews manually into `Module <N>/raw/`.)*

## 1. Non-Negotiable Safety Rules
- **Read-Only Only**: Never click `Submit`, `Try again`, `Retake`, `Start New Attempt`, `Mark as Completed`, or lab `Reset` buttons.
- **No Auth / CAPTCHA Bypass**: If Coursera shows a login page, SSO prompt, 2FA, or anti-bot challenge, stop immediately and ask the user to complete it directly in Chrome.
- **No Unwanted Scraping**: Capture linked external articles' URLs and titles from Coursera readings; do not crawl external third-party websites unless explicitly requested.

## 2. Step A — Inspect Official Hierarchy First
Check both the module overview URL (`/home/module/<N>`) and the left **Course outline** drawer on any lecture item:
- Record the course title, providers/instructors, all module numbers/titles, and completion statuses.
- Verify whether `<nav aria-label="Lessons">` contains visible sub-lesson headings or a **flat list** of items.
  - Note: Coursera's internal API (`onDemandCourseMaterialLessons.v1`) often wraps a flat module inside 1 hidden backend lesson. Mirror the **UI layout** on disk—do not create redundant `01_<module_name>/` folders when a module only has 1 flat list.

## 3. Step B — Extract Each Item Type Sequentially
Save outputs into `<Course Root>/Module <N>/raw/`.

If your browser tool (such as `chrome_devtools` `evaluate_script`) outputs `.json`, save structured `.json` payloads first (`MODULE_<N>_INDEX.json` and `01_<slug>.json` .. `NN_<slug>.json`), then run `scripts/json_to_markdown.py`. Otherwise you may write the structured `.md` files directly using the same numbering.

### Videos
- Capture title, listed duration, exact video player duration (`mm:ss`), and URL.
- Open the **Transcript** tab (and download/fetch the `.txt`/`.vtt` cue links if available in the DOM) to extract timestamped paragraphs and cues.
- Spot-check key visual slides or live demos (e.g., architecture diagrams, formulas, split-screen demos, silent demo sections where captions switch to music lyrics) and record timestamped visual notes.

### Readings
- Extract `rawText`, `markdownBody` (preserving headings, lists, links, code blocks, and tables), and image alt/caption descriptions.

### Labs & Jupyter Notebooks (`.ipynb` / `.py`)
- Open each lab/ungraded app item.
- If a direct `.ipynb`/`.py` download link or read-only notebook preview is available, save the `.ipynb`/`.py` or extract every markdown cell, code cell, and visible output in exact cell order.
- If launching a container is blocked or requires interactive cloud lab launch, record the lab overview instructions and URL as a partial/manual export note.

### Completed Quizzes (Practice & Graded)
- Open only via **`view-feedback`** (never start a new attempt).
- Capture `gradeHeader` (latest score, highest score, passing threshold), `fullDialogText`, and every input option (`name`, `labelText`, `checked` state, `describedByText` feedback, points earned).
- If `view-feedback` shows a lower latest attempt while keeping a 100% highest score, preserve the exact attempt details and highlight why any incorrect choice received its feedback.

## 4. Expected `MODULE_<N>_INDEX.json` Schema
```json
{
  "courseTitle": "Course Name",
  "provider": "Provider",
  "instructors": ["Instructor 1"],
  "courseUrl": "https://www.coursera.org/learn/.../home/welcome",
  "moduleNumber": 1,
  "moduleTitle": "Module Title",
  "moduleUrl": "https://www.coursera.org/learn/.../home/module/1",
  "moduleDescription": "...",
  "learningObjectives": ["..."],
  "moduleCompletionStatus": "...",
  "structureNote": "...",
  "items": [
    {
      "itemNumber": 1,
      "title": "Item Title",
      "type": "Video | Reading | Lab | Practice Assignment | Graded Assignment",
      "listedDuration": "4 min",
      "exactDuration": "4:33",
      "completionStatus": "Completed",
      "url": "https://...",
      "extractionStatus": "Extracted | Partial | Blocked",
      "extractedJsonFile": "_json/01_item_slug.json",
      "targetMdFile": "01_item_slug.md",
      "notes": "Visual slide / demo / lab notes"
    }
  ]
}
```
