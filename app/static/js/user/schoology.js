setInterval(1000, function () {
    $.ajax({
        type: 'POST',
        url: '/api/v1/internal/oauth/schoology/connect',
        data: {}
    }).done(function (data) {
        document.getElementById('confirmation').style.display = 'block';
        let resp = document.getElementById('error');
        if (data === '0') {
            resp.style.display = 'block';
        } else if (data === '1') {
            document.getElementById('error3').style.display = 'block';
        } else if (data === '2') {
            document.getElementById('error2').style.display = 'block';
        } else {
            document.getElementById('schoology_successful').style.display = 'block';
            document.getElementById('name').innerHTML = data.split('•')[0];
            document.getElementById('email').innerHTML = data.split('•')[1];
        }
    });
});

function prev() {
    if (step > 1) {
        for (const el of document.querySelectorAll(" [step='" + step + "']"))
            el.classList.add("hidden");

        for (const el of document.querySelectorAll(" [step='" + (step - 1) + "']"))
            el.classList.remove("hidden");

        step--;
    }

    const error = document.getElementById("error");
    if (error)
        error.innerHTML = "";
}

function nextSchoology() {
    max = 4;
    if (step < max) {
        for (const el of document.querySelectorAll(" [step='" + step + "']"))
            el.classList.add("hidden");

        for (const el of document.querySelectorAll(" [step='" + (step + 1) + "']"))
            el.classList.remove("hidden");

        step++;
    }

    const error = document.getElementById("error");
    if (error)
        error.innerHTML = "";
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
        url: '/api/v1/internal/oauth/schoology/get',
        data: {
            link: document.getElementById('sgy_link').value,
            key: document.getElementById('key').value,
            secret: document.getElementById('secret').value
        }
    });

    request.done((data) => window.open(data, 'Authorize with Schoology', 'height=400,width=800'));
    request.fail(() => (function () {
        const error = document.getElementById("error");
        error.style.display = 'block';
    }));
}
