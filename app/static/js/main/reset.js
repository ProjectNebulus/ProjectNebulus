const send = document.getElementById("send");
const confirm = document.getElementById("resetPsw");
const errors = document.querySelectorAll("#resetCode .error");
const codeInput = document.getElementById("code");
const newPsw = document.getElementById("newPsw");

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
        codeScreen(email);
    });
    request.fail(() => {
        send.disabled = false;
        send.innerHTML = "Error - Retry";
    });
}

send.addEventListener("click", sendEmail);

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
            codeInput.classList.add(...RED_BORDER);
            return;
        }
        errors[0].innerHTML = "";
        codeInput.classList.remove(...RED_BORDER);
        codeInput.classList.add(...GREEN_BORDER);
    })
});


const pageCounters = document.getElementsByClassName("pageCount");
const rect = pageCounters[0].parentElement.getBoundingClientRect();
const left = (rect.left + rect.width / 2 - 50) + "px";

for (const i in pageCounters) {
    pageCounters[i].className += " flex items-center p-6 space-x-2 absolute bottom-0";
    for (let j = 0; j < 3; j++) {
        if (j == i)
            pageCounters[i].innerHTML += "<div class='rounded-full w-2 h-2 bg-gray-400 dark:bg-gray-500'></div>"
        else
            pageCounters[i].innerHTML += "<div class='rounded-full w-2 h-2 bg-gray-300 dark:bg-gray-400'></div>"
    }

    pageCounters[i].style.left = left;
}