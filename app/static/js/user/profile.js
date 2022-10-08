function fetchStatus() {
    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/get/spotify'
    });

    request.done((data) => {
        if (data === '1') {
            document.getElementById('song').innerHTML = `
            <div style="float:right;display: grid; grid-auto-flow: column; align-content: center;">
            <i style="display:inline-block; color:#1BD661; margin-right:10px;" class="fa fa-spotify"></i> Spotify isn't Detected!
            <a target="_blank" href="https://open.spotify.com/">
                <button style="margin-left: 10px; display:grid; grid-auto-flow: column; align-content: center; justify-content: center;" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                Go to Spotify <i style="display:grid; grid-auto-flow: column; align-content: center; justify-content: center;" class="material-icons">open_in_newt</i>
                </button>
            </a>
            </div>    `;
        } else if (data === '2') {
            document.getElementById('song').innerHTML = `
            <div style="float:right;display: grid; grid-auto-flow: column; align-content: center;"><br>
            <i style="display:inline-block; color:#1BD661; margin-right:10px;" class="fa fa-spotify"></i> Spotify isn't Connected!
            <a target="_blank" href="/settings#connections">
                <button style="vertical-align: middle;" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                Connect Spotify <i style="vertical-align: middle; display: inline-block;" class="material-icons">open_in_newt</i>
                </button>
            </a>
            </div>  `;
        } else if (data === '3') {
            document.getElementById('song').innerHTML = `
            <div style="float:right;display: grid; grid-auto-flow: column; align-content: center;">
                <i style="display:inline-block; color:#1BD661; margin-right:10px;" class="fa fa-spotify"></i> Your Spotify Account is not registered in the developer dashboard!
                    <a target="_blank" href="https://developer.spotify.com/app">
                    <button style="margin-left: 10px; display:grid; grid-auto-flow: column; align-content: center; justify-content: center;" type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800">
                    Go to Spotify <i style="display:grid; grid-auto-flow: column; align-content: center; justify-content: center;" class="material-icons">open_in_newt</i>
                    </button>
                </a>
            </div>  `;
        } else {
            let songs = data.split(' • ');

            let name = songs[0];
            let artists = songs[1];
            let album = songs[2];
            let explicit = songs[3];
            let image = songs[4];
            let playing = songs[5];
            let timestamp = songs[6];
            let total = songs[7];
            let ratio = songs[8];
            document.getElementById('songname').innerText = name;
            document.getElementById('song').innerHTML = `
            <div> <!--class="grid grid-cols-2"!-->
            <div style="width:80px;vertical-align:middle; display:inline-block;"> 
                <img style="border-radius:10px;" class="mb-3 shadow-lg" src="${image}">
            </div>
            <div style="margin-left:15px; width: 250px;vertical-align:middle; display:inline-block;">
                <p class="text-2xl text-black dark:text-white overflow-x-hidden truncate"><i style="display:inline-block; color:#1BD661; margin-right:10px;" class="fa fa-spotify"></i> ${name} ${explicit}</p>
     
                <p class="text-xl text-gray-600 dark:text-gray-300 overflow-x-hidden truncate">${artists}</p>
                <p class="text-xl text-gray-600 dark:text-gray-300 overflow-x-hidden truncate">${album}</p>
            </div><br><br>
            <div class="text-center">
                <span style="text-align: center;font-size:25px;" class=" text-gray-600 dark:text-gray-300"><i style="font-size:25px !important;" class="material-icons">shuffle</i> 
                <i style="font-size:25px !important;" class="material-icons">skip_previous</i>
                <span style="font-size:25px !important;" class=" text-black dark:text-white">${playing}</span>
                 <i style="font-size:25px !important;" class="material-icons">skip_next</i>
                <i style="font-size:25px !important;" class="material-icons">loop</i>
                <i onclick="openModal('lyricModal')" style="font-size:25px !important;" class="material-icons">lyrics</i>
                
                </span> <br>
                  <div class="flex justify-between mb-1">
                  <span class="text-sm font-medium text-blue-700 dark:text-white">${timestamp}</span>
                  <span class="text-sm font-medium text-blue-700 dark:text-white">${total}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700" style="text-align:left; width:240px;;">
                  <div class="bg-green-400 h-2.5 rounded-full" style="text-align:left; width:240px;;width: ${Math.round(
                ratio
            )}%;"></div>
                </div>
                </div>
            
</div>`;
            const request = $.ajax({
                type: 'GET',
                url: '/api/v1/internal/get_lyrics',
                data: {
                    artist: artists,
                    song: name
                }
            });
            request.done((data) => {
                //alert(data);
                document.getElementById('lyricshere').innerHTML = data;
            });
        }
    });
}

function sendRQ(link) {
    const request = $.ajax({
        type: 'POST',
        url: link
    });
    request.done((data) => {
        return data;
    });
}

setInterval(fetchStatus, 500);
