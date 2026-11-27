"""Reusable python-docx layout primitives for Coursera Study Guides."""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

# Unified IBM/Coursera-inspired color palette
NAVY = RGBColor(0x0F, 0x29, 0x42)
BLUE = RGBColor(0x0F, 0x62, 0xFE)
TEAL = RGBColor(0x00, 0x7D, 0x79)
PURPLE = RGBColor(0x69, 0x29, 0xC4)
AMBER = RGBColor(0xB2, 0x50, 0x00)
GREEN = RGBColor(0x19, 0x80, 0x38)
RED = RGBColor(0xDA, 0x1E, 0x28)
SLATE = RGBColor(0x26, 0x26, 0x26)
MUTED = RGBColor(0x6F, 0x6F, 0x6F)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

HEX_NAVY = "0F2942"
HEX_BLUE = "0F62FE"
HEX_ICE = "EDF5FF"
HEX_ALT = "F4F7FB"
HEX_TEAL_BG = "E6FFFB"
HEX_TEAL = "007D79"
HEX_AMBER_BG = "FFF2E8"
HEX_AMBER = "B25000"
HEX_GREEN_BG = "DEFBE6"
HEX_GREEN = "198038"
HEX_PURPLE_BG = "F6F2FF"
HEX_PURPLE = "6929C4"
HEX_CODE_BG = "F4F6F8"
HEX_BORDER = "D0D7DE"


def create_study_guide(font_name: str = "Calibri", font_size: float = 10.5) -> Document:
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = font_name
    normal.font.size = Pt(font_size)
    normal.font.color.rgb = SLATE
    return doc


def set_cell_shading(cell, fill_hex: str) -> None:
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=140, right=140) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in [("top", top), ("bottom", bottom), ("left", left), ("right", right)]:
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, border_hex: str = HEX_BORDER) -> None:
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
        f'<w:left w:val="none"/><w:right w:val="none"/><w:insideV w:val="none"/>'
        f"</w:tblBorders>"
    )
    tblPr.append(borders)


def prevent_row_split(row) -> None:
    row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))


def repeat_header_row(row) -> None:
    row._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))


def add_field(run, field_text: str) -> None:
    fldChar1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls("w"))
    instrText = parse_xml(r'<w:instrText %s xml:space="preserve"> %s </w:instrText>' % (nsdecls("w"), field_text))
    fldChar2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls("w"))
    fldChar3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls("w"))
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def configure_header_footer(doc: Document, header_text: str, footer_left_text: str) -> None:
    sec = doc.sections[0]
    sec.page_width = Inches(8.5)
    sec.page_height = Inches(11.0)
    sec.top_margin = Inches(0.75)
    sec.bottom_margin = Inches(0.75)
    sec.left_margin = Inches(0.75)
    sec.right_margin = Inches(0.75)
    sec.different_first_page_header_footer = True

    hp = sec.header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hr = hp.add_run(header_text)
    hr.font.name = "Calibri"
    hr.font.size = Pt(8.8)
    hr.font.color.rgb = MUTED

    ftbl = sec.footer.add_table(rows=1, cols=2, width=Inches(7.0))
    ftbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0, c1 = ftbl.cell(0, 0), ftbl.cell(0, 1)
    c0.width = Inches(4.8)
    c1.width = Inches(2.2)
    r0 = c0.paragraphs[0].add_run(footer_left_text)
    r0.font.name = "Calibri"
    r0.font.size = Pt(8.8)
    r0.font.color.rgb = MUTED

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.add_run("Page ")
    add_field(p1.add_run(), "PAGE")
    p1.add_run(" of ")
    add_field(p1.add_run(), "NUMPAGES")
    for r in p1.runs:
        r.font.name = "Calibri"
        r.font.size = Pt(8.8)
        r.font.color.rgb = MUTED


def add_p(doc: Document, text: str = "", space_before=0, space_after=5, bold=False, italic=False, size=10.5, color=SLATE, align=WD_ALIGN_PARAGRAPH.LEFT, keep_with_next=False):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.18
    p.paragraph_format.keep_with_next = keep_with_next
    if text:
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        r.font.name = "Calibri"
        r.font.size = Pt(size)
        r.font.color.rgb = color
    return p


def add_bullet(doc: Document, lead: str, body: str, space_after=4):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.16
    if lead:
        r1 = p.add_run(lead)
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = NAVY
    r2 = p.add_run(body)
    r2.font.name = "Calibri"
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = SLATE
    return p


def add_code_block(doc: Document, code_text: str, language: str = "Python") -> None:
    """Render a syntax-styled code block inside a shaded container."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(7.0)
    cell = tbl.cell(0, 0)
    cell.width = Inches(7.0)
    set_cell_shading(cell, HEX_CODE_BG)
    set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(
        parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="16" w:space="0" w:color="{HEX_BLUE}"/>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
            f"</w:tcBorders>"
        )
    )
    prevent_row_split(tbl.rows[0])

    p_lang = cell.paragraphs[0]
    p_lang.paragraph_format.space_after = Pt(3)
    rl = p_lang.add_run(language.upper())
    rl.bold = True
    rl.font.name = "Calibri"
    rl.font.size = Pt(8.2)
    rl.font.color.rgb = BLUE

    p_code = cell.add_paragraph()
    p_code.paragraph_format.space_before = Pt(0)
    p_code.paragraph_format.space_after = Pt(0)
    p_code.paragraph_format.line_spacing = 1.08
    rc = p_code.add_run(code_text.rstrip())
    rc.font.name = "Consolas"
    rc.font.size = Pt(9.0)
    rc.font.color.rgb = SLATE

    add_p(doc, "", space_before=0, space_after=4)


def add_callout(doc: Document, title: str, lines: list[str], border_hex=HEX_BLUE, bg_hex=HEX_ICE, title_color=BLUE, trailing_space=True):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(7.0)
    cell = tbl.cell(0, 0)
    cell.width = Inches(7.0)
    set_cell_shading(cell, bg_hex)
    set_cell_margins(cell, top=110, bottom=110, left=180, right=150)
    cell._tc.get_or_add_tcPr().append(
        parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
            f'<w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/>'
            f"</w:tcBorders>"
        )
    )
    prevent_row_split(tbl.rows[0])

    p0 = cell.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(3)
    r0 = p0.add_run(title)
    r0.bold = True
    r0.font.name = "Calibri"
    r0.font.size = Pt(10.5)
    r0.font.color.rgb = title_color

    for i, ln in enumerate(lines):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(2 if i < len(lines) - 1 else 0)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(ln)
        r.font.name = "Calibri"
        r.font.size = Pt(10.0)
        r.font.color.rgb = SLATE

    if trailing_space:
        add_p(doc, "", space_before=0, space_after=4)


def add_styled_table(doc: Document, headers: list[str], rows: list[list[str]], col_widths: list[float], header_hex=HEX_NAVY, cell_pad=85, font_size=9.6, trailing_space=True):
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    set_table_borders(tbl)

    hdr_row = tbl.rows[0]
    repeat_header_row(hdr_row)
    prevent_row_split(hdr_row)
    for j, htext in enumerate(headers):
        cell = hdr_row.cells[j]
        cell.width = Inches(col_widths[j])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_shading(cell, header_hex)
        set_cell_margins(cell, top=cell_pad, bottom=cell_pad, left=105, right=105)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(htext)
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(font_size + 0.2)
        r.font.color.rgb = WHITE

    for i, row_data in enumerate(rows):
        row = tbl.rows[i + 1]
        prevent_row_split(row)
        bg = HEX_ALT if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = Inches(col_widths[j])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_shading(cell, bg)
            set_cell_margins(cell, top=cell_pad - 12, bottom=cell_pad - 12, left=105, right=105)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.12
            r = p.add_run(val)
            r.bold = (j == 0)
            r.font.name = "Calibri"
            r.font.size = Pt(font_size)
            r.font.color.rgb = NAVY if j == 0 else SLATE

    if trailing_space:
        add_p(doc, "", space_before=0, space_after=5)
    return tbl


def add_figure(doc: Document, img_path: Path, caption: str, width_in: float = 6.85) -> None:
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(6)
    p_img.paragraph_format.space_after = Pt(3)
    p_img.paragraph_format.keep_with_next = True
    p_img.add_run().add_picture(str(img_path), width=Inches(width_in))

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(8)
    r_cap = p_cap.add_run(caption)
    r_cap.italic = True
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(9.3)
    r_cap.font.color.rgb = MUTED


def add_section_heading(doc: Document, title: str, level: int = 1):
    h = doc.add_heading(title, level=level)
    h.paragraph_format.space_before = Pt(12 if level == 1 else 10)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    for r in h.runs:
        r.font.name = "Calibri"
        if level == 1:
            r.font.size = Pt(17)
            r.font.color.rgb = NAVY
            r.bold = True
        elif level == 2:
            r.font.size = Pt(13.5)
            r.font.color.rgb = BLUE
            r.bold = True
        else:
            r.font.size = Pt(11.5)
            r.font.color.rgb = TEAL
            r.bold = True
    return h


def add_subsection_banner(doc: Document, sub_num: str, title: str, item_type: str, duration: str, status: str, badge_hex: str = HEX_BLUE) -> None:
    add_section_heading(doc, f"{sub_num} {title}", level=2)
    tbl = doc.add_table(rows=1, cols=3)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    widths = [1.5, 2.2, 3.3]
    labels = [f"TYPE: {item_type.upper()}", f"DURATION: {duration}", f"STATUS: {status}"]
    for j in range(3):
        c = tbl.cell(0, j)
        c.width = Inches(widths[j])
        set_cell_shading(c, badge_hex if j == 0 else HEX_ALT)
        set_cell_margins(c, top=60, bottom=60, left=100, right=100)
        p = c.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(labels[j])
        r.bold = True
        r.font.name = "Calibri"
        r.font.size = Pt(9.0)
        r.font.color.rgb = WHITE if j == 0 else SLATE
    prevent_row_split(tbl.rows[0])
    set_table_borders(tbl, border_hex=HEX_BORDER)
    add_p(doc, "", space_before=0, space_after=2, keep_with_next=True)


def add_cover_banner(doc: Document, kicker: str, course_title: str, subtitle: str) -> None:
    banner = doc.add_table(rows=1, cols=1)
    banner.alignment = WD_TABLE_ALIGNMENT.CENTER
    banner.autofit = False
    banner.columns[0].width = Inches(7.0)
    bc = banner.cell(0, 0)
    bc.width = Inches(7.0)
    set_cell_shading(bc, HEX_NAVY)
    set_cell_margins(bc, top=220, bottom=220, left=220, right=220)

    p0 = bc.paragraphs[0]
    p0.paragraph_format.space_after = Pt(6)
    rk = p0.add_run(kicker)
    rk.bold = True
    rk.font.name = "Calibri"
    rk.font.size = Pt(10.5)
    rk.font.color.rgb = RGBColor(0x78, 0xA9, 0xFF)

    p1 = bc.add_paragraph()
    p1.paragraph_format.space_after = Pt(8)
    rc = p1.add_run(course_title)
    rc.bold = True
    rc.font.name = "Calibri"
    rc.font.size = Pt(22)
    rc.font.color.rgb = WHITE

    p2 = bc.add_paragraph()
    p2.paragraph_format.space_after = Pt(0)
    rm = p2.add_run(subtitle)
    rm.font.name = "Calibri"
    rm.font.size = Pt(13.5)
    rm.font.color.rgb = RGBColor(0xD0, 0xE2, 0xFF)

    add_p(doc, "", space_before=6, space_after=6)
