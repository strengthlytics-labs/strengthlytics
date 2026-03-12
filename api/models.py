from pydantic import BaseModel


class DrawerCreate(BaseModel):
    token: str
    label: str | None = None


class FeedbackCreate(BaseModel):
    text: str
    source: str | None = None
    context: str | None = None
    entry_type: str | None = None