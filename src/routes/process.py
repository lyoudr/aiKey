from fastapi import APIRouter, Request, HTTPException
import json
import base64

from src.utils.write_to_db import write_to_db

router = APIRouter(tags=["process"], prefix="/process")

@router.post("/")
async def receive_pubsub(request: Request):
    """Receives Pub/Sub messages and triggers file proceessing"""

    # Parse the incoming Pub/Sub message
    try:
        envelope = await request.json()
    except Exception:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        raise HTTPException(status_code=400, detail=msg)
    
    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        raise HTTPException(status_code=400, detail=msg)

    pubsub_message = envelope.get("message", {})
    
    
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        decoded_message = json.loads(
            base64.b64decode(pubsub_message["data"]).decode("utf-8")
        )
        print("decoded_message is ->", decoded_message)
        bucket_name = decoded_message["bucket"]
        file_name = decoded_message["name"]

        print(f"Received file event: {file_name} in {bucket_name}")
        write_to_db(bucket_name, file_name)
