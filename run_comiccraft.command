#!/bin/bash
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed. Install Python 3 and try again."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creating ComicCraft virtual environment..."
  python3 -m venv .venv || exit 1
fi

source .venv/bin/activate
python -m pip install --upgrade pip >/dev/null 2>&1
python -m pip install -r requirements.txt || exit 1

echo "Starting ComicCraft..."
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
