let validUser = false;
let validPass = false;
let lastKeyUpTime = Date.now();
let recheck = true;

window.addEventListener('load', function () {
    let submit = document.getElementById('log_in');
    submit.disabled = true;
    submit.style.color = 'gray';
    submit.style.backgroundColor = '#006097';
    // function launch_SSO(){
    //   document.getElementById("signin_form").style.display = "none";
    // }
    function checkValidUsername() {
        var response = document.getElementsByClassName("response")[0]
        response.innerHTML = '<span class="material-icons-outlined" style="color:lightgray;">pending</span>';

        // let status = document.getElementById('fail');

        if (document.getElementById('usrname').value === '') {
            response.innerHTML = '<i class="material-icons" style="color:red;">error</i>';
            return false; 
        } 
        else {
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
        var response = document.getElementsByClassName("response")[1]
        response.innerHTML = '<span class="material-icons-outlined" style="color:lightgray;">pending</span>';

        if (document.getElementById('psw').value === '') {
            response.innerHTML = '<i class="material-icons" style="color:red;">error</i>';
            return false;
        } else {
            let password = document.getElementById('psw').value;
            const xhttp = new XMLHttpRequest();
            xhttp.open('POST', '/signin_password', true);
            xhttp.setRequestHeader('Content-type', 'application/json');
            xhttp.addEventListener('load', reqListener2);
            xhttp.send(
                JSON.stringify({
                    password: password
                })
            );
        }
    }

    function checkStuff() {
        if (recheck && Date.now() - lastKeyUpTime > 300) {
            checkValidUsername();
            checkValidPassword();
            recheck = false;
        }
    }

    document.getElementById('usrname').onkeyup = function() {
        lastKeyUpTime = Date.now();
        recheck = true;
    };
    document.getElementById('psw').onkeyup = function() {
        lastKeyUpTime = Date.now();
        recheck = true;
    };

    setInterval(checkStuff, 200);
});

function reqListener1() {
    var response = document.getElementsByClassName('response')[0];

    // TODO(kev): switch case
    if (this.responseText === 'true') {
        response.style.color = 'green';
        response.innerHTML = '<i class="material-icons">check_circle</i>';
        validUser = true;
    } 
    else if (this.responseText === 'false') {
        response.style.color = 'red';
        response.innerHTML = '<i class="material-icons">error</i>';
        validUser = false;
    }

}

function reqListener2() {
    var response = document.getElementsByClassName("response")[1];

    // TODO(kev): switch case
    if (this.responseText === 'true') {
        response.style.color = 'green';
        response.innerHTML = '<i class="material-icons">check_circle</i>';
        validPass = true;
    } else if (this.responseText === 'false') {
        response.style.color = 'red';
        response.innerHTML = '<i class="material-icons">error</i>';
        validPass = false;
    }
}

function enableButton() {
    let submit = document.getElementById('log_in');
    if (validUser && validPass){
        submit.disabled = false;
        submit.style.color = 'white';
        submit.style.backgroundColor = '#00a2ff';
    } else {
        submit.disabled = true;
        submit.style.color = 'gray';
        submit.style.backgroundColor = '#006097';
    }
}

setInterval(enableButton, 200);

// function loginUser() {
//     let password = document.getElementById('psw').value;
//     let username = document.getElementById('usrname').value;

//     const xhttp = new XMLHttpRequest();
//     xhttp.open('POST', '/signin', true);
//     xhttp.setRequestHeader('Content-type', 'application/json');
//     xhttp.addEventListener('load', reqListener3);
//     xhttp.send(
//         JSON.stringify({
//             password: password
//         }
//     ));
// }

function reqListener3() {
    if (this.responseText === 'success') {
        window.location.href = '/dashboard';

    } else {
        let fail = document.getElementById('fail');
        fail.style.color = 'red';
        fail.innerHTML = 'There was an error when signing in';
    }
}