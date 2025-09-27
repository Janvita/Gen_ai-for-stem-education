# Generative AI for STEM Education
This project is a web application designed for STEM education using Generative AI. It has a Python FastAPI backend and a Vite frontend.

## Project Structure

root/
├── backend/      # FastAPI backend
├── app/          # Vite frontend
├── .venv/        # Python virtual environment
├── .gitignore
└── README.md

1. Create virtual environment:
python3 -m venv .venv

2. Activate it:
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate

3. Install dependencies:
pip install -r backend/requirements.txt

4. Run FastAPI server:
cd backend
uvicorn main:app --reload --port 8001


1. Open a new terminal (keep backend running)
2. Navigate to frontend:
cd app
3. Install dependencies:
npm install
4. Run frontend:
npm run dev

## Environmental variables

- Backend: backend/.env : Add the groq api key in this file

