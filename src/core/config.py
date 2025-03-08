from google.cloud import secretmanager
from pydantic import BaseSettings
from dotenv import load_dotenv
import redis
import os

load_dotenv()

# Function to access secret from Google Secret Manager
def access_secret_version(secret_id):
    """
    Access the payload for the given secret version from Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/ann-project-390401/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=secret_name)
    # Return the decoded secret payload
    return response.payload.data.decode('UTF-8')

def get_env(name):
    if os.getenv("ENV") == "local":
        return os.getenv(name)
    else:
        return access_secret_version(name)

class Settings(BaseSettings):
    DATABASE_URL: str = get_env("DATABASE_URL")
    DB_USER: str = get_env("DB_USER")
    DB_PASS: str = get_env("DB_PASS")
    DB_NAME: str = get_env("DB_NAME")
    DB_HOST: str = get_env("DB_HOST")
    DB_PORT: str = get_env("DB_PORT")
    DB_INSTANCE: str = get_env("DB_INSTANCE")
    SECRET_KEY: str = get_env("SECRET_KEY")

    class Config:
        env_file = ".env"

settings = Settings()

def get_settings() -> Settings:
    return settings

# Configure redis
redis_client = None

def get_redis():
    global redis_client
    if redis_client is None:
        redis_client = redis.StrictRedis(
            host='localhost',
            port=6379,
            db=0
        )
    return redis_client 

def close_redis():
    global redis_client
    if redis_client:
        redis_client.connection_pool.disconnect()



