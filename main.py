from fastapi import FastAPI
from routes.main import router as main_router


app = FastAPI()
app.include_router(main_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the sofifa-api!"}
