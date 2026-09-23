from fastapi import FastAPI
from pydantic import BaseModel

from src.generator import Generator


app = FastAPI(
    title="Delhi Traffic Rules Assistant"
)


generator = Generator()


class Question(BaseModel):
    query: str
    top_k: int = 5


@app.get("/")
def home():
    return {
        "message": "Delhi Traffic Rules API is running"
    }


@app.post("/ask")
def ask_question(question: Question):

    answer = generator.generate(
        question.query,
        question.top_k
    )

    return {
        "question": question.query,
        "answer": answer
    }