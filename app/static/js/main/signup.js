const EMAIL_REGEX =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
const VALID_USERNAME_REGEX = /^[A-Za-z][a-zA-Z\d\-_]{2,31}$/;
let email_valid = false;
let validPassword = false;

function createUser() {
    console.log(document.getElementById('chosen').value);
    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/create/user',
        data: JSON.stringify({
            email: document.getElementById('email').value,
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
            age: document.getElementById('bday').value,
            language: document.getElementById('languages').value,
            theme: document.getElementById('theme').value,
            avatar: document.getElementById('chosen').innerText
        }),

        contentType: 'application/json; charset=utf-8',
        dataType: 'json'
    });

    request.done((data) => (window.location.href = '/app'));
}

function nextModal(num) {
    document.getElementById('step' + num.toString()).style.display = 'none';
    document.getElementById('step' + (num + 1).toString()).style.display = 'block';
}

function next(num) {
    document.getElementById("stepBar").style.width = `${100 / 3 * (num + 1)}%`;
    document.getElementById("stepText").innerText = `${num + 1}`;
    if (num === 1) {
        if (
            checks[0].innerText === 'check' &&
            checks[1].innerText === 'check' &&
            checks[2].innerText === 'check' &&
            checks[3].innerText === 'check'
        ) {
            const request = $.ajax({
                type: 'POST',
                url: '/api/v1/internal/signup-email',
                contentType: 'application/json',
                data: JSON.stringify({
                    email: document.getElementById('email').value,
                    username: document.getElementById('username').value
                })
            });
            nextModal(num);
        } else alert("You can't move on yet!");
    } else if (num === 2) {
        console.log(checks);
        if (checks[4].innerHTML.includes('check') && checks[5].innerHTML.includes('check'))
            nextModal(num);
        else alert("You can't move on yet!");
    } else if (num === 3) nextModal(num);
}

function onComplete() {
    setTimeout(createUser, 1000);
}

function prev(num) {
    document.getElementById("step_").style.width = `${100 / 3 * (num - 1)}%`;
    document.getElementById("stepText").innerText = `${num - 1}`;
    if (num !== 1) {
        setTimeout(function () {
            document.getElementById('step' + num.toString()).style.display = 'none';
            document.getElementById('step' + (num - 1).toString()).style.display = 'block';
            document.getElementsByClassName('ease-in duration-75')[num * 2 - 2].innerHTML =
                '<svg style="display: inline-block;" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16l-4-4m0 0l4-4m-4 4h18"></path></svg> Previous';
        }, 1000);
    } else location.reload();
}

function validate(email) {
    return EMAIL_REGEX.test(email);
}

let username,
    validationIcons,
    password,
    passwordConfirm,
    email,
    bday,
    verification,
    errorMessages,
    checks;

window.addEventListener('load', function () {
    username = document.getElementById('username');
    validationIcons = document.getElementsByClassName('validation-icon');
    password = document.getElementById('password');
    passwordConfirm = document.getElementById('confirm-password');
    email = document.getElementById('email');
    bday = document.getElementById('bday');
    verification = document.getElementById('verification');
    errorMessages = document.getElementsByClassName('errormsg');
    checks = document.getElementsByClassName('validation-icon');

    const RED_BORDER = [
        'border',
        'text-red-900',
        'placeholder-red-700',
        'text-sm',
        'rounded-lg',
        'focus:ring-red-500',
        'focus:border-red-500',
        'block',
        'w-full',
        'p-2.5',
        'bg-red-500',
        'border-red-400'
    ];
    const GRAY = ["dark:bg-gray-800/75"];

    const GREEN_BORDER = [
        'border',
        'border-green-500',
        'text-green-900',
        'placeholder-green-700',
        'text-sm',
        'rounded-lg',
        'focus:ring-green-500',
        'focus:border-green-500',
        'block',
        'w-full',
        'p-2.5',
        'bg-green-600',
        'border-green-400'
    ];

    for (let i = 1; i < 23; i++) {
        document.getElementsByClassName('cat' + i.toString())[0].onclick = function () {
            document
                .getElementsByClassName(document.getElementById('chosen').innerText)[0]
                .classList.remove('pfp_selected');
            document.getElementById('chosen').innerText = 'cat' + i.toString();
            document.getElementsByClassName('cat' + i.toString())[0].classList.add('pfp_selected');
        };
    }
    const r_l = ',<.>/?;:\'"\\|[{]}=+-_`!@#$%^&*()_+';

    function changeUser() {
        let usernameStatus = errorMessages[1];
        const value = username.value;
        usernameStatus.style.color = 'pink';
        usernameStatus.innerHTML = '<br>';
        if (!value) {
            validationIcons[1].style.color = 'pink';
            validationIcons[1].innerHTML = '<i class="material-icons">close</i>';
            username.classList.remove(...GRAY);
            username.classList.add(...RED_BORDER);
            return false;
        }
        if (value.length < 3) {
            usernameStatus.innerHTML = 'Your username must be at least 3 characters long!';
            validationIcons[1].style.color = 'pink';
            validationIcons[1].innerHTML = '<i class="material-icons">close</i>';
            username.classList.remove(...GRAY);
            username.classList.add(...RED_BORDER);
            return false;
        }
        if (value.length > 32) {
            usernameStatus.innerHTML = 'Your username must be less than 32 characters long!';
            validationIcons[1].style.color = 'pink';
            validationIcons[1].innerHTML = '<i class="material-icons">close</i>';
            username.classList.remove(...GRAY);
            username.classList.add(...RED_BORDER);
            return false;
        }

        if (VALID_USERNAME_REGEX.test(value)) {
            const request = $.ajax({
                type: 'POST',
                url: '/api/v1/internal/check/signup/user',
                data: {
                    username: value
                }
            });

            request.done(function (data) {
                if (data === 'True') {
                    validationIcons[1].style.color = 'pink';
                    validationIcons[1].innerHTML = '<i class="material-icons">close</i>';
                    usernameStatus.innerHTML = 'This username already exists!';
                    username.classList.remove(...GREEN_BORDER);
                    username.classList.remove(...GRAY);
                    username.classList.add(...RED_BORDER);
                    return false;
                } else {
                    validationIcons[1].style.color = 'lightgreen';
                    validationIcons[1].innerHTML = '<i class="material-icons">check</i>';
                    username.classList.remove(...RED_BORDER);
                    username.classList.remove(...GRAY);
                    username.classList.add(...GREEN_BORDER);
                    usernameStatus.innerHTML = '<br>';
                }
            });
        } else {
            usernameStatus.innerHTML =
                'Your username may only contain letters, numbers, underscores, dashes, and spaces!';
            validationIcons[1].style.color = 'pink';
            validationIcons[1].innerHTML = '<i class="material-icons">close</i>';
            username.classList.remove(...GRAY);
            username.classList.add(...RED_BORDER);
            return false;
        }
    }

    function changeEmail() {
        const value = email.value;

        let emailStatus = errorMessages[0];
        emailStatus.style.color = 'pink';
        emailStatus.innerHTML = '<br>';

        if (email.value === '') {
            validationIcons[0].style.color = 'pink';
            validationIcons[0].innerHTML = '<i class="material-icons">close</i>';
            email.classList.remove(...GRAY);
            email.classList.add(...RED_BORDER);
            return false;
        }
        if (validate(value) === false && value !== '') {
            validationIcons[0].style.color = 'pink';
            validationIcons[0].innerHTML = '<i class="material-icons">close</i>';
            emailStatus.innerHTML = 'Please enter a valid email!';
            email.classList.remove(...GRAY);
            email.classList.add(...RED_BORDER);
            return false;
        }

        // alert(validate(value) && checkEmailExists(value));
        // return true;
        const request = $.ajax({
            type: 'POST',
            url: '/api/v1/internal/check/signup/email',
            data: {
                email: value
            }
        });

        request.done(function (data) {
            console.log(data);
            if (data === 'True') {
                validationIcons[0].style.color = 'pink';
                validationIcons[0].innerHTML = '<i class="material-icons">close</i>';
                emailStatus.innerHTML = 'This email already exists!';
                email.classList.remove(...GRAY);
                email.classList.remove(...GREEN_BORDER);
                email.classList.add(...RED_BORDER);
                return false;
            } else {
                validationIcons[0].style.color = 'lightgreen';
                validationIcons[0].innerHTML = '<i class="material-icons">check</i>';
                mail.classList.remove(...GRAY);
                email.classList.remove(...RED_BORDER);
                email.classList.add(...GREEN_BORDER);
                emailStatus.innerHTML = '<br>';
            }
        });
    }

    function confirmDate() {
        let status = errorMessages[5];
        status.style.color = 'pink';
        status.innerHTML = '<br>';
        let value = bday.value;
        if (value !== '') {
            validationIcons[5].style.color = 'lightgreen';
            validationIcons[5].innerHTML = '<i class="material-icons">check</i>';
            bday.classList.remove(...GRAY);
            bday.classList.remove(...RED_BORDER);
            bday.classList.add(...GREEN_BORDER);
            email_valid = true;
        } else {
            validationIcons[5].style.color = 'pink';
            validationIcons[5].innerHTML = '<i class="material-icons">close</i>';
            status.innerHTML = 'Invalid Birthday';
            bday.classList.remove(...GRAY);
            bday.classList.remove(...GREEN_BORDER);
            bday.classList.add(...RED_BORDER);
            email_valid = false;
        }
    }

    function confirmVerification() {
        let status = errorMessages[4];
        status.style.color = 'pink';
        status.innerHTML = '<br>';
        const request = $.ajax({
            type: 'POST',
            url: '/api/v1/internal/check/verification-code',
            contentType: 'application/json',
            data: JSON.stringify({value: verification.value})
        });
        request.done(function (data) {
            if (data === 'true') {
                validationIcons[4].style.color = 'lightgreen';
                validationIcons[4].innerHTML = '<i class="material-icons">check</i>';
                verification.classList.remove(...GRAY);
                verification.classList.remove(...RED_BORDER);
                verification.classList.add(...GREEN_BORDER);
                email_valid = true;
            } else {
                validationIcons[4].style.color = 'pink';
                validationIcons[4].innerHTML = '<i class="material-icons">close</i>';
                status.innerHTML = 'Incorrect Confirmation';
                verification.classList.remove(...GRAY);
                verification.classList.remove(...GREEN_BORDER);
                verification.classList.add(...RED_BORDER);
                email_valid = false;
            }
        });
    }

    function confirmPassword() {
        let status = errorMessages[3];
        status.style.color = 'pink';
        status.innerHTML = '<br>';
        let value = passwordConfirm.value;
        let value2 = password.value;
        if (value === '') {
            validationIcons[3].style.color = 'pink';
            validationIcons[3].innerHTML = '<i class="material-icons">close</i>';
            passwordConfirm.classList.remove(...GRAY);
            passwordConfirm.classList.remove(...GREEN_BORDER);
            passwordConfirm.classList.add(...RED_BORDER);
            email_valid = false;
            return false;
        }
        if (value === value2 && value !== '') {
            validationIcons[3].style.color = 'lightgreen';
            validationIcons[3].innerHTML = '<i class="material-icons">check</i>';
            passwordConfirm.classList.remove(...GRAY);
            passwordConfirm.classList.remove(...RED_BORDER);
            passwordConfirm.classList.add(...GREEN_BORDER);
            email_valid = true;
        } else {
            validationIcons[3].style.color = 'pink';
            validationIcons[3].innerHTML = '<i class="material-icons">close</i>';
            status.innerHTML = 'Two Passwords do not Match';
            passwordConfirm.classList.remove(...GRAY);
            passwordConfirm.classList.remove(...GREEN_BORDER);
            passwordConfirm.classList.add(...RED_BORDER);
            email_valid = false;
        }
    }

    if (localStorage.getItem('email') !== null) email.value = localStorage.getItem('email');

    function changePassword() {
        validPassword = false;

        let status = errorMessages[2];
        status.style.color = 'pink';
        status.innerHTML = '<br>';
        const value = password.value;
        if (!value) {
            password.classList.remove(...GRAY);
            password.classList.remove(...GREEN_BORDER);
            password.classList.add(...RED_BORDER);
            validationIcons[2].style.color = 'pink';
            validationIcons[2].innerHTML = '<i class="material-icons">close</i>';
            return false;
        }
        if (value.length < 6) {
            status.innerHTML = 'Password must be at least 6 characters long';
            password.classList.remove(...GRAY);
            password.classList.remove(...GREEN_BORDER);
            password.classList.add(...RED_BORDER);
            validationIcons[2].style.color = 'pink';
            validationIcons[2].innerHTML = '<i class="material-icons">close</i>';
            return false;
        } else if (!/\d/.test(value))
            status.innerHTML = 'Password must include at least 1 number';
        else {
            let hasSpecialCharacter = false;

            for (let i = 0; i < value.length; i++) {
                if (r_l.includes(value[i])) {
                    hasSpecialCharacter = true;
                    break;
                }
            }

            if (!hasSpecialCharacter) {
                status.innerHTML = 'Password must include at least 1 special character!';
                password.classList.remove(...GRAY);
                password.classList.remove(...GREEN_BORDER);
                password.classList.add(...RED_BORDER);
                validationIcons[2].style.color = 'pink';
                validationIcons[2].innerHTML = '<i class="material-icons">close</i>';
            } else {
                validPassword = true;
                password.classList.remove(...GRAY);
                password.classList.remove(...RED_BORDER);
                password.classList.add(...GREEN_BORDER);
                validationIcons[2].style.color = 'lightgreen';
                validationIcons[2].innerHTML = '<i class="material-icons">check</i>';
            }
        }
    }

    email.onkeyup = changeEmail;
    password.onkeyup = changePassword;
    passwordConfirm.onkeyup = confirmPassword;
    username.onkeyup = changeUser;
    bday.onkeyup = confirmDate;
    bday.onclick = confirmDate;
    keyUpDelay('#verification', 500, confirmVerification);
});
