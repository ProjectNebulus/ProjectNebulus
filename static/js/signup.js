window.addEventListener('load', function() {
  function validate(email)
  {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
  }

  let r_l = []
  var hasNumber = /\d/;  

  function changeEmail() 
  {
    var value = document.getElementById("email").value;
    if (validate(value))
    {
      document.getElementsByClassName("response")[0].style.color="green";
      ocument.getElementsByClassName("response")[0].innerHTML = '<i class="material-icons">check_circle</i>';
    }
    else
    {
      document.getElementsByClassName("response")[0].style.color="red";
      ocument.getElementsByClassName("response")[0].innerHTML = '<i class="material-icons">error</i>';
    }
  }

  if (localStorage.getItem('email') != null)
    document.getElementById("email").value = localStorage.getItem('email');
  
  function checkPassword()
  {
    var value = document.getElementById("password").value;
    if (value.length < 6)
    {
      document.getElementById("bubble2").style.display="block";
      document.getElementById("bubble").style.display="none";
      document.getElementById("bubble2").innerHTML = "Message: Password must be at least 6 characters long";
      document.getElementById("passwordValid").style.display="none";
    }
    else if (!hasNumber.test(value))
    {
      document.getElementById("bubble2").style.display="block";
      document.getElementById("bubble").style.display="none";
      document.getElementById("bubble2").innerHTML = "Message: Password must include at least 1 number";
      document.getElementById("passwordValid").style.display="none";
    }
    else if (true)
    {
      for (var i = 0; i < value.length; i++) {
        if (!r_l.includes(value[i])) {
          document.getElementById("bubble2").style.display="block";
          document.getElementById("bubble").style.display="none";
          document.getElementById("bubble2").innerHTML = "Message: Password must include at least 1 special character";
          document.getElementById("passwordValid").style.display="none";
        }
      }
    }
    else
    {
      document.getElementById("bubble").style.display="block";
      document.getElementById("bubble2").style.display="none";
      document.getElementById("bubble").innerHTML = "Message: Valid Password!";
      document.getElementById("passwordValid").style.display="block";

    }
  }  
});