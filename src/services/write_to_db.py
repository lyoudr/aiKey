from google.auth.transport.requests import Request 
from google.auth import default 
import aiohttp # Unlike `requests`, which is synchronous and blocks execution, aiohttp allows multiple HTTP requests to be processed concurrently using `async/await`
import asyncpg
import ast

from src.core.config import get_settings

settings = get_settings()

async def download_blob_async(bucket_name, file_name):
    """Downloads a blob asynchronously."""
    
    # Get credentials and generate an access token
    credentials, _ = default()
    credentials.refresh(Request())  # Refresh token for authentication
    token = credentials.token  # Extract access token

    url = f"https://storage.googleapis.com/{bucket_name}/{file_name}"
    headers = {"Authorization": f"Bearer {token}"}  # Set Authorization header
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.text()
            else:
                print(f"Failed to download {file_name}. Status: {resp.status}")
                return None

async def write_to_db(bucket_name: str, file_name: str):
    """
    Reads the file from Cloud Storage and writes to Cloud SQL
    Processes only files inside `output/` folder.
    """
    if not file_name.startswith("output/"):
        print(f"Skipping file: {file_name} (Not in output/)")
        return 

    # Read the file contents
    file_contents = await download_blob_async(bucket_name, file_name)
    if not file_contents:
        print(f"Skipping file: {file_name} (Failed to download)")
        return
    try:
        values = [
            (entry["patient_id"], entry["month"], entry["total_cost"])
            for item in file_contents.split("\n") if item
            for entry in [ast.literal_eval(item)]  # Parse and extract data in one step
        ]
    except (ValueError, SyntaxError) as e:
        print(f"Error decoding JSON in file: {file_name}. Error: {e}")
        return
    
    # Connect to Cloud SQL (PostgreSQL)
    dsn = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@/{settings.DB_NAME}?host=/cloudsql/{settings.DB_INSTANCE}"
    conn = await asyncpg.connect(dsn)


    # Insert query
    insert_query = """
    INSERT INTO patient_cost (patient_id, month, total_cost)
    VALUES ($1, $2, $3)
    ON CONFLICT (patient_id, month)
    DO UPDATE SET total_cost = EXCLUDED.total_cost, updated_time = NOW();
    """

    try:
        # Begin transaction
        async with conn.transaction():
            await conn.executemany(insert_query, values) # Batch insert
            print(f"Inserted {len(values)} records from {file_name}.")
    except Exception as e:
        print(f"Database error: {e}") 
    finally:
        await conn.close()