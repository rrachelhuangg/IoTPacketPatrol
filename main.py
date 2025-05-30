from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as flows_router
import os

config = dotenv_values(".env")

app = FastAPI()

@app.get('/')
async def root_page():
    return {"HELLO": "WORLD!"}

@app.on_event("startup")
def startup_db_client():
    # app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.mongodb_client = os.getenv('ATLAS_URI')
    # app.database = app.mongodb_client[config["DB_NAME"]]
    app.database = os.getenv('DB_NAME')

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(flows_router, tags=["flows"], prefix="/flows")