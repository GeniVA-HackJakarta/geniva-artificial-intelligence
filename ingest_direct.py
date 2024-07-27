import time
import pandas as pd
from tqdm import tqdm
from qdrant_client.http import models
from qdrant_client import QdrantClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class FoodMenuIngestor:
    """
    A class to ingest food menu data into a Qdrant vector database using Google Generative AI embeddings.
    """

    def __init__(self, host="170.64.228.233", port=6333, collection_name="food-menu", model_name="models/embedding-001", requests_per_minute=60):
        """
        Initialize the FoodMenuIngestor with Qdrant client and Google Generative AI embeddings.

        Args:
            host (str): Qdrant server host.
            port (int): Qdrant server port.
            collection_name (str): Name of the Qdrant collection to use.
            model_name (str): Name of the Google Generative AI embedding model to use.
            requests_per_minute (int): Maximum number of embedding requests per minute.
        """
        self.qdrant_client = QdrantClient(host, port=port)
        self.embeddings = GoogleGenerativeAIEmbeddings(model=model_name, google_api_key="AIzaSyBp2bF8al-3Wg9Tk-n93Nr91i87ttMzJEc")
        self.collection_name = collection_name
        self.requests_per_minute = requests_per_minute
        self.request_interval = 60.0 / requests_per_minute
        self.last_request_time = 0

    def create_collection(self):
        """
        Create or recreate the Qdrant collection for storing menu item embeddings.
        """
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
        )

    def rate_limited_embed(self, text):
        """
        Embed a single text with rate limiting.

        Args:
            text (str): Text to embed.

        Returns:
            list: Embedding vector.
        """
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.request_interval:
            time.sleep(self.request_interval - time_since_last_request)
        
        embedding = self.embeddings.embed_query(text)
        self.last_request_time = time.time()
        return embedding

    def ingest_data(self, data_path):
        """
        Ingest menu data from an Excel file into the Qdrant collection.

        Args:
            data_path (str): Path to the Excel file containing menu data.

        Returns:
            int: Number of points ingested into the collection.
        """
        df = pd.read_excel(data_path)
        df = df.head(100)

        points = []
        for index, row in tqdm(df.iterrows(), total=len(df)):
            text = row['menu_name']
            embedding = self.rate_limited_embed(text)
            point = models.PointStruct(
                id=index,
                vector=embedding,
                payload={
                    "text": text,
                    "menu_id": row["menu_id"],
                    "restoran_id": row["restaurant_id"]
            })
            points.append(point)
        
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        self.qdrant_client.close()
        
        return len(points)

    def run(self, data_path):
        """
        Run the full ingestion process: create collection and ingest data.

        Args:
            data_path (str): Path to the Excel file containing menu data.
        """
        self.create_collection()
        ingested_count = self.ingest_data(data_path)
        print(f"Ingested {ingested_count} points into the {self.collection_name} collection.")

if __name__ == "__main__":
    ingestor = FoodMenuIngestor()
    ingestor.run("core/temporary-data/menu.xlsx")