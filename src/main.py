from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager
import psycopg2
import select  
import asyncio
import os
import logging
import multiprocessing

from src.core.config import close_redis
from src.core.config import get_settings
from src.routes import user
from src.routes import patient
from src.routes import medical
from src.routes import process
from src.routes import auth

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
settings = get_settings()


# Use lifespan for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage app lifespan (startup and shutdown)."""
    # This is the equivalent of the startup event
    logger.info("Starting background task to listen for DB notifications...")
    # Start listening for DB notifications in the background
    asyncio.create_task(listen_for_db_notification())
    yield
    # This is the equivalent of the shutdown event (if necessary)
    logger.info("FastAPI app is shutting down...")

app = FastAPI(
    title=f"FastAPI",
    docs_url="/docs",
    description="FastAPI Documentation",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "tryItOutEnabled": True,
    },
    on_shutdown=[close_redis],
)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(patient.router)
app.include_router(medical.router)
app.include_router(process.router)

# WebSocket connection pool
active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connection from the frontend."""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Keep the connection alive
            await websocket.receive_text()
    except Exception as e:
        logger.error(f"Error with WebSocket connection {websocket.client}: {e}")
    finally:
        active_connections.remove(websocket)


# Configure Database listener and WebSocket
async def send_to_frontend(message: str):
    """Send message to all connected WebSocket clients."""
    for connection in active_connections:
        await connection.send_text(message)


async def listen_for_db_notification():
    """Listen for PostgreSQL notifications and push to WebSocket clients."""
    if os.getenv("ENV") == "local":
        dsn = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@localhost/{settings.DB_NAME}"
    else:
        dsn = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@/{settings.DB_NAME}?host=/cloudsql/{settings.DB_INSTANCE}"
    
    conn = psycopg2.connect(dsn)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()
    cursor.execute("LISTEN new_data_channel;")
    logger.info("Listening for new data...")

    while True:
        select.select([conn], [], [])
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            logger.info(f"New data received: {notify.payload}")
            # Send the notification to WebSocket clients
            await send_to_frontend(notify.payload)

def start_listening_for_db_notifications():
    """Function to start listening for DB notifications."""
    asyncio.run(listen_for_db_notification())  # Run the coroutine within the event loop

# Start background task on app startup
def start_background_task():
    """Start the database listener in a separate process."""
    p = multiprocessing.Process(target=start_listening_for_db_notifications)
    p.start()

@app.on_event("startup")
async def startup():
    """Start background task to listen for DB notifications."""
    logger.info("Starting background task to listen for DB notifications...")
    start_background_task()
