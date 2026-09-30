from typing import List, Dict, Any

def build_comic_layout(outline: List[Dict[str, Any]], story: List[Dict[str, Any]], image_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Merges outlines, detailed stories, and generated image filepaths into
    a unified, structured comic panel layout list for display and export.
    """
    layout = []
    
    for i in range(5):
        out_item = outline[i] if i < len(outline) else {}
        story_item = story[i] if i < len(story) else {}
        img_path = image_paths[i] if i < len(image_paths) else "/static/panels/placeholder.png"
        
        panel_num = i + 1
        title = story_item.get("title") or out_item.get("title") or f"Panel {panel_num}"
        scene_desc = out_item.get("scene_description") or story_item.get("scene_description") or ""
        caption = story_item.get("caption") or ""
        narration = story_item.get("narration") or ""
        dialogue = story_item.get("dialogue") or ""
        image_prompt = out_item.get("image_prompt") or ""
        
        layout.append({
            "panel_number": panel_num,
            "title": title,
            "image_path": img_path,
            "scene_description": scene_desc,
            "caption": caption,
            "narration": narration,
            "dialogue": dialogue,
            "image_prompt": image_prompt
        })
        
    return layout
