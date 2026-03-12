from fastapi import APIRouter, HTTPException
from db.db_bridge import create_workspace, open_workspace, save_feedback, list_feedback
from api.models import DrawerCreate, FeedbackCreate
from core.feedback import FeedbackEntry

router = APIRouter()

@router.get("/api/health")
def health():
    return {"ok": True}

@router.post("/api/workspace")
def create_workspace_endpoint(data: DrawerCreate):
    try:
        create_workspace(token=data.token, label=data.label)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return {"ok": True}

@router.get("/api/workspace/{token}")
def open_workspace_endpoint(token: str):
    try:
        workspace = open_workspace(token)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return workspace

@router.post("/api/workspace/{token}/feedback")
def save_feedback_endpoint(token: str, data: FeedbackCreate):
    feedback = FeedbackEntry(
        text=data.text,
        source=data.source,
        context=data.context,
        entry_type=data.entry_type,
    )

    try:
        feedback_id = save_feedback(token, feedback)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {"feedback_id": feedback_id}

@router.get("/api/workspace/{workspace_id}/feedback")
def list_feedback_endpoint(workspace_id: int):
    feedback = list_feedback(workspace_id)
    return feedback
    
@router.post("/api/workspaces/{workspace_id}/analyze")
