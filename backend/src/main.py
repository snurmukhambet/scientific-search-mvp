from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.core.llm import get_gemini_response

app = FastAPI()

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://127.0.0.1:5173",  # Vite dev server alternative
        "http://localhost",        # nginx proxy
        "http://127.0.0.1",       # nginx proxy alternative
        "http://localhost:80",     # explicit port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    query: str


@app.get("/")
def read_root():
    return {"message": "Scientific Search MVP API"}


@app.post("/api/ask")
def ask_gemini(question: Question):
    if not question.query.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    answer = get_gemini_response(question.query)

    return {"question": question.query, "answer": answer}
