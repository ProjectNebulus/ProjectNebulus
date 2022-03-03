const HAS_NUMBER = /\d/;
const EMAIL_REGEX =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

window.addEventListener('load', function () {
    function validate(email) {
        return EMAIL_REGEX.test(email);
    }

    const r_l = ',<.>/?;:\'"\\|[{]}=+-_`!@#$%^&*()_+';

    function changeEmail() {
        const value = document.getElementById('email').value;
        if (validate(value)) {
            document.getElementsByClassName('response')[0].style.color = 'green';
            document.getElementsByClassName('response')[0].innerHTML =
                '<i class="material-icons">check_circle</i>';
        } else {
            document.getElementsByClassName('response')[0].style.color = 'red';
            document.getElementsByClassName('response')[0].innerHTML =
                '<i class="material-icons">error</i>';
        }
    }

    if (localStorage.getItem('email') !== null)
        document.getElementById('email').value = localStorage.getItem('email');

    function checkPassword() {
        const value = document.getElementById('password').value;
        if (value.length < 6) {
            document.getElementById('bubble2').style.display = 'block';
            document.getElementById('bubble').style.display = 'none';
            document.getElementById('bubble2').innerHTML =
                'Message: Password must be at least 6 characters long';
            document.getElementById('passwordValid').style.display = 'none';
        } else if (!HAS_NUMBER.test(value)) {
            document.getElementById('bubble2').style.display = 'block';
            document.getElementById('bubble').style.display = 'none';
            document.getElementById('bubble2').innerHTML =
                'Message: Password must include at least 1 number';
            document.getElementById('passwordValid').style.display = 'none';
        } else {
            let hasSpecialCharacter = false;

            for (let i = 0; i < value.length; i++) {
                if (r_l.includes(value[i])) hasSpecialCharacter = true;
            }

            if (!hasSpecialCharacter) {
                document.getElementById('bubble2').style.display = 'block';
                document.getElementById('bubble').style.display = 'none';
                document.getElementById('bubble2').innerHTML =
                    'Message: Password must include at least 1 special character';
                document.getElementById('passwordValid').style.display = 'none';
            }
        }
    }

    document.getElementById('email').onkeyup = changeEmail;
    document.getElementById('password').onkeyup = checkPassword;
});

function signUp() {
    let status = document.getElementById('status');
    status.style.color = 'red';
    status.innerHTML = '<br>';

    if (document.getElementById('email').value === '') status.innerHTML = 'Please enter an email!';
    else if (document.getElementById('username').value === '')
        status.innerHTML = 'Please enter a username!';
    else if (document.getElementById('password').value === '')
        status.innerHTML = 'Please enter a password!';
    else if (document.getElementById('confirm').value === '')
        status.innerHTML = 'Please confirm your password!';
    else if (document.getElementById('password').value !== document.getElementById('confirm').value)
        status.innerHTML = 'Passwords do not match!';
    else {
        let submit = document.getElementById('submit');
        submit.disabled = true;
        submit.style.color = 'gray';
        submit.style.backgroundColor = '#006097';

        const xhttp = new XMLHttpRequest();
        xhttp.open('POST', '/signup', true);
        xhttp.setRequestHeader('Content-type', 'application/json');
        xhttp.addEventListener('load', reqListener);
        xhttp.send(
            JSON.stringify({
                username: document.querySelector('#username').value,
                password: document.querySelector('#password').value,
                email: document.querySelector('#email').value
            })
        );
    }
}

function reqListener() {
    let status = document.getElementById('status');
    let submit = document.getElementById('submit');

    if (this.responseText === '1') {
        status.style.color = 'red';
        status.innerHTML = 'That email and username already exist! Consider signing in instead.';
    } else if (this.responseText === '2') {
        status.style.color = 'red';
        status.innerHTML = 'Username already exists!';
    } else if (this.responseText === '3') {
        status.style.color = 'red';
        status.innerHTML = 'Email already exists!';
    } else {
        status.style.color = 'yellowgreen';
        status.innerHTML = 'Sign up successful!';
        window.location.href = '/dashboard?new_user=true';
    }

    submit.disabled = false;
    submit.style.color = 'white';
    submit.style.backgroundColor = '#00a2ff';
}
