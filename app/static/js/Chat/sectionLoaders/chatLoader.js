import formatTime from "../timeUtils/formatTime.js";
import timeDiff from "../timeUtils/timeDiff.js";
import toggleChat from "../sectionTogglers/chatToggler.js";
import replaceURLs from "../messageProcessing/replaceURLs.js";

let show_preview = false;

function getChat(chatID) {
    if (document.body.contains(document.getElementById('chatID'))) {
        if (chatID === document.getElementById('chatID').getAttribute('data-id')) {
            return false;
        }
    }
    toggleChat();
    document.getElementById(`notification_${chatID}`).classList.add('hidden');
    $.ajax({
        url: '/api/v1/internal/get-chat',
        type: 'POST',
        beforeSend: function () {
            if (!('hidden' in document.getElementById('preview_border').classList)) {
                document.getElementById('preview_border').classList.add('hidden');
                show_preview = true;
            }

            document.getElementById('chat').classList.add('hidden');
            $('#chat-members').hide();
            $('#chat-loading').show();
            $('#chat-member-loading').show();
        },
        contentType: 'application/json',
        data: JSON.stringify({
            chatID: chatID
        }),
        //right click: Profile, Close DM, Add Friend, Block, Mute @Coder N, Copy ID
        success: function (chat) {
            let dropdowns = [];
            let chat_el = document.getElementById('chat');
            let members = document.getElementById('chat-members');
            let chatContent = ``;
            let chatMembers = ``;
            let el = document.getElementById(`sidechat_${chat['_id']}`);
            let userChats = document.getElementById('user-chats');
            let userID = document.getElementById('user-data').textContent;
            userChats = [...userChats.children];
            userChats.map(function (elem) {
                elem.classList.remove('dark:bg-gray-600');
                elem.classList.add('dark:bg-gray-800/50');
            });
            el.classList.add('dark:bg-gray-600');
            el.classList.remove('dark:bg-gray-800/50');
            chatContent += `<div id="chatID" data-id="${chat['_id']}" class="w-0 h-0"></div>`;
            chat_el.innerHTML = '';
            chat_el.insertAdjacentHTML('beforeend', chatContent);
            chatContent = ``;

            if (chat['messages'].length === 0)
                return;


            chat['messages'].forEach(function (message, index) {
                let l = message['content'].match(/<img src="https:\/\/twemoji.maxcdn.com/g);

                if (!(l)){
                    l = 0;
                } else {
                    l = l.length;
                }

                if (l === 1 && message['content'].slice(-1) === '>'){
                    message['content'] = message['content'].slice(0, -7)+'w-10 h-10">';
                }
                message['content'] = replaceURLs(message['content'], message['id']);
                message['content'] = message['content'].replace('<br>', '');
                let prevMessage;
                if (index > 0) {
                    prevMessage = chat['messages'][index - 1];
                } else {
                    prevMessage = message;
                }

                if (prevMessage['sender']['username'] !== message['sender']['username'] || timeDiff(prevMessage, message) || index === 0) {

                    prevMessage['send_date'] = formatTime(prevMessage['send_date']);
                    prevMessage['content'] = prevMessage['content'].replace('<br>', '');
                    chatContent += `
                    <div class="flex mb-1 items-top space-x-4 mt-6 hover:bg-gray-100/50 dark:hover:bg-gray-700/50">
                        <img class="mt-1 w-10 h-10 rounded-full" data-dropdown-toggle="user_${prevMessage['sender']['username']}"
                             src="${prevMessage["sender"]["avatar"]["avatar_url"]}"
                             alt="${prevMessage["sender"]["username"]}'s Profile Picture">
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
        ${formatTime(message['send_date'], true)}</div> <div id="content_${message['id']}" class="message text-sm text-gray-500 dark:text-gray-400  mr-2">${message['content']}</div>`;
                }

                if (!dropdowns.includes(message["sender"]["username"])) {
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
                    dropdowns.push(message["sender"]["username"]);
                }
                chat_el.insertAdjacentHTML('beforeend', chatContent);
                chatContent = ``;
            });


            let other_color;

            chat['members'].forEach(function (other) {
                let color, chatProfile = other['user']['chatProfile'];
                if (!chatProfile['offline'] && chatProfile['status'] === 'None') color = 'bg-green-400';
                else if (chatProfile['status'] === 'Do Not Disturb') color = 'bg-red-500';
                else if (chatProfile['status'] === 'Idle') color = 'bg-amber-500';
                else color = 'bg-gray-700';

                if (other['user']['_id'] !== userID && chat['members'].length === 2) other_color = color;
                chatMembers += `
<div oncontextmenu='profile(this)' style="margin-bottom:4px;"
         class="p-2 flex items-center space-x-4 dark:bg-gray-800/50 bg-gray-300 dark:hover:bg-gray-700 hover:bg-gray-200 rounded-lg" id="member_${other['_id']}">`;
                chatMembers += `<div class="relative">
<img class="w-10 h-10 rounded-full" src="${other['user']['avatar']['avatar_url']}" alt="${other["user"]["username"]}'s Profile Picture">
<span class="bottom-0 left-7 absolute w-3.5 h-3.5 ${color} border-2 border-white dark:border-gray-800 rounded-full"></span>
</div>`;

                let status_emoji = chatProfile['status_emoji'];
                if (!status_emoji) status_emoji = '';

                let status_text = chatProfile['status_text'];
                if (!status_emoji) status_text = '';

                chatMembers += `
        <div class="space-y-1 font-medium dark:text-white">
            <div class="dark:text-gray-300" style="font-size:15px">${other['user']['username']}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400" style="font-size:13px;">${status_emoji} ${status_text}</div>
        </div>
    </div>
    `;
            });

            members.innerHTML = '';
            members.insertAdjacentHTML('beforeend', chatMembers);

            let tx;
            $('#chat-header').remove();
            let ms = document.getElementById(`${chat['_id']}_title`).innerText;
            if (chat['members'].length === 2) {
                tx = `
            <div id="chat-header" class = "flex items-center py-2 px-3 bg-gray-50/50 dark:bg-gray-700/50 backdrop-blur-sm dark:text-white text-black py-3 noselect " >
                <i class="material-icons text-gray-400"> alternate_email </i>
            <span class="mx-4">${ms}</span>
            <span class="inline-block w-3 h-3 ${other_color} rounded-full"></span>
        </div>
        <div id="chat-loading2"
                     style="height:calc(100% - 80px);
                            overflow-y:hidden; display:none;">
                    <div role="status"
                         class="sticky overflow-y-scroll-auto p-4 max-w-lg rounded shadow md:p-6  animate-pulse"
                         style="overflow-y:scroll;">
                        <div class="w-full flex items-top mt-4 space-x-3">
                            <svg class="w-14 h-14 text-gray-200 dark:text-gray-700"
                                 aria-hidden="true"
                                 fill="currentColor"
                                 viewBox="0 0 20 20"
                                 xmlns="http://www.w3.org/2000/svg">
                                <path fill-rule="evenodd"
                                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"
                                      clip-rule="evenodd">
                                </path>
                            </svg>
                            <div class="mt-2 w-full">
                                <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-32 mb-2">
                                </div>
                                <div class="w-48 mb-1 h-2 bg-gray-200 rounded-full dark:bg-gray-700">
                                </div>
                                <div class="w-full mb-2 h-2 bg-gray-200 rounded-full dark:bg-gray-700">
                                </div>
                                <div class="flex justify-center items-center mb-4 h-48 bg-gray-300 rounded dark:bg-gray-700">
                                    <svg class="w-12 h-12 text-gray-200 dark:text-gray-600"
                                         xmlns="http://www.w3.org/2000/svg"
                                         aria-hidden="true"
                                         fill="currentColor"
                                         viewBox="0 0 640 512">
                                        <path d="M480 80C480 35.82 515.8 0 560 0C604.2 0 640 35.82 640 80C640 124.2 604.2 160 560 160C515.8 160 480 124.2 480 80zM0 456.1C0 445.6 2.964 435.3 8.551 426.4L225.3 81.01C231.9 70.42 243.5 64 256 64C268.5 64 280.1 70.42 286.8 81.01L412.7 281.7L460.9 202.7C464.1 196.1 472.2 192 480 192C487.8 192 495 196.1 499.1 202.7L631.1 419.1C636.9 428.6 640 439.7 640 450.9C640 484.6 612.6 512 578.9 512H55.91C25.03 512 .0006 486.1 .0006 456.1L0 456.1z">
                                        </path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                        <div class="w-full flex items-center mt-4 space-x-3">
                            <div class="w-full flex items-center mt-4 space-x-3">
                                <svg class="w-14 h-14 text-gray-200 dark:text-gray-700"
                                     aria-hidden="true"
                                     fill="currentColor"
                                     viewBox="0 0 20 20"
                                     xmlns="http://www.w3.org/2000/svg">
                                    <path fill-rule="evenodd"
                                          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"
                                          clip-rule="evenodd">
                                    </path>
                                </svg>
                                <div class="w-full">
                                    <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-32 mb-2">
                                    </div>
                                    <div class="w-48 mt-1 h-2 bg-gray-200 rounded-full dark:bg-gray-700">
                                    </div>
                                    <div class="mt-1 w-full h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-1 ">
                                    </div>
                                    <div class="w-full h-2 bg-gray-200 rounded-full dark:bg-gray-700">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="w-full flex items-top mt-4 space-x-3">
                            <div class="w-full flex items-top mt-4 space-x-3">
                                <svg class="w-14 h-14 text-gray-200 dark:text-gray-700"
                                     aria-hidden="true"
                                     fill="currentColor"
                                     viewBox="0 0 20 20"
                                     xmlns="http://www.w3.org/2000/svg">
                                    <path fill-rule="evenodd"
                                          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"
                                          clip-rule="evenodd">
                                    </path>
                                </svg>
                                <div class="w-full">
                                    <div class="h-2.5 bg-gray-200 rounded-full dark:bg-gray-700 w-32 mb-2">
                                    </div>
                                    <div class="w-full h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-1 ">
                                    </div>
                                    <div class="w-48 h-2 bg-gray-200 rounded-full dark:bg-gray-700 mb-2">
                                    </div>
                                    <div class="flex justify-center items-center mb-4 h-48 bg-gray-300 rounded dark:bg-gray-700">
                                        <svg class="w-12 h-12 text-gray-200 dark:text-gray-600"
                                             xmlns="http://www.w3.org/2000/svg"
                                             aria-hidden="true"
                                             fill="currentColor"
                                             viewBox="0 0 640 512">
                                            <path d="M480 80C480 35.82 515.8 0 560 0C604.2 0 640 35.82 640 80C640 124.2 604.2 160 560 160C515.8 160 480 124.2 480 80zM0 456.1C0 445.6 2.964 435.3 8.551 426.4L225.3 81.01C231.9 70.42 243.5 64 256 64C268.5 64 280.1 70.42 286.8 81.01L412.7 281.7L460.9 202.7C464.1 196.1 472.2 192 480 192C487.8 192 495 196.1 499.1 202.7L631.1 419.1C636.9 428.6 640 439.7 640 450.9C640 484.6 612.6 512 578.9 512H55.91C25.03 512 .0006 486.1 .0006 456.1L0 456.1z">
                                            </path>
                                        </svg>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <span class="sr-only">Loading...</span>
                    </div>
                    <span class="sr-only">Loading...</span>
                </div>
        `;
                ms = '@' + ms;
            } else {
                tx = `
            <div
            id="chat-header" class = "flex items-center py-2 px-3 bg-gray-50/50 dark:bg-gray-700/50 backdrop-blur-sm dark:text-white text-black py-3 noselect " >
            <span class="mx-4">${ms}</span>
        </div>
        `;
            }

            chat_el.insertAdjacentHTML('beforebegin', tx);

            document.getElementById("msg_content").placeholder = `Message ${ms}`;

            $('#chat-loading').hide();
            let preview = document.getElementById('preview_border');
            document.getElementById('chat').style.height = preview.style.display === "none" ? "80%" : "64%";
            document.getElementById('chat').classList.remove('hidden');

            if (show_preview) document.getElementById('preview_border').classList.remove('hidden');

            let el_notifs = document.getElementById(`notification_${chat['_id']}`);
            el_notifs.classList.add('hidden');
            el_notifs.innerText = '0';
            $('#chat-member-loading').hide();
            $('#chat-members').show();
        }
    });
}

export default getChat;