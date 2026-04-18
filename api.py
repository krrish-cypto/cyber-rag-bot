from fastapi import FastAPI
from pydantic import BaseModel
from rag_engine import get_answer

app = FastAPI(title="Cyber RAG API")

class QueryRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_endpoint(request: QueryRequest):
    result = get_answer(request.query)
    return result