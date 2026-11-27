"""Export a .docx file to .pdf (via Microsoft Word COM on Windows or LibreOffice)
and render every page as PNG via PyMuPDF for visual layout verification.
"""

import argparse
import shutil
import subprocess
from pathlib import Path
import fitz


def export_pdf_word_com(docx_path: Path, pdf_path: Path) -> None:
    import win32com.client  # type: ignore

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        doc = word.Documents.Open(str(docx_path.resolve()), ReadOnly=True)
        doc.Fields.Update()
        doc.SaveAs(str(pdf_path.resolve()), FileFormat=17)  # wdFormatPDF
        doc.Close(False)
    finally:
        word.Quit()


def export_pdf_libreoffice(docx_path: Path, pdf_path: Path) -> None:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        raise RuntimeError("Neither Microsoft Word (win32com) nor LibreOffice (soffice) is available for PDF export.")
    out_dir = pdf_path.parent
    subprocess.run(
        [soffice, "--headless", "--convert-to", "pdf", "--outdir", str(out_dir), str(docx_path)],
        check=True,
    )
    generated = out_dir / f"{docx_path.stem}.pdf"
    if generated.resolve() != pdf_path.resolve() and generated.exists():
        shutil.move(str(generated), str(pdf_path))


def export_to_pdf(docx_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        export_pdf_word_com(docx_path, pdf_path)
    except Exception:
        export_pdf_libreoffice(docx_path, pdf_path)


def render_pdf_pages(pdf_path: Path, pages_dir: Path, dpi: int = 150) -> list[Path]:
    pages_dir.mkdir(parents=True, exist_ok=True)
    for old in pages_dir.glob("page_*.png"):
        old.unlink()

    doc = fitz.open(str(pdf_path))
    rendered = []
    try:
        for idx, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=dpi)
            out_png = pages_dir / f"page_{idx:02d}.png"
            pix.save(str(out_png))
            rendered.append(out_png)
    finally:
        doc.close()
    return rendered


def main():
    parser = argparse.ArgumentParser(description="Convert .docx to .pdf and render PNG previews per page.")
    parser.add_argument("docx_path", type=Path, help="Input .docx path")
    parser.add_argument("--export-pdf", type=Path, default=None, help="Output .pdf path (defaults next to .docx)")
    parser.add_argument("--pages-dir", type=Path, required=True, help="Directory to save rendered page PNGs")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for rendered page PNGs")
    args = parser.parse_args()

    pdf_path = args.export_pdf or args.docx_path.with_suffix(".pdf")
    export_to_pdf(args.docx_path, pdf_path)
    pages = render_pdf_pages(pdf_path, args.pages_dir, dpi=args.dpi)
    print(f"Exported PDF: {pdf_path} ({len(pages)} pages)")
    for p in pages:
        print(f"Rendered: {p.name}")


if __name__ == "__main__":
    main()
