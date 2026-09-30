import os
import time
import logging
from typing import List, Dict, Any

logger = logging.getLogger("comiccraft")

def save_pdf(layout: List[Dict[str, Any]], story_title: str = "ComicCraft AI Story", character_name: str = "Hero") -> str:
    """
    Compiles the 5 comic panels into a multi-page PDF using fpdf2 (with Pillow fallback).
    Saves to static/exports folder and returns the relative PDF file path.
    """
    export_dir = os.path.join("static", "exports")
    os.makedirs(export_dir, exist_ok=True)
    
    timestamp = int(time.time())
    filename = f"comic_{timestamp}.pdf"
    filepath = os.path.join(export_dir, filename)
    relative_path = f"/static/exports/{filename}"
    
    try:
        from fpdf import FPDF
        
        class ComicPDF(FPDF):
            def header(self):
                self.set_font("Helvetica", "B", 10)
                self.set_text_color(120, 120, 140)
                self.cell(0, 8, "COMICCRAFT AI - CREATIVE COMIC STORY", border=0, new_x="LMARGIN", new_y="NEXT", align="C")
                self.line(10, 15, 200, 15)
                self.ln(5)

            def footer(self):
                self.set_y(-15)
                self.set_font("Helvetica", "I", 8)
                self.set_text_color(150, 150, 170)
                self.cell(0, 10, f"Page {self.page_no()}/{{nb}} - Created with ComicCraft & Gemini AI", align="C")

        pdf = ComicPDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.alias_nb_pages()
        
        # Title Page / Header Section
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_text_color(30, 40, 70)
        pdf.cell(0, 12, story_title.encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT", align="C")
        
        pdf.set_font("Helvetica", "I", 12)
        pdf.set_text_color(100, 110, 130)
        pdf.cell(0, 8, f"Starring: {character_name}".encode('latin-1', 'replace').decode('latin-1'), new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(8)
        
        for panel in layout:
            p_num = panel.get("panel_number", 1)
            p_title = panel.get("title", f"Panel {p_num}")
            img_rel_path = panel.get("image_path", "").lstrip("/")
            scene_desc = panel.get("scene_description", "")
            caption = panel.get("caption", "")
            narration = panel.get("narration", "")
            dialogue = panel.get("dialogue", "")
            
            if p_num > 1 and p_num % 2 == 1:
                pdf.add_page()
            else:
                pdf.ln(5)
                
            # Panel Title Box
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_fill_color(240, 243, 250)
            pdf.set_text_color(20, 30, 60)
            pdf.cell(0, 9, f" {p_title}".encode('latin-1', 'replace').decode('latin-1'), border=1, fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)
            
            # Embed Image
            if os.path.exists(img_rel_path):
                try:
                    pdf.image(img_rel_path, w=140, x=(210 - 140) / 2)
                    pdf.ln(4)
                except Exception as img_err:
                    logger.warning(f"Could not embed image {img_rel_path} in PDF: {img_err}")
                    
            # Scene Description (Italics)
            if scene_desc:
                pdf.set_font("Helvetica", "I", 10)
                pdf.set_text_color(90, 95, 110)
                pdf.multi_cell(0, 5, f"Scene: {scene_desc}".encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(2)
                
            # Caption & Ambient Box
            if caption:
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(180, 50, 50)
                pdf.multi_cell(0, 5, f"Caption: {caption}".encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(2)
                
            # Dialogue / Speech Bubble
            if dialogue:
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_text_color(10, 80, 160)
                pdf.multi_cell(0, 6, f"Dialogue: {dialogue}".encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(2)
                
            # Narration
            if narration:
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(40, 40, 50)
                pdf.multi_cell(0, 5, f"Narration: {narration}".encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(4)
                
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(4)
            
        pdf.output(filepath)
        logger.info(f"Successfully generated PDF export: {filepath}")
        return relative_path

    except Exception as e:
        logger.error(f"FPDF export error: {e}. Generating fallback canvas PDF...")
        # Fallback PDF generation using Pillow
        from PIL import Image, ImageDraw, ImageFont
        canvas_img = Image.new("RGB", (1200, 1600), color=(255, 255, 255))
        draw = ImageDraw.Draw(canvas_img)
        draw.text((400, 50), f"COMICCRAFT: {story_title.upper()}", fill=(0, 0, 0))
        
        y_offset = 120
        for panel in layout:
            p_title = panel.get("title", "")
            draw.text((100, y_offset), p_title, fill=(30, 30, 100))
            y_offset += 40
            
            img_path = panel.get("image_path", "").lstrip("/")
            if os.path.exists(img_path):
                try:
                    p_img = Image.open(img_path).resize((400, 250))
                    canvas_img.paste(p_img, (100, y_offset))
                    y_offset += 270
                except Exception:
                    pass
            y_offset += 30
            
        canvas_img.save(filepath, "PDF", resolution=100.0)
        return relative_path
