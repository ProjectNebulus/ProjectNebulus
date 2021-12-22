function loginUser() {
  
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/signin", true);
  xhttp.setRequestHeader('Content-type', 'application/json');
  xhttp.addEventListener('load', reqListener);
  xhttp.send(JSON.stringify({username: document.querySelector('#usrname').value, password: document.querySelector('#psw').value}));
}

function reqListener(){
  let text = document.getElementById('fail');
  if (this.responseText == 'True'){
    text.innerHTML = 'Your login attempt was successful';
    text.style.color = 'green';
    window.location.href='/dashboard?new_user=false';
  } else {
    text.innerHTML = 'That username/email and password does not exist';
    text.style.color = 'red';
  }
}
