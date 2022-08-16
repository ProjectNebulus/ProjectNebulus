const controlCenter = document.getElementById('control-center');
const controlCenter2 = document.getElementById('controlcenter2');
const focus = document.getElementById('focus');
const focusText = document.getElementById('focusText');

const FULL_DASH_ARRAY = 283;
const WARNING_THRESHOLD = 10;
const ALERT_THRESHOLD = 5;

const COLOR_CODES = {
    info: {
        color: "green"
    },
    warning: {
        color: "orange",
        threshold: WARNING_THRESHOLD
    },
    alert: {
        color: "red",
        threshold: ALERT_THRESHOLD
    }
};


setInterval(() => {
        if (localStorage.getItem('originalTimer')) {
            const current = localStorage.getItem('currentTimer').split('\n');
            let TIME_LIMIT = parseInt(localStorage.getItem('originalTimer'));


            let timeLeft = (parseInt(current[2]) * 3600 + parseInt(current[3]) * 60 + parseInt(current[4]));
            focus.classList.remove('hidden');

            document.getElementById("base-timer-label").innerHTML = formatTime1(
                timeLeft
            );
            const circleDasharray = `${(
                calculateTimeFraction(timeLeft, TIME_LIMIT) * FULL_DASH_ARRAY
            ).toFixed(0)} 283`;
            document
                .getElementById("base-timer-path-remaining")
                .setAttribute("stroke-dasharray", circleDasharray);

            const {alert, warning, info} = COLOR_CODES;
            if (timeLeft <= alert.threshold) {
                document
                    .getElementById("base-timer-path-remaining")
                    .classList.remove(warning.color);
                document
                    .getElementById("base-timer-path-remaining")
                    .classList.add(alert.color);
            } else if (timeLeft <= warning.threshold) {
                document
                    .getElementById("base-timer-path-remaining")
                    .classList.remove(info.color);
                document
                    .getElementById("base-timer-path-remaining")
                    .classList.add(warning.color);
            }


        } else {

            let focus = document.getElementById('focus');
            if (!(focus.classList.contains('hidden'))) {
                focus.classList.add('hidden');
            }
        }

    }
    ,
    1000);


function formatTime1(time) {
    let minutes = Math.floor(time / 60);
    const hours = Math.floor(minutes / 60);
    minutes = minutes % 60
    let seconds = time % 60;

    if (seconds < 10) {
        seconds = `0${seconds}`;
    }
    if (minutes < 10){
        minutes = `0${minutes}`;
    }

    if (hours) {
        return `${hours}:${minutes}:${seconds}`;
    }
    return `${minutes}:${seconds}`
}


function calculateTimeFraction(timeLeft, time_limit) {
    const rawTimeFraction = timeLeft / time_limit;
    return rawTimeFraction - (1 / time_limit) * (1 - rawTimeFraction);
}

/*
setInterval(() => {
    let original = localStorage.getItem('originalTimer');

    if (!original) {
        focus.classList.add('hidden');
        return;
    }
    original = parseInt(original);

    focus.classList.remove('hidden');
    const current = localStorage.getItem('currentTimer').split('\n');
    const secondsPast =
        original - (parseInt(current[2]) * 3600 + parseInt(current[3]) * 60 + parseInt(current[4]));

    let timeText = 'Focusing ' + (current[0] !== '' ? 'on ' + current[0] : '') + ' for ';
    timeText += secondsPast > 3600 ? Math.floor(secondsPast / 3600) + ':' : '';
    timeText += padWith0(Math.floor(secondsPast / 60)) + ':';
    timeText += padWith0(secondsPast % 60);

    focusText.innerHTML = timeText;
}, 1000);

function padWith0(num) {
    let string = num.toString();
    if (num < 10) string = '0' + string;
    return string;
}

*/
for (const icon of controlCenter.getElementsByTagName('i'))
    icon.className +=
        ' material-icons text-center text-sm text-white rounded-full bg-purple-600 w-5 h-5 mr-1';

for (const a of controlCenter.getElementsByTagName('a'))
    a.className +=
        ' text-gray-500 dark:text-gray-400 focus:outline-none hover:bg-purple-800 text-left text-sm rounded-lg p-2.5 w-36 cursor-pointer';

controlCenter2.classList.add('grid-cols-2');
controlCenter2.classList.remove('flex-col');
let chatStatus = document.getElementById('chatStatus')
if (window.location.pathname === "/chat") {
    $.ajax({
        url: '/api/v1/internal/get-chat-status',
        type: 'GET'
    }).done(function (data) {
        let status_text = document.getElementById('profile-status-text');
        let profile_username = document.getElementById('profile-username');
        if (!(data['statusText'])) {
            status_text.innerText = "No status";
        } else {
            status_text.innerText = data['statusText'];
        }
        profile_username.innerText = data['username'];
        let profile_avatar = document.getElementById('profile-avatar');
        profile_avatar.src = data['avatar'];
        let color;

        if (data['status'] === "Do Not Disturb") {
            color = '#ef4444';
        } else if (data['status'] === "Idle") {
            color = "#f59e0b";
        } else if (data['status'] === "Invisible") {
            color = "#374151";
        } else {
            color = '#4ade80';
        }

        document.getElementById('status-color').style.backgroundColor = color;
        document.getElementById('profile-status').style.backgroundColor = color;
        document.getElementById('status-name').innerText = data['status'];
        chatStatus.classList.remove('hidden');
        document.getElementById('status-name').innerText = data['status'];
    });
} else {
    chatStatus.classList.add('hidden');
}
