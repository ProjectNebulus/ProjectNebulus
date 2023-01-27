const VALID_USERNAME_REGEX = /^[A-Za-z][a-zA-Z\d\-_]{2,31}$/;
const EMAIL_REGEX =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}])|(([a-zA-Z\-\d]+\.)+[a-zA-Z]{2,}))$/;

let currentTab;

function openTab(id_name) {
    currentTab.style.display = "none";
    const tab = document.getElementById(id_name);
    if (!tab)
        return;

    currentTab = tab;
    currentTab.style.display = "block";

    for (const img of document.querySelectorAll("#" + id_name + " img"))
        img.style.display = "inline-block";
}

window.addEventListener('DOMContentLoaded', function () {
    modals.add("change-modal");

    currentTab = document.getElementById("generalSettings");
    linkProxy(openTab);

    let validEmail = false;

    for (const el of document.querySelectorAll("#access-check, #enter-value, #confirm-password, #confirm-email"))
        el.classList.add('bg-gray-50', 'border', 'border-gray-300', 'text-gray-900', 'text-sm', 'rounded-lg', 'block',
            'p-2.5', 'focus:ring-blue-500', 'focus:border-blue-500', 'dark:focus:ring-blue-500', 'w-full', 'dark:bg-gray-700',
            'dark:focus:border-blue-500', 'dark:border-gray-600', 'dark:placeholder-gray-400', 'dark:text-white');

    document.getElementById("toggle_context_menu").checked = localStorage.getItem("enableContextMenu") != null;

    const bgCards = document.querySelectorAll('.card img');
    const wallpaper = localStorage.getItem('wallpaper');

    for (const card of bgCards) {
        if (card.src === wallpaper) card.parentElement.classList.add('selected_card');

        card.addEventListener('click', () => {
            if (card.classList.contains('selected_card')) return;

            localStorage.setItem('wallpaper', card.src);

            const brightness = document.documentElement.classList.contains("dark") ? 0 : 255;
            document.body.style.background = `linear-gradient(rgba(${brightness}, ${brightness}, ${brightness}, 0.6), rgba(${brightness}, ${brightness}, ${brightness}, 0.6)), url('${card.src}') no-repeat center center fixed`;
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
        let opensPage = option.getAttribute('onclick').substring(9);
        opensPage = opensPage.substring(0, opensPage.length - 2);

        option.addEventListener('click', () => {
            if (!option.classList.contains('bg-gray-300')) window.location.href = '#' + opensPage;

            for (const op of sidebarOptions) op.classList.remove('bg-gray-300', 'dark:bg-gray-600');

            option.classList.add('bg-gray-300', 'dark:bg-gray-600');
        });

        if (sidebarOptions[0] !== option && search.length > 1 && opensPage === search[1]) {
            sidebarOptions[0].classList.remove('bg-gray-300', 'dark:bg-gray-600');
            option.classList.add('bg-gray-300', 'dark:bg-gray-600');
            openTab(opensPage);
        }
    }

    function hasSpecialCharacter(str) {
        const r_l = ',<.>/?;:\'"\\|[{]}=+-_`!@#$%^&*()_+';

        for (const c in str) {
            if (r_l.includes(c))
                return true;
        }
        return false;
    }


    function checkPsw() {
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
            if (data === "True") {
                btn.disabled = false;
                error.style.color = "greenyellow";
                error.innerHTML = "Correct Password!";
                timeout(10 * 60 * 1000);
            } else {
                error.style.color = "red";
                error.innerHTML = "Incorrect Password";
            }
        });

        req.fail(() => error.innerHTML = "An error occurred! Retry?");
    }

    function checkVerifCode() {
        if (!validEmail)
            return;

        const codeInput = document.getElementById("confirm-email");

        const req = $.ajax({
            url: "/api/v1/internal/check/verification-code",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({value: codeInput.value})
        });

        req.done(data => {
            const status = document.getElementById("error");
            const statusIcon = codeInput.parentElement.children[0];

            if (data === "true") {
                status.style.color = "greenyellow";
                status.innerHTML = "Correct Validation Code";
                statusIcon.style.color = "greenyellow";
                statusIcon.innerHTML = "check_circle";
                next();
                document.getElementById("replace").innerHTML = "Confirm Change";
                document.getElementById("enter-value").disabled = true;
            } else {
                status.style.color = "red";
                status.innerHTML = "Incorrect Validation Code";
                statusIcon.style.color = "red";
                statusIcon.innerHTML = "error";
            }
        });
    }

    function validInput() {
        if (document.getElementById("replace").innerText === "Confirm Change")
            return;

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
                        validEmail = false;
                    } else {
                        error.style.color = "greenyellow";
                        error.innerHTML = "Valid email!";
                        validEmail = true;
                    }

                    document.getElementById("send-email").disabled = !validEmail;
                });

                req.fail(() => {
                    error.style.color = "red";
                    error.innerHTML = "An error occurred! Retry?";
                });

                return true;
            }

        return false;
    }

    keyUpDelay('#access-check', 1000, () => checkPsw());
    keyUpDelay('#enter-value', 1000, () => validInput());
    keyUpDelay("#confirm-email", 1000, () => checkVerifCode())

    const confirm = document.getElementById("confirm-change");
    confirm.addEventListener("click", () => {
        confirm.disabled = true;
        const value = document.getElementById("enter-value").value;

        const req = $.ajax({
            url: "/api/v1/internal/update/setting",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                "type": type,
            })
        });

        req.done(() => {
            document.getElementById("error").innerHTML = type.charAt(0).toUpperCase() + type.substring(1) + " changed! "
                + '<span onclick="location.reload()" class="text-blue-500 hover:text-blue-600 underline cursor-pointer">Reload</span>';
            document.getElementById(type + "-display").innerText = value;
        });
    });

    function sendEmail() {
        if (!validEmail) {
            document.getElementById("confirm-email").innerHTML = ""
            return;
        }

        const button = document.getElementById("send-email");
        button.disabled = true;
        button.innerText = "Sending...";

        const req = $.ajax({
            url: "/api/v1/internal/reset-email",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({email: document.getElementById("enter-value").value})
        })

        req.done(() => {
            button.innerHTML = "Done";
            setTimeout(() => {
                button.innerHTML = "Resend in 5s";
                setTimeout(() => {
                    button.innerHTML = "Resend";
                    button.disabled = false;
                }, 5000);
            }, 1000);
        });

        req.fail(() => {
            button.innerHTML = "Error";
            setTimeout(() => {
                button.innerHTML = "Retry in 3s";
                setTimeout(() => {
                    button.innerHTML = "Retry";
                    button.disabled = false;
                }, 3000);
            }, 1000);
        });
    }

    bindFunc("#send-email", sendEmail);

    modal = new Modal(document.getElementById("change-modal"));
});

let step = 1, max = 3;
let type, modal, expireTimeout = null;

function timeout(delay) {
    if (expireTimeout)
        clearTimeout(expireTimeout);

    expireTimeout = setTimeout(() => {
        if (step === 1)
            return;

        while (step > 1)
            prev();
        expireTimeout = null;

        document.getElementById("access-check").value = "";
        document.querySelector("#change-modal .disabled-css").disabled = true;
        const error = document.getElementById("error");
        error.style.color = "red";
        error.innerHTML = "Please enter your password again.";
    }, delay);
}

function openSettingsModal(settingType) {
    type = settingType;

    const capsType = settingType.charAt(0).toUpperCase() + settingType.substring(1);
    const input = document.getElementById("enter-value");

    while (step > 1)
        prev();

    for (const el of document.querySelectorAll("[step]:not([step='1'])"))
        el.classList.add("hidden");

    modal.show();
    max = 3;

    input.value = "";

    if (input.placeholder.includes(capsType))
        return;

    input.disabled = false;
    input.setAttribute("autocomplete", "new-" + settingType);
    input.setAttribute("name", settingType);
    input.setAttribute("placeholder", "New " + capsType)
    input.setAttribute("type", capsType === "Username" ? "text" : capsType.toLowerCase());
    input.setAttribute("step", capsType === "Email" ? "2,3" : "3");

    document.getElementById("replace").innerHTML = "Enter New " + capsType;
    document.getElementById("error").innerHTML = "";
}

function prev() {
    if (step > 1) {
        for (const el of document.querySelectorAll(" [step*='" + step + "']"))
            el.classList.add("hidden");

        for (const el of document.querySelectorAll(" [step*='" + (step - 1) + "']"))
            el.classList.remove("hidden");

        step--;

        if (type === "username" && step === 2)
            prev();
        else {
            document.getElementById("confirm-email").style.display = type === "email" && step === 2 ? "block" : "none";
            document.getElementById("confirm-password").style.display = type === "password" && step === 2 ? "block" : "none";
        }
    }

    const error = document.getElementById("error");
    if (error)
        error.innerHTML = "";
}

function next() {
    max = 3;
    if (step < max) {
        for (const el of document.querySelectorAll(" [step*='" + step + "']"))
            el.classList.add("hidden");

        for (const el of document.querySelectorAll(" [step*='" + (step + 1) + "']"))
            el.classList.remove("hidden");

        step++;

        if (step === 2) {
            if (type === "username")
                next();
            else {
                document.getElementById("confirm-email").style.display = type === "email" ? "block" : "none";
                document.getElementById("confirm-password").style.display = type === "password" ? "block" : "none";
            }
        }
    }

    const error = document.getElementById("error");
    if (error)
        error.innerHTML = "";
}
