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
            let songs = data.split(" • ");
            let song = songs[0];
            let artist = songs[1]
            let art = songs[2]
            let art2 = songs[3];
            document.getElementById('song').innerHTML = `<div class="p-6 max-w-sm bg-white rounded-lg border border-gray-200 shadow-md dark:bg-gray-800 dark:border-gray-700">
            <p> ${song} - ${artist} <br><br>
            <img style="display: inline-block; margin:20px;" class="mb-3 w-24 h-24 rounded-full shadow-lg" src="${art}">
            <img style="float:left; margin:20px; display: inline-block;" class="mb-3 w-24 h-24 shadow-lg" src=${art2}>
            </div>
            `;


        }
    });
}

fetchStatus();
setInterval(fetchStatus, 5000);
