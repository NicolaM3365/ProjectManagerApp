// Function to add a new task
const addNewTask = (title, description, status, assigned_to) => {
    const newId = project.tasks.length ? Math.max(project.tasks.map(t => t.id)) + 1 : 1;
    const newTask = { id: newId, title, description, status, assigned_to };
    project.tasks.push(newTask);
    renderTasks();
};

// Function to edit an existing task
const editTask = (id, updatedTitle, updatedDescription, updatedStatus, updatedAssignedTo) => {
    const task = project.tasks.find(t => t.id === id);
    if (task) {
        task.title = updatedTitle;
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
                <td>${task.title}</td>
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
    const newTitle = prompt("Enter title for new task:");
    const newDescription = prompt("Enter description for new task:");
    const newStatus = prompt("Enter status for new task:");
    const newAssignedTo = prompt("Enter assigned_to for new task:");
    addNewTask(newTitle, newDescription, newStatus, newAssignedTo);
});

// Event listeners for editing and deleting tasks
document.addEventListener('click', event => {
    if (event.target.classList.contains('editTask')) {
        const id = parseInt(event.target.dataset.taskId);
        const task = project.tasks.find(t => t.id === id);

        // Open modal and get updated details (Assuming a modal will be used)
        const updatedTitle = prompt("Enter new title for task:", task.title);
        const updatedDescription = prompt("Enter new description for task:", task.description);
        const updatedStatus = prompt("Enter new status for task:", task.status);
        const updatedAssignedTo = prompt("Enter new assigned_to for task:", task.assigned_to);

        editTask(id, updatedTitle, updatedDescription, updatedStatus, updatedAssignedTo);
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




