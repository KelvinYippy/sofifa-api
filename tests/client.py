from fastapi import FastAPI
from routes.main import router as main_router
from fastapi.testclient import TestClient

def create_client():
    app = FastAPI()
    app.include_router(main_router)
    client = TestClient(app)
    return client
