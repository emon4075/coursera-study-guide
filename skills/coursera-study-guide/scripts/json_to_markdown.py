"""Convert browser-extracted Coursera module JSON files into clean Markdown files.

Supports both flat module item lists (`items`) and multi-lesson structures (`lessons`),
handling Videos, Readings, Labs/Notebooks, and Practice/Graded Quizzes.
"""

import argparse
import json
import re
import shutil
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_paragraph_text(text: str) -> tuple[str, str]:
    """Strip Coursera's 'Play video starting at ...' prefix and return (timestamp, body)."""
    m = re.match(
        r"^Play video starting at :[^\n]*\n(\d+:\d+)\n(.*)$",
        text.strip(),
        flags=re.DOTALL,
    )
    if m:
        ts, body = m.group(1), m.group(2).strip()
        if ts.startswith(":"):
            ts = "0" + ts
        return ts, body
    return "", text.strip()


def format_video_md(data: dict, extra_notes: str = "") -> str:
    lines = [
        f"# {data.get('itemNumber', '')}. {data.get('title', 'Video')}".lstrip(". "),
        "",
        f"- **Type:** {data.get('type', 'Video')}",
        f"- **Duration:** {data.get('listedDuration', '')} (exact `{data.get('exactDuration', '')}`)",
        f"- **URL:** {data.get('url', '')}",
        "",
        "## Transcript",
        "",
    ]
    if data.get("paragraphs"):
        for p in data["paragraphs"]:
            ts, body = clean_paragraph_text(p.get("text", ""))
            lines.append(f"**[{ts}]** {body}" if ts else body)
            lines.append("")
    elif data.get("txtTranscript"):
        lines.append(data["txtTranscript"].strip())
        lines.append("")
    elif data.get("fullTextFromCues"):
        lines.append(data["fullTextFromCues"].strip())
        lines.append("")

    cues = data.get("cues") or []
    if cues:
        lines.extend(["## Timestamped Cues (VTT)", ""])
        for cue in cues:
            lines.append(f"- `{cue['time']}` {cue['text']}")
        lines.append("")

    if extra_notes:
        lines.extend(["## Extracted Visual Notes", "", extra_notes, ""])
    return "\n".join(lines).rstrip() + "\n"


def format_reading_md(data: dict) -> str:
    lines = [
        f"# {data.get('itemNumber', '')}. {data.get('title', 'Reading')}".lstrip(". "),
        "",
        f"- **Type:** {data.get('type', 'Reading')}",
        f"- **Estimated Duration:** {data.get('listedDuration', '')}",
        f"- **URL:** {data.get('url', '')}",
        "",
        "## Content",
        "",
        (data.get("markdownBody") or data.get("rawText") or "").strip(),
        "",
    ]
    links = data.get("links") or []
    if links:
        lines.extend(["## Referenced Links", ""])
        for lk in links:
            lines.append(f"- [{lk.get('text', lk['href'])}]({lk['href']})")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def format_lab_md(data: dict) -> str:
    lines = [
        f"# {data.get('itemNumber', '')}. {data.get('title', 'Lab')}".lstrip(". "),
        "",
        f"- **Type:** {data.get('type', 'Lab')}",
        f"- **Estimated Duration:** {data.get('listedDuration', '')}",
        f"- **URL:** {data.get('url', '')}",
        "",
    ]
    if data.get("notebookFile"):
        lines.append(f"- **Notebook File:** `{data['notebookFile']}`")
        lines.append("")

    cells = data.get("cells") or []
    if cells:
        lines.extend(["## Notebook Cells", ""])
        for idx, cell in enumerate(cells, start=1):
            ctype = cell.get("cell_type", "code")
            src = cell.get("source", "")
            if isinstance(src, list):
                src = "".join(src)
            if ctype == "markdown":
                lines.append(f"### Cell {idx} (Markdown)")
                lines.append("")
                lines.append(src.strip())
                lines.append("")
            else:
                lines.append(f"### Cell {idx} (Code)")
                lines.append("")
                lines.append("```python")
                lines.append(src.rstrip())
                lines.append("```")
                if cell.get("outputs"):
                    lines.extend(["", "**Output:**", "```text", str(cell["outputs"]).strip(), "```"])
                lines.append("")
    else:
        body = (data.get("markdownBody") or data.get("rawText") or data.get("instructions") or "").strip()
        if body:
            lines.extend(["## Lab Overview / Instructions", "", body, ""])
    return "\n".join(lines).rstrip() + "\n"


def parse_quiz_questions(data: dict) -> list[dict]:
    """Combine Coursera view-feedback inputs metadata and fullDialogText."""
    text = data.get("fullDialogText", "")
    parts = re.split(r"\n(?=\d+\.\nQuestion \d+\n)", text)
    q_blocks = [p for p in parts if re.match(r"^\d+\.\nQuestion \d+\n", p.strip())]

    groups = []
    seen = {}
    for inp in data.get("inputs", []):
        gname = inp.get("name", "")
        if gname not in seen:
            seen[gname] = []
            groups.append(seen[gname])
        seen[gname].append(inp)

    questions = []
    for idx, block in enumerate(q_blocks):
        lines_blk = [ln.strip() for ln in block.strip().splitlines() if ln.strip()]
        prompt = lines_blk[2] if len(lines_blk) > 2 else ""
        points = ""
        for ln in reversed(lines_blk):
            if re.match(r"^\d+\s*/\s*\d+\s*point", ln):
                points = ln
                break

        opts = groups[idx] if idx < len(groups) else []
        feedback = ""
        for opt in opts:
            if opt.get("describedByText"):
                feedback = opt["describedByText"].strip()
                break

        questions.append(
            {
                "number": idx + 1,
                "prompt": prompt,
                "points": points,
                "options": opts,
                "feedback": feedback,
            }
        )
    return questions


def format_quiz_md(data: dict) -> str:
    grade_single_line = " | ".join(
        ln.strip()
        for ln in data.get("gradeHeader", "").splitlines()
        if ln.strip() and ln.strip() != "Next item"
    )
    lines = [
        f"# {data.get('itemNumber', '')}. {data.get('title', 'Quiz')}".lstrip(". "),
        "",
        f"- **Type:** {data.get('type', 'Quiz')}",
        f"- **URL:** {data.get('url', '')}",
        f"- **Grade Summary:** {grade_single_line}",
        "",
    ]
    for q in parse_quiz_questions(data):
        lines.append(f"## Question {q['number']} ({q['points']})")
        lines.append("")
        lines.append(q["prompt"])
        lines.append("")
        for opt in q["options"]:
            mark = "x" if opt.get("checked") else " "
            lines.append(f"- [{mark}] {opt.get('labelText', '')}")
        lines.append("")
        if q["feedback"]:
            fb = q["feedback"].replace("\n\n", " — ").replace("\n", " ")
            lines.append(f"**Feedback:** {fb}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def convert_item(raw_root: Path, json_archive: Path, item_meta: dict, sub_dir: str = "") -> Path:
    src_rel = item_meta["extractedJsonFile"]
    src_json = raw_root / src_rel
    if not src_json.exists():
        # Also allow reading directly from _json/ if re-running
        alt_json = json_archive / Path(src_rel).name
        if sub_dir:
            alt_json = json_archive / sub_dir / Path(src_rel).name
        src_json = alt_json

    data = load_json(src_json)
    itype = (data.get("type") or item_meta.get("type") or "").lower()
    notes = item_meta.get("notes", "")

    if "video" in itype or data.get("cues") or data.get("txtTranscript"):
        md_content = format_video_md(data, extra_notes=notes)
    elif "quiz" in itype or "assignment" in itype or data.get("inputs"):
        md_content = format_quiz_md(data)
    elif "lab" in itype or "app" in itype or data.get("cells"):
        md_content = format_lab_md(data)
    else:
        md_content = format_reading_md(data)

    target_rel = item_meta.get("targetMdFile") or f"{Path(src_rel).stem}.md"
    dst_md = raw_root / target_rel
    dst_md.parent.mkdir(parents=True, exist_ok=True)
    dst_md.write_text(md_content, encoding="utf-8")

    archive_dst = (json_archive / sub_dir / src_json.name) if sub_dir else (json_archive / src_json.name)
    archive_dst.parent.mkdir(parents=True, exist_ok=True)
    if src_json.resolve() != archive_dst.resolve() and src_json.exists():
        shutil.move(str(src_json), str(archive_dst))
    return dst_md


def convert_raw_dir(raw_dir: Path, index_name: str | None = None) -> None:
    if index_name:
        idx_path = raw_dir / index_name
    else:
        candidates = sorted(raw_dir.glob("MODULE_*_INDEX.json"))
        if not candidates:
            candidates = sorted((raw_dir / "_json").glob("MODULE_*_INDEX.json"))
        if not candidates:
            raise FileNotFoundError(f"No MODULE_*_INDEX.json found in {raw_dir}")
        idx_path = candidates[0]

    mod_idx = load_json(idx_path)
    mod_num = mod_idx.get("moduleNumber", 1)
    json_archive = raw_dir / "_json"
    json_archive.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Module {mod_num}: {mod_idx.get('moduleTitle', '')}",
        "",
        f"- **Course:** {mod_idx.get('courseTitle', '')} ({mod_idx.get('provider', '')})",
        f"- **Instructors:** {', '.join(mod_idx.get('instructors', []))}",
        f"- **Module URL:** {mod_idx.get('moduleUrl', '')}",
        f"- **Status:** {mod_idx.get('moduleCompletionStatus', '')}",
        "",
        "## Description",
        "",
        mod_idx.get("moduleDescription", ""),
        "",
        "## Learning Objectives",
        "",
    ]
    for obj in mod_idx.get("learningObjectives", []):
        lines.append(f"- {obj}")

    if mod_idx.get("structureNote"):
        lines.extend(["", "## Structure Note", "", mod_idx["structureNote"]])

    # Support flat `items` or nested `lessons`
    if mod_idx.get("items"):
        lines.extend(["", f"## Module {mod_num} Items (In Course Order)", "", "| # | Type | Title | Duration | Status | File |", "|---|---|---|---|---|---|"])
        for it in mod_idx["items"]:
            dst_md = convert_item(raw_dir, json_archive, it)
            dur = it.get("listedDuration", "")
            if it.get("exactDuration"):
                dur = f"{dur} ({it['exactDuration']})"
            rel_link = dst_md.relative_to(raw_dir).as_posix()
            lines.append(
                f"| {it['itemNumber']} | {it['type']} | {it['title']} | {dur} | {it.get('completionStatus', '')} | [{dst_md.name}]({rel_link}) |"
            )
    elif mod_idx.get("lessons"):
        lines.extend(["", "## Lessons & Items", ""])
        for lesson in mod_idx["lessons"]:
            folder = lesson.get("folderName", "")
            lines.append(f"### Lesson {lesson.get('lessonNumber', '')}: {lesson.get('lessonTitle', '')}")
            lines.append("")
            lines.append("| # | Type | Title | Duration | Status | File |")
            lines.append("|---|---|---|---|---|---|")
            for it in lesson.get("items", []):
                dst_md = convert_item(raw_dir, json_archive, it, sub_dir=folder)
                dur = it.get("listedDuration", "")
                if it.get("exactDuration"):
                    dur = f"{dur} ({it['exactDuration']})"
                rel_link = dst_md.relative_to(raw_dir).as_posix()
                lines.append(
                    f"| {it['itemNumber']} | {it['type']} | {it['title']} | {dur} | {it.get('completionStatus', '')} | [{dst_md.name}]({rel_link}) |"
                )
            lines.append("")

    md_index_path = raw_dir / f"MODULE_{mod_num}_INDEX.md"
    md_index_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    idx_archive = json_archive / idx_path.name
    if idx_path.resolve() != idx_archive.resolve() and idx_path.exists():
        shutil.move(str(idx_path), str(idx_archive))
    print(f"Converted Module {mod_num} JSONs -> Markdown at {raw_dir}")


def main():
    parser = argparse.ArgumentParser(description="Convert extracted Coursera module JSON files to Markdown.")
    parser.add_argument("--raw-dir", required=True, type=Path, help="Path to Module N/raw directory")
    parser.add_argument("--index", default=None, help="Optional index JSON filename")
    args = parser.parse_args()
    convert_raw_dir(args.raw_dir, args.index)


if __name__ == "__main__":
    main()
