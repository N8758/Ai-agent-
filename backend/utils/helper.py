"""
Helper utilities to read/write JSON tasks safely.
"""

import json
import os
from threading import Lock

_lock = Lock()


def load_tasks(path):
    """
    Loads tasks from the JSON file at `path`.
    Returns a list (possibly empty).
    """
    if not os.path.exists(path):
        # ensure directory exists
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump([], f)
        return []

    with _lock:
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if not isinstance(data, list):
                    # reset if file corrupted
                    return []
                return data
            except json.JSONDecodeError:
                return []


def save_tasks(path, tasks):
    """
    Writes the list of tasks to path atomically.
    """
    # simple lock to avoid concurrent writes
    with _lock:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
