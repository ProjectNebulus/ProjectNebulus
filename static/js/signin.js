let usernameInput = document.getElementById('usrname');
let passwordInput = document.getElementById('psw');
let lastKeyUpTime = Date.now();
let recheck = true;

function SSO() {
    document.getElementById('signin_form').style.display = 'none';
        if("SSO" in document.getElementById("sso")){
            document.getElementById('signin_form').style.display = 'none';
            document.getElementById("sso").innerHTML = "Return to Log In"

        }else{
            document.getElementById('signin_form').style.display = 'block';
        }
            document.getElementById("sso").innerHTML = "<span class=\"material-icons-outlined md-36\">key</span> SSO Login"


}

window.addEventListener('load', function () {
        let submit = document.getElementById('log_in');
        submit.style.color = 'gray';
        submit.style.backgroundColor = '#006097';

        function checkCredentials() {
            const response = document.getElementsByClassName('response')[0];
            response.classList.add("text-blue-600")
            response.innerHTML = loadingIcon + 'Please wait...';
            const response2 = document.getElementsByClassName('response')[1];
            response2.classList.add("text-blue-600")
            response2.innerHTML = loadingIcon + 'Please wait...';

            if (document.getElementById('usrname').value === '') {
                response.innerHTML =
                    ' <p class="mt-2 text-sm text-red-600 dark:text-red-500"><span class="font-medium">Ahhh!</span> Please enter a username!</p>';
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
            if (document.getElementById('psw').value === '') {
                console.log('password is empty');
                response2.innerHTML =
                    ' <p class="mt-2 text-sm text-red-600 dark:text-red-500"><span class="font-medium">Ahhh!</span> Please enter a password!</p>';
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
            let username = document.getElementById('usrname').value;
            let password = document.getElementById('psw').value;
            const xhttp = new XMLHttpRequest();
            xhttp.open('POST', '/signin_check', true);
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
            if (recheck && Date.now() - lastKeyUpTime > 300) {
                checkCredentials();
                recheck = false;
            }
        }

        document.getElementById('usrname').onkeyup = function () {
            lastKeyUpTime = Date.now();
            recheck = true;
        };
        document.getElementById('psw').onkeyup = function () {
            lastKeyUpTime = Date.now();
            recheck = true;
        };

        setInterval(checkStuff, 200);
    }
)



function reqListener1() {
    const response = document.getElementsByClassName('response')[0];
    const response2 = document.getElementsByClassName('response')[1];
    let loginButton = document.getElementById('log_in');

    // TODO(kev): switch case

    if (this.responseText.split("-")[0] === 'true') {
        response.style.color = 'green';
        response.innerHTML = '<p class="material-icons">check_circle</p>';

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
        if (this.responseText.split("-")[1] == "true") {
            response2.style.color = 'green';
            response2.innerHTML = '<p class="material-icons">check_circle</p>';

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

    } else if (this.responseText.split("-")[0] === 'false') {
        response.style.color = 'red';
        response.innerHTML = '<p class="material-icons">error</p>';
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


    } else if (this.responseText.split('-')[1] === 'false') {
        response2.style.color = 'red';
        response2.innerHTML = '<p class="material-icons">error</p>';
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
        loginButton.disabled = false;
        usernameInput.disabled = true;
        passwordInput.disabled = true;
    }


}


function loginUser() {
    window.location.href = '/dashboard';
}