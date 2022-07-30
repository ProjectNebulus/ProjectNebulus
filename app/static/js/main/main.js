const siteName = window.location.protocol + '//' + window.location.host;

const interval = setInterval(changeFavicon, 1000);
Array.prototype.insert = (index, item) => this.splice(index, 0, item);

window.addEventListener("beforeunload", () => clearInterval(interval));

if (!localStorage.getItem('color-theme')) {
    const darkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
    localStorage.setItem('color-theme', darkTheme ? 'dark' : 'light');
}

if (localStorage.getItem('color-theme') === 'dark') document.documentElement.classList.add('dark');
else document.documentElement.classList.remove('dark');

/** Returns a string containing a loading icon, with the parameters defining length and width. */
function loadingIcon(length, width, fill) {
    if (width === undefined) width = length;

    return `
    <div role="status">
        <svg class="inline mr-2 w-${length} h-${width} text-gray-200 animate-spin dark:text-gray-600 fill-${fill}" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
            <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
        </svg>
        <span class="sr-only">Loading...</span>
    </div>`;
}

function keyUpDelay(querySelector, duration, func) {
    new KeyUpTimer(querySelector, duration, func).enable();
}

/**
 * This class calls a function once an input's value has not been changed for a certain amount of time.
 * @param func The function to be called.
 * @param duration The duration in milliseconds of the input value not changing, before it calls the function.
 * @param querySelector The CSS selector to the element used.
 * */
class KeyUpTimer {
    constructor(querySelector, duration, func) {
        this.selector = querySelector;
        this.duration = duration;
        this.func = func;
        this.lastKeyUpTime = 0;
        this.recheck = false;
    }

    enable() {
        this.elements = document.querySelectorAll(this.selector);
        this.onKeyUp = (e) => {
            this.lastKeyUpTime = Date.now();
            this.recheck = true;
            this.lastKeyEvent = e;
        };

        for (const element of this.elements) element.addEventListener('keyup', this.onKeyUp);

        this.interval = setInterval(() => {
            if (!this.recheck) return;

            if (Date.now() - this.lastKeyUpTime > this.duration) {
                this.recheck = false;
                this.func(this.lastKeyEvent);
            }
        }, 100);
    }

    disable() {
        for (const element of this.elements)
            element.removeEventListener('keyup', this.onKeyUp);
        clearInterval(this.interval);
    }
}

function detectTheme() {
    if (!localStorage.getItem('color-theme')) {
        const darkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
        localStorage.setItem('color-theme', darkTheme ? 'dark' : 'light');
    }

    if (localStorage.getItem('color-theme') === 'dark')
        document.documentElement.classList.add('dark');
    else document.documentElement.classList.remove('dark');
}

function invertSite() {
    const banner = document.getElementById('homeBanner');

    if (localStorage.getItem('color-theme') === 'dark') {
        if (window.location.href.endsWith('/notepad')) document.getElementById('editor').style.filter = 'invert(1)';
        if (window.location.pathname === '/') {
            let wallpaper = localStorage.getItem('wallpaper');
            if (!wallpaper) wallpaper = '/static/images/darkwallpaper.png';

            document.body.style.background = `linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)) 0% 0% / cover, url("${wallpaper}") center center no-repeat fixed`;
            document.body.style.backgroundSize = 'cover';
            document.getElementById('chart').innerHTML = `
   
        <iframe style="background: rgba(0, 0,0 , 0.5); border-radius:10px;border: none; margin:10px; " width="80%" height="580" src="https://charts.mongodb.com/charts-project-0-dixeb/embed/charts?id=62c4eb23-6d77-4441-8174-0fc61c500111&maxDataAge=10&theme=dark&autoRefresh=true"></iframe>
   `;
        }
        if (banner) banner.style.filter = 'brightness(100%)';

        for (const logo of document.getElementsByTagName('logo'))
            if (!logo.getAttribute('no-revert'))
                logo.style.filter = 'brightness(100%)';
    } else {
        if (window.location.href.endsWith('/notepad')) {
            document.getElementById('editor').style.filter = 'invert(0)';
        }
        if (window.location.href.endsWith('/')) {
            let wallpaper = localStorage.getItem('wallpaper');
            if (wallpaper === null) {
                document.body.style.backgroundColor = 'white';
                document.body.style.backgroundImage = '';
            } else {
                document.body.style.background = `linear-gradient( rgba(256, 256, 256, 0.5), rgba(256, 256, 256, 0.2) ), url('${wallpaper}') no-repeat center center fixed`;
                document.body.style.backgroundSize = 'cover';
            }
            document.getElementById('chart').innerHTML = `<iframe style="background: rgba(255, 255, 255, 0.5); border-radius:10px;border: none; margin:10px; " width="80%" height="580" src="https://charts.mongodb.com/charts-project-0-dixeb/embed/charts?id=62c4eb23-6d77-4441-8174-0fc61c500111&maxDataAge=10&theme=lightk&autoRefresh=true"></iframe>;`
        }

        if (banner) banner.style.filter = 'brightness(70%)';

        for (const logo of document.getElementsByTagName('logo')) {
            if (logo.getAttribute('no-revert') === null) logo.style.filter = 'brightness(70%)';
        }
    }

    for (const frame of document.getElementsByTagName('iframe')) {
        if (frame && (frame.src.includes(siteName) || !frame.src.includes('http'))) {
            const innerDoc = frame.contentDocument || frame.contentWindow.document;

            if (document.documentElement.classList.contains('dark')) {
                innerDoc.documentElement.classList.add('dark');
                let wallpaper = localStorage.getItem('wallpaper');
                if (wallpaper === null) {
                    innerDoc.body.style.background = '#111926';
                } else {
                    document.body.style.backgroundSize = 'cover';
                    document.body.style.background = `linear-gradient( rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.2) ), url('${wallpaper}') no-repeat center center fixed`;
                    document.body.style.backgroundSize = 'cover';
                    for (let header of document.getElementsByClassName("modalheader")) {
                        header.style =
                            `background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.2)) 0% 0% / cover, url("${wallpaper}") ;
                    background-position: center top;
                    background-size: 100% auto;`
                    }

                }
            } else {
                innerDoc.documentElement.classList.remove('dark');
                let wallpaper = localStorage.getItem('wallpaper');
                if (wallpaper === null) {
                    innerDoc.body.style.background = 'white';
                } else {
                    document.body.style.backgroundSize = 'cover';
                    document.body.style.background = `linear-gradient( rgba(256, 256, 256, 0.5), rgba(256, 256, 256, 0.2) ), url('${wallpaper}') no-repeat center center fixed`;
                    document.body.style.backgroundSize = 'cover';
                    for (let header of document.getElementsByClassName("modalheader")) {
                        header.style =
                            `background: linear-gradient(rgba(256, 256, 256, 0.5), rgba(256, 256, 256, 0.2)) 0% 0% / cover, url("${wallpaper}") ;
                    background-position: center top;
                    background-size: 100% auto;`
                    }
                }
            }
        }
    }

    if (localStorage.getItem('color-theme') === 'dark') {
        let elements = document.getElementsByClassName('changeable-gradient');
        console.log(elements);
        for (let element of elements) {
            element.classList.remove('gradient-text');
            element.classList.add('gradient-text-dark');
        }
    } else {
        let elements = document.getElementsByClassName('changeable-gradient');
        console.log(elements);
        for (let element of elements) {
            element.classList.remove('gradient-text-dark');
            element.classList.add('gradient-text');
        }
    }
}

let isOnline = true;
window.addEventListener('load', function () {
    invertSite();

    isOnline = navigator.onLine;
    if (isOnline) online();
    else offline();

    window.addEventListener('online', online);
    window.addEventListener('offline', offline);

    for (const logo of document.getElementsByTagName('logo')) {
        let img;
        if (!logo.getAttribute('image')) img = '/static/images/nebulusCats/v3.gif';
        else img = logo.getAttribute('image');

        //if (!img.includes("/static/images/nebulusCats")) img += "/static/images/nebulusCats";

        let size = logo.getAttribute('size');

        if (size === null) {
            logo.style.width = size;
            logo.style.height = size;
        }
        logo.innerHTML =
            `<img alt="logo" style="` +
            logo.getAttribute('style') +
            '" class="' +
            logo.className +
            '" src="' +
            img +
            '">';

        logo.removeAttribute('style');
        logo.removeAttribute('class');
    }
});

let statusInterval = 0;
let shouldGetSpotify = true;
let requestAttempts = 0;

function onFailedRequest() {
    if (requestAttempts > 5) {
        if (isOnline) {
            isOnline = false;
            offline();
        }
    }

    requestAttempts++;
}

function online() {
    isOnline = true;
    requestAttempts = 0;
    if (shouldGetSpotify) statusInterval = setInterval(navFetchStatus, 1000);

    document.getElementById('wifi').innerHTML = 'wifi';
    document.getElementById('wifi').classList.add('bg-blue-600');
    document.getElementById('wifi').classList.remove('bg-red-600');
}

function offline() {
    isOnline = false;
    if (shouldGetSpotify) clearInterval(statusInterval);

    document.getElementById('wifi').innerHTML = 'wifi_off';
    document.getElementById('wifi').classList.remove('bg-blue-600');
    document.getElementById('wifi').classList.add('bg-red-600');
}

function navFetchStatus() {
    if (!document.getElementById('spotifyStatus')) return;

    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/spotify-status'
    });

    request.done((data) => {
        if (parseInt(data)) {
            document.getElementById('spotifyStatus').innerHTML = '';
            shouldGetSpotify = false;
            clearInterval(statusInterval);
            return;
        }

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

        document.getElementById('spotifyStatus').innerHTML = `
            <div style="width:150px;float:left;">
                <img style="display: inline-block; margin:20px; border-radius:10px;" class="mb-3 w-20 h-20 shadow-lg" src="${image}" alt="Song Title">
            </div>
            <div style="width: calc(90% - 150px);float:left;">
                <div style="margin-top:20px;">
                <p class="truncate text-lg text-black dark:text-white"><i style="display:inline-block; color:#1BD661; margin-right:10px;" class="fab fa-spotify"></i> ${name} ${explicit} </p>
                    <p class="truncate text-sm text-gray-600 dark:text-gray-300">${artists} - ${album}</p></div>
                <div class="w-full bg-gray-200 rounded-full dark:bg-gray-700 h-1">
                    <div class="bg-white text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full h-1" style="width: ${Math.round(
            ratio
        )}%"> </div>
                </div>
                <p class="truncate text-sm text-gray-600 dark:text-gray-300">${timestamp} of ${total}
                    ${playing}
                    <i style="margin-left:20px;color:white;" class="material-icons">skip_next</i>
                </p></div>`;
        document.getElementById('spotifyStatus').classList.remove("flex-col");
        //document.getElementById('spotifyStatus').classList.remove("flex");
    });

    request.fail(onFailedRequest);
}

const list = ['Red', 'Blue', 'Green', 'Blurple', 'Pink', 'Jade', 'Yellow'];

let index = 0;

for (let i = 0; i < list.length; i++) {
    fetch(`/static/images/nebulusCats/new${list[i]}.png`)
        .then(response => response.blob())
        .then(imageBlob => list[i] = URL.createObjectURL(imageBlob));
}

function changeFavicon() {
    let link = document.querySelector("link[rel~='icon']");
    index = (index + 1) % list.length;
    link.href = list[index];
}

function openModal(object_id) {
    let targetEl = document.getElementById(object_id);
    const options = {
        placement: 'bottom-right',
        backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40'
    };
    const modal = new Modal(targetEl);
    modal.show();
    return true;
}

function closeModal(object_id) {
    let targetEl = document.getElementById(object_id);
    const options = {
        placement: 'bottom-right',
        backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40'
    };
    const modal = new Modal(targetEl, options);
    modal.hide();
    let elements = document.querySelectorAll('[modal-backdrop]');
    for (let i = 0; i < elements.length; i++) {
        elements[i].style.display = 'none';
    }
    return true;
}
