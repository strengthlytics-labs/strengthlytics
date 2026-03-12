from __future__ import annotations

import psycopg
from typing import Optional

from config import get_database_url
from core.feedback import FeedbackEntry


def _get_conn():
    return psycopg.connect(get_database_url())


def normalize_token(token: str) -> str:
    return (token or "").strip().upper()



def create_workspace(token: str, label: Optional[str] = None) -> int:
    token_norm = normalize_token(token)

    if len(token_norm) < 4:
        raise ValueError("Token must be at least 4 characters")

    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM workspaces WHERE token = %s;", (token_norm,))
            if cur.fetchone():
                raise ValueError("Token already exists")

            cur.execute(
                "INSERT INTO workspaces (token, label) VALUES (%s, %s) RETURNING id;",
                (token_norm, label),
            )
            workspace_id = int(cur.fetchone()[0])

        conn.commit()

    return workspace_id

def open_workspace(token: str) ->dict:
    token_norm = normalize_token(token)

    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, token, label FROM workspaces WHERE token = %s;", (token_norm,))
            workspace = cur.fetchone()
            if workspace is None:
                raise ValueError("workspace not found")
            
            workspace_id,workspace_token, workspace_label = workspace

    return {
        "id": workspace_id,
        "token": workspace_token,
        "label": workspace_label
        }


def save_feedback(token, feedback):
    token_norm = normalize_token(token)

    with _get_conn() as conn:
        with conn.cursor() as cur: 
            cur.execute("SELECT id FROM workspaces WHERE token = %s;", (token_norm,))
            workspace = cur.fetchone()           
            if workspace is None:
                raise ValueError("workspace not found")
            workspace_id = workspace[0]
            cur.execute(
                "INSERT INTO feedback_entries (workspace_id, feedback_date, text, source, context, entry_type ) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;", 
                (workspace_id, feedback.feedback_date, feedback.text, feedback.source, feedback.context, feedback.entry_type,),
                )
        
            feedback_entry_id = int(cur.fetchone()[0])

        conn.commit()
    return feedback_entry_id