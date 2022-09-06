import renderNewMessage from './messageRenderer.js';

// This function is ran when the websocket receives the "new_message" event
function newMessageHandler(data) {
    let userChats = document.getElementById('user-chats'); // Get user-chats div
    let el = document.getElementById(`sidechat_${data['chatID']}`); // Get the actual div that holds the chat that the message was sent in
    let chatID = document.getElementById('chatID').getAttribute('data-id'); // Get the the current chat's ID
    userChats.prepend(el); // Move the side chat div to the top of the list
    if (chatID === data['chatID']) {
        // If the user is currently on the chat that the message was sent in, this functon is run to render the new message
        renderNewMessage(data);
    } else {
        // Otherwise, increment the notification div
        let el_notifs = document.getElementById(`notification_${data['chatID']}`); // Get the div that holds the notifications for this chat
        el_notifs.classList.remove('hidden'); // If the div is hidden, make it visible
        el_notifs.innerText = (parseInt(el_notifs.innerText) + 1).toString(); // Increment the value in the div
        // Make a request to the backend to increment the amount of unread messages on this chat for the user
        $.ajax({
            url: '/api/v1/internal/update/unread',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                chat_id: chatID
            })
        });
    }
}

export default newMessageHandler;
