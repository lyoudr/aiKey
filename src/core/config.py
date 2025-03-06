from google.cloud import secretmanager
from pydantic import BaseSettings
from dotenv import load_dotenv
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

class Settings(BaseSettings):
    DATABASE_URL: str = access_secret_version("DATABASE_URL")
    DB_USER: str = access_secret_version("DB_USER")
    DB_PASS: str = access_secret_version("DB_PASS")
    DB_NAME: str = access_secret_version("DB_NAME")
    DB_HOST: str = access_secret_version("DB_HOST")
    DB_PORT: str = access_secret_version("DB_PORT")
    DB_INSTANCE: str = access_secret_version("DB_INSTANCE")

    class Config:
        env_file = ".env"

settings = Settings()

def get_settings() -> Settings:
    return settings