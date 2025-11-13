"""
AI Task Scheduler (Version 3)
----------------------------------
✔ Fully Date-Based Scheduling
✔ Tasks grouped under exact deadline date
✔ Maintains AI scoring + urgency logic
✔ Detects overdue tasks
✔ Clean simplest output format

Output Example:
{
    "2025-11-14 (Fri)": ["Task A (2h)", "Task B (1h)"],
    "2025-11-17 (Mon)": ["Task C (3h)"]
}
"""

from datetime import datetime
from collections import OrderedDict

PRIORITY_WEIGHTS = {
    "High": 50,
    "Medium": 30,
    "Low": 10
}


# ----------------------------
# Helper Functions
# ----------------------------

def _parse_deadline(deadline):
    if not deadline:
        return None
    try:
        return datetime.strptime(deadline, "%Y-%m-%d")
    except:
        return None


def _weekday_text(date: datetime):
    return date.strftime("%a")  # Mon, Tue, Wed etc.


def _formatted_date(date: datetime):
    return date.strftime("%Y-%m-%d")  # 2025-11-14


def _is_overdue(deadline):
    if not deadline:
        return False
    try:
        d = datetime.strptime(deadline, "%Y-%m-%d")
        return d.date() < datetime.now().date()
    except:
        return False


def _task_score(task):
    """
    Same AI scoring:
    - priority weight
    - near deadline weight
    - urgent boost
    """
    priority = task.get("priority", "Medium")
    hours = float(task.get("estimatedHours", 1))

    priority_w = PRIORITY_WEIGHTS.get(priority, 20)

    deadline_str = task.get("deadline", None)
    deadline = _parse_deadline(deadline_str)

    # deadline scoring
    if deadline is None:
        deadline_weight = 5
    else:
        days_left = (deadline - datetime.now()).days
        if days_left <= 0:
            deadline_weight = 100
        else:
            deadline_weight = max(10, 50 - days_left)

    urgent_boost = 40 if deadline and (deadline - datetime.now()).days <= 2 else 0

    return priority_w + deadline_weight + urgent_boost


def _sort_tasks(tasks):
    active = [t for t in tasks if not t.get("done", False)]

    # sort by score (desc), then deadline date (asc)
    return sorted(
        active,
        key=lambda x: (
            -_task_score(x),
            x.get("deadline", "9999-12-31")
        )
    )


# ----------------------------
# MAIN: DATE-BASED SCHEDULE
# ----------------------------

def generate_schedule(tasks, daily_hours_override=None):
    """
    DATE BASED SCHEDULING (NO WEEKDAYS)
    -----------------------------------
    Groups tasks under their real deadlines.

    Returns:
    {
        "2025-11-14 (Fri)": ["Work (2h)", "Study (1h)"],
        "2025-11-17 (Mon)": ["AI Agent Build (3h)"]
    }
    """

    task_list = _sort_tasks(tasks)

    schedule = OrderedDict()

    for t in task_list:
        name = t.get("name", "Unnamed Task")
        hours = float(t.get("estimatedHours", 1))
        deadline = t.get("deadline", None)

        # create nice text: "2025-11-14 (Fri)"
        if deadline:
            d = _parse_deadline(deadline)
            weekday = _weekday_text(d)
            date_key = f"{_formatted_date(d)} ({weekday})"
        else:
            date_key = "No Deadline"

        # overdue marking
        is_over = _is_overdue(deadline)
        display_name = f"⚠ OVERDUE: {name}" if is_over else name

        # create date block
        if date_key not in schedule:
            schedule[date_key] = []

        # add task
        schedule[date_key].append(f"{display_name} ({hours}h)")

    return schedule
