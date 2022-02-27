function fetchStatus() {
    const request = $.ajax({
        type: "POST",
        url: "/spoistatus"
    });

    request.done((data) => {
        if (data === "no_song_is_playing_right_now") {
            data = "No song is playing on Spotify right now!";
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