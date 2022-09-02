import formatTime from '../../timeUtils/formatTime.js';
import replaceURLs from '../../messageProcessing/replaceURLs.js';

function renderNewMessage(message) {
    let chat_el = document.getElementById('chat');
    let l = message['content'].match(/<img src="https:\/\/twemoji.maxcdn.com/g);

    if (!l) {
        l = 0;
    } else {
        l = l.length;
    }
    if (l === 1 && message['content'].slice(-1) === '>') {
        message['content'] = message['content'].slice(0, -7) + 'w-10 h-10">';
    }
    if (!message['group']) {
        chat_el.insertAdjacentHTML(
            'afterbegin',
            `<div class="flex items-top space-x-4 mt-2" id="${message['id']}">
                    <img class="mt-1 w-10 h-10 rounded-full"
                         src="${message['author'][2]}"
                         alt="">
                    <div class="space-y-1 font-medium dark:text-white">
                        <div>${
                message['author'][1]
            } <span class="ml-3 text-sm text-gray-400">${formatTime(
                message['send_date']
            )}</span></div>
                        <div id="content_${
                message['id']
            }" class="text-sm text-gray-500 dark:text-gray-400">${
                message['content']
            }</div>
                    </div>
                </div>`
        );
    } else {
        console.log(formatTime(message['send_date'], true));
        chat_el.insertAdjacentHTML(
            'afterbegin',
            `<div class="group flex flex-row hover:bg-gray-100/50 dark:hover:bg-gray-700/50"><div class="opacity-0 text-gray-600 uppercase mr-2 group-hover:opacity-100" style="margin-top:3px;font-size:10px;width:50px;">
        ${formatTime(message['send_date'], true)}</div> <div id="content_${
                message['id']
            }" class="message text-sm text-gray-500 dark:text-gray-400  mr-2">${
                message['content']
            }</div>`
        );
    }

    let url = replaceURLs(message['content'], message['id']);
    console.log(url);
    $(`#content_${message['id']}`).html(url);
    if ($('#chat').children.length >= 40) {
        $('#chat').children.last.remove();
    }
    $('#chat').scrollTop(0);
}

export default renderNewMessage;
