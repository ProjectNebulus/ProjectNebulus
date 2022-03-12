let validUser = false;
let validPass = false;
let lastKeyUpTime = Date.now();
let recheck = true;

function SSO() {
        document.getElementById('signin_form').style.display = 'none';
}

window.addEventListener('load', function () {
    let submit = document.getElementById('log_in');
    submit.style.color = 'gray';
    submit.style.backgroundColor = '#006097';
    function checkValidUsername() {
        const response = document.getElementsByClassName('response')[0];
        response.classList.add("text-blue-600")
        response.innerHTML = loadingIcon + 'Please wait...';

        if (document.getElementById('usrname').value === '') {
            response.innerHTML =
                ' <p class="mt-2 text-sm text-red-600 dark:text-red-500"><span class="font-medium">Ahhh!</span> We coudn\'t find that username</p>';
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
            return false;
        } else {
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
    }

    function checkValidPassword() {
        const response = document.getElementsByClassName('response')[1];
        response.classList.add("text-blue-600")
        response.innerHTML = loadingIcon + 'Please wait...';

        if (document.getElementById('psw').value === '') {
            response.innerHTML =
                '<p class="mt-2 text-sm text-red-600 dark:text-red-500"><span class="font-medium">Incorrect Password.</p>';
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
            return false;
        } else {
            let password = document.getElementById('psw').value;
            let username = document.getElementById('usrname').value;
            const xhttp = new XMLHttpRequest();
            xhttp.open('POST', '/signin_check', true);
            xhttp.setRequestHeader('Content-type', 'application/json');
            xhttp.addEventListener('load', reqListener2);
            xhttp.send(
                JSON.stringify({
                    username :username,
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

    document.getElementById('usrname').onkeyup = function () {
        lastKeyUpTime = Date.now();
        recheck = true;
    };
    document.getElementById('psw').onkeyup = function () {
        lastKeyUpTime = Date.now();
        recheck = true;
    };

    setInterval(checkStuff, 200);
});

function reqListener1() {
    const response = document.getElementsByClassName('response')[0];
    const response2 = document.getElementsByClassName('response')[1];
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
            if (this.responseText.split("-")[1] == "true"){
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
     
        validUser = true;
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
        
        validUser = false;
    }
}

function reqListener2() {
    const response = document.getElementsByClassName('response')[1];

    // TODO(kev): switch case
    if (this.responseText === 'true') {
        response.style.color = 'green';
        response.innerHTML = '<p class="material-icons">check_circle</p>';
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
        validPass = true;
    } else if (this.responseText === 'false') {
        response.style.color = 'red';
        response.innerHTML = '<p class="material-icons">error</p>';
      document
            .getElementById('psw')
            .classList.remove(
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
        
        validPass = false;
    }
}

function enableButton() {
    let submit = document.getElementById('log_in');
    let usrname = document.getElementById('usrname');
    let psw = document.getElementById('psw');
    if (validUser && validPass) {
        usrname.disabled = true;
        psw.disabled = true;
        submit.style.color = 'white';
        submit.style.backgroundColor = '#00a2ff';
    } else {
        submit.style.color = 'gray';
        submit.style.backgroundColor = '#006097';
    }
}

setInterval(enableButton, 200);

function loginUser() {
    document.getElementById("log_in").innerHTML = '<svg role="status" class="inline mr-3 w-4 h-4 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg"> <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/> <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/> </svg> Loading...'
    let password = document.getElementById('psw').value;
    let username = document.getElementById('usrname').value;

    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/signin', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.addEventListener('load', reqListener3);
    xhttp.send(
        JSON.stringify({
            username: username,
            password: password
        })
    );
}

function reqListener3() {
  
    if (this.responseText === 'success') {
        window.location.href = '/dashboard';
        
    } else {
        console.log("Error:");
        console.log(this.responseText);
        console.log(".");
        alert(this.responseText);
        let fail = document.getElementById('fail');
        fail.style.color = 'red';
        fail.innerHTML = 'There was an error when signing in';
      document.getElementById("log_in").innerHTML = "Log In"
    }
}
