let sidebar = document.getElementById('sidebar_');
let override = false;
sidebar.style.height =
    'calc(100%-' + document.getElementById('navbar').getBoundingClientRect().height + 'px)';
sidebar.onclick = () => {
    sidebar.classList.toggle('expanded');
    override = true;
};

document.addEventListener('click', (ev) => {
    if (!override) sidebar.classList.remove('expanded');
    override = false;
});

if (!(window.location.pathname === '/chat')) {
    let io = window.io;

    $.ajax({
        url: '/api/v1/internal/get-total-unread',
        type: 'GET'
    }).done(function (data) {
        let chat_sidebar = document.getElementById('chat-icon-sidebar');
        chat_sidebar.insertAdjacentHTML(
            'beforeend',
            `<span id="notification_chat_sidebar" class="${
                parseInt(data) > 0 ? '' : 'hidden'
            } overflow-hidden pointer-events-none flex flex-grow left-5 top-0 absolute text-sm bg-red-500 border-4 border-white dark:border-gray-800 rounded-full w-5 h-5" style="padding-left:6px;padding-right:7px">${data}</span>`
        );
        let chat_notif_sidebar = document.getElementById('notification_chat_sidebar');

        let socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
        socket.emit('user_loaded', {});

        function notifyMe(title, body, img) {
            if (!window.Notification) {
                console.log('Browser does not support notifications.');
            } else {
                // check if permission is already granted
                if (Notification.permission === 'granted') {
                    // show notification here
                    var notify = new Notification(title, {
                        body: body,
                        icon: img
                    });
                } else {
                    // request permission from user
                    Notification.requestPermission()
                        .then(function (p) {
                            if (p === 'granted') {
                                // show notification here
                                var notify = new Notification(title, {
                                    body: body,
                                    icon: img
                                });
                            } else {
                                console.log('User blocked notifications.');
                            }
                        })
                        .catch(function (err) {
                            console.error(err);
                        });
                }
            }
        }

        socket.on('new_message', function (data) {
            console.log('NEW MESSAGE YAY');
            notifyMe(
                `New message from ${data['author'][1]}`,
                `${data['content']}`,
                data['author'][2]
            );
            chat_notif_sidebar.classList.remove('hidden');
            chat_notif_sidebar.innerHTML = (parseInt(chat_notif_sidebar.innerHTML) + 1).toString();
        });

        window.onunload = socket.disconnect;
    });
}
