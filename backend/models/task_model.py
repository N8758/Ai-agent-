"""
Task model helper. Simple dataclass-like wrapper to create task dicts.
"""

from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Task:
    id: int
    name: str
    estimated_hours: float = 1.0
    deadline: Optional[str] = None  # expect "YYYY-MM-DD" or None
    priority: str = "Medium"
    done: bool = False

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "estimatedHours": self.estimated_hours,
            "deadline": self.deadline,
            "priority": self.priority,
            "done": self.done
        }
