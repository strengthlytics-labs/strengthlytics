from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/api/health")
def health():
    return {"ok": True}

app.mount("/", StaticFiles(directory="web", html=True), name="web")