window.onload = function() {
    var details = document.getElementsByTagName("details");
    if (details.length > 0)
      document.addEventListener("click", function() { details[0].open = false; });
  }