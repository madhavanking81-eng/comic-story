import os
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger("comiccraft")

def generate_story(outline: List[Dict[str, Any]], character: str, setting: str, tone: str, art_style: str) -> List[Dict[str, Any]]:
    """
    Expands panel outlines into full comic story panels containing narration, caption, and dialogue.
    Returns list of dicts with story attributes for each panel.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if api_key:
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=api_key)
            
            system_instruction = (
                "You are an acclaimed comic book writer. Given a 5-panel outline, generate "
                "engaging narration, environmental sound captions, and character dialogue for each panel. "
                "Output ONLY a JSON array of 5 objects matching the panel order. "
                "Keys per object: 'panel_number' (int), 'title' (string), 'caption' (string), 'narration' (string), 'dialogue' (string)."
            )
            
            prompt = f"""
Outline panels: {json.dumps(outline)}
Character: {character}
Setting: {setting}
Tone: {tone}
Art Style: {art_style}

Format: JSON array of 5 objects:
[
  {{
    "panel_number": 1,
    "title": "...",
    "caption": "*WHOOSH!* A cold breeze sweeps through...",
    "narration": "In the heart of the realm, a legend wakes.",
    "dialogue": "{character}: 'No turning back now!'"
  }}, ...
]
"""
            response = client.models.generate_content(
                model='gemini-2.5-pro',
                contents=prompt,
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
                
            story_panels = json.loads(text_resp.strip())
            if isinstance(story_panels, list) and len(story_panels) == 5:
                return story_panels
        except Exception as e:
            logger.warning(f"Gemini Pro API call failed or not configured, using fallback story generator: {e}")
            
    # Fallback story generator
    char_name = character if character else "Hero"
    
    story_panels = []
    sound_fx = ["*SWOOSH!*", "*GLOW!*", "*RUMBLE!*", "*KABOOM!*", "*SHINE!*"]
    
    for idx, panel in enumerate(outline):
        p_num = panel.get("panel_number", idx + 1)
        p_title = panel.get("title", f"Panel {p_num}")
        p_desc = panel.get("scene_description", "")
        
        if p_num == 1:
            caption = f"{sound_fx[0]} The wind whispers ancient secrets across {setting}."
            narration = f"Every great legend begins with a single resolute step into the unknown."
            dialogue = f"{char_name}: \"Today marks the start of something extraordinary!\""
        elif p_num == 2:
            caption = f"{sound_fx[1]} A strange pulse of energy resonates through the air!"
            narration = f"Deep within {setting}, an forgotten wonder reveals itself."
            dialogue = f"{char_name}: \"What is this magnificent power? It defies explanation!\""
        elif p_num == 3:
            caption = f"{sound_fx[2]} The ground shudders as shadows loom close!"
            narration = f"Danger strikes without warning, testing the true spirit of the adventurer."
            dialogue = f"{char_name}: \"I won't back down! Stand firm!\""
        elif p_num == 4:
            caption = f"{sound_fx[3]} Energy surges as power erupts in full force!"
            narration = f"Channeling every ounce of courage, victory is snatched from the brink."
            dialogue = f"{char_name}: \"Taste the true strength of a hero!\""
        else:
            caption = f"{sound_fx[4]} Warm sunlight bathes the peaceful landscape once more."
            narration = f"The storm passes, leaving behind a legacy of bravery and new possibilities."
            dialogue = f"{char_name}: \"Until our next grand adventure!\""
            
        story_panels.append({
            "panel_number": p_num,
            "title": p_title,
            "caption": caption,
            "narration": narration,
            "dialogue": dialogue,
            "scene_description": p_desc
        })
        
    return story_panels
