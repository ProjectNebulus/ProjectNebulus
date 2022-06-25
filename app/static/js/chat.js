io = window.io


function createChat(username) {
    document.getElementById("dropdown").style.display = "none";
    const request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/create-chat-dm",
        data: JSON.stringify({
            member: username
        }),

        contentType: 'application/json; charset=utf-8',
    });
    //refresh bar
    document.getElementById("user-chats").innerHTML = "";
    $.ajax({
        url: '/api/v1/internal/fetch-chats',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            index: chatAmount
        })


    }).done(load);
}

function changeSearch() {
    let value = document.getElementById("search").value;
    if (value.length > 0) {
        document.getElementById("search_items").innerHTML = `
<li>
<div class="py-2.5 rounded-lg mx-auto block px-4 py-2 mx-2 dark:hover:text-white">
                <svg role="status" class="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
</svg>
    Searching...
</div>
</li>
            `;
        const request = $.ajax({
            type: "POST",
            url: "/api/v1/internal/search-user",
            data: JSON.stringify({
                search: value
            }),

            contentType: 'application/json; charset=utf-8',
        });
        request.done((data) => {
            document.getElementById("search_items").innerHTML = "";
            let temp_arr = []
            if (data === "0") {
                document.getElementById("search_items").innerHTML += `
                    <li class="text-center mb-5">
                        No Results Found
                    </li>`
            }
            else {
                let datas = data.split("•");
                for (let i = 0; i < datas.length; i++) {

                    if (i % 3 === 0) {
                        temp_arr = [];
                        temp_arr.push(datas[i]);
                    }
                    if (i % 3 === 1) {
                        temp_arr.push(datas[i]);
                    }
                    if (i % 3 === 2) {
                        temp_arr.push(datas[i]);
                        let element = temp_arr;
                        console.log(element);

                        document.getElementById("search_items").innerHTML += `
                    <div>
                        <span onclick="createChat('${element[1]}');" class="truncate py-2.5 rounded-lg mx-auto block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 mx-2 dark:hover:text-white" style="text-align:left;">
                <img src="${element[0]}" class="inline-block w-10 h-10 rounded-full" alt="dates">
                ${element[1]} <span class="text-gray-500 ml-2">${element[2]}</span></span>
                    </div>
`
                    }
                }
            }
        });
    }
}

//setInterval(changeSearch, 500)
//setup before functions
var typingTimer;                //timer identifier
var doneTypingInterval = 5000;  //time in ms, 5 seconds for example
var $input = $('#search');

//on keyup, start the countdown
$input.on('keyup', function () {
    clearTimeout(typingTimer);
    typingTimer = setTimeout(doneTyping, doneTypingInterval);
});

//on keydown, clear the countdown
$input.on('keydown', function () {
    clearTimeout(typingTimer);
});

//user is "finished typing," do something
function doneTyping () {
    changeSearch();
}

function makeCall() {
    let chatAmount = $('#user-chats > div').length;
    console.log(chatAmount);
    $.ajax({
        url: '/api/v1/internal/fetch-chats',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            index: chatAmount
        })


    }).done(load);
}
function updateToMessage(message){
    let chat_el = document.getElementById('chat');
        chat_el.insertAdjacentHTML('afterbegin', `<div class="flex items-top space-x-4 mt-2" id="${message['id']}">
                        <img class="mt-1 w-10 h-10 rounded-full"
                             src="${message['author'][2]}"
                             alt="">
                        <div class="space-y-1 font-medium dark:text-white">
                            <div>${message['author'][1]} <span class="ml-3 text-sm text-gray-400">${message['send_date']}</span></div>
                            <div class="text-sm text-gray-500 dark:text-gray-400">${message['content']}</div>
                        </div>
                    </div>`);


    $('#chat').children().last().remove();
    $('#chat').scrollTop(0);
}
let socket;
$(document).ready(function () {
    makeCall();
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        console.log('socket emitting');
        socket.emit('user_loaded', {});
    });
    socket.on('new_message', function(data){

        console.log('socketio recieved event!');
        let userChats = document.getElementById('user-chats');
        let el = document.getElementById(`sidechat_${data['chatID']}`);
        userChats.prepend(el);


        updateToMessage(data);
    });

    window.onunload = function(){
        socket.emit('user_loaded', {}, function() {
                    socket.disconnect();
        });
    }
    $('#chat').on('scroll', function(){
     console.log('chat is scrolling');
     let el = document.getElementById('chat');
     let chat_index = el.children.length - (Math.floor(el.children.length/2))
     console.log(Math.floor(el.scrollHeight-$(this).height())*-1)
        if($(this).scrollTop()===Math.floor(el.scrollHeight-$(this).height())*-1+100){
         let chatID = document.getElementById('chatID').getAttribute('data-id');
         $.ajax({
             url: '/api/v1/internal/fetch-messages',
             type: 'POST',
             contentType: 'application/json',
             data: JSON.stringify({
                 chatID: chatID,
                 current_index: chat_index
             })
         }).done(function (messages) {
             let chatContent = ``;
             messages.forEach(function (message) {
                 chatContent += `<div class="flex items-top space-x-4 mt-2" id="${message['id']}">
                        <img class="mt-1 w-10 h-10 rounded-full"
                             src="${message['sender']['avatar']['avatar_url']}"
                             alt="">
                        <div class="space-y-1 font-medium dark:text-white">
                            <div>${message['sender']['username']} <span class="ml-3 text-sm text-gray-400">${message['send_date']}</span></div>
                            <div class="text-sm text-gray-500 dark:text-gray-400">${message['content']}</div>
                        </div>
                    </div>`;
             });
             let chat = document.getElementById('chat');
             chat.insertAdjacentHTML('beforeend', chatContent);
         });
     }
});

$('#chat-sidebar').on('scroll', function () {
        let div = $(this).get(0);

        if (div.scrollTop + div.clientHeight >= div.scrollHeight) {
            makeCall();
        }
    }
);
});



function load(data) {
    let s = ``
    let userID = document.getElementById('user-data').textContent
    let div = document.getElementById('user-chats')
    data.forEach(function (chat) {
        if (data.indexOf(chat) === 0){
            s+= `
            <div onclick="getChat('${chat['_id']}')" id="sidechat_${chat['_id']}" style="margin-bottom:4px;"
             class="p-2 flex items-center space-x-4 dark:bg-gray-600 bg-gray-300 dark:hover:bg-gray-700 hover:bg-gray-200 rounded-lg" >`
        }else {
            s += `
            <div onclick="getChat('${chat['_id']}')" id="sidechat_${chat['_id']}" style="margin-bottom:4px;"
             class="p-2 flex items-center space-x-4 dark:bg-gray-800 bg-gray-300 dark:hover:bg-gray-700 hover:bg-gray-200 rounded-lg" >`
        }
        if (chat['members'].length === 2) {
            let other = chat['members'].filter(function (user) {
                return (user['_id'] != userID)
            })[0]

            if (other['chatProfile']['status'] === 'Online') {
                s += `<div class="relative">
    <img class="w-10 h-10 rounded-full" src="${other['avatar']['avatar_url']}" alt="">
    <span class="bottom-0 left-7 absolute  w-3 h-3 bg-green-400 border-white dark:border-gray-800 rounded-full"></span>
</div>`
            }
            else if (other['chatProfile']['status'] === 'Do Not Disturb') {
                s += `<div class="relative">
    <img class="w-10 h-10 rounded-full" src="${other['avatar']['avatar_url']}" alt="">
    <span class="bottom-0 left-7 absolute  w-3.5 h-3.5 bg-red-500 border-2 border-white dark:border-gray-800 rounded-full"></span>
</div>`
            }
            else {
                s += `<div class="relative">
    <img class="w-10 h-10 rounded-full" src="${other['avatar']['avatar_url']}" alt="">
    <span class="bottom-0 left-7 absolute  w-3.5 h-3.5 bg-gray-700 border-2 border-white dark:border-gray-800 rounded-full"></span>
</div>`
            }
            let status_emoji = other['chatProfile']['status_emoji']
            if (!(status_emoji)) {
                status_emoji = ''
            }
            let status_text = other['chatProfile']['status_text']
            if (!(status_emoji)) {
                status_text = ''
            }
            s +=
                `
            <div class="space-y-1 font-medium dark:text-white">
                <div class="dark:text-gray-300" style="font-size:20px">${other['username']}</div>
                <div class="text-sm text-gray-500 dark:text-gray-400" style="font-size:13px;">${status_emoji} ${status_text}</div>
            </div>
        </div>

        `

        }
        else {
            s += `
               <div class="flex items-center space-x-4">
    <img class="w-10 h-10 p-1 rounded-full ring-2 ring-gray-300 dark:ring-gray-500" src="${chat['avatar']['avatar_url']}" alt="Bordered avatar">
                `;

            if (!(chat['title'])) {
                chat['title'] = `${chat['owner']['username']}'s Chat` ;
            }

            s +=
                `<div class="space-y-1 font-medium dark:text-white">
        <div style="font-size:20px;" class="dark:text-gray-300">${chat["title"]}</div>
        <div style="font-size:13px;" class="text-sm text-gray-500 dark:text-gray-400">${chat['members'].length} Members</div>
    </div>
</div>`
        }
    });

    div.insertAdjacentHTML('beforeend', s);



    let selected = document.getElementById('user-chats');
    selected.children[0].click();
}

function changeStatus(status){
    $.ajax({
        url: '/api/v1/internal/set-status',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            status: status
        })
    });
}

window.onunload = function(){
    changeStatus("Offline");
}
window.addEventListener("load", function(){
    changeStatus('Online');
});


function openFriends(){
    $.ajax({
        url: '/api/v1/internal/get-friends',
        type: 'GET',
        contentType: 'application/json',
        data: JSON.stringify({
        })


    }).done((data) =>  {
        document.getElementById("members-sidebar").style.display= "none";
        document.getElementById("main-area").style.display = "none";
        document.getElementById("blocked").style.display = "none";
        document.getElementById("friends").style.display = "block";
        document.getElementById("emojis").style.display = "none";
        document.getElementById("emails").style.display = "none";
    });
}
function openBlocked(){
    $.ajax({
        url: '/api/v1/internal/get-blocks',
        type: 'GET',
        contentType: 'application/json',
        data: JSON.stringify({
        })


    }).done((data) =>  {
        document.getElementById("members-sidebar").style.display= "none";
        document.getElementById("main-area").style.display = "none";
        document.getElementById("blocked").style.display = "block";
        document.getElementById("friends").style.display = "none";
        document.getElementById("emojis").style.display = "none";
        document.getElementById("emails").style.display = "none";
    });
}
function toggleEmail(){
    document.getElementById("members-sidebar").style.display= "none";
    document.getElementById("main-area").style.display = "none";
    document.getElementById("blocked").style.display = "none";
    document.getElementById("friends").style.display = "none";
    document.getElementById("emojis").style.display = "none";
    document.getElementById("emails").style.display = "block";
    document.getElementById("email_iframe").src = '/chat/email';
}

function toggleEmoji(){
    document.getElementById("members-sidebar").style.display= "none";
    document.getElementById("main-area").style.display = "none";
    document.getElementById("blocked").style.display = "none";
    document.getElementById("friends").style.display = "none";
    document.getElementById("emojis").style.display = "block";
    document.getElementById("emails").style.display = "none";
}

function toggleChat(){
    document.getElementById("members-sidebar").style.display= "block";
    document.getElementById("main-area").style.display = "block";
    document.getElementById("blocked").style.display = "none";
    document.getElementById("friends").style.display = "none";
    document.getElementById("emojis").style.display = "none";
    document.getElementById("emails").style.display = "none";
}
window.addEventListener("keydown", function (event) {
    let form = document.getElementById("msg");
    if (event.keyCode === 13 && !event.shiftKey) {
        form.submit();
    }
});
document.oncontextmenu = rightClick;

function rightClick(clickEvent) {
    clickEvent.preventDefault();
    // return false;
}
function profile(node){
    function insertAfter(referenceNode, newNode) {
        referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
    }

    var el = document.createElement("span");
    el.innerHTML = `
                <div id="dropdown" class="absolute z-10 bg-white divide-y divide-gray-100 rounded shadow w-44 dark:bg-gray-700">
    <ul class="py-1 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownDefault">
      <li>
        <span class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Profile</span>
      </li>
      <li>
        <span class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Close DM</a>
      </li>
      <li>
        <span class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Add Friend</a>
      </li>
      <li>
        <span class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Mute @Coder N</a>
      </li>
      <li>
        <span class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Block</a>
      </li>
    </ul>
</div>`
    insertAfter(node, el);
}
function getChat(chatID){
    console.log(chatID);
    $.ajax({
        url: '/api/v1/internal/get-chat',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
                chatID: chatID
            }
        ),
        //right click: Profile, Close DM, Add Friend, Block, Mute @Coder N, Copy ID
        success: function (chat) {
            let chat_el = document.getElementById('chat');
            let members = document.getElementById('chat-members')
            console.log(chat);
            let chatContent = ``
            let chatMembers = ``;
            let el = document.getElementById(`sidechat_${chat['_id']}`);
            let userChats = document.getElementById('user-chats');
            userChats = [...userChats.children];
            userChats.map(function(elem){
                elem.classList.remove('dark:bg-gray-600');
                elem.classList.add('dark:bg-gray-800');
                }
            );
            el.classList.add('dark:bg-gray-600');
            el.classList.remove('dark:bg-gray-800');
            chatContent += `<div id="chatID" data-id="${chat['_id']}" class="w-0 h-0"></div>`

            chat['messages'].forEach(function (message) {
                chatContent+= `<div class="flex items-top space-x-4 mt-2" id="${message['id']}">
                        <img class="mt-1 w-10 h-10 rounded-full " data-dropdown-toggle="user_${message['id']}"
                             src="${message['sender']['avatar']['avatar_url']}"
                             alt="">
                        <div class="space-y-1 font-medium dark:text-white">
                            <div><span  data-dropdown-toggle="user_${message['id']}" class="hover:underline">${message['sender']['username']}</span> <span class="ml-3 text-sm text-gray-400">${message['send_date']}</span></div>
                            <div class="text-sm text-gray-500 dark:text-gray-400">${message['content']}</div>
                        </div>
                    </div>
                    <div id="user_${message['id']}" class="z-50 hidden bg-white divide-y divide-gray-100 rounded shadow w-80 dark:bg-gray-700 dark:divide-gray-600 rounded-lg block" data-popper-placement="bottom" style="position: absolute; inset: 0px auto auto 0px; margin: 0px; transform: translate3d(0px, 215px, 0px);">
                                    <div style="border-radius:10px 10px 0 0; height:60px;background:rgba
                                        (191, 198, 205);"></div>
                                    <div class="px-4 py-3 text-xl text-gray-900 dark:text-white border-b border-l">
                                        <div style="text-align: left; margin-left:3px;">
                                            <div style="margin-top:-60px;">
                                                <img style="background:rgb(18,25,38)" src="${message['sender']["avatar"]['avatar_url']}" class="w-24 h-24 rounded-full border-white dark:border-gray-700 border-2 object-cover" alt="${message['sender']['username']}'s Profile Picture">
                                                <span class="absolute  w-5 h-5 bg-green-400 border-2 border-white dark:border-gray-700 rounded-full" style="left:90px;top:85px;"></span>
                                            </div>
                                            <div>${message['sender']['username']}</div>
                                           
                                            
                                            <input id="msg" placeholder="Message @${message['sender']['username']}" required="" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm
                                                       mb-6 rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5
                                                       dark:bg-gray-900 dark:border-gray-600 dark:placeholder-gray-400
                                                       dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                                        </div>
                                    </div>
                                </div>
`;
            });

            chat['members'].forEach(function (other) {
                chatMembers += `<div 
        oncontextmenu='profile(this)'
        style="margin-bottom:4px;"
             class="p-2 flex items-center space-x-4 dark:bg-gray-800 bg-gray-300 dark:hover:bg-gray-700 hover:bg-gray-200 rounded-lg" >`
                if (other['chatProfile']['status'] === 'Online') {
                    chatMembers += `<div class="relative">
    <img class="w-10 h-10 rounded-full" src="${other['avatar']['avatar_url']}" alt="">
    <span class="bottom-0 left-7 absolute  w-3 h-3 bg-green-400 border-white dark:border-gray-800 rounded-full"></span>
</div>`
                } else if (other['chatProfile']['status'] === 'Do Not Disturb') {
                    chatMembers += `<div class="relative">
    <img class="w-10 h-10 rounded-full" src="${other['avatar']['avatar_url']}" alt="">
    <span class="bottom-0 left-7 absolute  w-3.5 h-3.5 bg-red-500 border-2 border-white dark:border-gray-800 rounded-full"></span>
</div>`
                } else {
                    chatMembers += `<div class="relative">
    <img class="w-10 h-10 rounded-full" src="${other['avatar']['avatar_url']}" alt="">
    <span class="bottom-0 left-7 absolute  w-3.5 h-3.5 bg-gray-700 border-2 border-white dark:border-gray-800 rounded-full"></span>
</div>`
                }
                let status_emoji = other['chatProfile']['status_emoji']
                if (!(status_emoji)) {
                    status_emoji = ''
                }
                let status_text = other['chatProfile']['status_text']
                if (!(status_emoji)) {
                    status_text = ''
                }
                chatMembers +=
                    `
            <div class="space-y-1 font-medium dark:text-white">
                <div class="dark:text-gray-300" style="font-size:20px">${other['username']}</div>
                <div class="text-sm text-gray-500 dark:text-gray-400" style="font-size:13px;">${status_emoji} ${status_text}</div>
            </div>
        </div>
        `
            });

            chat_el.innerHTML = "";
            chat_el.insertAdjacentHTML('beforeend', chatContent);
            members.innerHTML = "";
            members.insertAdjacentHTML('beforeend', chatMembers);
        }
    });

}
function sendMessage(){
    let el = document.getElementById('msg_content');
    let val = el.value;
    el.value = '';
    let chatID = document.getElementById('chatID').getAttribute('data-id');
    socket.emit('new_message', {
        chatType: 'chat',
        chatID: chatID,
        content: val
    });


}

window.onload = function(){
    const tx = document.getElementsByTagName("textarea");
    for (let i = 0; i < tx.length; i++) {
        tx[i].setAttribute("style", "height:" + (tx[i].scrollHeight) + "px;overflow-y:hidden;");
        tx[i].addEventListener("input", OnInput, false);
    }

    function OnInput() {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";
    }

}