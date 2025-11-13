from flask import Flask, request, jsonify
from flask_cors import CORS
from db import init_db, get_tasks, add_task, delete_task, mark_done
from scheduler import generate_schedule

app = Flask(__name__)
CORS(app)   # Fix CORS issue automatically

# Initialize SQLite database
init_db()


# -------------------------
# HOME ROUTE
# -------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Task Agent Backend (SQLite) Running"}), 200


# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# -------------------------
# GET ALL TASKS
# -------------------------
@app.route("/tasks", methods=["GET"])
def get_tasks_route():
    return jsonify(get_tasks()), 200


# -------------------------
# ADD NEW TASK
# -------------------------
@app.route("/tasks", methods=["POST"])
def add_task_route():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        name = data["name"]
        estimated_hours = float(data.get("estimatedHours", 1))
        deadline = data.get("deadline", None)
        priority = data.get("priority", "Medium")
    except Exception as e:
        return jsonify({"error": "Missing or invalid fields", "details": str(e)}), 400

    add_task(name, estimated_hours, deadline, priority)

    return jsonify({"message": "Task added"}), 201


# -------------------------
# DELETE TASK
# -------------------------
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_route(task_id):
    ok = delete_task(task_id)

    if not ok:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Deleted"}), 200


# -------------------------
# MARK TASK AS DONE
# -------------------------
@app.route("/tasks/<int:task_id>/done", methods=["PUT"])
def mark_done_route(task_id):
    ok = mark_done(task_id)

    if not ok:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Updated"}), 200


# -------------------------
# GENERATE SCHEDULE
# -------------------------
@app.route("/schedule", methods=["GET"])
def get_schedule_route():
    daily_hours = request.args.get("dailyHours", None)

    if daily_hours:
        try:
            daily_hours = float(daily_hours)
        except:
            return jsonify({"error": "dailyHours must be a number"}), 400

    tasks = get_tasks()
    schedule = generate_schedule(tasks, daily_hours_override=daily_hours)

    return jsonify(schedule), 200


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
