from __future__ import annotations

import psycopg
from typing import Optional, Sequence

from config import get_database_url


def _get_conn():
    return psycopg.connect(get_database_url())


def _get_or_create_workspace_id(cur, token: str, label: Optional[str] = None) -> int:
    # Try get
    cur.execute("SELECT id FROM workspaces WHERE token = %s;", (token,))
    row = cur.fetchone()
    if row:
        return int(row[0])

    # Create
    cur.execute(
        "INSERT INTO workspaces (token, label) VALUES (%s, %s) RETURNING id;",
        (token, label),
    )
    return int(cur.fetchone()[0])


def save_feedback(token: str, entry: Feedback, label: Optional[str] = None) -> int:
    """
    Saves one feedback entry to DB under a workspace token.
    Returns the inserted feedback_entries.id
    """
    if not token or not token.strip():
        raise ValueError("token must not be empty")

    with _get_conn() as conn:
        with conn.cursor() as cur:
            workspace_id = _get_or_create_workspace_id(cur, token.strip(), label=label)

            data = entry.to_dict()
            cur.execute(
                """
                INSERT INTO feedback_entries
                    (workspace_id, entry_date, source, context, entry_type, text)
                VALUES
                    (%s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (
                    workspace_id,
                    data["entry_date"],
                    data["source"],
                    data["context"],
                    data["entry_type"],
                    data["text"],
                ),
            )
            new_id = int(cur.fetchone()[0])
        conn.commit()
    return new_id


def list_feedback(token: str) -> list[dict]:
    """Fetches all feedback rows for a workspace token (newest first)."""
    if not token or not token.strip():
        raise ValueError("token must not be empty")

    with _get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM workspaces WHERE token = %s;", (token.strip(),))
            row = cur.fetchone()
            if not row:
                return []

            workspace_id = int(row[0])
            cur.execute(
                """
                SELECT id, created_at, entry_date, source, context, entry_type, text
                FROM feedback_entries
                WHERE workspace_id = %s
                ORDER BY created_at DESC;
                """,
                (workspace_id,),
            )
            rows = cur.fetchall()

    # Return as simple dicts (UI-friendly)
    return [
        {
            "id": r[0],
            "created_at": r[1],
            "entry_date": r[2],
            "source": r[3],
            "context": r[4],
            "entry_type": r[5],
            "text": r[6],
        }
        for r in rows
    ]