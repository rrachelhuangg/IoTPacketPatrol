from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from dotenv import load_dotenv
from routes import router as flows_router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
load_dotenv()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
async def root_page():
    # return {"HELLO": "WORLD!"}
    with open("index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(os.getenv('ATLAS_URI'))
    app.database = app.mongodb_client[os.getenv('DB_NAME')]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(flows_router, tags=["flows"], prefix="/flows")