function fetchStatus() {
    const request = $.ajax({
        type: 'POST',
        url: '/spoistatus'
    });

    request.done((data) => {
        if (data === 'no_song_is_playing_right_now')
            data = 'No song is playing on Spotify right now!';

        document.getElementById('song').innerHTML = '<p>' + data + '</p>';
    });
}

setInterval(fetchStatus, 5000);
