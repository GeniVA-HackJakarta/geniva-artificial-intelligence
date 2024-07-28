import base64
from prompt import Prompt
from config import config
from langchain_core.messages import HumanMessage

def generate_image_description(model: object, embedding: object, client: object, image: bytes) -> str:
    
    base64_image = base64.b64encode(image).decode('utf-8')
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": Prompt.desc_prompt
            },
            {
                "type": "image_url",
                "image_url": "data:image/png;base64," + base64_image
            }
        ]
    )
    response = model.invoke([message])
    response = response.content
    print("[Image Description]", response)

    vector = embedding.embed_query(response)
    semantic_search_result = client.search(
        query_vector=vector,
        limit=config.QDRANT_LIMIT,
        collection_name=config.QDRANT_COLLECTION_NAME,
    )
    context_retrieved = [
        {
            "text": hit.payload["text"],
            "menu_id": hit.payload["menu_id"],
            "restoran_id": hit.payload["restoran_id"],
            "score": hit.score
        } 
        for hit in semantic_search_result
    ][:3]
    
    return context_retrieved