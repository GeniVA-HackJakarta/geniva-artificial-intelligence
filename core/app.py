import base64
import uvicorn
from functools import lru_cache
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import config
from prompt import Prompt
from models.request import RequestBody
from tools.agent_maps import MapsAgent
from tools.agent_excel import ExcelAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.image_description import generate_image_description
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from db.connect import get_postgres_connection, get_redis_connection, get_qdrant_connection


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@lru_cache()
def get_agents():
    """Initialize and cache agent instances."""
    return {
        "maps": MapsAgent(
            api_key=config.GEMINI_API_KEY,
            gmaps_api_key=config.GMAPS_API_KEY,
            model_name=config.GEMINI_MODEL_NAME,
            temperature=config.GEMINI_TEMPERATURE
        ),
        "visual": ChatGoogleGenerativeAI(
            model=config.GEMINI_VISION_MODEL_NAME,
            api_key=config.GEMINI_API_KEY
        ),
        "excel": ExcelAgent(
            api_key=config.GEMINI_API_KEY,
            model_name=config.GEMINI_MODEL_NAME,
            temperature=config.GEMINI_TEMPERATURE
        )
    }

@lru_cache()
def get_embedding_model():
    """Initialize and cache embedding model."""
    return GoogleGenerativeAIEmbeddings(
        model=config.QDRANT_EMBEDDING_NAME, 
        google_api_key=config.GEMINI_API_KEY
    )

@lru_cache()
def get_qdrant_client():
    """Get and cache Qdrant client connection."""
    return get_qdrant_connection()

@app.get("/")
async def root():
    return {"message": "AI service started..."}

@app.get("/test-connection/{db_type}")
async def test_connection(db_type: str):
    connections = {
        "postgres": get_postgres_connection,
        "redis": get_redis_connection,
        "qdrant": get_qdrant_connection
    }
    
    if db_type not in connections:
        raise HTTPException(status_code=400, detail=f"Invalid database type: {db_type}")
    
    conn = connections[db_type]()
    if conn:
        return {"message": f"{db_type.capitalize()} connection successful"}
    raise HTTPException(status_code=500, detail=f"{db_type.capitalize()} connection failed")

@app.post("/generate-recommendation")
def generate_recommendation(request_body: RequestBody):
    agents = get_agents()
    
    if request_body.query and request_body.file:
        return handle_query_with_image(request_body, agents)
    elif request_body.query and not request_body.file:
        return handle_query_without_image(request_body, agents)
    elif not request_body.query and request_body.file:
        return handle_image_only(request_body, agents)
    else:
        raise HTTPException(status_code=400, detail="Invalid request: provide either a query or a file")

def handle_query_with_image(request_body: RequestBody, agents):
    image_content = base64.b64decode(request_body.file)
    context_data = generate_image_description(
        model=agents["visual"],
        embedding=get_embedding_model(),
        client=get_qdrant_client(),
        image=image_content
    )
    result = agents["excel"].direct_invoke(query=request_body.query, context_data=context_data)
    return {"message": result}

def handle_query_without_image(request_body: RequestBody, agents):
    tool_chosen, _ = agents["excel"].choice_route(query=request_body.query)
    if tool_chosen == "transportation":
        result = agents["maps"].invoke(query=request_body.query, lon=request_body.lon, lat=request_body.lat)
    else:
        result = agents["excel"].invoke(query=request_body.query, inst_prompt=Prompt.inst_prompt)
    result["type"] = tool_chosen
    return {"message": result}

def handle_image_only(request_body: RequestBody, agents):
    image_content = base64.b64decode(request_body.file)
    context_data = generate_image_description(
        model=agents["visual"],
        embedding=get_embedding_model(),
        client=get_qdrant_client(),
        image=image_content
    )
    result = agents["excel"].direct_invoke(query=request_body.query, context_data=context_data)
    result["type"] = "menu_makanan"
    return {"message": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)