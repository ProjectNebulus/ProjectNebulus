window.addEventListener('load', function () {
    const bgCards = document.querySelectorAll('.card img');
    const wallpaper = localStorage.getItem('wallpaper');

    for (const card of bgCards) {
        if (card.src === wallpaper) card.parentElement.classList.add('selected_card');

        card.addEventListener('click', () => {
            if (card.classList.contains('selected_card')) return;

            localStorage.setItem('wallpaper', card.src);
            document.body.style.background = `linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)), url('${card.src}') no-repeat center center fixed`;
            document.body.style.backgroundSize = 'cover';
            document.querySelector('.selected_card').classList.remove('.selected_card');
        });
    }

    document.getElementById('no-filter').addEventListener('click', () => {
        localStorage.removeItem('wallpaper');
        document.body.style.backgroundImage = '';
        document.body.style.background = document.documentElement.classList.contains('dark')
            ? '#111926'
            : 'white';
    });

    const sidebarOptions = document.querySelectorAll('aside:not(#sidebar_) li > span');
    const search = location.href.split('#');
    console.log(search[1]);

    for (const option of sidebarOptions) {
        let opensPage = option.getAttribute('onclick').substring(10);
        opensPage = opensPage.substring(0, opensPage.length - 2);

        option.addEventListener('click', () => {
            if (!option.classList.contains('bg-gray-300')) window.location = '#' + opensPage;

            for (const op of sidebarOptions) op.classList.remove('bg-gray-300', 'dark:bg-gray-600');

            option.classList.add('bg-gray-300', 'dark:bg-gray-600');
        });

        if (sidebarOptions[0] !== option && search.length > 1 && opensPage === search[1]) {
            sidebarOptions[0].classList.remove('bg-gray-300', 'dark:bg-gray-600');
            option.classList.add('bg-gray-300', 'dark:bg-gray-600');
            open_pls(opensPage);
        }
    }

    $.ajax({
        type: 'POST',
        url: '/api/v1/internal/connect-to-schoology',
        data: {}
    }).done(function (data) {
        document.getElementById('confirmation').style.display = 'block';
        resp = document.getElementById('error');
        if (data === 'error!!!') {
            document.getElementById('error').style.display = 'block';
        } else if (data === '2') {
            document.getElementById('error2').style.display = 'block';
        } else {
            document.getElementById('successconfirm').style.display = 'block';
            document.getElementById('name').innerHTML = data.split('•')[0];
            document.getElementById('email').innerHTML = data.split('•')[1];
        }
    });
});

function prev(step) {
    document.getElementById('step' + step).style.display = 'none';
    document.getElementById('step' + (step - 1)).style.display = 'block';
}

function next(step) {
    document.getElementById('step' + step).style.display = 'none';
    document.getElementById('step' + (step + 1)).style.display = 'block';
}

function changeInput() {
    let link = document.getElementById('sgy_link').value;
    if (!link.includes('https://') || !link.includes('schoology.')) {
        document.getElementById('error').innerHTML = 'cancel';
        document.getElementById('error').style.color = 'pink';
        document.getElementById('step_2_button').disabled = true;
        document.getElementById('step_2_button').classList.add('bg-yellow-700', 'text-gray-400');
        document
            .getElementById('step_2_button')
            .classList.remove('bg-yellow-400', 'hover:bg-yellow-500');
    } else {
        document.getElementById('error').innerHTML = 'check_circle';
        document.getElementById('error').style.color = 'lightgreen';
        document.getElementById('step_2_button').disabled = false;
        document.getElementById('step_2_button').classList.remove('bg-yellow-700', 'text-gray-400');
        document
            .getElementById('step_2_button')
            .classList.add('bg-yellow-400', 'hover:bg-yellow-500');
        // convert whatever link to /api
        // https://app.schoology.com/courses --> https://app.schoology.com/api
        // find how many slashes there are in link
        let slashes = (link.match('/') || []).length;
        // if 2 slashes
        if (slashes === 2) {
            //remove last slash
            link = link.slice(0, -1);
            //add /api
            link = link + '/api';
        } else {
            //if 1 slash
            //add /api
            link = link + '/api';
        }
        document.getElementById('apikeylink').href = link;
    }
}

function launch_sgy() {
    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/get-schoology',
        data: {
            link: document.getElementById('sgy_link').value,
            key: document.getElementById('key').value,
            secret: document.getElementById('secret').value
        }
    });

    request.done((data) => window.open(data, 'Authorize with Schoology2', 'height=400,width=800'));
    request.fail(() => (error.style.display = 'block'));
}
