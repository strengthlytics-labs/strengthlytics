from fastapi import APIRouter
from db.db_bridge import create_workspace
from api.models import DrawerCreate

router = APIRouter()

@router.get("/api/health")
def health():
    return {"ok": True}

@router.post("/api/workspace")
def create_workspace_endpoint(data: DrawerCreate):
    create_workspace(token=data.token, label=data.label)

    return {"ok": True}