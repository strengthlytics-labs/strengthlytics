from fastapi import APIRouter
from db.db_bridge import create_workspace, open_workspace, save_feedback
from api.models import DrawerCreate, FeedbackCreate
from core.feedback import FeedbackEntry

router = APIRouter()

@router.get("/api/health")
def health():
    return {"ok": True}

@router.post("/api/workspace")
def create_workspace_endpoint(data: DrawerCreate):
    create_workspace(token=data.token, label=data.label)

    return {"ok": True}

@router.get("/api/workspaces/{token}")
def open_workspace_endpoint(token: str):
    workspace = open_workspace(token)

    return workspace

@router.post("/api/workspaces/{token}/feedback")
def save_feedback_endpoint(token: str, data: FeedbackCreate):

    feedback = FeedbackEntry(
    text=data.text,
    source=data.source,
    context=data.context,
    entry_type=data.entry_type
)
    feedback_id = save_feedback(token, feedback)
    return {"feedback_id": feedback_id}
