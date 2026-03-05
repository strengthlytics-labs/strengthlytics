from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve the frontend from /web
app.mount("/", StaticFiles(directory="web", html=True), name="web")

@app.get("/api/health")
def health():
    return {"ok": True}