import toIsoString from '../timeUtils/toIsoString.js';

$('#pressMe').on('click', sendMessage);
function sendMessage(socket) {
    let chatBox = document.getElementById('msg_content');
    if (!/\S/.test(chatBox.value)) return;

    let el = document.getElementById('preview');
    el.classList.add('hidden');
    chatBox.value = '';
    let val = el.innerHTML.replace('<br>', '');
    el.innerHTML = '';

    if (val.endsWith('<br>')) val = val.substring(0, val.length - 4);

    let send_date = new Date();
    send_date = toIsoString(send_date);
    let chatID = document.getElementById('chatID').getAttribute('data-id');
    socket.emit('new_message', {
        chatType: 'chat',
        chatID: chatID,
        content: val,
        send_date: send_date
    });
}

export default sendMessage;
