


function selectChanged(){
    document.getElementById('schoolName').innerText = 'Your '+document.getElementById('selection').value+' account';
    document.getElementById('schoolInput').placeholder= 'Your '+document.getElementById('selection').value+' Username';
    document.getElementById('typeHere').style.display = 'block';

}
function SSO() {

        if( document.getElementById("sso").innerText.includes("SSO")){
            document.getElementById('signin_form').style.display = 'none';
            document.getElementById("sso").innerHTML = "Return to Log In"
            document.getElementById('signin_form2').style.display = 'block';

        }else {
            document.getElementById('signin_form').style.display = 'block';
            document.getElementById('signin_form2').style.display = 'none';
            document.getElementById("sso").innerHTML = "<span class=\"material-icons-outlined md-36\">key</span> SSO Login"
        }


}
function Schoology() {

    if( document.getElementById("schoologyy").innerText.includes("Schoology")){
        document.getElementById('signin_form').style.display = 'none';
        document.getElementById("schoologyy").innerHTML = "Return to Log In"
        document.getElementById('signin_form3').style.display = 'block';
        document.getElementById("launchBTN").style.display = "block";

    }else {
        document.getElementById('signin_form').style.display = 'block';
        document.getElementById('signin_form3').style.display = 'none';
        document.getElementById("schoologyy").innerHTML = "Schoology Login"
        document.getElementById("launchBTN").style.display = "none";
    }


}
$('#confirmBTN').on('click', function() {
    var $this = $(this);
    $this.button('loading');
    setTimeout(function() {

        var request =  $.ajax({
            type: "POST",
            url: "/schoology",
            data: {
                "link": "https://"+document.getElementById("domain").value+".schoology.com/"
            }
        });
        request.done(function(data) {
            $this.button('reset');
            resp = document.getElementById("resp")
            if (data==="error!!!"){
                resp.style.color = "red";
                resp.innerHTML = "Login Failed. Reason: Clicked Deny on Schoology or closed Schoology popup window. Make sure Popups are enabled on your browser. Click Authorize again and click Approve this time!";
                document.getElementById('auth').style.display = 'inline';
                document.getElementById('connectbtn').style.display = 'none';

            }else{
                resp.style.color = "green";
                resp.innerHTML = "Successfully linked the Schoology Account <b>"+data+"</b>!";
                //window.location.replace("/settings");
            }

        });

    }, 1000);



});
function startSchoology(){
    let domain = document.getElementById("domain").value;
    let newurl = "";
    var request =  $.ajax({
        type: "GET",
        url: "/generateURL_Signin",
        data: {
        }
    });
    // request.done(function(data){
    //     alert("done");
    //     newurl = data;
    //     alert(data);
    // });
    // alert(data);
    // alert(newurl);

    //newwindow2=window.open(newurl.replace('bins',domain),'Authorize with Schoology2','height=400,width=800')
    request.done(function (data){
        newwindow2=window.open(data.replace('bins',domain),'Authorize with Schoology2','height=400,width=800')
    })
    document.getElementById("launchBTN").style.display = "none";
    document.getElementById("confirmBTN").style.display = "none";
    document.getElementById("selectdomain").style.display = "none";
    function checkIfDone(){
        var request =  $.ajax({
            type: "GET",
            url: "/checkConnectedSchoology",
            data: {
            }
        });
        request.done(function(data){
                if (data==="False"){
                    checkIfDone();
                }else{
                    return;
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
function confirmSchoology(){
    var request =  $.ajax({
        type: "POST",
        url: "/schoology",
        data: {
            "link": "https://"+document.getElementById("domain").value+".schoology.com/"
        }
    })
    request.done(function(data){
        document.getElementById("confirmBTN").style.display = "none";
        if (data==="error!!!"){

            document.getElementById("launchBTN").style.display = "block";
            document.getElementById("error").style.display = "block";

        }
        else{
            let email = data.split("•")[1];
            let name = data.split("•")[0];
            document.getElementById("confirmation").style.display = "block";
            document.getElementById("name").innerHTML = name;
            document.getElementById("email").innerHTML = email;

        }

    })

}
window.addEventListener('load', function () {
    document.querySelector('#domain').addEventListener('input', resizeInput);

    let lastKeyUpTime1 = Date.now();
        let recheck = true;
        let loginButton = document.getElementById('log_in');
        loginButton.style.color = 'gray';
        loginButton.style.backgroundColor = '#006097';
        loginButton.disabled = true;

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
    }
        if (this.responseText.split("-")[1] === "true") {
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

    if (this.responseText.split("-")[0] === 'false' && document.getElementById('usrname').value !== '') {
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

    }
    if (this.responseText.split('-')[1] === 'false' && document.getElementById('psw').value !== '') {
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