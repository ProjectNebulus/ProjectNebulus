function fetchStatus() {
    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/spotify-status'
    });

    request.done((data) => {
        if (data === "You aren't listening to anything!") {
            data = 'Music Paused';
            document.getElementById('song').innerHTML = '<p>' + data + '</p>';
        } else {
            let songs = data.split("-");
            song = songs[0];
            artist = songs[1]
            art = songs[2]
            document.getElementById('song').innerHTML =
                '<p>' +
                song + " - " + artist +
                '</p><br><img class="mb-3 w-24 h-24 rounded-full shadow-lg" src=\'' +
                art +
                "' >";
        }
    });
}

fetchStatus();
setInterval(fetchStatus, 5000);
