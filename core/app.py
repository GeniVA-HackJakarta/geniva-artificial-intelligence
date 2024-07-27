import uvicorn
from config import config
from prompt import Prompt
from tools.agent_excel import ExcelAgent
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI, HTTPException, File, UploadFile
from tools.image_description import generate_image_description
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
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

agent_visual = ChatGoogleGenerativeAI(
    model=config.GEMINI_VISION_MODEL_NAME,
    api_key=config.GEMINI_API_KEY
)
agent_excel = ExcelAgent(
    api_key=config.GEMINI_API_KEY,
    model_name=config.GEMINI_MODEL_NAME,
    temperature=config.GEMINI_TEMPERATURE
)
client_qdrant = get_qdrant_connection()
embedding_model = GoogleGenerativeAIEmbeddings(model=config.QDRANT_EMBEDDING_NAME, google_api_key=config.GEMINI_API_KEY)


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

@app.post("/get-recommendation-text")
async def recommendation_text(query: str):
    result = agent_excel.invoke(query=query, inst_prompt=Prompt.inst_prompt)
    return {"message": result}

@app.post("/get-recommendation-image")
def recommendation_image(file: UploadFile = File(...)):
    image_content = file.file.read()
    result = generate_image_description(model=agent_visual, embedding=embedding_model, client=client_qdrant, image=image_content)
    return {"message": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)