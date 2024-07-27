import base64
import uvicorn
from config import config
from prompt import Prompt
from models.request import RequestBody
from tools.agent_excel import ExcelAgent
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
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

@app.post("/generate-recommendation")
def generate_recommendation(request_body: RequestBody):
    if request_body.query and request_body.file:
        question = request_body.query
        image_content = base64.b64decode(request_body.file)
        context_data = generate_image_description(model=agent_visual, embedding=embedding_model, client=client_qdrant, image=image_content)
        result = agent_excel.direct_invoke(query=question, context_data=context_data)
        return {"message": result}
    elif request_body.query and request_body.file is None:
        result = agent_excel.invoke(query=request_body.query, inst_prompt=Prompt.inst_prompt)
        return {"message": result}
    elif request_body.query is None and request_body.file:
        image_content = base64.b64decode(request_body.file)
        result = generate_image_description(model=agent_visual, embedding=embedding_model, client=client_qdrant, image=image_content)
        return {"message": result}
    else:
        raise HTTPException(status_code=400, detail="Invalid request: provide either a query or a file")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)