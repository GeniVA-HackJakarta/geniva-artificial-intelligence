import psycopg2
from redis import Redis
from config import config
from qdrant_client import QdrantClient

def get_postgres_connection():
    try:
        conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            database=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def get_redis_connection():
    try:
        redis_client = Redis.from_url(config.REDIS_URL)
        redis_client.ping()
        print("Redis connection successful")
        return redis_client
    except Exception as e:
        print(f"Error connecting to Redis: {e}")
        return None

def get_qdrant_connection():
    try:
        qdrant_client = QdrantClient(config.QDRANT_URL)
        qdrant_client.get_collections()
        print("Qdrant connection successful")
        return qdrant_client
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        return None

if __name__ == "__main__":
    get_postgres_connection()
    get_redis_connection()
    get_qdrant_connection()