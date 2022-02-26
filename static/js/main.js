window.onload = function () {
    let details = document.getElementsByTagName("details");
    if (details.length > 0)
        document.addEventListener("click", function () {
            if (event.target != details[0])
                details[0].open = false;
        });
}