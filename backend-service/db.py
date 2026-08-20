import os

import psycopg


def get_connection():
    """Create and return a PostgreSQL database connection."""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    return psycopg.connect(database_url)

def check_database():
    """Check whether PostgreSQL is reachable."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            return cur.fetchone() == (1,)

def init_db():
    """Create the messages table if it does not already exist."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )


def save_message(message):
    """Save a message to PostgreSQL."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO messages (content)
                VALUES (%s)
                """,
                (message,),
            )


def get_latest_message():
    """Return the most recently saved message."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT content
                FROM messages
                ORDER BY id DESC
                LIMIT 1
                """
            )

            row = cur.fetchone()

    return row[0] if row else None