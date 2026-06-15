from fastapi import FastAPI
from api.router import router

app = FastAPI(title="PropSelectAI Backend")

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Hello from PropSelectAI backend"}
