from google.cloud import storage
from google.cloud.sql.connector import Connector, IPTypes
import ast

from src.core.config import get_settings

settings = get_settings()

def write_to_db(bucket_name: str, file_name: str):
    """
    Reads the file from Cloud Storage and writes to Cloud SQL
    Processes only files inside `output/` folder.
    """
    if not file_name.startswith("output/"):
        print(f"Skipping file: {file_name} (Not in output/)")
        return 

    # Connect to Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Read the file contents
    file_contents = blob.download_as_text()
    try:
        patient_costs = [ast.literal_eval(item) for item in file_contents.split("\n") if item]
    except (ValueError, SyntaxError) as e:
        print(f"Error decoding JSON in file: {file_name}. Error: {e}")
        return
    
    # Connect to Cloud SQL (PostgreSQL)
    connector = Connector()
    conn = connector.connect(
        settings.DB_INSTANCE,  # Set the Cloud SQL connection name
        "pg8000",  # Specify the DB driver (postgresql, mysql, etc.)
        user=settings.DB_USER,
        password=settings.DB_PASS,
        db=settings.DB_NAME,
        ip_type=IPTypes.PUBLIC
    )
    cursor = conn.cursor()
    
    # Convert data to tuples
    values = [
        f'{(entry["patient_id"], entry["month"], entry["total_cost"])}'
        for entry in patient_costs
    ]

    # Insert query
    insert_query = f"""
    INSERT INTO patient_cost (patient_id, month, total_cost)
    VALUES {', '.join(values)}
    ON CONFLICT (patient_id, month)
    DO UPDATE SET total_cost = EXCLUDED.total_cost, updated_time = NOW();
    """

    try:
        cursor.execute(insert_query) # Batch insert
        conn.commit()
        print(f"Inserted {len(values)} records from {file_name}.")
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()