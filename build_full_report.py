# -*- coding: utf-8 -*-
"""
Main Entry Point for HUIT Course Project Report Generator
Course: CÁC VẤN ĐỀ HIỆN ĐẠI TRONG TRÍ TUỆ NHÂN TẠO
Topic: MÔ HÌNH NGÔN NGỮ LỚN CHO PHÁT HIỆN TIN GIẢ VÀ KIỂM CHỨNG THÔNG TIN TIẾNG VIỆT
Team:
  - Nguyễn Hữu Trí (MSSV: 2045230111) - Nhóm trưởng
  - Võ Bạch Kim Thịnh (MSSV: 2045230096)
  - Trần Nguyên Khải (MSSV: 2045230048)
Instructor: TS. Trần Khải Thiện
"""

import os
import html
import docx
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml
import latex2mathml.converter
from lxml import etree

from build_report_data import (
    ABBREVIATIONS, TEAM_MEMBERS, DATASET_SURVEY_TABLE,
    BASELINES_SURVEY_TABLE, RETRIEVAL_RESULTS_TABLE,
    VERDICT_RESULTS_TABLE, PER_CLASS_METRICS_TABLE,
    PROMPT_ABLATION_TABLE, CASE_STUDIES_TABLE, REFERENCES_LIST
)
from build_chapters import build_all_chapters

print("Starting document creation...")

# ============================================================
# 1. Setup Document and Page Geometry
# ============================================================
doc = docx.Document()

# Configure Settings for Automatic Field Updates (TOC, page numbers)
doc.settings.element.append(parse_xml(
    r'<w:updateFields xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="true"/>'
))

# MathML to OMML Transformer
xsl_path = r'C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL'
xslt = etree.parse(xsl_path)
transform = etree.XSLT(xslt)

def latex_to_omml(latex_code):
    mml = latex2mathml.converter.convert(latex_code)
    tree = etree.fromstring(mml)
    omml = transform(tree)
    return etree.tostring(omml, encoding='utf-8').decode('utf-8')

def add_equation_table(latex_code, eq_number=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    omml_xml = latex_to_omml(latex_code)
    omml_para = f'<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{omml_xml}</m:oMathPara>'
    p._element.append(parse_xml(omml_para))
    return p

COLOR_PRIMARY = RGBColor(0, 0, 0)   # Standard Black matching DACN01_VuPhuLoc.docx
COLOR_TEXT = RGBColor(0, 0, 0)

def style_heading_1(text):
    p = doc.add_paragraph(style='Heading 1')
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.line_spacing = 1.2
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    return p

def style_heading_2(text):
    p = doc.add_paragraph(style='Heading 2')
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.line_spacing = 1.2
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_PRIMARY
    return p

def style_heading_3(text):
    p = doc.add_paragraph(style='Heading 3')
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.line_spacing = 1.2
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.italic = True
    run.font.color.rgb = COLOR_TEXT
    return p

def add_body_p(text="", bold_prefix=None, italic=False, space_after=4):
    p = doc.add_paragraph(style='Normal')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.first_line_indent = Inches(0.5)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.3
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(13)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_TEXT
        
    if text:
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.font.italic = italic
        r.font.color.rgb = COLOR_TEXT
    return p

def add_bullet_p(text, bold_prefix=None):
    p = doc.add_paragraph(style='Normal')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.25
    
    r_bullet = p.add_run("•  ")
    r_bullet.font.name = 'Times New Roman'
    r_bullet.font.size = Pt(13)
    r_bullet.font.bold = True
    r_bullet.font.color.rgb = COLOR_PRIMARY
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Times New Roman'
        r_pre.font.size = Pt(13)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_TEXT
        
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.color.rgb = COLOR_TEXT
    return p

def add_table_caption(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.italic = True
    r.font.color.rgb = COLOR_PRIMARY
    return p

def add_figure(image_path, caption_text, width_inches=5.8):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(4)
    p_img.paragraph_format.keep_with_next = True
    run = p_img.add_run()
    run.add_picture(image_path, width=Inches(width_inches))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(3)
    p_cap.paragraph_format.space_after = Pt(10)
    r_cap = p_cap.add_run(caption_text)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(11.5)
    r_cap.font.bold = True
    r_cap.font.italic = True
    r_cap.font.color.rgb = COLOR_PRIMARY
    return p_img, p_cap

def format_table(table, col_widths, col_alignments=None, font_size=11):
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    header_row = table.rows[0]
    trPr = header_row._tr.get_or_add_trPr()
    trPr.append(parse_xml(r'<w:tblHeader xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
    
    for i, cell in enumerate(header_row.cells):
        cell.width = Inches(col_widths[i])
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.font.size = Pt(font_size)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0, 0, 0)
            
    for row_idx, row in enumerate(table.rows[1:]):
        for col_idx, cell in enumerate(row.cells):
            cell.width = Inches(col_widths[col_idx])
            p = cell.paragraphs[0]
            if col_alignments and col_idx < len(col_alignments):
                p.alignment = col_alignments[col_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(font_size)
                r.font.color.rgb = RGBColor(0, 0, 0)

def add_leader_tab_entry(p_or_doc, title, page_num, level=0, is_bold=False, font_size=11.5):
    """Adds a paragraph with right-aligned dot leader tab stop for figures/tables/lists."""
    p = p_or_doc.add_paragraph() if hasattr(p_or_doc, 'add_paragraph') else p_or_doc
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    # Text area width = 9070 dxa (approx 6.3 inches)
    pPr = p._element.get_or_add_pPr()
    tabs_xml = r'<w:tabs xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:tab w:val="right" w:leader="dot" w:pos="9070"/></w:tabs>'
    pPr.append(parse_xml(tabs_xml))
    
    if level > 0:
        p.paragraph_format.left_indent = Inches(0.25 * level)
        
    r_tit = p.add_run(title)
    r_tit.font.name = 'Times New Roman'
    r_tit.font.size = Pt(font_size)
    r_tit.font.bold = is_bold
    r_tit.font.color.rgb = COLOR_TEXT
    
    r_tab = p.add_run()
    r_tab.font.name = 'Times New Roman'
    r_tab._element.append(parse_xml(r'<w:tab xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>'))
    
    r_p = p.add_run(str(page_num))
    r_p.font.name = 'Times New Roman'
    r_p.font.size = Pt(font_size)
    r_p.font.bold = is_bold
    r_p.font.color.rgb = COLOR_TEXT
    return p

# ============================================================
# 2. SECTION 0: BÌA CHÍNH VÀ BÌA PHỤ (COVER PAGES)
# ============================================================
sec0 = doc.sections[0]
sec0.top_margin = Pt(56.7)
sec0.bottom_margin = Pt(56.7)
sec0.left_margin = Pt(85.05)
sec0.right_margin = Pt(56.7)
sec0.header.is_linked_to_previous = False
sec0.footer.is_linked_to_previous = False

# Note: pgBorders will be attached to sec0 after all sections are created,
# to prevent python-docx from cloning borders into subsequent sections.

logo_path = r'E:\VanDe_AI\docs\assets\huit_logo.jpeg'

def render_main_cover():
    """Render Bìa Chính (Outer Cover Page)"""
    def add_p(text, font_size=13, bold=True, space_before=0, space_after=2, color=COLOR_TEXT):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.color.rgb = color
        return p

    add_p("BỘ CÔNG THƯƠNG", font_size=14, bold=True, space_before=10)
    add_p("TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP. HỒ CHÍ MINH", font_size=15, bold=True)
    add_p("KHOA CÔNG NGHỆ THÔNG TIN", font_size=14, bold=True)
    add_p("----o0o----", font_size=14, bold=False, space_after=14)
    
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(14)
    run_img = p_img.add_run()
    run_img.add_picture(logo_path, width=Inches(2.2))
    
    add_p("BÁO CÁO ĐỒ ÁN MÔN HỌC", font_size=16, bold=True, space_before=6, color=COLOR_PRIMARY)
    add_p("CÁC VẤN ĐỀ HIỆN ĐẠI TRONG TRÍ TUỆ NHÂN TẠO", font_size=15, bold=True, color=COLOR_PRIMARY)
    add_p("ĐỀ TÀI:", font_size=13, bold=True, space_before=10)
    
    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_before = Pt(4)
    p_topic.paragraph_format.space_after = Pt(20)
    p_topic.paragraph_format.line_spacing = 1.25
    r_t = p_topic.add_run("MÔ HÌNH NGÔN NGỮ LỚN CHO PHÁT HIỆN TIN GIẢ\nVÀ KIỂM CHỨNG THÔNG TIN TIẾNG VIỆT")
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(18)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_PRIMARY
    
    tbl_info = doc.add_table(rows=5, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_info.autofit = False
    
    tPr = tbl_info._tbl.tblPr
    tPr.append(parse_xml(r'''
        <w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
            <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>
            <w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tblBorders>
    '''))
    
    info_rows = [
        ("GIẢNG VIÊN HƯỚNG DẪN:", "TS. TRẦN KHẢI THIỆN"),
        ("SINH VIÊN THỰC HIỆN:", "1. Nguyễn Hữu Trí     - MSSV: 2045230111 (Nhóm trưởng)"),
        ("", "2. Võ Bạch Kim Thịnh - MSSV: 2045230096"),
        ("", "3. Trần Nguyên Khải  - MSSV: 2045230048"),
        ("CHUYÊN NGÀNH:", "Khoa học Dữ liệu / Trí tuệ Nhân tạo")
    ]
    
    for idx, (label, val) in enumerate(info_rows):
        row = tbl_info.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.6)
        cell_val.width = Inches(3.8)
        
        p_l = cell_lbl.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_l.paragraph_format.space_before = Pt(1)
        p_l.paragraph_format.space_after = Pt(1)
        r_l = p_l.add_run(label)
        r_l.font.name = 'Times New Roman'
        r_l.font.size = Pt(12.5)
        r_l.font.bold = True
        
        p_v = cell_val.paragraphs[0]
        p_v.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_v.paragraph_format.space_before = Pt(1)
        p_v.paragraph_format.space_after = Pt(1)
        r_v = p_v.add_run(val)
        r_v.font.name = 'Times New Roman'
        r_v.font.size = Pt(12.5)
        r_v.font.bold = (idx == 0 or "Nhóm trưởng" in val)

    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(18)
    add_p("TP. HỒ CHÍ MINH, THÁNG 09 NĂM 2026", font_size=13, bold=True, space_before=15)

def render_sub_cover():
    """Render Bìa Phụ (Inner Sub-Cover Page)"""
    def add_p(text, font_size=13, bold=True, space_before=0, space_after=2, color=COLOR_TEXT):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.color.rgb = color
        return p

    add_p("BỘ CÔNG THƯƠNG", font_size=13.5, bold=True, space_before=8)
    add_p("TRƯỜNG ĐẠI HỌC CÔNG THƯƠNG TP. HỒ CHÍ MINH", font_size=14.5, bold=True)
    add_p("KHOA CÔNG NGHỆ THÔNG TIN - BỘ MÔN TRÍ TUỆ NHÂN TẠO", font_size=13, bold=True)
    add_p("----o0o----", font_size=13, bold=False, space_after=10)
    
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(2)
    p_img.paragraph_format.space_after = Pt(10)
    run_img = p_img.add_run()
    run_img.add_picture(logo_path, width=Inches(1.8))
    
    add_p("BÁO CÁO ĐỒ ÁN MÔN HỌC (BÌA PHỤ)", font_size=15, bold=True, space_before=4, color=COLOR_PRIMARY)
    add_p("HỌC PHẦN: CÁC VẤN ĐỀ HIỆN ĐẠI TRONG TRÍ TUỆ NHÂN TẠO", font_size=14, bold=True, color=COLOR_PRIMARY)
    add_p("ĐỀ TÀI:", font_size=12.5, bold=True, space_before=6)
    
    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_before = Pt(2)
    p_topic.paragraph_format.space_after = Pt(4)
    p_topic.paragraph_format.line_spacing = 1.2
    r_t = p_topic.add_run("MÔ HÌNH NGÔN NGỮ LỚN CHO PHÁT HIỆN TIN GIẢ\nVÀ KIỂM CHỨNG THÔNG TIN TIẾNG VIỆT")
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(16.5)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_PRIMARY
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("(VIETNAMESE FACT-CHECKING & FAKE NEWS VERIFICATION USING LLMS)")
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(80, 80, 80)
    
    tbl_info = doc.add_table(rows=6, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_info.autofit = False
    
    tPr = tbl_info._tbl.tblPr
    tPr.append(parse_xml(r'''
        <w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
            <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>
            <w:insideH w:val="none"/><w:insideV w:val="none"/>
        </w:tblBorders>
    '''))
    
    info_rows = [
        ("GIẢNG VIÊN HƯỚNG DẪN:", "TS. TRẦN KHẢI THIỆN"),
        ("SINH VIÊN THỰC HIỆN:", "1. Nguyễn Hữu Trí - MSSV: 2045230111\n    Email: nguyenhuutri868@gmail.com (Nhóm trưởng)"),
        ("", "2. Võ Bạch Kim Thịnh - MSSV: 2045230096\n    Email: bizero1424@gmail.com"),
        ("", "3. Trần Nguyên Khải - MSSV: 2045230048\n    Email: khaitran17635@gmail.com"),
        ("CHUYÊN NGÀNH:", "Khoa học Dữ liệu / Trí tuệ Nhân tạo"),
        ("KHÓA HỌC / NIÊN KHÓA:", "Đại học chính quy Khóa 13 (2023 - 2027)")
    ]
    
    for idx, (label, val) in enumerate(info_rows):
        row = tbl_info.rows[idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.5)
        cell_val.width = Inches(3.9)
        
        p_l = cell_lbl.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_l.paragraph_format.space_before = Pt(1)
        p_l.paragraph_format.space_after = Pt(1)
        r_l = p_l.add_run(label)
        r_l.font.name = 'Times New Roman'
        r_l.font.size = Pt(11.5)
        r_l.font.bold = True
        
        p_v = cell_val.paragraphs[0]
        p_v.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_v.paragraph_format.space_before = Pt(1)
        p_v.paragraph_format.space_after = Pt(1)
        r_v = p_v.add_run(val)
        r_v.font.name = 'Times New Roman'
        r_v.font.size = Pt(11.5)
        r_v.font.bold = (idx == 0 or "Nhóm trưởng" in val)

    p_sig_box = doc.add_paragraph()
    p_sig_box.paragraph_format.space_before = Pt(14)
    p_sig_box.paragraph_format.space_after = Pt(2)
    r_sb = p_sig_box.add_run("CÁN BỘ CHẤM 1: .......................................            CÁN BỘ CHẤM 2: .......................................")
    r_sb.font.name = 'Times New Roman'
    r_sb.font.size = Pt(11)
    r_sb.font.bold = True
    p_sig_box.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_p("TP. HỒ CHÍ MINH, THÁNG 09 NĂM 2026", font_size=12.5, bold=True, space_before=12)

render_main_cover()
doc.add_page_break()
render_sub_cover()

# ============================================================
# 3. SECTION 1: TRANG SƠ BỘ (FRONT MATTER - ROMAN i, ii, iii...)
# ============================================================
sec1 = doc.add_section(WD_SECTION_START.NEW_PAGE)
sec1.top_margin = Pt(56.7)
sec1.bottom_margin = Pt(56.7)
sec1.left_margin = Pt(85.05)
sec1.right_margin = Pt(56.7)
sec1.header.is_linked_to_previous = False
sec1.footer.is_linked_to_previous = False

sectPr1 = sec1._sectPr
for elem in sectPr1.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgBorders'):
    sectPr1.remove(elem)
pgNumType1 = parse_xml(r'<w:pgNumType xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fmt="lowerRoman" w:start="1"/>')
sectPr1.append(pgNumType1)

f_p1 = sec1.footer.paragraphs[0]
f_p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
f_run1 = f_p1.add_run()
f_run1.font.name = 'Times New Roman'
f_run1.font.size = Pt(11)
f_run1._element.append(parse_xml(r'<w:fldSimple xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:instr="PAGE"/>'))

# 3.1. LỜI CAM ĐOAN
style_heading_1("LỜI CAM ĐOAN")
add_body_p("Nhóm sinh viên thực hiện đồ án môn học với đề tài: “Mô hình ngôn ngữ lớn cho phát hiện tin giả và kiểm chứng thông tin tiếng Việt”, xin cam đoan một cách danh dự và nghiêm túc rằng:")
add_bullet_p("Đồ án môn học này là công trình nghiên cứu độc lập, nghiêm túc của tập thể các thành viên trong nhóm dưới sự dẫn dắt, định hướng chuyên môn của Giảng viên hướng dẫn TS. Trần Khải Thiện.", bold_prefix="1. Tính nguyên bản: ")
add_bullet_p("Toàn bộ dữ liệu, mã nguồn thí nghiệm, các kết quả đánh giá định lượng (Accuracy, Macro-F1, Strict FEVER Score) và các hình vẽ biểu đồ trình bày trong báo cáo đều được thực thi trung thực trên các bộ benchmark chuẩn công bố (ViWikiFC, ViFactCheck, ReINTEL) và môi trường thực nghiệm của nhóm, không có bất kỳ hành vi ngụy tạo hay bóp méo dữ liệu.", bold_prefix="2. Tính trung thực dữ liệu: ")
add_bullet_p("Các tài liệu tham khảo, các định dạng thuật toán (BM25, BGE-M3, RRF, Cross-Encoder, QLoRA) và các baseline đối sánh (SemViQA, ViFactCheck AAAI-25, ReINTEL VLSP-20, Program-FC) đều được trích dẫn nguồn gốc học thuật xuất bản một cách minh bạch, đầy đủ theo chuẩn IEEE.", bold_prefix="3. Trích dẫn học thuật: ")
add_bullet_p("Nội dung báo cáo chưa từng được công bố để nhận học vị hay chứng chỉ tại bất kỳ cơ sở đào tạo nào khác.", bold_prefix="4. Trách nhiệm học thuật: ")
add_body_p("Nhóm xin chịu mọi trách nhiệm cá nhân và tập thể trước Hội đồng chấm đồ án, Bộ môn Trí tuệ Nhân tạo và Khoa Công nghệ Thông tin - Trường Đại học Công Thương TP. Hồ Chí Minh nếu phát hiện bất kỳ sự gian lận nào.")

p_sig = doc.add_paragraph()
p_sig.paragraph_format.space_before = Pt(20)
p_sig.paragraph_format.space_after = Pt(4)

tbl_sig = doc.add_table(rows=3, cols=2)
tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_sig.autofit = False
tbl_sig._tbl.tblPr.append(parse_xml(r'''
    <w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
        <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>
        <w:insideH w:val="none"/><w:insideV w:val="none"/>
    </w:tblBorders>
'''))
c0, c1 = tbl_sig.cell(0, 0), tbl_sig.cell(0, 1)
c0.width = Inches(3.2)
c1.width = Inches(3.2)
p0 = c0.paragraphs[0]
p1 = c1.paragraphs[0]
p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
p1.alignment = WD_ALIGN_PARAGRAPH.CENTER

r1_date = p1.add_run("TP. Hồ Chí Minh, ngày 16 tháng 09 năm 2026\nĐại diện tập thể sinh viên thực hiện\n")
r1_date.font.name = 'Times New Roman'
r1_date.font.size = Pt(12)
r1_date.font.italic = True
r1_tit = p1.add_run("Nhóm trưởng\n\n\n\n")
r1_tit.font.name = 'Times New Roman'
r1_tit.font.size = Pt(12.5)
r1_tit.font.bold = True
r1_name = p1.add_run("Nguyễn Hữu Trí\n(Ký và ghi rõ họ tên)")
r1_name.font.name = 'Times New Roman'
r1_name.font.size = Pt(12)
r1_name.font.bold = True

r0_mem = p0.add_run("\nThành viên đồng thực hiện\n\n\n\n")
r0_mem.font.name = 'Times New Roman'
r0_mem.font.size = Pt(12.5)
r0_mem.font.bold = True
r0_names = p0.add_run("Võ Bạch Kim Thịnh  –  Trần Nguyên Khải\n(Ký và ghi rõ họ tên)")
r0_names.font.name = 'Times New Roman'
r0_names.font.size = Pt(12)
r0_names.font.bold = True

doc.add_page_break()

# 3.2. LỜI CẢM ƠN
style_heading_1("LỜI CẢM ƠN")
add_body_p("Để hoàn thành đồ án môn học “Các vấn đề hiện đại trong Trí tuệ Nhân tạo” với đề tài nghiên cứu chuyên sâu về ứng dụng Mô hình Ngôn ngữ Lớn trong Kiểm chứng thông tin và Phát hiện tin giả tiếng Việt, nhóm chúng em đã nhận được sự quan tâm, chỉ dẫn tận tình và tạo mọi điều kiện thuận lợi nhất từ phía các Thầy Cô giáo và Nhà trường.")
add_body_p("Lời đầu tiên, nhóm chúng em xin được bày tỏ lòng biết ơn sâu sắc và chân thành nhất tới Thầy TS. Trần Khải Thiện – Giảng viên trực tiếp phụ trách và giảng dạy học phần. Trong suốt thời gian diễn ra học phần, Thầy không chỉ trang bị cho chúng em những nền tảng lý thuyết vững chắc về các mô hình AI tiên tiến, học sâu đa phương thức và xử lý ngôn ngữ tự nhiên hiện đại, mà còn định hướng đề tài nghiên cứu bám sát các công bố khoa học quốc tế uy tín (AAAI, ACL, EMNLP). Sự tận tâm theo dõi, những phản biện sắc bén và các góp ý định hướng về phương pháp tiếp cận RAG, kỹ nghệ Prompting và cơ chế phân loại hai bước TVC đã giúp chúng em vượt qua nhiều nút thắt kỹ thuật khó khăn để hoàn thiện hệ thống.")
add_body_p("Nhóm chúng em cũng xin chân thành cảm ơn Ban Giám hiệu Trường Đại học Công Thương TP. Hồ Chí Minh (HUIT), Ban Chủ nhiệm Khoa Công nghệ Thông tin cùng quý Thầy Cô giảng viên trong Khoa đã luôn tạo môi trường học tập, nghiên cứu năng động, hỗ trợ cơ sở vật chất và truyền cảm hứng say mê nghiên cứu khoa học cho sinh viên.")
add_body_p("Mặc dù nhóm đã nỗ lực hết mình với tinh thần làm việc nghiêm túc, khoa học và cầu thị, song do giới hạn về mặt thời gian cũng như nguồn lực tính toán GPU trong phạm vi một đồ án môn học, báo cáo chắc chắn khó tránh khỏi những thiếu sót nhất định. Nhóm rất mong nhận được những nhận xét, góp ý quý báu từ Thầy TS. Trần Khải Thiện và Hội đồng để đề tài có thể tiếp tục được phát triển và nâng cao chất lượng hơn nữa trong tương lai.")
add_body_p("Chúng em xin kính chúc Thầy dồi dào sức khỏe, hạnh phúc và gặt hái thêm nhiều thành tựu rực rỡ trong sự nghiệp nghiên cứu khoa học và giảng dạy cao quý!")

p_end_ack = doc.add_paragraph()
p_end_ack.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_end_ack.paragraph_format.space_before = Pt(14)
r_ack = p_end_ack.add_run("Tập thể nhóm sinh viên thực hiện đề tài\nNguyễn Hữu Trí – Võ Bạch Kim Thịnh – Trần Nguyên Khải")
r_ack.font.name = 'Times New Roman'
r_ack.font.size = Pt(12)
r_ack.font.bold = True
r_ack.font.italic = True

doc.add_page_break()

# 3.3. NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN
style_heading_1("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN")
add_body_p("TS. Trần Khải Thiện", bold_prefix="Họ và tên Giảng viên: ")
add_body_p("Các vấn đề hiện đại trong Trí tuệ Nhân tạo", bold_prefix="Môn học: ")
add_body_p("Mô hình ngôn ngữ lớn cho phát hiện tin giả và kiểm chứng thông tin tiếng Việt", bold_prefix="Tên đề tài: ")
add_body_p("1. Nguyễn Hữu Trí (2045230111) | 2. Võ Bạch Kim Thịnh (2045230096) | 3. Trần Nguyên Khải (2045230048)", bold_prefix="Sinh viên thực hiện: ")

add_body_p("Ý KIẾN NHẬN XÉT VÀ ĐÁNH GIÁ:", bold_prefix=None, italic=True)
for _ in range(14):
    p_dot = doc.add_paragraph()
    p_dot.paragraph_format.space_before = Pt(2)
    p_dot.paragraph_format.space_after = Pt(2)
    r_d = p_dot.add_run("………………………………………………………………………………………………………………………………………………")
    r_d.font.name = 'Times New Roman'
    r_d.font.size = Pt(11)

p_gv_sig = doc.add_paragraph()
p_gv_sig.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_gv_sig.paragraph_format.space_before = Pt(18)
r_gv_s = p_gv_sig.add_run("TP. Hồ Chí Minh, ngày ..... tháng ..... năm 2026\nGIẢNG VIÊN HƯỚNG DẪN\n(Ký và ghi rõ họ tên)\n\n\n\nTS. TRẦN KHẢI THIỆN")
r_gv_s.font.name = 'Times New Roman'
r_gv_s.font.size = Pt(12)
r_gv_s.font.bold = True

doc.add_page_break()

# 3.4. BẢNG PHÂN CÔNG CÔNG VIỆC
style_heading_1("BẢNG PHÂN CÔNG CÔNG VIỆC")
add_body_p("Để đảm bảo tiến độ và chất lượng khoa học cao nhất của đồ án môn học, nhóm đã phân công nhiệm vụ cụ thể dựa trên năng lực và thế mạnh chuyên môn của từng thành viên, đồng thời duy trì sự phối hợp chặt chẽ trong từng giai đoạn:")

tbl_work = doc.add_table(rows=4, cols=4)
tbl_work.rows[0].cells[0].paragraphs[0].text = "STT"
tbl_work.rows[0].cells[1].paragraphs[0].text = "Tên"
tbl_work.rows[0].cells[2].paragraphs[0].text = "Mã số sinh viên"
tbl_work.rows[0].cells[3].paragraphs[0].text = "Công việc thực hiện"

work_data = [
    ("1", "Võ Bạch Kim Thịnh", "2045230096", "Viết rõ bài toán, mục tiêu, phạm vi nghiên cứu; Phân định bản chất khoa học giữa Fake News Detection và Fact Verification; Khảo sát toàn diện 7 mô hình Baseline (kiến trúc, số liệu công bố, đối chuẩn so sánh)."),
    ("2", "Trần Nguyên Khải", "2045230048", "Khảo sát và phân tích sâu 6 bộ dữ liệu; Mô tả chi tiết ViWikiFC, ViFactCheck (nguồn gốc, quy mô, nhãn, cách chia tập train/val/test); Thực hiện quy trình chuẩn hóa Data Harmonization; Trình bày các bảng số liệu thực nghiệm và biểu đồ."),
    ("3", "Nguyễn Hữu Trí (Nhóm trưởng)", "2045230111", "Xây dựng kiến trúc Pipeline hệ thống SER + TVC + RAG; Thiết kế thuật toán lai ghép BM25+BGE-M3+RRF+Reranker; Xây dựng bộ phân loại hai bước TVC; Tối ưu hóa LLM Qwen2.5-7B (4-bit NF4) và tổng hợp báo cáo.")
]

for idx, (stt, name, mssv, task) in enumerate(work_data):
    r_cells = tbl_work.rows[idx+1].cells
    r_cells[0].paragraphs[0].text = stt
    r_cells[1].paragraphs[0].text = name
    r_cells[2].paragraphs[0].text = mssv
    r_cells[3].paragraphs[0].text = task

format_table(tbl_work, [0.5, 1.8, 1.3, 2.9], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.JUSTIFY], font_size=10.5)

doc.add_page_break()

# 3.5. MỤC LỤC
p_toc_heading = doc.add_paragraph()
p_toc_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_toc_heading.paragraph_format.space_before = Pt(14)
p_toc_heading.paragraph_format.space_after = Pt(10)
p_toc_heading.paragraph_format.keep_with_next = True
r_th = p_toc_heading.add_run("MỤC LỤC")
r_th.font.name = 'Times New Roman'
r_th.font.size = Pt(16)
r_th.font.bold = True
r_th.font.color.rgb = COLOR_PRIMARY

toc_entries = [
    ("LỜI CAM ĐOAN", "i", 0),
    ("LỜI CẢM ƠN", "ii", 0),
    ("NHẬN XÉT CỦA GIẢNG VIÊN HƯỚNG DẪN", "iii", 0),
    ("BẢNG PHÂN CÔNG CÔNG VIỆC", "iv", 0),
    ("MỤC LỤC", "v", 0),
    ("DANH MỤC CÁC KÝ HIỆU VÀ CHỮ VIẾT TẮT", "vi", 0),
    ("DANH MỤC HÌNH ẢNH", "vii", 0),
    ("DANH MỤC BẢNG BIỂU", "viii", 0),
    ("CHƯƠNG 1: MỞ ĐẦU", "1", 0),
    ("1.1. Bối cảnh và Tính cấp thiết của đề tài", "1", 1),
    ("1.2. Phân định bản chất khoa học: Phát hiện tin giả vs. Kiểm chứng thông tin", "2", 1),
    ("1.3. Mục tiêu nghiên cứu", "3", 1),
    ("1.3.1. Mục tiêu khoa học", "3", 2),
    ("1.3.2. Mục tiêu thực tiễn", "4", 2),
    ("1.4. Đối tượng và Phạm vi nghiên cứu", "4", 1),
    ("1.5. Đóng góp chính của đề tài", "4", 1),
    ("1.6. Bố cục của báo cáo đồ án", "5", 1),
    ("CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ CÁC CÔNG TRÌNH LIÊN QUAN", "6", 0),
    ("2.1. Hệ thống kiểm chứng thông tin (Fact Verification) và Bài toán FEVER", "6", 1),
    ("2.2. Kiến trúc Retrieval-Augmented Generation (RAG)", "7", 1),
    ("2.3. Thuật toán truy xuất từ vựng BM25 (Best Matching 25)", "8", 1),
    ("2.4. Mô hình biểu diễn ngữ nghĩa đa ngôn ngữ BGE-M3", "9", 1),
    ("2.5. Dung hợp thứ hạng nghịch đảo (Reciprocal Rank Fusion - RRF)", "10", 1),
    ("2.6. Tái xếp hạng bằng Cross-Encoder Reranker", "11", 1),
    ("2.7. Mô hình Qwen2.5-7B-Instruct và Kỹ thuật lượng tử hóa 4-bit NF4", "12", 1),
    ("2.8. Thách thức đặc thù trong Xử lý ngôn ngữ tự nhiên tiếng Việt", "13", 1),
    ("2.8.1. Phân định ranh giới từ (Word Segmentation)", "13", 2),
    ("2.8.2. Dấu thanh điệu và Chuẩn hóa Unicode", "13", 2),
    ("2.8.3. Khan hiếm tài nguyên ngữ liệu kiểm chứng", "14", 2),
    ("2.9. Khảo sát toàn diện các Baseline và Công trình liên quan", "14", 1),
    ("2.9.1. Baseline 1: BM25 + InfoXLM-Large (ViWikiFC gốc)", "14", 2),
    ("2.9.2. Baseline 2: SemViQA / SemViQA Faster (SOTA ViWikiFC)", "15", 2),
    ("2.9.3. Baseline 3: ViFactCheck Baseline (AAAI 2025)", "15", 2),
    ("2.9.4. Baseline 4: ReINTEL SOTA Baseline (VLSP 2020)", "16", 2),
    ("2.9.5. Baseline 5: Program-FC (ACL 2023)", "16", 2),
    ("2.9.6. Baseline 6: Self-Checker / RAG-FactLLM (2024)", "17", 2),
    ("2.9.7. Baseline 7: LLM Direct Prompting (Ablation)", "17", 2),
    ("CHƯƠNG 3: DỮ LIỆU THỰC NGHIỆM VÀ QUY TRÌNH TIỀN XỬ LÝ", "18", 0),
    ("3.1. Khảo sát các bộ dữ liệu Fact-Checking và Fake News đã công bố", "18", 1),
    ("3.2. Tập dữ liệu ViWikiFC (Bách khoa toàn thư Wikipedia)", "19", 1),
    ("3.3. Tập dữ liệu ViFactCheck (Báo chí chính thống đa lĩnh vực - AAAI 2025)", "20", 1),
    ("3.4. Quy trình Chuẩn hóa và Hợp nhất dữ liệu (Data Harmonization)", "21", 1),
    ("3.5. Xây dựng Kho ngữ liệu tri thức thống nhất (Unified Evidence Corpus)", "22", 1),
    ("CHƯƠNG 4: PHƯƠNG PHÁP ĐỀ XUẤT: HỆ THỐNG SER + TVC + RAG", "23", 0),
    ("4.1. Kiến trúc tổng thể hệ thống", "23", 1),
    ("4.2. Mô-đun Truy xuất bằng chứng ngữ nghĩa (Semantic Evidence Retrieval - SER)", "24", 1),
    ("4.2.1. Sparse Retrieval với BM25Okapi", "24", 2),
    ("4.2.2. Dense Retrieval với BGE-M3 + FAISS", "24", 2),
    ("4.2.3. Dung hợp thứ hạng nghịch đảo RRF", "25", 2),
    ("4.2.4. Neural Cross-Encoder Reranking", "25", 2),
    ("4.3. Mô-đun Phân loại phán quyết hai bước (Two-step Verdict Classification - TVC)", "26", 1),
    ("4.3.1. Phân tích nguyên nhân thất bại phân loại 3 nhãn trực tiếp", "26", 2),
    ("4.3.2. Bước 1: Bộ lọc tính đầy đủ (Sufficiency Filter)", "26", 2),
    ("4.3.3. Bước 2: Xác minh lập trường (Stance Verification)", "27", 2),
    ("4.3.4. Thiết kế kỹ nghệ Prompting Few-shot tiếng Việt", "27", 2),
    ("4.4. Mô-đun RAG Rationale Generation và Trích xuất có cấu trúc (Pydantic)", "28", 1),
    ("CHƯƠNG 5: KẾT QUẢ THỰC NGHIỆM VÀ ĐÁNH GIÁ", "30", 0),
    ("5.1. Thiết lập thực nghiệm và Siêu tham số", "30", 1),
    ("5.2. Kết quả đánh giá mô-đun Truy xuất bằng chứng (SER)", "31", 1),
    ("5.3. Kết quả đánh giá mô-đun Phân loại phán quyết (TVC)", "32", 1),
    ("5.4. Nghiên cứu thành phần (Ablation Study)", "33", 1),
    ("5.5. So sánh hiệu quả các chiến lược kỹ nghệ Prompting", "34", 1),
    ("5.6. Phân tích định tính và Nghiên cứu trường hợp điển hình (Case Studies)", "35", 1),
    ("5.6.1. Ca 1: Phán quyết SUPPORTED (Kiểm chứng tri thức bách khoa)", "35", 2),
    ("5.6.2. Ca 2: Phán quyết REFUTED (Phát hiện tin xuyên tạc sự thật)", "35", 2),
    ("5.6.3. Ca 3: Phán quyết NOT ENOUGH INFO (Lọc thiếu căn cứ)", "36", 2),
    ("5.6.4. Ca 4: Phân tích sai sót (Error Analysis)", "36", 2),
    ("CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "38", 0),
    ("6.1. Kết luận", "38", 1),
    ("6.2. Hạn chế", "38", 1),
    ("6.3. Hướng phát triển trong tương lai", "39", 1),
    ("TÀI LIỆU THAM KHẢO", "40", 0)
]

for title, page_num, level in toc_entries:
    add_leader_tab_entry(doc, title, page_num, level=level, is_bold=(level==0))

doc.add_page_break()

# 3.7. DANH MỤC CÁC KÝ HIỆU VÀ CHỮ VIẾT TẮT
style_heading_1("DANH MỤC CÁC KÝ HIỆU VÀ CHỮ VIẾT TẮT")
tbl_abbr = doc.add_table(rows=len(ABBREVIATIONS) + 1, cols=3)
tbl_abbr.rows[0].cells[0].paragraphs[0].text = "Viết tắt"
tbl_abbr.rows[0].cells[1].paragraphs[0].text = "Tên tiếng Anh"
tbl_abbr.rows[0].cells[2].paragraphs[0].text = "Tên tiếng Việt"

for idx, (abbr, en, vi) in enumerate(ABBREVIATIONS):
    tbl_abbr.rows[idx+1].cells[0].paragraphs[0].text = abbr
    tbl_abbr.rows[idx+1].cells[1].paragraphs[0].text = en
    tbl_abbr.rows[idx+1].cells[2].paragraphs[0].text = vi

format_table(tbl_abbr, [1.5, 2.5, 2.5], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

doc.add_page_break()

# 3.8. DANH MỤC HÌNH ẢNH
style_heading_1("DANH MỤC HÌNH ẢNH")
figures_list = [
    ("Hình 3.1", "So sánh quy mô và phân chia dữ liệu giữa các Benchmark tiếng Việt", "22"),
    ("Hình 4.1", "Sơ đồ kiến trúc tổng thể hệ thống SER + TVC + RAG Fact-Checking tiếng Việt", "23"),
    ("Hình 5.1", "Hiệu năng truy xuất bằng chứng đối chứng trên tập kiểm thử (SER Module)", "31"),
    ("Hình 5.2", "So sánh kết quả thực nghiệm Ablation Study giữa 3 cấu hình hệ thống", "33"),
    ("Hình 5.3", "Ma trận nhầm lẫn (Confusion Matrix) của phương pháp đề xuất SER + TVC + RAG", "32")
]
for fig_id, fig_desc, page_num in figures_list:
    add_leader_tab_entry(doc, f"{fig_id}: {fig_desc}", page_num, level=0, is_bold=False)

doc.add_page_break()

# 3.9. DANH MỤC BẢNG BIỂU
style_heading_1("DANH MỤC BẢNG BIỂU")
tables_list = [
    ("Bảng 1.1", "So sánh bản chất khoa học giữa Phát hiện tin giả và Kiểm chứng thông tin", "3"),
    ("Bảng 2.1", "Tổng hợp đối sánh toàn diện các phương pháp Baseline và đề xuất", "17"),
    ("Bảng 3.1", "Tổng hợp các bộ dữ liệu Fact-Checking và Fake News đã công bố", "18"),
    ("Bảng 3.2", "Thống kê chi tiết quy mô và phân phối nhãn của tập dữ liệu ViWikiFC", "19"),
    ("Bảng 3.3", "Thống kê chi tiết tập dữ liệu ViFactCheck theo 12 chuyên mục báo chí", "20"),
    ("Bảng 4.1", "Lược đồ dữ liệu đầu ra có cấu trúc (Pydantic Schema) của mô-đun RAG", "28"),
    ("Bảng 5.1", "Kết quả thực nghiệm mô-đun truy xuất bằng chứng ngữ nghĩa (SER)", "31"),
    ("Bảng 5.2", "Kết quả thực nghiệm mô-đun phân loại phán quyết (TVC) trên tập kiểm thử", "32"),
    ("Bảng 5.3", "Bảng chi tiết hiệu năng phân loại theo từng lớp (Per-class Performance)", "32"),
    ("Bảng 5.4", "Kết quả nghiên cứu thành phần (Ablation Study) giữa 3 cấu hình hệ thống", "33"),
    ("Bảng 5.5", "So sánh hiệu năng giữa các chiến lược kỹ nghệ Prompting", "34"),
    ("Bảng 5.6", "Tổng hợp các ca kiểm chứng thực tế điển hình và phân tích sai sót", "36")
]
for tbl_id, tbl_desc, page_num in tables_list:
    add_leader_tab_entry(doc, f"{tbl_id}: {tbl_desc}", page_num, level=0, is_bold=False)

# ============================================================
# 4. SECTION 2: NỘI DUNG CHÍNH (MAIN BODY - ARABIC 1, 2, 3...)
# ============================================================
sec2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
sec2.top_margin = Pt(56.7)
sec2.bottom_margin = Pt(56.7)
sec2.left_margin = Pt(85.05)
sec2.right_margin = Pt(56.7)
sec2.header.is_linked_to_previous = False
sec2.footer.is_linked_to_previous = False

sectPr2 = sec2._sectPr
for elem in sectPr2.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgBorders'):
    sectPr2.remove(elem)
for elem in sectPr2.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgNumType'):
    sectPr2.remove(elem)
pgNumType2 = parse_xml(r'<w:pgNumType xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:start="1"/>')
sectPr2.append(pgNumType2)

# Running Header
h_p2 = sec2.header.paragraphs[0]
h_p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
h_run = h_p2.add_run("Báo cáo Đồ án môn học: Các vấn đề hiện đại trong Trí tuệ Nhân tạo - HUIT")
h_run.font.name = 'Times New Roman'
h_run.font.size = Pt(8.5)
h_run.font.italic = True
h_run.font.color.rgb = RGBColor(120, 120, 120)

# Centered page number in footer
f_p2 = sec2.footer.paragraphs[0]
f_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
f_run2 = f_p2.add_run()
f_run2.font.name = 'Times New Roman'
f_run2.font.size = Pt(11)
f_run2._element.append(parse_xml(r'<w:fldSimple xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:instr="PAGE"/>'))

# Build all chapters
helpers = (
    style_heading_1, style_heading_2, style_heading_3,
    add_body_p, add_bullet_p, add_table_caption,
    add_figure, format_table, add_equation_table
)
build_all_chapters(doc, helpers)

# ============================================================
# 5. SAVE FINAL DOCUMENT
# ============================================================
# Set standard A4 paper size for all sections (210mm x 297mm)
for s in doc.sections:
    s.page_width = Mm(210)
    s.page_height = Mm(297)

# Attach page border ONLY to Section 0 (Cover pages: Bìa chính và Bìa phụ)
sectPr0 = doc.sections[0]._sectPr
for elem in sectPr0.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgBorders'):
    sectPr0.remove(elem)

pgBorders = parse_xml(r'''
    <w:pgBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:offsetFrom="page">
        <w:top w:val="twistedLines1" w:sz="18" w:space="24" w:color="auto"/>
        <w:left w:val="twistedLines1" w:sz="18" w:space="24" w:color="auto"/>
        <w:bottom w:val="twistedLines1" w:sz="18" w:space="24" w:color="auto"/>
        <w:right w:val="twistedLines1" w:sz="18" w:space="24" w:color="auto"/>
    </w:pgBorders>
''')
sectPr0.append(pgBorders)

# Explicitly guarantee that Section 1 and Section 2 have NO pgBorders
for s in doc.sections[1:]:
    for elem in s._sectPr.findall('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pgBorders'):
        s._sectPr.remove(elem)

output_path = r'E:\VanDe_AI\docs\BAO_CAO_DO_AN_HUIT.docx'
doc.save(output_path)
print(f"SUCCESS: Document saved to {output_path}!")

