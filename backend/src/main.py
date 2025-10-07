from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core.llm import get_gemini_response

app = FastAPI()


class Question(BaseModel):
    query: str


@app.get("/")
def read_root():
    return {"message": "Scientific Search MVP API"}


@app.post("/api/ask")
def ask_gemini(question: Question):
    if not question.query.strip():
        raise HTTPException(status_code=400, detail="Вопрос не может быть пустым")

    answer = get_gemini_response(question.query)

    return {"question": question.query, "answer": answer}
