function fetchStatus() {
    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/spotify-status'
    });

    request.done((data) => {
        if (data === "<i style=\"display:inline-block; color:greenyellow; margin-right:10px;\" class=\"fab fa-spotify\"></i> You aren't listening to anything!") {
            data = 'Music Paused';
            document.getElementById('song').innerHTML = '<p>' + data + '</p>';
        } else {
            let songs = data.split(" • ");

            let name = songs[0]
            let artists = songs[1]
            let album = songs[2]
            let explicit = songs[3]
            let image = songs[4]
            let playing = songs[5]
            let timestamp = songs[6]
            let total = songs[7]
            let ratio = songs[8]
            document.getElementById('song').innerHTML = `
            <div style="float:Left;width:30%;"> 
                <img style="display: inline-block; margin:20px;" class="mb-3 w-24 h-24 shadow-lg" src="${image}">
            </div>
            <div style="float:left;width:70%;">
                <p><i style="display:inline-block; color:greenyellow; margin-right:10px;" class="fab fa-spotify"></i>  ${name} ${explicit} by <u>${artists}</u> <br>on <u>${album}</u><br>
                <center>${playing}</center> <br>
                  <div class="flex justify-between mb-1">
                  <span class="text-base font-medium text-blue-700 dark:text-white">${timestamp}</span>
                  <span class="text-sm font-medium text-blue-700 dark:text-white">${total}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-blue-600 h-2.5 rounded-full" style="width: ${Math.round(ratio)}%;"></div>
                </div>
            </div>
              
          
            `;


        }
    });
}

fetchStatus();
setInterval(fetchStatus, 1000);
