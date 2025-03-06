import sys 
import os 

from fastapi import FastAPI

from src.routes import user
from src.routes import patient
from src.routes import medical
from src.routes import process

app = FastAPI(
    title=f"FastAPI",
    docs_url="/docs",
    description="FastAPI Documentation",
    swagger_ui_parameters={
        "persistAuthorization": True,
        "tryItOutEnabled": True,
    },
)
app.include_router(user.router)
app.include_router(patient.router)
app.include_router(medical.router)
app.include_router(process.router)