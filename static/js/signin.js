let validUser = false;
let validPass = false;
let lastKeyUpTime = Date.now();
let recheck = true;


window.addEventListener('load', function () {
    let submit = document.getElementById('log_in');
    submit.disabled = true;
    submit.style.color = 'gray';
    submit.style.backgroundColor = '#006097';
    function SSO(){
      document.getElementById("signin_form").style.display = "none";
    }
    function checkValidUsername() {
        const response = document.getElementsByClassName("response")[0]

        response.innerHTML = loadingIcon + 'Please wait...';

        if (document.getElementById('usrname').value === '') {
            response.innerHTML = ' <p class="mt-2 text-sm text-red-600 dark:text-red-500"><span class="font-medium">Ahhh!</span> We coudn\'t find that username</p>';
            document.getElementById('usrname').classList.add('bg-red-50', 'border', 'border-red-500', 'text-red-900', 'placeholder-red-700', 'text-sm', 'rounded-lg', 'focus:ring-red-500', 'focus:border-red-500', 'block', 'w-full', 'p-2.5', 'dark:bg-red-100', 'dark:border-red-400');
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
        const response = document.getElementsByClassName("response")[1]
        response.innerHTML = loadingIcon + ' Please wait...';

        if (document.getElementById('psw').value === '') {
            response.innerHTML = '<p class="mt-2 text-sm text-red-600 dark:text-red-500"><span class="font-medium">Incorrect Password.</p>';
          document.getElementById('psw').classList.add('bg-red-50', 'border', 'border-red-500', 'text-red-900', 'placeholder-red-700', 'text-sm', 'rounded-lg', 'focus:ring-red-500', 'focus:border-red-500', 'block', 'w-full', 'p-2.5', 'dark:bg-red-100', 'dark:border-red-400');
            return false;
        }
        else {
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
    const response = document.getElementsByClassName('response')[0];

    // TODO(kev): switch case
    if (this.responseText === 'true') {
        response.style.color = 'green';
        response.innerHTML = '<p class="material-icons">check_circle</p>';
          
        document.getElementById('usrname').classList.add('g-green-50', 'border', 'border-green-500', 'text-green-900', 'placeholder-green-700', 'text-sm', 'rounded-lg', 'focus:ring-green-500', 'focus:border-green-500', 'block', 'w-full', 'p-2.5', 'dark:bg-green-100', 'dark:border-green-400');
        validUser = true;
    } 
    else if (this.responseText === 'false') {
        response.style.color = 'red';
        response.innerHTML = '<p class="material-icons">error</p>';
      document.getElementById('usrname').classList.add('bg-red-50', 'border', 'border-red-500', 'text-red-900', 'placeholder-red-700', 'text-sm', 'rounded-lg', 'focus:ring-red-500', 'focus:border-red-500', 'block', 'w-full', 'p-2.5', 'dark:bg-red-100', 'dark:border-red-400');
        validUser = false;
    }

}

function reqListener2() {
    const response = document.getElementsByClassName("response")[1];

    // TODO(kev): switch case
    if (this.responseText === 'true') {
        response.style.color = 'green';
        response.innerHTML = '<p class="material-icons">check_circle</p>';
      document.getElementById('psw').classList.add('g-green-50', 'border', 'border-green-500', 'text-green-900', 'placeholder-green-700', 'text-sm', 'rounded-lg', 'focus:ring-green-500', 'focus:border-green-500', 'block', 'w-full', 'p-2.5', 'dark:bg-green-100', 'dark:border-green-400');
        validPass = true;
    }
    else if (this.responseText === 'false') {
        response.style.color = 'red';
        response.innerHTML = '<p class="material-icons">error</p>';
      document.getElementById('psw').classList.add('bg-red-50', 'border', 'border-red-500', 'text-red-900', 'placeholder-red-700', 'text-sm', 'rounded-lg', 'focus:ring-red-500', 'focus:border-red-500', 'block', 'w-full', 'p-2.5', 'dark:bg-red-100', 'dark:border-red-400');
        validPass = false;
    }
}

function enableButton() {
    let submit = document.getElementById('log_in');
    if (validUser && validPass) {
        submit.disabled = false;
        submit.style.color = 'white';
        submit.style.backgroundColor = '#00a2ff';
    }
    else {
        submit.disabled = true;
        submit.style.color = 'gray';
        submit.style.backgroundColor = '#006097';
    }
}

setInterval(enableButton, 200);

function loginUser() {
    let password = document.getElementById('psw').value;
    let username = document.getElementById('usrname').value;

    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/signin', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.addEventListener('load', reqListener3);
    xhttp.send(
        JSON.stringify({
            password: password
        }
    ));
}

function reqListener3() {
    if (this.responseText === 'success') {
        window.location.href = '/dashboard';

    } else {
        let fail = document.getElementById('fail');
        fail.style.color = 'red';
        fail.innerHTML = 'There was an error when signing in';
    }
}