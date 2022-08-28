function loadSocket(io) {
    let socket = io.connect('http://' + document.domain + ':' + location.port + '/chat'); // Initialize the websocket
    socket.emit('user_loaded', {}); // Emit the "user_loaded" event. This will add the user to all of their chat "rooms"
    return socket;
}

export default loadSocket;