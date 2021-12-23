function loginUser() {
  var status = document.getElementById("fail");
  status.style.color = "red";
  
  if (document.getElementById("usrname").value == "") {
    status.innerHTML = "Please fill in the username!";
    return;
  }

  if (document.getElementById("psw").value == "") {
    status.innerHTML = "Please fill in the password!";
    return;
  }

  status.innerHTML = "";

  var submit = document.getElementById("log_in");
  submit.disabled = true;
  submit.style.color = "gray";
  submit.style.backgroundColor = "#006097";

  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/signin", true);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.addEventListener('load', reqListener);
  xhttp.send(JSON.stringify({username: document.querySelector('#usrname').value, password: document.querySelector('#psw').value}));
}

function reqListener() {
  let text = document.getElementById('fail');

  if (this.responseText == 'True')
  {
    text.innerHTML = 'Login Successful!';
    text.style.color = 'greenyellow';
    window.location.href='/dashboard?new_user=false';
  }
  else 
  {
    text.innerHTML = 'The username/password is incorrect.';
    text.style.color = 'red';
  }
  
  var submit = document.getElementById("log_in");
  submit.disabled = false;
  submit.style.color = "white";
  submit.style.backgroundColor = "#00a2ff";
}
