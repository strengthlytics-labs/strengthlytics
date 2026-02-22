import os
import psycopg

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS workspaces (
    id           BIGSERIAL PRIMARY KEY,
    token        TEXT NOT NULL UNIQUE,
    label        TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS feedback_entries (
    id            BIGSERIAL PRIMARY KEY,
    workspace_id  BIGINT NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    entry_date    DATE NOT NULL DEFAULT CURRENT_DATE,
    source        TEXT,
    context       TEXT,
    entry_type    TEXT,
    text          TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_feedback_workspace_created_at
ON feedback_entries (workspace_id, created_at DESC);
"""

def get_db_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("Missing DATABASE_URL env var.")
    return db_url

def init_db() -> None:
    db_url = get_db_url()
    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)
        conn.commit()
    print("✅ Database initialized.")

if __name__ == "__main__":
    init_db()