let main, reset, recaptcha, code;

function resetScreen() {
    main.classList.toggle('hidden');
    reset.classList.toggle('hidden');
    emailInput.value = email.value;
}

let prevScreen;

function recaptchaScreen() {
    let screen;
    for (screen of [main, reset, code]) {
        if (!screen.classList.contains('hidden')) break;
    }

    prevScreen = screen;
    screen.classList.add('hidden');
    recaptcha.classList.remove('hidden');
}

function onComplete() {
    setTimeout(recaptchaSuccess, 1000);
}

function recaptchaSuccess() {
    if (!grecaptcha.getResponse()) return;

    recaptcha.classList.add('hidden');
    prevScreen.classList.remove('hidden');
}

function selectChanged() {
    document.getElementById('schoolName').innerText =
        'Your ' + document.getElementById('selection').value + ' account';
    document.getElementById('schoolInput').placeholder =
        'Your ' + document.getElementById('selection').value + ' Email';
    document.getElementById('typeHere').style.display = 'block';
}

function SSO() {
    if (document.getElementById('sso').innerText.includes('SSO')) {
        document.getElementById('signin_form').style.display = 'none';
        document.getElementById('sso').innerHTML = 'Return to Log In';
        document.getElementById('signin_form2').style.display = 'block';
        document.getElementById('schoologyy').style.display = 'none';
    } else {
        document.getElementById('signin_form').style.display = 'block';
        document.getElementById('signin_form2').style.display = 'none';
        document.getElementById('sso').innerHTML =
            '<span class="material-icons-outlined md-36">key</span> SSO Login';
        document.getElementById('schoologyy').style.display = 'block';
    }
}

function Schoology() {
    if (document.getElementById('schoologyy').innerText.includes('Schoology')) {
        document.getElementById('signin_form').style.display = 'none';
        document.getElementById('schoologyy').innerHTML = 'Return to Log In';
        document.getElementById('signin_form3').style.display = 'block';
        document.getElementById('launchBTN').style.display = 'block';
        document.getElementById('sso').style.display = 'none';
    } else {
        document.getElementById('signin_form').style.display = 'block';
        document.getElementById('signin_form3').style.display = 'none';
        document.getElementById('schoologyy').innerHTML = 'Schoology Login';
        document.getElementById('launchBTN').style.display = 'none';
        document.getElementById('sso').style.display = 'block';
    }
}

$('#confirmBTN').on('click', function () {
    const $this = $(this);
    $this.button('loading');
    setTimeout(function () {
        const request = $.ajax({
            type: 'POST',
            url: '/api/v1/internal/signin-with-schoology',
            data: {
                link: 'https://' + document.getElementById('domain').value + '.schoology.com/'
            }
        });

        request.done(function (data) {
            $this.button('reset');
            let resp = document.getElementById('resp');
            if (data === '1') {
                resp.style.color = 'red';
                resp.innerHTML =
                    'Login Failed. Reason: Clicked Deny on Schoology or closed Schoology popup window. Make sure Popups are enabled on your browser. Click Authorize again and click Approve this time!';
                document.getElementById('auth').style.display = 'inline';
                document.getElementById('connectbtn').style.display = 'none';
            } else if (data === '2') {
                resp.style.color = 'red';
                resp.innerHTML =
                    'Login Failed. Reason: Your account is not connected to Schoology. Please signin normally and then connect your schoology account to signin with Schoology.';
                document.getElementById('auth').style.display = 'inline';
                document.getElementById('connectbtn').style.display = 'none';
            } else {
                resp.style.color = 'lightgreen';
                resp.innerHTML = 'Successfully linked the Schoology Account <b>' + data + '</b>!';
                //window.location.replace("/settings");
            }
        });
    }, 1000);
});

function startSchoology() {
    let domain = document.getElementById('domain').value;
    const request = $.ajax({
        type: 'GET',
        url: '/api/v1/internal/generate-schoology-oauth-url',
        data: {}
    });

    let newwindow2;
    request.done(
        (data) =>
            (newwindow2 = window.open(
                data.replace('bins', domain),
                'Authorize with Schoology2',
                'height=400,width=800'
            ))
    );

    document.getElementById('launchBTN').style.display = 'none';
    document.getElementById('confirmBTN').style.display = 'none';
    document.getElementById('selectdomain').style.display = 'none';

    function checkIfDone() {
        const request = $.ajax({
            type: 'GET',
            url: '/api/v1/internal/check/schoology',
            data: {}
        });

        request.done((data) => {
            if (data === 'False') checkIfDone();
        });
    }

    checkIfDone();
    document.getElementById('confirmBTN').style.display = 'block';
}

function confirmSchoology() {
    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/signin-with-schoology',
        data: {
            link: 'https://' + document.getElementById('domain').value + '.schoology.com/'
        }
    });
    request.done(function (data) {
        document.getElementById('confirmBTN').style.display = 'none';
        if (data === '1' || data === '2') {
            document.getElementById('launchBTN').style.display = 'block';
            document.getElementById('error').style.display = 'block';
            if (data === '1')
                document.getElementById('error').innerHTML =
                    'Login Failed. Reason: Clicked Deny on Schoology or closed Schoology popup window. Make sure Popups are enabled on your browser. Click Authorize again and click Approve this time!';
            else
                document.getElementById('error').innerHTML =
                    'Login Failed. Reason: Your account is not connected to Schoology. Please signin normally and then connect your schoology account to signin with Schoology.';
        } else {
            let email = data.split('•')[1];
            let name = data.split('•')[0];
            document.getElementById('confirmation').style.display = 'block';
            document.getElementById('name').innerHTML = name;
            document.getElementById('email').innerHTML = email;

            window.location.href = '/app';
        }
    });
}

const NORMAL_BORDER = [
    'dark:bg-gray-900/50',
    'border',
    'border-gray-400',
    'dark:border-gray-600',
    'focus:border-gray-500',
    'focus:bg-gray-700',
    'focus:ring-0',
    'dark:text-white'
];

const RED_BORDER = [
    'border',
    'border-red-500',
    'text-red-900',
    'placeholder-red-700',
    'focus:ring-red-500',
    'focus:border-red-500',
    'bg-red-400',
    'border-red-800'
];
const GREEN_BORDER = [
    'bg-green-500',
    'border-2',
    'border-green-800',
    'text-green-900',
    'placeholder-green-700',
    'focus:ring-green-500',
    'focus:border-green-500',
];
let email, password;

function clearBorders() {
    email.classList.remove(...RED_BORDER);
    email.classList.remove(...GREEN_BORDER);
    email.classList.add(...NORMAL_BORDER);

    password.classList.remove(...RED_BORDER);
    password.classList.remove(...GREEN_BORDER);
    password.classList.add(...NORMAL_BORDER);
}

window.addEventListener('load', function () {
    email = document.getElementById('email');
    password = document.getElementById('psw');
    main = document.getElementById('main');
    recaptcha = document.getElementById('recaptcha');
    reset = document.getElementById('reset');
    code = document.getElementById('resetCode');

    email.classList.add(...NORMAL_BORDER);
    password.classList.add(...NORMAL_BORDER);

    let loginAttempts = 0;
    let showRecaptcha = false;

    let loginButton = document.getElementById('log_in');
    loginButton.style.color = 'gray';
    loginButton.style.backgroundColor = '#006097';
    loginButton.disabled = true;

    function checkCredentials() {
        if (showRecaptcha) {
            if (grecaptcha.getResponse()) {
                showRecaptcha = false;
                grecaptcha.reset();
            } else return;
        }

        const errorEmail = document.getElementById('error-msg');
        const errorPassword = document.getElementById('password-error-msg');

        if (email.value === '') errorEmail.innerHTML = 'Please enter your email!';
        else if (!/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}/.test(email.value)) {
            errorEmail.innerHTML = 'Did you enter a valid email?';
            clearBorders();
            return;
        }

        if (password.value === '') errorPassword.innerHTML = 'Please enter a password!';

        if (email.value === '' || password.value === '') {
            clearBorders();
            return;
        }

        const xhttp = new XMLHttpRequest();
        xhttp.open('POST', '/api/v1/internal/check/signin', true);
        xhttp.setRequestHeader('Content-type', 'application/json');
        xhttp.addEventListener('load', afterCheck);
        xhttp.send(
            JSON.stringify({
                email: email.value,
                password: password.value
            })
        );

        function afterCheck() {
            const emailError = document.getElementById('error');
            const passwordError = document.getElementById('password-error');
            const emailErrorMsg = document.getElementById('error-msg');
            const passwordErrorMsg = document.getElementById('password-error-msg');

            if (this.responseText === 'True') {
                emailError.style.color = 'lightgreen';
                emailError.innerHTML = '<p class="material-icons">check_circle</p>';
                emailErrorMsg.style.color = 'lightgreen';
                emailErrorMsg.innerHTML = 'Correct Email!';

                email.classList.remove(...NORMAL_BORDER);
                email.classList.remove(...RED_BORDER);
                email.classList.add(...GREEN_BORDER);

                passwordError.style.color = 'lightgreen';
                passwordError.innerHTML = '<p class="material-icons">check_circle</p>';
                passwordErrorMsg.style.color = 'lightgreen';
                passwordErrorMsg.innerHTML = 'Correct Password!';

                password.classList.remove(...NORMAL_BORDER);
                password.classList.remove(...RED_BORDER);
                password.classList.add(...GREEN_BORDER);

                let loginButton = document.getElementById('log_in');
                loginButton.disabled = false;
                loginButton.style.color = 'white';
                loginButton.style.backgroundColor = '#3E82F8';
                loginButton.classList.add('hover:bg-blue-800');
            } else {
                emailError.style.color = 'red';
                emailError.innerHTML = '<p class="material-icons">error</p>';
                emailErrorMsg.style.color = 'red';
                emailErrorMsg.innerHTML = 'Invalid email or password!';

                email.classList.remove(...NORMAL_BORDER);
                email.classList.remove(...GREEN_BORDER);
                email.classList.add(...RED_BORDER);

                passwordError.style.color = 'red';
                passwordError.innerHTML = '<p class="material-icons">error</p>';
                passwordErrorMsg.style.color = 'red';
                passwordErrorMsg.innerHTML = 'Invalid email or password!';

                password.classList.remove(...NORMAL_BORDER);
                password.classList.remove(...GREEN_BORDER);
                password.classList.add(...RED_BORDER);

                let loginButton = document.getElementById('log_in');
                loginButton.style.color = 'gray';
                loginButton.style.backgroundColor = '#006097';
                loginButton.disabled = true;

                loginAttempts++;
                if (loginAttempts % 3 === 0) {
                    showRecaptcha = true;
                    recaptchaScreen();
                }
            }
        }
    }

    keyUpDelay('#email, #psw', 500, checkCredentials);
});

const loginUser = () => {
    document.getElementById("log_in").innerHTML = loadingIcon(5) + "Logging in...";
    window.location.href = getRedirectParam();
}

function getRedirectParam() {
    let qd = {};
    if (location.search)
        location.search
            .substring(1)
            .split('&')
            .forEach(function (item) {
                let s = item.split('='),
                    k = s[0],
                    v = s[1] && decodeURIComponent(s[1]); //  null-coalescing / short-circuit
                //(k in qd) ? qd[k].push(v) : qd[k] = [v]
                (qd[k] = qd[k] || []).push(v); // null-coalescing / short-circuit
            });

    if (qd['redirect']) return qd['redirect'][0];
    return '/app';
}
