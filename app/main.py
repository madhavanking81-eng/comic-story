import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("comiccraft")

app = FastAPI(
    title="ComicCraft - AI Comic Story Creator",
    description="Generate AI-powered comic book storylines, dialogues, artwork, and exportable PDFs using Google Gemini models.",
    version="1.0.0"
)

# Ensure static directories exist
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/panels", exist_ok=True)
os.makedirs("static/exports", exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include application routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
