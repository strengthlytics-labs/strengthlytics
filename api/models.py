from pydantic import BaseModel


class DrawerCreate(BaseModel):
    token: str
    label: str | None = None