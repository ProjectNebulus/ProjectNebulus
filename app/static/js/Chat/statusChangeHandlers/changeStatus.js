// This function emits the "user_status_change" event. This event is received by the webserver and the user's status is changed
function changeStatus(status, socket) {
    socket.emit('user_status_change', {chatType: 'chat', status: status});
}

window.onbeforeunload = function () {
    changeStatus('Offline'); // Will set the user's offline value to True
};
window.addEventListener('load', function () {
    changeStatus('Online'); // Will set the users' offline value to False
});