import os
import logging
from typing import Optional
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

logger = logging.getLogger("comiccraft")
router = APIRouter()

templates = Jinja2Templates(directory="templates")

class PromptRequest(BaseModel):
    story_prompt: str
    character_name: Optional[str] = "Hero"
    setting: Optional[str] = "Enchanted Forest"
    story_tone: Optional[str] = "Dramatic"
    art_style: Optional[str] = "Comic Book"

@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Loads the homepage form (index.html)."""
    return templates.TemplateResponse(request=request, name="index.html")

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form("Hero"),
    setting: str = Form("Enchanted Forest"),
    story_tone: str = Form("Dramatic"),
    art_style: str = Form("Comic Book")
):
    """
    Handles form submissions from index.html:
    1. Generates 5-panel outline via Gemini Flash.
    2. Expands into narration & dialogue via Gemini Pro.
    3. Generates comic illustrations for each panel.
    4. Builds comic layout structure.
    5. Exports PDF and renders comic_preview.html.
    """
    try:
        logger.info(f"Generating comic for prompt: {story_prompt}")
        
        # 1. Outline Generation
        outline = generate_outline(story_prompt, character_name, setting, story_tone, art_style)
        
        # 2. Story Narration & Dialogue Generation
        story = generate_story(outline, character_name, setting, story_tone, art_style)
        
        # 3. Panel Image Generation
        image_paths = []
        for panel in outline:
            p_num = panel.get("panel_number", len(image_paths) + 1)
            img_prompt = panel.get("image_prompt", f"{story_prompt}, {art_style}")
            img_path = generate_image(img_prompt, p_num, art_style)
            image_paths.append(img_path)
            
        # 4. Build Layout
        layout = build_comic_layout(outline, story, image_paths)
        
        # 5. Export PDF
        story_title = f"{character_name}'s Adventure"
        pdf_path = save_pdf(layout, story_title=story_title, character_name=character_name)
        
        return templates.TemplateResponse(request=request, name="comic_preview.html", context={
            "story_title": story_title,
            "character_name": character_name,
            "setting": setting,
            "story_tone": story_tone,
            "art_style": art_style,
            "story_prompt": story_prompt,
            "layout": layout,
            "pdf_path": pdf_path
        })
    except Exception as e:
        logger.error(f"Error generating comic: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Comic Generation Error: {str(e)}")

@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    """API endpoint receiving JSON requests and returning structured JSON output with PDF path."""
    try:
        outline = generate_outline(payload.story_prompt, payload.character_name, payload.setting, payload.story_tone, payload.art_style)
        story = generate_story(outline, payload.character_name, payload.setting, payload.story_tone, payload.art_style)
        
        image_paths = []
        for panel in outline:
            p_num = panel.get("panel_number", len(image_paths) + 1)
            img_prompt = panel.get("image_prompt", payload.story_prompt)
            image_paths.append(generate_image(img_prompt, p_num, payload.art_style))
            
        layout = build_comic_layout(outline, story, image_paths)
        story_title = f"{payload.character_name}'s Tale"
        pdf_path = save_pdf(layout, story_title=story_title, character_name=payload.character_name)
        
        return JSONResponse(content={
            "status": "success",
            "story_title": story_title,
            "character_name": payload.character_name,
            "pdf_path": pdf_path,
            "layout": layout
        })
    except Exception as e:
        logger.error(f"JSON API generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-success", response_class=HTMLResponse)
async def export_success_page(request: Request, pdf: Optional[str] = None):
    """Confirmation page after PDF download."""
    return templates.TemplateResponse(request=request, name="export_success.html", context={
        "pdf_path": pdf or "/static/exports/comic_latest.pdf"
    })

@router.post("/test-image")
async def test_image_generation(prompt: str = Form("A heroic anime warrior facing a dragon"), art_style: str = Form("anime")):
    """Developer test route to generate a single image."""
    img_path = generate_image(prompt, panel_num=1, art_style=art_style)
    return JSONResponse(content={"status": "success", "image_path": img_path, "prompt": prompt})
