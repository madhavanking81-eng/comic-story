# ComicCraft - AI Comic Story Creator

ComicCraft is a web application that leverages **Google Gemini AI models** and AI image generation to automatically produce personalized 5-panel comic book storylines, dialogues, and downloadable PDF comic books.

## Features

- **Personalized Story Inputs**: Prompt, Character Name, Setting, Tone (Dramatic, Funny, etc.), and Art Style (Comic Book, Anime, Pixel Art, etc.).
- **Gemini Flash Integration (`gemini_flash.py`)**: Rapidly generates a structured 5-panel storyline outline.
- **Gemini Pro Integration (`gemini_pro.py`)**: Crafts detailed narration, ambient sound captions, and speech dialogues.
- **AI Artwork Generation (`image_generator.py`)**: Renders stylized 5-panel comic illustrations based on image prompts.
- **Layout Engine (`layout_builder.py`)**: Combines imagery and narrative bubbles panel-by-panel.
- **PDF Export (`exporters.py`)**: Compiles the complete comic into a professional multi-page PDF using `fpdf2`.
- **FastAPI Backend (`routes.py`)**: Provides browser HTML forms (`/generate`) and direct JSON API endpoints (`/generate-comic/json`).

## Project Structure

```
ComicCraft/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI initialization & static mounts
│   ├── routes.py            # API routes (/, /generate, /generate-comic/json, /export-success, /test-image)
│   ├── gemini_flash.py      # Outline generation using Gemini Flash
│   ├── gemini_pro.py        # Narration & dialogue generation using Gemini Pro
│   ├── image_generator.py   # Comic illustration generation
│   ├── layout_builder.py    # Layout assembly
│   └── exporters.py         # PDF compilation & export
├── templates/
│   ├── index.html           # Input form page
│   ├── comic_preview.html   # Sequential 5-panel comic viewer
│   └── export_success.html  # Export success page
├── static/
│   ├── css/
│   │   └── style.css        # Glassmorphic dark comic theme
│   ├── panels/              # Generated comic panel images
│   └── exports/             # Exported PDF files
├── requirements.txt         # Dependencies
├── .env.example             # API key sample file
└── README.md                # Documentation
```

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Set your Gemini API key in environment or `.env`:
   ```bash
   set GEMINI_API_KEY=your_actual_key
   ```
   *(Note: ComicCraft includes smart fallbacks so it works cleanly out-of-the-box even without an API key!)*

3. Run the development server:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

4. Open your browser and navigate to:
   - Web App: `http://127.0.0.1:8000`
   - API Docs: `http://127.0.0.1:8000/docs`
