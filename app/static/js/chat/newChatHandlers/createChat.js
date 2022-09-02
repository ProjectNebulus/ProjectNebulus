// Function to create a chat
// The websocket emits a message to create a chat
// The webserver recieves this message and creates a chat
// The webserver emits a message to all of the members that are added
function createChat(members, socket) {
    document.getElementById('dropdown').style.display = 'none';
    socket.emit('new_chat', {members: [members]});
}

export default createChat;
