import replaceURLs from '../messageProcessing/replaceURLs.js';
import timeDiff from '../timeUtils/timeDiff.js';
import formatTime from '../timeUtils/formatTime.js';

function chatScrollHandler() {
    console.log('chat is scrolling');
    let el = document.getElementById('chat');
    let chat_index = $('.message').length;
    console.log(
        Math.abs(Math.floor(el.scrollHeight - $(this).height()) * -1 - $(this).scrollTop())
    );
    if (Math.abs(Math.floor(el.scrollHeight - $(this).height()) * -1 - $(this).scrollTop()) < 2) {
        let chatID = document.getElementById('chatID').getAttribute('data-id');
        $.ajax({
            url: '/api/v1/internal/fetch-messages',
            type: 'POST',
            contentType: 'application/json',
            beforeSend: function () {
                //document.getElementById('chat').classList.add('hidden');
                $('#chat-loading2').show();
            },
            data: JSON.stringify({
                chatID: chatID,
                current_index: chat_index
            })
        }).done(function (messages) {
            console.log(messages);
            let dropdowns = [];

            let chat_el = document.getElementById('chat');

            let chatContent = ``;

            messages.forEach(function (message, index) {
                let l = message['content'].match(/<img src="https:\/\/twemoji.maxcdn.com/g);

                l = l ? l.length : 0;

                if (l === 1 && message['content'].slice(-1) === '>')
                    message['content'] = message['content'].slice(0, -7) + 'w-10 h-10">';

                message['content'] = replaceURLs(message['content'], message['id']);
                message['content'] = message['content'].replace('<br>', '');
                let prevMessage;
                if (index > 0) prevMessage = messages[index - 1];
                else prevMessage = message;

                if (
                    prevMessage['sender']['username'] !== message['sender']['username'] ||
                    timeDiff(prevMessage, message) ||
                    index === 0
                ) {
                    prevMessage['send_date'] = formatTime(prevMessage['send_date']);
                    prevMessage['content'] = prevMessage['content'].replace('<br>', '');
                    chatContent += `
                    <div class="flex mb-1 items-top space-x-4 mt-6 hover:bg-gray-100/50 dark:hover:bg-gray-700/50">
                        <img class="mt-1 w-10 h-10 rounded-full" data-dropdown-toggle="user_${prevMessage['sender']['username']}"
                             src="${prevMessage['sender']['avatar']['avatar_url']}"
                             alt="${prevMessage['sender']['username']}'s Profile Picture">
                        <div class="space-y-1 font-medium dark:text-white">
                            <div>
                                <span data-dropdown-toggle="user_${prevMessage['sender']['username']}" class="hover:underline cursor-pointer">${prevMessage['sender']['username']}</span>
                                <span class="ml-3 text-sm text-gray-400">${prevMessage['send_date']}</span>
                            </div>
                            <div id="content_${prevMessage['id']}" class="message text-sm text-gray-500 dark:text-gray-400 " style="margin-left:1.5px;">${prevMessage['content']}</div>
                        </div>
                    </div>`;
                } else {
                    chatContent += `<div class="group flex flex-row hover:bg-gray-100/50 dark:hover:bg-gray-700/50"><div class="opacity-0 text-gray-600 uppercase mr-2 group-hover:opacity-100" style="margin-top:3px;font-size:10px;width:50px;">
        ${formatTime(message['send_date'], true)}</div> <div id="content_${
                        message['id']
                    }" class="message text-sm text-gray-500 dark:text-gray-400  mr-2">${
                        message['content']
                    }</div><div class="edit-controls flex bg-gray-500 dark:bg-gray-800/75 material-icons rounded-lg group-hover:opacity-100 opacity-0 text-gray-200 dark:text-gray-500 overflow-hidden shadow" style="margin-top: -20px;" onclick="override=true">
<span class="hover:bg-gray-200 dark:hover:bg-gray-700 p-2">edit</span>
<span onclick="deleteMaterial(this)" class="hover:bg-gray-200 dark:hover:bg-gray-700 p-2">delete</span>
</div>`;
                }

                if (!dropdowns.includes(message['sender']['username'])) {
                    chatContent += `
                        <div id="user_${message['sender']['username']}" class="z-50 hidden bg-white divide-y divide-gray-100 rounded shadow w-80 dark:bg-gray-700 dark:divide-gray-600 rounded-lg block" data-popper-placement="bottom" style="position: absolute; inset: 0px auto auto 0px; margin: 0px; transform: translate3d(0px, 215px, 0px);">
                            <div style="border-radius:10px 10px 0 0; height:60px;background:rgba(191, 198, 205);"></div>
                            <div class="px-4 py-3 text-xl text-gray-900 dark:text-white border-b border-l">
                                <div style="text-align: left; margin-left:3px;">
                                    <div style="margin-top:-60px;">
                                        <img style="background:rgb(18,25,38)" class="w-24 h-24 rounded-full border-white dark:border-gray-700 border-2 object-cover" alt="${message['sender']['username']}'s Profile Picture">
                                        <span class="absolute  w-5 h-5 bg-green-400 border-2 border-white dark:border-gray-700 rounded-full" style="left:90px;top:85px;"></span>
                                    </div>
                                    <div>${message['sender']['username']}</div>
                                    
                                    <input id="msg" placeholder="Message @${message['sender']['username']}" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm
                                               mb-6 rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5
                                               dark:bg-gray-900 dark:border-gray-600 dark:placeholder-gray-400
                                               dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                </div>
                            </div>
                        </div>`;
                    dropdowns.push(message['sender']['username']);
                }
                chat_el.insertAdjacentHTML('beforeend', chatContent);
                chatContent = ``;
            });

            $('#chat-loading2').hide();
            let preview = document.getElementById('preview_border');
            document.getElementById('chat').style.height =
                preview.style.display === 'none' ? '80%' : '64%';
            document.getElementById('chat').classList.remove('hidden');
        });
    }
}

export default chatScrollHandler;
