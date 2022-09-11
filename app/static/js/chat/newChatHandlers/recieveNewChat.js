function handleNewChat(chat, socket) {
    let el = document.getElementById('user-chats');
    el.innerHTML = '';
    let s = ``;
    s += `
    <div onclick="getChat('${chat['_id']}')" id="sidechat_${chat['_id']}" style="margin-bottom:15px;"
     class="p-2 flex items-center space-x-4 dark:bg-gray-800/50 bg-gray-30/500 dark:hover:bg-gray-700/50 hover:bg-gray-200/50  rounded-lg" >`;
    if (chat['members'].length === 2) {
        let other = chat['members'].filter(function (user) {
            return user['_id'] != userID;
        })[0];

        if (other['chatProfile']['status'] === 'Online') {
            s += `<div class="relative">
<button class="rounded-full border-gray-300 border-none w-8 h-8
                             dark:bg-gray-900 dark:hover:bg-gray-800 ">
                        <logo image="${other['avatar']['avatar_url']}" no-revert=""  class="h-4 mx-auto my-auto "><img alt="logo" style="filter: brightness(100%);" ></logo>
                    </button>
<span class="bottom-0 left-7 absolute  w-3 h-3 bg-green-400 border-white dark:border-gray-800 rounded-full"></span>
</div>`;
        } else if (other['chatProfile']['status'] === 'Do Not Disturb') {
            s += `<div class="relative">
<button class="rounded-full border-gray-300 border-none w-8 h-8
                             dark:bg-gray-900 dark:hover:bg-gray-800 ">
                        <logo image="${other['avatar']['avatar_url']}" no-revert="" class="h-4 mx-auto my-auto " ><img alt="logo" style="filter: brightness(100%);" ></logo>
                    </button><span class="bottom-0 left-7 absolute  w-3.5 h-3.5 bg-red-500 border-2 border-white dark:border-gray-800 rounded-full"></span>
</div>`;
        } else {
            s += `<div class="relative">
                    <button class="rounded-full border-gray-300 border-none w-8 h-8
                             dark:bg-gray-900 dark:hover:bg-gray-800 ">
                        <logo image="${other['avatar']['avatar_url']}" no-revert=""  class="h-4 mx-auto my-auto " ><img alt="logo" style="filter: brightness(100%);"></logo>
                    </button><span class="bottom-0 left-7 absolute  w-3.5 h-3.5 bg-gray-700 border-2 border-white dark:border-gray-800 rounded-full"></span>
</div>`;
        }
        let status_emoji = other['chatProfile']['status_emoji'];
        if (!status_emoji) {
            status_emoji = '';
        }
        let status_text = other['chatProfile']['status_text'];
        if (!status_emoji) {
            status_text = '';
        }
        s += `
        <div class="space-y-1 font-medium dark:text-white">
            <div class="dark:text-gray-300" style="font-size:15px">${other['username']}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400" style="font-size:13px;">${status_emoji} ${status_text}</div>
        </div>
    </div>

    `;
    } else {
        s += `
           <div class="flex items-center space-x-4">
<button class="rounded-full border-gray-300 border-none w-8 h-8
                             dark:bg-gray-900 dark:hover:bg-gray-800 ">
                        <logo image="${chat['avatar']['avatar_url']}" no-revert=""><img alt="logo" style="filter: brightness(100%);" class="h-4 mx-auto my-auto " ></logo>
                    </button>
            `;

        if (!chat['title']) {
            chat['title'] = `${chat['owner']['username']}'s Chat`;
        }

        s += `<div class="space-y-1 font-medium dark:text-white">
    <div style="font-size:15px;" class="dark:text-gray-300">${chat['title']}</div>
    <div style="font-size:13px;" class="text-sm text-gray-500 dark:text-gray-400">${chat['members'].length} Members</div>
</div>
</div>`;
    }
    socket.emit('join_a_room', data['id']);
}
