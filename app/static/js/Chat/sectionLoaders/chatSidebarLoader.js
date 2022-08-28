function load(data, getFirst = false) {
    console.log('Loading data!');
    let s = ``;
    let userID = document.getElementById('user-data').textContent;
    let div = document.getElementById('user-chats');
    data.forEach(function (chat) {
        let unread = chat['members'].filter(function (user) {
            return user['user']['_id'] === userID;
        })[0]['unread'];

        if (data.indexOf(chat) === 0 && getFirst) {
            s += `
        <div onclick="getChat('${chat['_id']}')" id="sidechat_${chat['_id']}" style="margin-bottom:4px;"
         class="p-2 flex items-center space-x-4 dark:bg-gray-600 bg-gray-300 dark:hover:bg-gray-700 hover:bg-gray-200 rounded-lg" >`;
        } else {
            s += `
        <div onclick="getChat('${chat['_id']}')" id="sidechat_${chat['_id']}" style="margin-bottom:4px;"
         class="p-2 flex items-center space-x-4 dark:bg-gray-800/50 bg-gray-300 dark:hover:bg-gray-700 hover:bg-gray-200 rounded-lg" >`;
        }
        if (chat['members'].length === 2) {
            let other = chat['members'].filter(function (user) {
                return user['user']['_id'] != userID;
            })[0]['user'];

            let color;
            if (!other['chatProfile']['offline'] && other['chatProfile']['status'] === 'None') {
                color = 'bg-green-400';
            } else if (other['chatProfile']['status'] === 'Do Not Disturb') {
                color = 'bg-red-500';
            } else if (other['chatProfile']['status'] === 'Idle') {
                color = 'bg-amber-500';
            } else {
                color = 'bg-gray-700';
            }
            let visibility;
            if (unread === '0') {
                visibility = 'hidden';
            } else {
                visibility = '';
            }
            s += `<div class="relative">
 <button class="rounded-full border-gray-300 border-none w-8 h-8
                             dark:bg-gray-900 dark:hover:bg-gray-800 ">
                              
                        <logo image="${other['avatar']['avatar_url']}" no-revert=""  class="h-4 mx-auto my-auto " ><img class="ml-2 h-4 w-4" src="${other['avatar']['avatar_url']}" alt="logo" style="filter: brightness(100%);"></logo>
                    </button>
                    <span id="notification_${chat['_id']}" class="${visibility} overflow-hidden flex flex-grow left-5 top-0 absolute text-sm bg-red-500 border-4 border-white dark:border-gray-800 rounded-full w-5 h-5" style="padding-left:7px;padding-right:7px">${unread}</span>
<span class="bottom-0 left-7 absolute  w-3 h-3 ${color} border-white dark:border-gray-800 rounded-full"></span>
</div>`;
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
            <div class="dark:text-gray-300" style="font-size:15px" id="${chat['_id']}_title" >${other['username']}</div>
            <div class="text-sm text-gray-500 dark:text-gray-400" style="font-size:13px;">${status_emoji} ${status_text}</div>
        </div>
    </div>
    `;
        } else {
            s += `
           <div class="flex items-center space-x-4">
<img class="w-10 h-10 p-1 rounded-full ring-2 ring-gray-300 dark:ring-gray-500" src="${chat['avatar']['avatar_url']}" alt="Bordered avatar">
            `;

            if (!chat['title']) {
                chat['title'] = `${chat['owner']['username']}'s Chat`;
            }

            s += `<div class="space-y-1 font-medium dark:text-white">
    <div style="font-size:15px;" id="${chat['id']}_title" class="dark:text-gray-300">${chat['title']}</div>
    <div style="font-size:13px;" class="text-sm text-gray-500 dark:text-gray-400">${chat['members'].length} Members</div>
</div>
</div>`;
        }
    });

    div.insertAdjacentHTML('beforeend', s);
    console.log('Loaded data!')

}

export default load;