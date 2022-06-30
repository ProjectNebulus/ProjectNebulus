const send = document.getElementById("send");
const confirm = document.getElementById("resetPsw");
const codeInput = document.getElementById("code");
const newPsw = document.getElementById("newPsw");
let icons, errors;

function codeScreen(email) {
    code.classList.toggle("hidden");
    reset.classList.toggle("hidden");

    if (email)
        document.getElementById("username-email").innerHTML = document.getElementById("username-email").innerHTML.replace("[email]", email);
}

function sendEmail() {
    send.disabled = true;
    send.innerHTML = "Sending...";

    const request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/reset-email",
        contentType: "application/json",
        data: JSON.stringify({username: document.getElementById("reset-username").value})
    });

    request.done((email) => {
        send.disabled = false;
        if (email !== "0")
            codeScreen(email);
        else
            send.innerHTML = "Invalid input";
    });
    request.fail(() => {
        send.disabled = false;
        send.innerHTML = "Error - Retry";
    });
}

send.addEventListener("click", sendEmail);

window.addEventListener("load", () => {
    icons = code.getElementsByClassName("flex absolute items-center material-icons");
    errors = code.getElementsByClassName("error");

    const pageCounters = document.getElementsByClassName("pageCount");

    for (const i in pageCounters) {
        pageCounters[i].className += " flex items-center justify-center p-6 space-x-2 absolute bottom-0";
        for (let j = 0; j < 3; j++) {
            if (j == i)
                pageCounters[i].innerHTML += "<div class='rounded-full w-2 h-2 bg-gray-400 dark:bg-gray-500'></div>"
            else
                pageCounters[i].innerHTML += "<div class='rounded-full w-2 h-2 bg-gray-300 dark:bg-gray-400'></div>"
        }
        pageCounters[i].style.width = "calc(100% - 4rem)";
    }
});

confirm.addEventListener("click", () => {
    
});

keyUpDelay("#code", 1000, () => {
    const request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/check-verification-code",
        contentType: "application/json",
        data: JSON.stringify({value: codeInput.value})
    });

    request.done((data) => {
        if (data !== "true") {
            errors[0].innerHTML = "Invalid code, try again.";
            errors[0].classList.remove("text-green-500");
            errors[0].classList.add("text-red-500");
            codeInput.classList.add(...RED_BORDER);
            icons[0].classList.remove("text-gray-500");
            icons[0].classList.add("text-red-500");
            icons[0].innerHTML = "close";
        }
        else {
            errors[0].innerHTML = "";
            errors[0].classList.remove("text-red-500");
            errors[0].classList.add("text-green-500");
            codeInput.classList.remove(...RED_BORDER);
            codeInput.classList.add(...GREEN_BORDER);
            codeInput.disabled = true;
            icons[0].classList.remove("text-gray-500");
            icons[0].classList.remove("text-red-500");
            icons[0].classList.add("text-green-500");
            icons[0].innerHTML = "done";
        }
    })
});

keyUpDelay("#newPsw", 1000, checkPassword)

function checkPassword() {
    errors[1].classList.remove("rotate-45");
    errors[1].style.color = 'red';
    errors[1].innerHTML = '<br>';
    const value = newPsw.value;
    if (value === "") {
        // User hasn't entered a password
        errors[1].innerHTML =
            'Please enter a password!';
        newPsw.classList.remove(...GREEN_BORDER);
        newPsw.classList.add(...RED_BORDER);
        icons[1].style.color = 'red';
        icons[1].innerHTML = '<i class="material-icons">close</i>';
        return false;
    }
    if (value.length < 6) {
        errors[1].innerHTML = 'Password must be at least 6 characters long';
        newPsw.classList.remove(...GREEN_BORDER);
        newPsw.classList.add(...RED_BORDER);
        icons[1].style.color = 'red';
        icons[1].innerHTML = '<i class="material-icons">close</i>';
        return false;
    }
    else if (!HAS_NUMBER.test(value)) {
        errors[1].innerHTML = 'Password must include at least 1 number';
        return false;
    }
    else {
        let hasSpecialCharacter = false;

        for (let i = 0; i < value.length; i++) {
            if (r_l.includes(value[i])) {
                hasSpecialCharacter = true;
                break;
            }
        }

        if (!hasSpecialCharacter) {
            errors[1].innerHTML =
                'Password must include at least 1 special character!';
            newPsw.classList.remove(...GREEN_BORDER);
            newPsw.classList.add(...RED_BORDER);
            icons[1].style.color = 'red';
            icons[1].innerHTML = '<i class="material-icons">close</i>';
        }
        else {
            newPsw.classList.remove(...RED_BORDER);
            newPsw.classList.add(...GREEN_BORDER);
            icons[1].style.color = 'green';
            icons[1].innerHTML = '<i class="material-icons">check</i>';
        }
    }
}