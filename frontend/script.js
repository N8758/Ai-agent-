const API_URL = "https://ai-agent-1-18wb.onrender.com";

function showToast(msg, type = "success") {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.innerText = msg;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// ----------------------------
// Add Task
// ----------------------------
document.getElementById("taskForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("taskName").value.trim();
    const hours = parseFloat(document.getElementById("taskHours").value);
    const deadline = document.getElementById("taskDeadline").value;
    const priority = document.getElementById("taskPriority").value;

    if (!name) return showToast("Task name is required!", "error");
    if (hours <= 0) return showToast("Hours must be greater than zero!", "error");

    const task = { name, estimatedHours: hours, deadline, priority };

    try {
        const res = await fetch(`${API_URL}/tasks`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(task)
        });

        await res.json();
        showToast("Task added successfully!");
        loadTasks();

        document.getElementById("taskForm").reset();
    } catch (error) {
        showToast("Failed to add task!", "error");
    }
});


// ----------------------------
// Load Tasks
// ----------------------------
async function loadTasks() {
    try {
        const res = await fetch(`${API_URL}/tasks`);
        const tasks = await res.json();

        const taskList = document.getElementById("taskList");
        taskList.innerHTML = "";

        tasks.forEach(t => {
            const isOverdue = t.deadline && new Date(t.deadline) < new Date();
            const overdueClass = isOverdue ? "overdue" : "";

            const li = document.createElement("li");
            li.innerHTML = `
                <span class="${overdueClass}">
                    ${t.name} (${t.estimatedHours}h, ${t.priority})
                </span>
                <button onclick="deleteTask(${t.id})">Delete</button>
            `;
            taskList.appendChild(li);
        });
    } catch {
        showToast("Unable to load tasks!", "error");
    }
}

loadTasks();


// ----------------------------
// Delete Task
// ----------------------------
async function deleteTask(id) {
    try {
        await fetch(`${API_URL}/tasks/${id}`, { method: "DELETE" });
        showToast("Task deleted!");
        loadTasks();
    } catch {
        showToast("Failed to delete task!", "error");
    }
}


// ----------------------------
// Generate Schedule
// ----------------------------
document.getElementById("btnSchedule").addEventListener("click", async () => {
    try {
        const res = await fetch(`${API_URL}/schedule`);
        const scheduleData = await res.json();

        const scheduleDiv = document.getElementById("schedule");
        scheduleDiv.innerHTML = "";

        Object.keys(scheduleData).forEach(day => {
            const div = document.createElement("div");
            div.className = "schedule-day";

            div.innerHTML = `<h3>${day}</h3>`;

            scheduleData[day].forEach(item => {
                const p = document.createElement("p");

                if (item.includes("⚠ OVERDUE")) {
                    p.classList.add("overdue-text");
                }

                p.textContent = "- " + item;
                div.appendChild(p);
            });

            scheduleDiv.appendChild(div);
        });

        showToast("Schedule Updated!");
    } catch {
        showToast("Failed to generate schedule", "error");
    }
});
