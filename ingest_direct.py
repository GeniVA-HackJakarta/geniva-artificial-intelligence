import pandas as pd
from fastembed import TextEmbedding
from qdrant_client.http import models
from qdrant_client import QdrantClient

class FoodMenuIngestor:
    """
    A class to ingest food menu data into a Qdrant vector database using FastEmbed embeddings.
    """

    def __init__(self, host="localhost", port=6333, collection_name="food-menu", model_name='jinaai/jina-embeddings-v2-base-en'):
        """
        Initialize the FoodMenuIngestor with Qdrant client and FastEmbed model.

        Args:
            host (str): Qdrant server host.
            port (int): Qdrant server port.
            collection_name (str): Name of the Qdrant collection to use.
            model_name (str): Name of the FastEmbed model to use.
        """
        self.qdrant_client = QdrantClient(host, port=port)
        self.model = TextEmbedding(model_name)
        self.collection_name = collection_name

    def create_collection(self):
        """
        Create or recreate the Qdrant collection for storing menu item embeddings.
        """
        self.qdrant_client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
        )

    def ingest_data(self, data_path):
        """
        Ingest menu data from an Excel file into the Qdrant collection.

        Args:
            data_path (str): Path to the Excel file containing menu data.

        Returns:
            int: Number of points ingested into the collection.
        """
        df = pd.read_excel(data_path)

        points = []
        texts = df['menu_name'].tolist()
        embeddings = list(self.model.embed(texts))

        for index, (text, embedding) in enumerate(zip(texts, embeddings)):
            point = models.PointStruct(
                id=index,
                vector=embedding.tolist(),
                payload={"text": text}
            )
            points.append(point)
        
        self.qdrant_client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
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