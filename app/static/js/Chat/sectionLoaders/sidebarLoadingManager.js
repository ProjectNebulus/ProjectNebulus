import load from './chatSidebarLoader.js';

function makeCall(getFirst = true) {


    let chatAmount = document.getElementById('user-chats').childElementCount;
    $.ajax({
        url: '/api/v1/internal/fetch-chats',
        type: 'POST',
        beforeSend: function () {
            // $('#user-chats').hide();
            $('#chat-list-loading').show();
        },
        contentType: 'application/json',
        data: JSON.stringify({
            index: chatAmount
        })
    }).done(function (data) {
        console.log('Made call!');
        load(data, getFirst);
        if (getFirst) {
            let selected = document.getElementById('user-chats');
            selected.children[0].click();
        }
        $('#chat-list-loading').hide();
        $('#user-chats').show();
    });
}

export default makeCall;