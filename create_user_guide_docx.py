"""
Generates a polished, professional Word document (Instagram_Downloader_Guide.docx)
with complete setup instructions for Person X (macOS & Windows).
"""

import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=200, right=200):
    """Sets inner padding for a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def create_callout_box(doc, text_lines, title="💡 NOTE", fill_hex="F8FAFC", border_hex="3B82F6"):
    """Creates a modern callout box with a colored left accent border."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, fill_hex)
    set_cell_margins(cell, top=160, bottom=160, left=240, right=200)

    # Set left border only
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(title)
    run_t.font.name = 'Calibri'
    run_t.font.size = Pt(10.5)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor.from_string(border_hex)

    for line in text_lines:
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_before = Pt(2)
        p2.paragraph_format.space_after = Pt(2)
        run_l = p2.add_run(line)
        run_l.font.name = 'Calibri'
        run_l.font.size = Pt(10)
        run_l.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_code_block(doc, code_text):
    """Adds a dark terminal-styled code block."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "0F172A")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(226, 232, 240)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_word_guide(output_path):
    doc = Document()

    # Set standard page margins (1 inch)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ------------------ DOCUMENT HEADER ------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("🎬 Instagram Bulk Reels Downloader")
    run_title.font.name = 'Calibri'
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(15, 23, 42)  # Slate 900

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Complete User Setup & Quick Start Guide (macOS & Windows)")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(13)
    run_sub.font.color.rgb = RGBColor(79, 70, 229)  # Indigo 600

    # Meta card table
    meta_tbl = doc.add_table(rows=2, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    col_widths = [Inches(1.8), Inches(4.7)]

    headers = [
        ("GitHub Repository:", "https://github.com/rudrabanduni/yt-bulk-reels-downloader"),
        ("System Compatibility:", "Apple macOS (MacBook, iMac, Mac Mini) & Microsoft Windows")
    ]
    for row_idx, (label, val) in enumerate(headers):
        row = meta_tbl.rows[row_idx]
        cell_lbl = row.cells[0]
        cell_val = row.cells[1]

        cell_lbl.width = col_widths[0]
        cell_val.width = col_widths[1]

        set_cell_background(cell_lbl, "F1F5F9")
        set_cell_background(cell_val, "F8FAFC")
        set_cell_margins(cell_lbl, top=80, bottom=80, left=120, right=120)
        set_cell_margins(cell_val, top=80, bottom=80, left=120, right=120)

        p_lbl = cell_lbl.paragraphs[0]
        p_lbl.paragraph_format.space_after = Pt(0)
        r_lbl = p_lbl.add_run(label)
        r_lbl.font.name = 'Calibri'
        r_lbl.font.bold = True
        r_lbl.font.size = Pt(9.5)
        r_lbl.font.color.rgb = RGBColor(30, 41, 59)

        p_val = cell_val.paragraphs[0]
        p_val.paragraph_format.space_after = Pt(0)
        r_val = p_val.add_run(val)
        r_val.font.name = 'Calibri'
        r_val.font.size = Pt(9.5)
        if "http" in val:
            r_val.font.bold = True
            r_val.font.color.rgb = RGBColor(37, 99, 235)  # Blue link
        else:
            r_val.font.color.rgb = RGBColor(71, 85, 105)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ------------------ SECTION: INTRODUCTION ------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(4)
    r_h1 = h1.add_run("1. Introduction & Overview")
    r_h1.font.name = 'Calibri'
    r_h1.font.size = Pt(16)
    r_h1.font.bold = True
    r_h1.font.color.rgb = RGBColor(15, 23, 42)

    intro_p = doc.add_paragraph()
    intro_p.paragraph_format.space_after = Pt(6)
    intro_p.paragraph_format.line_spacing = 1.15
    r_intro = intro_p.add_run(
        "This software is a fast, 100% free tool designed to download Instagram Reels in bulk. "
        "Unlike web downloaders that force you to open individual reels and paste links one by one, "
        "this software allows you to provide a creator's profile URL and automatically downloads all "
        "accessible Reels in high quality into an organized folder on your computer."
    )
    r_intro.font.name = 'Calibri'
    r_intro.font.size = Pt(11)
    r_intro.font.color.rgb = RGBColor(51, 65, 85)

    features = [
        ("Full Profile Bulk Downloading", "Enter an Instagram username or profile link to discover and download all videos from that creator."),
        ("Multi-Link Support", "Paste several Reel links separated by spaces or line breaks to download them in a single batch."),
        ("Text File / Notepad Support", "Put links in a text file (reels.txt) and download everything at once."),
        ("Automatic Chat Cleaner", "Paste WhatsApp or Telegram export lines with timestamps and names; the software automatically filters out chat clutter and extracts only valid Reel URLs."),
        ("Zero Complex Setup", "No third-party packages or subscription keys required. The software automatically configures itself on the first run.")
    ]
    for title, desc in features:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        rt = bp.add_run(f"{title}: ")
        rt.font.name = 'Calibri'
        rt.font.size = Pt(10.5)
        rt.font.bold = True
        rt.font.color.rgb = RGBColor(15, 23, 42)
        rd = bp.add_run(desc)
        rd.font.name = 'Calibri'
        rd.font.size = Pt(10.5)
        rd.font.color.rgb = RGBColor(71, 85, 105)

    # ------------------ SECTION: HOW TO DOWNLOAD ------------------
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(4)
    r_h2 = h2.add_run("2. How to Download the Software")
    r_h2.font.name = 'Calibri'
    r_h2.font.size = Pt(16)
    r_h2.font.bold = True
    r_h2.font.color.rgb = RGBColor(15, 23, 42)

    dl_steps = [
        ("Step 1: Open the GitHub Page", "Open your web browser (Safari, Chrome, or Edge) and go to:\nhttps://github.com/rudrabanduni/yt-bulk-reels-downloader"),
        ("Step 2: Download the ZIP File", "Near the top-right of the page, click the green button labeled '<> Code', then click 'Download ZIP'."),
        ("Step 3: Extract the Folder", "Locate the downloaded file in your 'Downloads' folder (yt-bulk-reels-downloader-main.zip). Double-click it to unzip. You will now have a folder named 'yt-bulk-reels-downloader-main'.")
    ]
    for s_title, s_desc in dl_steps:
        p_step = doc.add_paragraph()
        p_step.paragraph_format.space_before = Pt(4)
        p_step.paragraph_format.space_after = Pt(2)
        r_st = p_step.add_run(s_title)
        r_st.font.name = 'Calibri'
        r_st.font.bold = True
        r_st.font.size = Pt(11)
        r_st.font.color.rgb = RGBColor(30, 41, 59)

        p_desc = doc.add_paragraph()
        p_desc.paragraph_format.space_after = Pt(6)
        r_sd = p_desc.add_run(s_desc)
        r_sd.font.name = 'Calibri'
        r_sd.font.size = Pt(10.5)
        r_sd.font.color.rgb = RGBColor(71, 85, 105)

    # ------------------ SECTION: MAC QUICK START ------------------
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(4)
    r_h3 = h3.add_run("3. Step-by-Step for MacBook / macOS Users")
    r_h3.font.name = 'Calibri'
    r_h3.font.size = Pt(16)
    r_h3.font.bold = True
    r_h3.font.color.rgb = RGBColor(15, 23, 42)

    mac_intro = doc.add_paragraph()
    mac_intro.paragraph_format.space_after = Pt(6)
    r_mi = mac_intro.add_run(
        "To make your experience effortless, you only need to run a single command once. "
        "This creates a dedicated desktop application so you will NEVER have to touch the Terminal again!"
    )
    r_mi.font.name = 'Calibri'
    r_mi.font.size = Pt(11)
    r_mi.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph("One-Time Setup (Takes 10 Seconds):", style='Heading 3')
    mac_steps = [
        "1. Press Command (⌘) + Space on your Mac keyboard to open Spotlight Search.",
        "2. Type Terminal and press Enter to open the Mac Terminal.",
        "3. Copy and paste the following single command into the Terminal, then press Enter:"
    ]
    for s in mac_steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(s)
        r.font.name = 'Calibri'
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(51, 65, 85)

    add_code_block(doc, "cd ~/Downloads/yt-bulk-reels-downloader-main && chmod +x create_mac_app.sh && ./create_mac_app.sh")

    create_callout_box(
        doc,
        [
            "You will now see a new app on your Mac Desktop called 'Instagram Downloader.app'.",
            "You can close the Terminal window now. You will never have to open it again!",
            "Whenever you want to download Reels, just double-click 'Instagram Downloader' directly from your Desktop."
        ],
        title="✨ DESKTOP APP CREATED!",
        fill_hex="ECFDF5",
        border_hex="10B981"
    )

    doc.add_paragraph("Alternative (Without any Terminal commands):", style='Heading 3')
    alt_p = doc.add_paragraph()
    alt_p.paragraph_format.space_after = Pt(6)
    r_alt = alt_p.add_run(
        "If you don't even want to type any commands: Simply open the downloaded folder in Finder, "
        "find the file named 'Run Downloader.command', and double-click it. The window will open immediately!"
    )
    r_alt.font.name = 'Calibri'
    r_alt.font.size = Pt(10.5)
    r_alt.font.color.rgb = RGBColor(71, 85, 105)

    # ------------------ SECTION: WINDOWS USERS ------------------
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(4)
    r_h4 = h4.add_run("4. Step-by-Step for Windows Users")
    r_h4.font.name = 'Calibri'
    r_h4.font.size = Pt(16)
    r_h4.font.bold = True
    r_h4.font.color.rgb = RGBColor(15, 23, 42)

    win_p = doc.add_paragraph()
    win_p.paragraph_format.space_after = Pt(6)
    r_win = win_p.add_run(
        "Windows users have it even simpler—no terminal required at all:\n"
        "1. Extract the downloaded ZIP file into your folder.\n"
        "2. Double-click 'Run Downloader.bat' (or 'Run Downloader (No Console).vbs' to launch with no command window).\n"
        "3. The interactive window will pop up immediately on your screen!"
    )
    r_win.font.name = 'Calibri'
    r_win.font.size = Pt(10.5)
    r_win.font.color.rgb = RGBColor(51, 65, 85)

    # ------------------ SECTION: HOW TO USE THE GUI ------------------
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(4)
    r_h5 = h5.add_run("5. How to Use the Graphical Window")
    r_h5.font.name = 'Calibri'
    r_h5.font.size = Pt(16)
    r_h5.font.bold = True
    r_h5.font.color.rgb = RGBColor(15, 23, 42)

    gui_intro = doc.add_paragraph()
    gui_intro.paragraph_format.space_after = Pt(6)
    r_gi = gui_intro.add_run(
        "When the application opens, you are greeted with a clean, friendly window with 3 simple options:"
    )
    r_gi.font.name = 'Calibri'
    r_gi.font.size = Pt(10.5)
    r_gi.font.color.rgb = RGBColor(51, 65, 85)

    gui_options = [
        ("Option A: Bulk Download All Reels from a Profile",
         "1. Select the top radio button: 'All Reels from a Profile'.\n"
         "2. In the text box, paste the creator's profile URL (e.g., https://www.instagram.com/mindforgeh/) or just their handle (e.g., @mindforgeh).\n"
         "3. Click the big blue button: '⬇️ Start Download'.\n"
         "4. The app will automatically discover all accessible Reels from their profile and download them sequentially!"),

        ("Option B: Download a Single Reel or Multiple Reels",
         "1. Select the second radio button: 'Single Reel or Multiple Reel Links'.\n"
         "2. Paste one Reel link, or paste several links separated by spaces or new lines.\n"
         "3. Click '⬇️ Start Download'."),

        ("Option C: Batch Download from a Text File",
         "1. Select 'Batch from Text File'.\n"
         "2. You can leave it blank to automatically use 'reels.txt', or click '📂 Browse File...' to choose your file.\n"
         "3. Click '⬇️ Start Download'.")
    ]
    for opt_title, opt_body in gui_options:
        p_ot = doc.add_paragraph()
        p_ot.paragraph_format.space_before = Pt(6)
        p_ot.paragraph_format.space_after = Pt(2)
        r_ott = p_ot.add_run(opt_title)
        r_ott.font.name = 'Calibri'
        r_ott.font.bold = True
        r_ott.font.size = Pt(11)
        r_ott.font.color.rgb = RGBColor(79, 70, 229)

        p_ob = doc.add_paragraph()
        p_ob.paragraph_format.space_after = Pt(6)
        r_obb = p_ob.add_run(opt_body)
        r_obb.font.name = 'Calibri'
        r_obb.font.size = Pt(10)
        r_obb.font.color.rgb = RGBColor(51, 65, 85)

    # ------------------ SECTION: WHERE FILES GO ------------------
    h6 = doc.add_paragraph()
    h6.paragraph_format.space_before = Pt(14)
    h6.paragraph_format.space_after = Pt(4)
    r_h6 = h6.add_run("6. Where Are Your Videos Stored?")
    r_h6.font.name = 'Calibri'
    r_h6.font.size = Pt(16)
    r_h6.font.bold = True
    r_h6.font.color.rgb = RGBColor(15, 23, 42)

    storage_p = doc.add_paragraph()
    storage_p.paragraph_format.space_after = Pt(6)
    r_sp = storage_p.add_run(
        "All downloaded videos are saved inside the 'downloads' folder within the software directory:\n"
        "• Single Reels are saved to: downloads/reels/\n"
        "• Profile bulk downloads are organized by creator name: downloads/<username>/\n\n"
        "💡 Quick Finder Shortcut: Simply click the '📁 Open Downloads' button in the application window, "
        "and your computer will immediately open the folder in Finder (on Mac) or File Explorer (on Windows)!"
    )
    r_sp.font.name = 'Calibri'
    r_sp.font.size = Pt(10.5)
    r_sp.font.color.rgb = RGBColor(51, 65, 85)

    # ------------------ SECTION: TROUBLESHOOTING ------------------
    h7 = doc.add_paragraph()
    h7.paragraph_format.space_before = Pt(14)
    h7.paragraph_format.space_after = Pt(4)
    r_h7 = h7.add_run("7. Helpful Tips & Troubleshooting")
    r_h7.font.name = 'Calibri'
    r_h7.font.size = Pt(16)
    r_h7.font.bold = True
    r_h7.font.color.rgb = RGBColor(15, 23, 42)

    tips = [
        ("Automatic Deduplication", "The software keeps an internal archive so you never accidentally download the exact same Reel twice. However, if you delete a video from your disk and run the downloader again, it recognizes it's missing and re-downloads it for you!"),
        ("Keeping the Engine Updated", "Instagram occasionally modifies its web security. If downloads ever slow down or fail, simply click the '🔄 Check Updates' button in the top right of the application window. The app will automatically update its download engine to the latest release."),
        ("Private Profiles (Optional)", "Public profiles and public reels require zero login. If you need to download from a private creator account you follow, export your cookies to a file named 'cookies.txt' and place it inside the folder.")
    ]
    for t_title, t_desc in tips:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(4)
        p_t.paragraph_format.space_after = Pt(2)
        r_tt = p_t.add_run(f"• {t_title}: ")
        r_tt.font.name = 'Calibri'
        r_tt.font.bold = True
        r_tt.font.size = Pt(10.5)
        r_tt.font.color.rgb = RGBColor(30, 41, 59)
        r_td = p_t.add_run(t_desc)
        r_td.font.name = 'Calibri'
        r_td.font.size = Pt(10.5)
        r_td.font.color.rgb = RGBColor(71, 85, 105)

    # ------------------ FOOTER / SIGN OFF ------------------
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    foot_p = doc.add_paragraph()
    foot_p.paragraph_format.space_before = Pt(10)
    r_foot = foot_p.add_run("Enjoy seamless bulk downloading! For updates and source code, visit: https://github.com/rudrabanduni/yt-bulk-reels-downloader")
    r_foot.font.name = 'Calibri'
    r_foot.font.italic = True
    r_foot.font.size = Pt(9.5)
    r_foot.font.color.rgb = RGBColor(100, 116, 139)

    doc.save(str(output_path))
    print(f"[+] Document successfully created at: {output_path}")

if __name__ == "__main__":
    out_file = Path(__file__).parent.resolve() / "Instagram_Downloader_Guide.docx"
    build_word_guide(out_file)
