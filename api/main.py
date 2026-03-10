from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.endpoints import router

app = FastAPI()

app.include_router(router)

app.mount("/", StaticFiles(directory="web", html=True))