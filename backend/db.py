import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "tasks.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            estimated_hours REAL,
            deadline TEXT,
            priority TEXT,
            done INTEGER DEFAULT 0
        );
    """)
    conn.commit()
    conn.close()

def get_tasks():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "id": r["id"],
            "name": r["name"],
            "estimatedHours": r["estimated_hours"],
            "deadline": r["deadline"],
            "priority": r["priority"],
            "done": bool(r["done"])
        })
    return result

def add_task(name, hours, deadline, priority):
    conn = get_conn()
    conn.execute(
        "INSERT INTO tasks (name, estimated_hours, deadline, priority) VALUES (?, ?, ?, ?)",
        (name, hours, deadline, priority)
    )
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = get_conn()
    cur = conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted

def mark_done(task_id):
    conn = get_conn()
    cur = conn.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
    conn.commit()
    updated = cur.rowcount > 0
    conn.close()
    return updated
