function loadSocket(io) {
    let socket = io.connect('https://' + document.domain + ':' + location.port + '/chat', {transports: ['websocket', 'polling', 'flashsocket']}); // Initialize the websocket
    socket.emit('user_loaded', {}); // Emit the "user_loaded" event. This will add the user to all of their chat "rooms"
    return socket;
}

export default loadSocket;
