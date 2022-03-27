const HAS_NUMBER = /\d/;
const EMAIL_REGEX =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
let email_valid = false;
let password_valid = false;

function next(num){
    //document.getElementsByClassName("ease-in duration-75")[num*2-1].innerHTML = "<svg role=\"status\" class=\"inline mr-3 w-4 h-4 text-white animate-spin\" viewBox=\"0 0 100 101\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"> <path d=\"M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z\" fill=\"#E5E7EB\"/> <path d=\"M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z\" fill=\"currentColor\"/> </svg> Loading..."
    if (num === 1) {
        const myTimeout = setTimeout(function () {
            var request = $.ajax({
                type: "POST",
                url: "/sendEmail",
                data: {
                    "email": document.getElementById("email").value

                }
            });
            document.getElementById("step" + num.toString()).style.display = "none";
            document.getElementById("step" + (num + 1).toString()).style.display = "block";
            //document.getElementsByClassName("ease-in duration-75")[num * 2 - 1].innerHTML = "Next <svg style=\"display: inline-block;\" class=\"ml-2 -mr-1 w-5 h-5\" fill=\"currentColor\" viewBox=\"0 0 20 20\" xmlns=\"http://www.w3.org/2000/svg\"><path fill-rule=\"evenodd\" d=\"M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z\" clip-rule=\"evenodd\"></path></svg>"
        }, 3000);

    }else{
        if (num === 1 && !EMAIL_REGEX.test(document.getElementById("email").value)) {
            //document.getElementById("error").innerText = "Invalid Email";
        } else if (num === 1 && EMAIL_REGEX.test(document.getElementById("email").value)) {

        } else {
            //document.getElementById("error").innerText = "";
            const myTimeout = setTimeout(function () {

                document.getElementById("step" + num.toString()).style.display = "none";
                document.getElementById("step" + (num + 1).toString()).style.display = "block";
            }, 1000);
        }

    }



}
function prev(num){
    //document.getElementsByClassName("ease-in duration-75")[num*2-2].innerHTML = "<svg role=\"status\" class=\"inline mr-3 w-4 h-4 text-white animate-spin\" viewBox=\"0 0 100 101\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"> <path d=\"M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z\" fill=\"#E5E7EB\"/> <path d=\"M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z\" fill=\"currentColor\"/> </svg> Loading..."
    if (num === 1){
        location.reload();
    }else{
        const myTimeout =  setTimeout(function() {

            document.getElementById("step" + num.toString()).style.display = "none";
            document.getElementById("step" + (num - 1).toString()).style.display = "block";
            document.getElementsByClassName("ease-in duration-75")[num * 2 - 2].innerHTML = "<svg style=\"display: inline-block;\" class=\"w-6 h-6\" fill=\"none\" stroke=\"currentColor\" viewBox=\"0 0 24 24\" xmlns=\"http://www.w3.org/2000/svg\"><path stroke-linecap=\"round\" stroke-linejoin=\"round\" stroke-width=\"2\" d=\"M7 16l-4-4m0 0l4-4m-4 4h18\"></path></svg> Previous"
        }, 1000);

    }


}
window.addEventListener('load', function () {
    function validate(email) {
        return EMAIL_REGEX.test(email);
    }

    const r_l = ',<.>/?;:\'"\\|[{]}=+-_`!@#$%^&*()_+';

    function changeEmail() {
        let status = document.getElementsByClassName('errormsg')[1];
        status.style.color = 'red';
        status.innerHTML = '<br>';
        const value = document.getElementById('email').value;
        if (validate(value)) {
            document.getElementsByClassName('username-error')[1].style.color = 'green';
            document.getElementsByClassName('username-error')[1].innerHTML =
                '<i class="material-icons">check_circle</i>';
            document
                .getElementById('email')
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
                .getElementById('email')
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
            email_valid = true;
        } else {
            document.getElementsByClassName('username-error')[1].style.color = 'red';
            document.getElementsByClassName('username-error')[1].innerHTML =
                '<i class="material-icons">error</i>';
            status.innerHTML = 'Invalid Email';
            document
                .getElementById('email')
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
                .getElementById('email')
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
            email_valid = false;
        }
    }

    function confirmPassword() {
        let status = document.getElementsByClassName('errormsg')[3];
        status.style.color = 'red';
        status.innerHTML = '<br>';
        let value = document.getElementById('confirm-password').value;
        let value2 = document.getElementById('password').value;
        if (value === value2 && value !== "") {
            document.getElementsByClassName('username-error')[3].style.color = 'green';
            document.getElementsByClassName('username-error')[3].innerHTML =
                '<i class="material-icons">check_circle</i>';
            document
                .getElementById('confirm-password')
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
                .getElementById('confirm-password')
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
            email_valid = true;
        } else {
            document.getElementsByClassName('username-error')[3].style.color = 'red';
            document.getElementsByClassName('username-error')[3].innerHTML =
                '<i class="material-icons">error</i>';
            status.innerHTML = 'Two Passwords do not Match';
            document
                .getElementById('confirm-password')
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
                .getElementById('confirm-password')
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
            email_valid = false;
        }
    }

    if (localStorage.getItem('email') !== null)
        document.getElementById('email').value = localStorage.getItem('email');

    function checkPassword() {
        let status = document.getElementsByClassName('errormsg')[2];
        status.style.color = 'red';
        status.innerHTML = '<br>';
        const value = document.getElementById('password').value;
        if (value.length < 6) {
            status.innerHTML =
                'Password must be at least 6 characters long';
            password_valid = false;
        } else if (!HAS_NUMBER.test(value)) {
            status.innerHTML =
                'Message: Password must include at least 1 number';
            password_valid = false;
        } else {
            let hasSpecialCharacter = false;

            for (let i = 0; i < value.length; i++) {
                if (r_l.includes(value[i])) hasSpecialCharacter = true;
            }

            if (!hasSpecialCharacter) {
                status.innerHTML =
                    'Password must include at least 1 special character';
                document
                    .getElementById('password')
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
                    .getElementById('password')
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
                document.getElementsByClassName('username-error')[2].style.color = 'red';
                document.getElementsByClassName('username-error')[2].innerHTML =
                    '<i class="material-icons">error</i>';
                password_valid = false;
            } else {
                password_valid = true;
                document
                    .getElementById('password')
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
                    .getElementById('password')
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
                document.getElementsByClassName('username-error')[2].style.color = 'green';
                document.getElementsByClassName('username-error')[2].innerHTML =
                    '<i class="material-icons">check_circle</i>';
            }
        }
    }

    document.getElementById('email').onkeyup = changeEmail;
    document.getElementById('password').onkeyup = checkPassword;
    document.getElementById('confirm-password').onkeyup = confirmPassword;
});

function signUp() {
    console.log(password_valid);
    console.log(email_valid);

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
        if (!email_valid) {
            status.innerHTML = 'Please enter a valid email!';
            return false;
        }
        else if (!password_valid) {
            status.innerHTML = 'Please enter a valid password!';
            return false;
        }
        else if (!(password_valid && email_valid)) {
            status.innerHTML = 'Please enter a valid email and password!';
            return false;
        }

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
