function selectChanged() {
    document.getElementById('schoolName').innerText = 'Your ' + document.getElementById('selection').value + ' account';
    document.getElementById('schoolInput').placeholder = 'Your ' + document.getElementById('selection').value + ' Username';
    document.getElementById('typeHere').style.display = 'block';

}

function SSO() {

    if (document.getElementById("sso").innerText.includes("SSO")) {
        document.getElementById('signin_form').style.display = 'none';
        document.getElementById("sso").innerHTML = "Return to Log In"
        document.getElementById('signin_form2').style.display = 'block';
        document.getElementById("schoologyy").style.display = "none";

    } else {
        document.getElementById('signin_form').style.display = 'block';
        document.getElementById('signin_form2').style.display = 'none';
        document.getElementById("sso").innerHTML = "<span class=\"material-icons-outlined md-36\">key</span> SSO Login"
        document.getElementById("schoologyy").style.display = "block";
    }


}

function Schoology() {

    if (document.getElementById("schoologyy").innerText.includes("Schoology")) {
        document.getElementById('signin_form').style.display = 'none';
        document.getElementById("schoologyy").innerHTML = "Return to Log In"
        document.getElementById('signin_form3').style.display = 'block';
        document.getElementById("launchBTN").style.display = "block";
        document.getElementById("sso").style.display = "none";

    } else {
        document.getElementById('signin_form').style.display = 'block';
        document.getElementById('signin_form3').style.display = 'none';
        document.getElementById("schoologyy").innerHTML = "Schoology Login"
        document.getElementById("launchBTN").style.display = "none";
        document.getElementById("sso").style.display = "block";
    }


}

$('#confirmBTN').on('click', function () {
    var $this = $(this);
    $this.button('loading');
    setTimeout(function () {

        var request = $.ajax({
            type: "POST",
            url: "/api/v1/internal/signin-with-schoology",
            data: {
                "link": "https://" + document.getElementById("domain").value + ".schoology.com/"
            }
        });
        request.done(function (data) {
            $this.button('reset');
            resp = document.getElementById("resp")
            if (data === "1") {
                resp.style.color = "red";
                resp.innerHTML = "Login Failed. Reason: Clicked Deny on Schoology or closed Schoology popup window. Make sure Popups are enabled on your browser. Click Authorize again and click Approve this time!";
                document.getElementById('auth').style.display = 'inline';
                document.getElementById('connectbtn').style.display = 'none';


            } else if (data === '2') {
                resp.style.color = "red";
                resp.innerHTML = "Login Failed. Reason: Your account is not connected to Schoology. Please signin normally and then connect your schoology account to signin with Schoology.";
                document.getElementById('auth').style.display = 'inline';
                document.getElementById('connectbtn').style.display = 'none';

            } else {
                resp.style.color = "green";
                resp.innerHTML = "Successfully linked the Schoology Account <b>" + data + "</b>!";
                //window.location.replace("/settings");
            }

        });

    }, 1000);


});

function startSchoology() {
    let domain = document.getElementById("domain").value;
    let newurl = "";
    var request = $.ajax({
        type: "GET",
        url: "/api/v1/internal/generate-schoology-oauth-url",
        data: {}
    });
    // request.done(function(data){
    //     alert("done");
    //     newurl = data;
    //     alert(data);
    // });
    // alert(data);
    // alert(newurl);

    //newwindow2=window.open(newurl.replace('bins',domain),'Authorize with Schoology2','height=400,width=800')
    request.done(function (data) {
        newwindow2 = window.open(data.replace('bins', domain), 'Authorize with Schoology2', 'height=400,width=800')
    })
    document.getElementById("launchBTN").style.display = "none";
    document.getElementById("confirmBTN").style.display = "none";
    document.getElementById("selectdomain").style.display = "none";

    function checkIfDone() {
        var request = $.ajax({
            type: "GET",
            url: "/api/v1/internal/check-schoology-connection",
            data: {}
        });
        request.done(function (data) {
                if (data === "False") {
                    checkIfDone();
                } else {

                }
            }
        )
    }

    checkIfDone();
    document.getElementById("confirmBTN").style.display = "block";

}

function resizeInput() {
    this.style.width = this.value.length + "ch";
}

function confirmSchoology() {
    var request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/signin-with-schoology",
        data: {
            "link": "https://" + document.getElementById("domain").value + ".schoology.com/"
        }
    })
    request.done(function (data) {


        document.getElementById("confirmBTN").style.display = "none";
        if (data === "1" || data === "2") {
            document.getElementById("launchBTN").style.display = "block";
            document.getElementById("error").style.display = "block";
            if (data === "1") {
                document.getElementById("error").innerHTML = "Login Failed. Reason: Clicked Deny on Schoology or closed Schoology popup window. Make sure Popups are enabled on your browser. Click Authorize again and click Approve this time!";
            } else {
                document.getElementById("error").innerHTML = "Login Failed. Reason: Your account is not connected to Schoology. Please signin normaly and then connect your schoology account to signin with Schoology.";
            }

        } else {
            let email = data.split("•")[1];
            let name = data.split("•")[0];
            document.getElementById("confirmation").style.display = "block";
            document.getElementById("name").innerHTML = name;
            document.getElementById("email").innerHTML = email;

            window.location.href = '/dashboard'

        }

    })

}

window.addEventListener('load', function () {

        let lastKeyUpTime1 = Date.now();
        let recheck = true;
        let loginButton = document.getElementById('log_in');
        loginButton.style.color = 'gray';
        loginButton.style.backgroundColor = '#006097';
        loginButton.disabled = true;

        function checkCredentials() {
            const response = document.getElementById('username-error');


            const response2 = document.getElementById('password-error');

            const errorUsername = document.getElementsByClassName('username-error-msg');
            const errorPassword = document.getElementsByClassName('password-error-msg');
            if (document.getElementById('usrname').value === '') {
                errorUsername.innerHTML =
                    'Hey! Please enter a username!';
                document
                    .getElementById('usrname')
                    .classList.add(
                    'bg-red-50',
                    'border',
                    'border-red-500',
                    'text-red-900',
                    'placeholder-red-700',
                    'text-sm',
                    'rounded-lg',
                    'focus:ring-red-500',
                    'focus:border-red-500',
                    'block',
                    'w-full',
                    'p-2.5',
                    'dark:bg-red-100',
                    'dark:border-red-400'
                );
            }
            else {
                errorUsername.innerHTML = '';
            }
            if (document.getElementById('psw').value === '') {
                console.log('password is empty');
                errorPassword.innerHTML =
                    'Hey! Please enter a password!';
                document
                    .getElementById('psw')
                    .classList.add(
                    'bg-red-50',
                    'border',
                    'border-red-500',
                    'text-red-900',
                    'placeholder-red-700',
                    'text-sm',
                    'rounded-lg',
                    'focus:ring-red-500',
                    'focus:border-red-500',
                    'block',
                    'w-full',
                    'p-2.5',
                    'dark:bg-red-100',
                    'dark:border-red-400'
                );
            } else {
                errorPassword.innerHTML = '';
            }
            let username = document.getElementById('usrname').value;
            let password = document.getElementById('psw').value;
            const xhttp = new XMLHttpRequest();
            xhttp.open('POST', '/api/v1/internal/check-signin', true);
            xhttp.setRequestHeader('Content-type', 'application/json');
            xhttp.addEventListener('load', reqListener1);
            xhttp.send(
                JSON.stringify({
                    username: username,
                    password: password
                })
            );
        }

        function checkStuff() {
            if (recheck && Date.now() - lastKeyUpTime1 > 300) {
                checkCredentials();
                recheck = false;
            }
        }

        document.getElementById('usrname').onkeyup = function () {
            lastKeyUpTime1 = Date.now();
            recheck = true;
        };
        document.getElementById('psw').onkeyup = function () {
            lastKeyUpTime1 = Date.now();
            recheck = true;
        };

        setInterval(checkStuff, 200);

    }
)


function reqListener1() {
    console.log(this.responseText);
    const usernameError = document.getElementById('username-error');
    const passwordError = document.getElementById('password-error');
    const usernameErrorMsg = document.getElementById('username-error-msg');
    const passwordErrorMsg = document.getElementById('password-error-msg');
    // TODO(kev): switch case

    if (this.responseText.split("-")[0] === 'true') {
        usernameError.style.color = 'green';
        usernameError.innerHTML = '<p class="material-icons">check_circle</p>';
        usernameErrorMsg.style.color = 'green';
        usernameErrorMsg.innerHTML = 'Correct Username!';

        document
            .getElementById('usrname')
            .classList.remove(
            'bg-red-50',
            'border',
            'border-red-500',
            'text-red-900',
            'placeholder-red-700',
            'text-sm',
            'rounded-lg',
            'focus:ring-red-500',
            'focus:border-red-500',
            'block',
            'w-full',
            'p-2.5',
            'dark:bg-red-100',
            'dark:border-red-400'
        );
        document
            .getElementById('usrname')
            .classList.add(
            'g-green-50',
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
            'dark:bg-green-100',
            'dark:border-green-400'
        );
    }
    if (this.responseText.split("-")[1] === "true") {
        passwordError.style.color = 'green';
        passwordError.innerHTML = '<p class="material-icons">check_circle</p>';
        passwordErrorMsg.style.color = 'green';
        passwordErrorMsg.innerHTML = 'Correct Password!';

        document
            .getElementById('psw')
            .classList.remove(
            'bg-red-50',
            'border',
            'border-red-500',
            'text-red-900',
            'placeholder-red-700',
            'text-sm',
            'rounded-lg',
            'focus:ring-red-500',
            'focus:border-red-500',
            'block',
            'w-full',
            'p-2.5',
            'dark:bg-red-100',
            'dark:border-red-400'
        );
        document
            .getElementById('psw')
            .classList.add(
            'g-green-50',
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
            'dark:bg-green-100',
            'dark:border-green-400'
        );
    }

    if (this.responseText.split("-")[0] === 'false' && document.getElementById('usrname').value !== '') {
        usernameError.style.color = 'red';
        usernameError.innerHTML = '<p class="material-icons">error</p>';
        usernameErrorMsg.style.color = 'red';
        usernameErrorMsg.innerHTML = 'Incorrect Username!';
        document
            .getElementById('usrname')
            .classList.add(
            'g-green-50',
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
            'dark:bg-green-100',
            'dark:border-green-400'
        );
        document
            .getElementById('usrname')
            .classList.add(
            'bg-red-50',
            'border',
            'border-red-500',
            'text-red-900',
            'placeholder-red-700',
            'text-sm',
            'rounded-lg',
            'focus:ring-red-500',
            'focus:border-red-500',
            'block',
            'w-full',
            'p-2.5',
            'dark:bg-red-100',
            'dark:border-red-400'
        );

    }
    if (this.responseText.split('-')[1] === 'false' && document.getElementById('psw').value !== '') {
        passwordError.style.color = 'red';
        passwordError.innerHTML = '<p class="material-icons">error</p>';
        passwordErrorMsg.style.color = 'red';
        passwordErrorMsg.innerHTML = 'Incorrect Password!';
        document
            .getElementById('psw')
            .classList.add(
            'g-green-50',
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
            'dark:bg-green-100',
            'dark:border-green-400'
        );
        document
            .getElementById('psw')
            .classList.add(
            'bg-red-50',
            'border',
            'border-red-500',
            'text-red-900',
            'placeholder-red-700',
            'text-sm',
            'rounded-lg',
            'focus:ring-red-500',
            'focus:border-red-500',
            'block',
            'w-full',
            'p-2.5',
            'dark:bg-red-100',
            'dark:border-red-400'
        );
    }

    if (this.responseText.split('-')[1] === 'true' && this.responseText.split('-')[0] === 'true') {
        let loginButton = document.getElementById('log_in');
        let usernameInput = document.getElementById('usrname');
        let passwordInput = document.getElementById('psw');
        loginButton.disabled = false;
        loginButton.style.backgroundColor = '#1B64F1';
        usernameInput.disabled = true;
        passwordInput.disabled = true;
    }


}


function loginUser() {
    let username = document.getElementById('usrname').value;
    let password = document.getElementById('psw').value;
    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/v1/internal/sign-in', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.addEventListener('load', reqListener2);
    xhttp.send(
        JSON.stringify({
            username: username,
            password: password
        })
    );
}


function reqListener2() {
    if (this.responseText === 'true') {
        let status = document.getElementById('fail');
        status.style.color = 'yellowgreen';
        status.innerHTML = 'Login was successful!';
        window.location.href = '/dashboard';
    } else {
        let status = document.getElementById('fail');
        status.style.color = 'red';
        status.innerHTML = 'Login failed!';
    }
}