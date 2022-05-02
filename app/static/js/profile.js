function fetchStatus() {
    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/spotify-status'
    });

    request.done((data) => {
        if (data === "1") {
            document.getElementById('song').innerHTML = `
            <i style="display:inline-block; color:#1BD661; margin-right:10px;" class="fab fa-spotify"></i> Spotify isn't Detected!
            <a target="_blank" href="https://open.spotify.com/">
                <button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                Go to Spotify <i class="material-icons">open_in_newt</i>
                </button>
            </a>
            
            `
        } else if (data === "2"){
            document.getElementById('song').innerHTML = `
            <i style="display:inline-block; color:#1BD661; margin-right:10px;" class="fab fa-spotify"></i> Spotify isn't Connected!
            <a target="_blank" href="/settings#connections">
                <button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                Connect Spotify <i class="material-icons">open_in_newt</i>
                </button>
            </a>
            
            `
        }else {
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
            <i style="display:inline-block; color:#1BD661; margin-right:10px;" class="fab fa-spotify"></i>
            <div style="float:Left;width:30%;"> 
                <img style="display: inline-block; margin:20px;" class="mb-3 w-24 h-24 shadow-lg" src="${image}">
            </div>
            <div style="float:left;width:70%;">
                <p class="text-2xl text-black dark:text-white">${name} ${explicit}</p>
                <p class="text-xl text-gray-600 dark:text-gray-300">${artists}</p>
                <p class="text-xl text-gray-600 dark:text-gray-300">${album}</p>
                <center>${playing}</center> <br>
                  <div class="flex justify-between mb-1">
                  <span class="text-base font-medium text-blue-700 dark:text-white">${timestamp}</span>
                  <span class="text-sm font-medium text-blue-700 dark:text-white">${total}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                  <div class="bg-green-400 h-2.5 rounded-full" style="width: ${Math.round(ratio)}%;"></div>
                </div>
            </div>
              
          
            `;


        }
    });
}

fetchStatus();
setInterval(fetchStatus, 1000);
