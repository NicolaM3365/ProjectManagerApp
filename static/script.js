// Function to add a new task

const addNewTask = (project_id, name, description, status, assigned_to) => {
    // Find the project by project_id
    const project = projects.find(p => p.project_id === project_id);

    if (!project) return; // Handle error: no project with the provided project_id exists

    if (!project.tasks) project.tasks = []; // Initialize tasks array if it doesn't exist

    // Generate a new task_id based on existing task_ids
    const newTaskId = project.tasks.length ? Math.max(...project.tasks.map(t => t.task_id)) + 1 : 1;

    // Assign the new task to the project's tasks.
    const newTask = { task_id: newTaskId, name, description, status, assigned_to };
    project.tasks.push(newTask);

    // Optionally: Call a function to update the UI or perform other actions
    renderTasks(); // Example: this could re-render the list of tasks in the UI
};



// Function to edit an existing task
const editTask = (id, updatedName, updatedDescription, updatedStatus, updatedAssignedTo) => {
    const task = project.tasks.find(t => t.id === id);
    if (task) {
        task.name = updatedName;
        task.description = updatedDescription;
        task.status = updatedStatus;
        task.assigned_to = updatedAssignedTo;
        renderTasks();
    }
};

// Function to delete a task
const deleteTask = (id) => {
    const index = project.tasks.findIndex(t => t.id === id);
    if (index > -1) {
        project.tasks.splice(index, 1);
        renderTasks();
    }
};

// Function to render tasks
const renderTasks = () => {
    const taskTable = document.getElementById('taskTable');
    taskTable.innerHTML = '';
    project.tasks.forEach(task => {
        const row = `
            <tr>
                <td>${task.name}</td>
                <td>${task.description}</td>
                <td>${task.status}</td>
                <td>${task.assigned_to}</td>
                <td>
                    <button class="editTask" data-task-id="${task.id}">Edit</button>
                    <button class="deleteTask" data-task-id="${task.id}">Delete</button>
                </td>
            </tr>
        `;
        taskTable.innerHTML += row;
    });
};

// Event listener for adding new task
document.getElementById('newTask').addEventListener('click', () => {
    // Open modal and get details (Assuming a modal will be used)
    const newName = prompt("Enter name for new task:");
    const newDescription = prompt("Enter description for new task:");
    const newStatus = prompt("Enter status for new task:");
    const newAssignedTo = prompt("Enter assigned_to for new task:");
    addNewTask(newName, newDescription, newStatus, newAssignedTo);
});

// Event listeners for editing and deleting tasks
document.addEventListener('click', event => {
    if (event.target.classList.contains('editTask')) {
        const id = parseInt(event.target.dataset.taskId);
        const task = project.tasks.find(t => t.id === id);

        // Open modal and get updated details (Assuming a modal will be used)
        const updatedName = prompt("Enter new name for task:", task.name);
        const updatedDescription = prompt("Enter new description for task:", task.description);
        const updatedStatus = prompt("Enter new status for task:", task.status);
        const updatedAssignedTo = prompt("Enter new assigned_to for task:", task.assigned_to);

        editTask(id, updatedName, updatedDescription, updatedStatus, updatedAssignedTo);
    } else if (event.target.classList.contains('deleteTask')) {
        const id = parseInt(event.target.dataset.taskId);
        const confirmDelete = confirm("Are you sure you want to delete this task?");
        if (confirmDelete) {
            deleteTask(id);
        }
    }
});

// Initial rendering of tasks
window.addEventListener('DOMContentLoaded', () => {
    renderTasks();
});



"""included below is the code for the server side"""

async function deleteTask(id) {
    // Delete from the client-side data model first (for immediate UI update)
    const index = project.tasks.findIndex(t => t.id === id);
    if (index > -1) {
        project.tasks.splice(index, 1);
        renderTasks();
    }

    // Then notify the server to delete it permanently from JSON
    const response = await fetch(`/api/delete_task/${id}`, {
        method: "DELETE"
    });

    if (response.ok) {
        console.log("Task deleted successfully on server");
    } else {
        console.log("Failed to delete task on server");
    }
}


