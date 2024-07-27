import uvicorn
from config import config
from typing import Optional
from tools.agent_excel import ExcelAgent
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.connect import get_postgres_connection, get_redis_connection, get_qdrant_connection


app = FastAPI()
origin = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_methods=origin,
    allow_headers=origin,
    allow_credentials=True,
)

agent_excel = ExcelAgent(
    api_key=config.GEMINI_API_KEY,
    model_name=config.GEMINI_MODEL_NAME,
    temperature=config.GEMINI_TEMPERATURE
)


@app.get("/")
async def root():
    return {"message": "AI service started..."}

@app.get("/test-postgres")
async def test_postgres():
    conn = get_postgres_connection()
    if conn:
        return {"message": "PostgreSQL connection successful"}
    raise HTTPException(status_code=500, detail="PostgreSQL connection failed")

@app.get("/test-redis")
async def test_redis():
    conn = get_redis_connection()
    if conn:
        return {"message": "Redis connection successful"}
    raise HTTPException(status_code=500, detail="Redis connection failed")

@app.get("/test-qdrant")
async def test_qdrant():
    conn = get_qdrant_connection()
    if conn:
        return {"message": "Qdrant connection successful"}
    raise HTTPException(status_code=500, detail="Qdrant connection failed")

@app.get("/get-recommendation")
async def get_recommendation(query: str, base_prompt: Optional[str], inst_prompt: Optional[str]):
    result = agent_excel.invoke(query=query)
    return {"message": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)