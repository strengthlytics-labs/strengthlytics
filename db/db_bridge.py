from __future__ import annotations

import psycopg
from typing import Optional

from config import get_database_url


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

