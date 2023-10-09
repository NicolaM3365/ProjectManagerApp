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
        return char.charCodeAt(0)*LARGE_PRIME + (acc << 5) - acc;
    }, 0);
    return `hsl(${stringUniqueHash % 360}, 95%, 35%)`;
}
