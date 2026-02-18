from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Smart Restaurant AI Agent")

app.include_router(api_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
