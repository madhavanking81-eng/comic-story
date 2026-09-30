import os
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger("comiccraft")

def generate_outline(prompt: str, character: str, setting: str, tone: str, art_style: str) -> List[Dict[str, Any]]:
    """
    Generates a structured 5-panel comic outline using Gemini Flash (or fallback engine).
    Returns a list of dictionaries with panel_number, title, scene_description, and image_prompt.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=api_key)
            
            system_instruction = (
                "You are an expert comic book editor and story writer. "
                "Output ONLY a valid JSON array containing exactly 5 panel objects. "
                "Each object must have these exact keys: 'panel_number' (integer 1 to 5), "
                "'title' (string), 'scene_description' (string), and 'image_prompt' (string). "
                "Do not include any markdown formatting, backticks, or extra commentary."
            )
            
            user_prompt = f"""
Create a 5-panel comic story outline based on the following details:
- Main Story Prompt: {prompt}
- Main Character: {character}
- Setting: {setting}
- Story Tone: {tone}
- Art Style: {art_style}

Format requirement: A JSON array of 5 objects:
[
  {{
    "panel_number": 1,
    "title": "Panel 1: ...",
    "scene_description": "...",
    "image_prompt": "Comic art style of {art_style}, main character {character} in {setting}..."
  }}, ...
]
"""
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                )
            )
            
            text_resp = response.text.strip()
            if text_resp.startswith("```json"):
                text_resp = text_resp[7:]
            if text_resp.startswith("```"):
                text_resp = text_resp[3:]
            if text_resp.endswith("```"):
                text_resp = text_resp[:-3]
            
            outline = json.loads(text_resp.strip())
            if isinstance(outline, list) and len(outline) == 5:
                return outline
        except Exception as e:
            logger.warning(f"Gemini Flash API call failed or not configured, using fallback generator: {e}")
            
    # Intelligent fallback outline generator
    char_name = character if character else "Hero"
    loc = setting if setting else "the mystical world"
    t_style = art_style if art_style else "comic book"
    mood = tone if tone else "dramatic"
    
    return [
        {
            "panel_number": 1,
            "title": f"Panel 1: The Journey Begins",
            "scene_description": f"{char_name} steps into {loc}, sensing that an unusual adventure is about to unfold in a {mood} atmosphere.",
            "image_prompt": f"Vivid {t_style} artwork: {char_name} standing at the entrance of {loc}, looking heroic and determined, dramatic lighting, detailed background."
        },
        {
            "panel_number": 2,
            "title": f"Panel 2: An Unexpected Discovery",
            "scene_description": f"While exploring deeper into {loc}, {char_name} spots something glowing with eerie magic.",
            "image_prompt": f"Vivid {t_style} comic scene: {char_name} discovering an ancient glowing relic in {loc}, mysterious sparkles and vibrant colors."
        },
        {
            "panel_number": 3,
            "title": f"Panel 3: The Rising Conflict",
            "scene_description": f"A sudden obstacle erupts in {loc}! {char_name} prepares to face the unexpected challenge.",
            "image_prompt": f"Vivid {t_style} comic action panel: {char_name} taking a protective combat stance as shadows swirl in {loc}, energetic comic sound effect style."
        },
        {
            "panel_number": 4,
            "title": f"Panel 4: The Climax",
            "scene_description": f"With bravery and quick thinking, {char_name} unleashes an incredible display of skill to resolve the crisis.",
            "image_prompt": f"Vivid {t_style} dynamic splash page style: {char_name} triumphantly using glowing magic or hero skills in {loc}, intense burst of colorful energy."
        },
        {
            "panel_number": 5,
            "title": f"Panel 5: A New Horizon",
            "scene_description": f"Peace returns to {loc}. {char_name} looks forward to the next grand tale waiting beyond the horizon.",
            "image_prompt": f"Vivid {t_style} cinematic closing shot: {char_name} standing on a scenic overlook in {loc} during a breathtaking golden sunset, triumphant ending pose."
        }
    ]
