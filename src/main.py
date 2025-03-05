import sys 
import os 

from fastapi import FastAPI

from routes import user
from routes import patient
from routes import medical

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