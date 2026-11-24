
import sqlite3
from pathlib import Path
from datetime import datetime


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "nexus.db"

DATA_DIR.mkdir(exist_ok=True)


class NexusMemory:

    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    instruction TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'PENDING',
                    result TEXT,
                    error TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

    def create_task(self, instruction):
        now = datetime.now().isoformat(timespec="seconds")

        with self.connection:
            cursor = self.connection.execute("""
                INSERT INTO tasks
                (instruction, status, created_at, updated_at)
                VALUES (?, 'PENDING', ?, ?)
            """, (instruction, now, now))

        return cursor.lastrowid

    def update_task(self, task_id, status, result=None, error=None):
        allowed_statuses = {
            "PENDING",
            "RUNNING",
            "AWAITING_APPROVAL",
            "COMPLETED",
            "FAILED"
        }

        if status not in allowed_statuses:
            raise ValueError("Invalid task status")

        now = datetime.now().isoformat(timespec="seconds")

        with self.connection:
            self.connection.execute("""
                UPDATE tasks
                SET status = ?,
                    result = ?,
                    error = ?,
                    updated_at = ?
                WHERE task_id = ?
            """, (status, result, error, now, task_id))

    def get_task(self, task_id):
        cursor = self.connection.execute(
            "SELECT * FROM tasks WHERE task_id = ?",
            (task_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_tasks(self):
        cursor = self.connection.execute(
            "SELECT * FROM tasks ORDER BY task_id DESC"
        )
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        self.connection.close()
