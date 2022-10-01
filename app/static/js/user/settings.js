const VALID_USERNAME_REGEX = /^[A-Za-z][a-zA-Z\d\-_]{2,31}$/;
const EMAIL_REGEX =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}])|(([a-zA-Z\-\d]+\.)+[a-zA-Z]{2,}))$/;

window.addEventListener('DOMContentLoaded', function () {
    document.getElementById("toggle_context_menu").checked = localStorage.getItem("enableContextMenu") != null;

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

    const sidebarOptions = document.querySelectorAll('aside:not(#sidebar) li > span');
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

    function hasSpecialCharacter(str) {
        const r_l = ',<.>/?;:\'"\\|[{]}=+-_`!@#$%^&*()_+';

        for (const c in str) {
            if (r_l.includes(c))
                return true;
        }
        return false;
    }

    function validation() {
        const error = document.getElementById("error");
        const btn = document.querySelector("#change-modal .disabled-css");
        error.innerHTML = "<br>"
        btn.disabled = true;

        const req = $.ajax({
            url: "/api/v1/internal/check/access",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({"password": document.getElementById("access-check").value})
        });

        req.done(data => {
            btn.disabled = false;

            timeout();

            if (data === "True") {
                error.style.color = "greenyellow";
                error.innerHTML = "Correct Password!";
            } else {
                error.style.color = "red";
                error.innerHTML = "Incorrect Password";
            }
        });

        req.fail(() => {
            btn.disabled = false;
            error.innerHTML = "An error occurred! Retry?";
        });
    }

    function valid(type) {
        const error = document.getElementById("error");
        const value = document.getElementById("enter-value").value;
        document.getElementById("confirm-change").disabled = true;

        if (!value) return false;
        error.style.color = "red";

        if (type === "username") {
            if (value.length < 3)
                error.innerHTML = "Username must be at least 3 characters long!";
            else if (value.length > 32)
                error.innerHTML = "Username must be less than 32 characters long";
            else if (!VALID_USERNAME_REGEX.test(value))
                error.innerHTML = 'Your username may only contain letters, numbers, underscores, dashes, and spaces!'
            else {
                error.innerHTML = loadingIcon(5);

                const req = $.ajax({
                    url: "/api/v1/internal/check/signup/user",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({username: value})
                })

                req.done(data => {
                    if (data === "True") {
                        error.style.color = "red";
                        error.innerHTML = "Username exists!";
                    } else {
                        error.style.color = "greenyellow";
                        error.innerHTML = "Valid username!";
                        document.getElementById("confirm-change").disabled = false;
                    }
                });

                req.fail(() => {
                    error.style.color = "red";
                    error.innerHTML = "An error occurred! Retry?";
                });

                document.getElementById("confirm-change").disabled = false;
                return true;
            }
        } else if (type === "password") {
            if (value.length < 6)
                error.innerHTML = "Password must be at least 6 characters long!";
            else if (!/\d/.test(value))
                error.innerHTML = 'Password must include at least 1 number';
            else if (!hasSpecialCharacter(value))
                error.innerHTML = 'Password must include at least 1 special character';
            else {
                error.style.color = "greenyellow";
                error.innerHTML = "Valid password!";
                return true;
            }
        } else if (type === "email")
            if (EMAIL_REGEX.test(value)) {
                error.style.color = "greenyellow";
                error.innerHTML = "Valid email!";
                document.getElementById("confirm-change").disabled = false;

                const req = $.ajax({
                    url: "/api/v1/internal/check/signup/email",
                    type: "POST",
                    contentType: "application/json",
                    data: JSON.stringify({email: value})
                })

                req.done(data => {
                    if (data === "True") {
                        error.style.color = "red";
                        error.innerHTML = "Email exists!";
                    } else {
                        error.style.color = "greenyellow";
                        error.innerHTML = "Valid email!";
                        document.getElementById("confirm-change").disabled = false;
                    }
                });

                req.fail(() => {
                    error.style.color = "red";
                    error.innerHTML = "An error occurred! Retry?";
                });

                return true;
            }

        return false;
    }

    function timeout() {
        if (expireTimeout)
            clearTimeout(expireTimeout);

        setTimeout(() => {
            prev();
            const error = document.getElementById("error");
            error.style.color = "red";
            error.innerHTML = "Please enter your password again.";
        }, 5 * 60 * 1000);
    }

    for (const el of document.querySelectorAll("[step]:not([step='1'])"))
        el.classList.add("hidden");

    keyUpDelay('#access-check', 1000, () => validation());
    keyUpDelay('#enter-value', 1000, () => valid(type));

    const confirm = document.getElementById("confirm-change");
    confirm.addEventListener("click", () => {
        confirm.disabled = true;

        const req = $.ajax({
            url: "/api/v1/internal/update/setting",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "type": type,
                "value": document.getElementById("enter-value").value
            })
        });

        req.done(() => {
            document.getElementById("error").innerHTML = "Username changed!";
            location.reload();
        });
    });

    modal = new Modal(document.getElementById("change-modal"));
});

let step = 1, max = 3;
let type, modal;

function changeSettingsModal(settingType) {
    modal.show();
    max = 3;

    const capsType = settingType.charAt(0).toUpperCase() + settingType.substring(1);
    const input = document.getElementById("enter-value");

    if (input.placeholder.includes(capsType))
        return;

    step = 1;

    input.value = "";

    input.setAttribute("autocomplete", "new-" + settingType);
    input.setAttribute("name", settingType);
    input.setAttribute("placeholder", "New " + capsType)
    input.setAttribute("type", capsType === "Password" ? "password" : "text");

    type = settingType;
    document.getElementById("replace").innerHTML = "Enter New " + capsType;
    document.getElementById("confirm-password").style.display = (capsType === "Password" && step === 2) ? "block" : "none";
    document.getElementById("error").innerHTML = "";
}

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

function next() {
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
