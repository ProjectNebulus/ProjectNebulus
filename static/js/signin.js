function loginUser() {
    var status = document.getElementById('fail');
    status.style.color = 'red';

    if (document.getElementById('usrname').value == '') {
        status.innerHTML = 'Please fill in the username!';
        return;
    }

    if (document.getElementById('psw').value == '') {
        status.innerHTML = 'Please fill in the password!';
        return;
    }

    status.innerHTML = '<br>';

    var submit = document.getElementById('log_in');
    submit.disabled = true;
    submit.style.color = 'gray';
    submit.style.backgroundColor = '#006097';

    var xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/signin', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.addEventListener('load', reqListener);
    xhttp.send(
        JSON.stringify({
            username: document.querySelector('#usrname').value,
            password: document.querySelector('#psw').value
        })
    );
}

function reqListener() {
    let text = document.getElementById('fail');

    if (this.responseText == '0') {
        text.innerHTML = 'Login Successful!';
        text.style.color = 'greenyellow';
        console.log('Success');
        window.location.href = '/dashboard';
    } else if (this.responseText == '1') {
        text.innerHTML = 'The password is incorrect.';
        text.style.color = 'red';
    } else if (this.responseText == '2') {
        text.innerHTML = 'This username/email does not exist.';
        text.style.color = 'red';
    }

    var submit = document.getElementById('log_in');
    submit.disabled = false;
    submit.style.color = 'white';
    submit.style.backgroundColor = '#00a2ff';
}
