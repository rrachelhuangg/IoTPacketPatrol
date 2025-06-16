from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from dotenv import load_dotenv
from routes import router as flows_router
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from infer_router import infer_router

import os

app = FastAPI()
load_dotenv()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/')
async def root_page():
    with open("pages/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get('/demo')
async def model_page():
    with open("pages/demo.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get('/about')
async def about_page():
    with open("pages/about.html", "r") as file:
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
app.include_router(infer_router)