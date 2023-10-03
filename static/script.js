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




// Create a new socket.io connection object
let socket = io();

/* On first connection, show all previous messages (received from the server) */
socket.on('connect', function () {
    PREVIOUS_MESSAGES.forEach(addMessage);
});

/* When a new message is received from the server, show it */
socket.on('chatEvent', addMessage);

/* When the server sends a clear event, clear the chat display */
socket.on('clearChat', clearChat);

/* When the user submits the form, send the message to the server

Note that it's up to the server to broadcast it to everyone, so that the sender will
only see their own message appear in the chat display when everyone sees it.

This is intentional, to avoid the chat display being out of sync with the server.
But if you want to change this, you can do so by adding a call to addMessage here, and changing
the server to omit the sender from the broadcast.
*/
document.getElementById('chat-form').addEventListener('submit', function (event) {
    event.preventDefault();

    let nameInput = event.target.elements.name;
    if (!nameInput.value) {
        alert('You have to first enter your name!');
        return;
    }

    let messageInput = event.target.elements.message;

    socket.emit('chatEvent', { name: nameInput.value, text: messageInput.value });
    messageInput.value = '';
});

// -------- Helpers --------

/* Add a single message to the chat display element*/
function addMessage(message) {
    // Create a new paragraph element for the message
    let p = document.createElement('p');
    p.innerText = `${message.name}: ${message.text}`;
    p.style.color = nameToColour(message.name);

    // Add the paragraph to the chat display
    let chatDisplay = document.getElementById('chat-display');
    chatDisplay.append(p);

    // Scroll to the bottom of the chat display
    chatDisplay.scrollTo(0, chatDisplay.scrollHeight);
}

/* Clear the chat display element */
function clearChat() {
    document.getElementById('chat-display').innerHTML = '';
}

/* Convert a string to a colour via a basic hash function (consistent colour for each name).
Slightly adapted from https://stackoverflow.com/a/66494926/493553 (CC BY-SA 4.0)
*/
function nameToColour(stringInput) {
    const LARGE_PRIME = 2147483647;
    let stringUniqueHash = Array.from(stringInput).reduce((acc, char) => {
        return char.charCodeAt(0) * LARGE_PRIME + (acc << 5) - acc;
    }, 0);
    return `hsl(${stringUniqueHash % 360}, 95%, 35%)`;
}
