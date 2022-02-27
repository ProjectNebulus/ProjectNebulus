function fetchStatus() {
    const request = $.ajax({
        type: "POST",
        url: "/spoistatus"
    });

    request.done((data) => {
        if (data === "You aren't listening to anything!") {
            data = "Music Paused";
            document.getElementById("song").innerHTML = "<p>" + data + "</p>";
        }
        else{
            const request2 = $.ajax({
                type: "POST",
                url: "/spoistatus2"
            });
            request2.done((data2) => {
                document.getElementById("song").innerHTML = "<p>" + data + "</p><br><img class=\"mb-3 w-24 h-24 rounded-full shadow-lg\" src='"+data2+"' >";
            })

        }


    });

}

setInterval(fetchStatus, 5000);