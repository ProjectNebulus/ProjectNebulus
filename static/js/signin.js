window.addEventListener('load', function () {
    let submit = document.getElementById('log_in');
    submit.disabled = true;
    submit.style.color = 'gray';
    submit.style.backgroundColor = '#006097';

    function checkValidUsername() {
        let status = document.getElementById('fail');
        status.style.color = 'red';


        if (document.getElementById('usrname').value === '') {
            return false;
        } else {
            let username = document.getElementById('usrname').value;
            const xhttp = new XMLHttpRequest();
            xhttp.open('POST', '/signin_username', true);
            xhttp.setRequestHeader('Content-type', 'application/json');
            xhttp.addEventListener('load', reqListener1);
            xhttp.send(
                JSON.stringify({
                    username: username
                })
            );

        }
    }

    function checkValidPassword() {
        let status = document.getElementById('fail');
        status.innerHTML = '<br>';
        status.style.color = 'red';


        if (document.getElementById('psw').value === '') {
            return false;
        } else {
            let password = document.getElementById('psw').value;
            let username = document.getElementById('usrname').value;
            const xhttp = new XMLHttpRequest();
            xhttp.open('POST', '/signin_password', true);
            xhttp.setRequestHeader('Content-type', 'application/json');
            xhttp.addEventListener('load', reqListener2);
            xhttp.send(
                JSON.stringify({
                    username: username,
                    password: password
                })
            );
        }
    }

    document.getElementById('usrname').onkeyup = checkValidUsername;
    document.getElementById('psw').onkeyup = checkValidPassword;


});

function reqListener1() {
    let submit = document.getElementById('log_in');
    // TODO(kev): switch case
    if (this.responseText === 'true') {
        document.getElementsByClassName('response')[0].style.color = 'green';
        document.getElementsByClassName('response')[0].innerHTML =
            '<i class="material-icons">check_circle</i>';
    } else if (this.responseText === 'false') {
        document.getElementsByClassName('response')[0].style.color = 'red';
        document.getElementsByClassName('response')[0].innerHTML =
            '<i class="material-icons">error</i>';
    }

}

function reqListener2() {
    let submit = document.getElementById('log_in');
    // TODO(kev): switch case
    if (this.responseText === 'true') {
        document.getElementsByClassName('response')[1].style.color = 'green';
        document.getElementsByClassName('response')[1].innerHTML =
            '<i class="material-icons">check_circle</i>';
        submit.disabled = false;
        submit.style.color = 'white';
        submit.style.backgroundColor = '#00a2ff';
    } else if (this.responseText === 'false') {
        document.getElementsByClassName('response')[1].style.color = 'red';
        document.getElementsByClassName('response')[1].innerHTML =
            '<i class="material-icons">error</i>';
    }
}


function loginUser() {
    window.location.href = '/dashboard';
}


