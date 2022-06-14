const siteName = window.location.protocol + "//" + window.location.host;

Array.prototype.insert = (index, item) => this.splice(index, 0, item);

/** Returns a string containing a loading icon, with the parameters defining length and width. */
function loadingIcon(length, width) {
    if (width === undefined)
        width = length;

    return `<!-- By Sam Herbert (@sherb), for everyone. More @ https://goo.gl/7AJzbL -->
    <svg width="38" height="38" viewBox="0 0 38 38" xmlns="http://www.w3.org/2000/svg" stroke="#fff" style="width: ${length}; height: ${width}; display: inline">
        <g fill="none" fill-rule="evenodd">
            <g transform="translate(1 1)" stroke-width="2">
                <circle stroke-opacity=".5" cx="18" cy="18" r="18"/>
                <path d="M36 18c0-9.94-8.06-18-18-18">
                    <animateTransform
                        attributeName="transform"
                        type="rotate"
                        from="0 18 18"
                        to="360 18 18"
                        dur="1s"
                        repeatCount="indefinite"/>
                </path>
            </g>
        </g>
    </svg>`;
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
        }

        for (const element of this.elements)
            element.addEventListener("keyup", this.onKeyUp)

        this.interval = setInterval(() => {
            if (!this.recheck)
                return;

            if (Date.now() - this.lastKeyUpTime > this.duration) {
                this.recheck = false;
                this.func(this.lastKeyEvent);
            }
        }, 100);
    }

    disable() {
        for (const element of this.elements)
            element.removeEventListener("keyup", this.onKeyUp)

        clearInterval(this.interval);
    }
}

if ('serviceWorker' in navigator) {
    // we are checking here to see if the browser supports the service worker api
    window.addEventListener('load', async function () {
        await navigator.serviceWorker.register(/*'../static/js/sw.js'*/ '../sw.js', {scope: "/"}).then(
            function (registration) {
                // Registration was successful
                console.log(
                    'Service Worker registration was successful with scope: ',
                    registration.scope
                );
            },
            function (error) {
                console.log('ServiceWorker registration failed: ', error);
            }
        );
    });
}

function detectTheme() {
    if (!localStorage.getItem('color-theme')) {
        const darkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
        localStorage.setItem('color-theme', darkTheme ? 'dark' : 'light');
    }

    if (localStorage.getItem("color-theme") === "dark")
        document.documentElement.classList.add('dark');
    else
        document.documentElement.classList.remove('dark');
}

function invertSite() {
    const banner = document.getElementById("homeBanner");

    if (localStorage.getItem("color-theme") === "dark") {
        if (window.location.href.endsWith("/notepad")) {
            document.getElementById("editor").style.filter = "invert(1)";
        }
        if (window.location.pathname === "/") {
            //document.body.style.backgroundImage = "url(\"/static/images/darkwallpaper.png\")";
            document.body.style.backgroundSize = "cover";
            document.body.style.background = "linear-gradient( rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.2) ), url('/static/images/darkwallpaper.png') no-repeat center center fixed";
            //document.body.style.backgroundImage = "url(\"/static/images/darkwallpaper.png\")";
            document.body.style.backgroundSize = "cover";

        }
        if (banner) banner.style.filter = "brightness(100%)";

        for (const logo of document.getElementsByTagName("logo")) {
            if (!logo.getAttribute("no-revert"))
                logo.style.filter = "brightness(100%)";
        }
    }
    else {
        if (window.location.href.endsWith("/notepad")) {
            document.getElementById("editor").style.filter = "invert(0)";
        }
        if (window.location.href.endsWith("/")) {
            document.body.style.backgroundColor = "white";
            document.body.style.backgroundImage = "";
        }


        if (banner) banner.style.filter = "brightness(70%)";

        for (const logo of document.getElementsByTagName("logo")) {
            if (logo.getAttribute("no-revert") === null)
                logo.style.filter = "brightness(70%)";
        }
    }

    const frame = document.getElementsByTagName("iframe")[0];

    if (frame && (frame.src.includes(siteName) || !frame.src.includes("http"))) {
        const innerDoc = frame.contentDocument || frame.contentWindow.document;

        if (document.documentElement.classList.contains("dark")) {
            innerDoc.documentElement.classList.add("dark");
            innerDoc.body.style.background = "#111926";
        }
        else {
            innerDoc.documentElement.classList.remove("dark");
            innerDoc.body.style.background = "white";
        }
    }

    if (localStorage.getItem("color-theme") === "dark") {
        let elements = document.getElementsByClassName("changeable-gradient");
        console.log(elements);
        for (let element of elements) {
            element.classList.remove("gradient-text");
            element.classList.add("gradient-text-dark");
        }
    }
    else {
        let elements = document.getElementsByClassName("changeable-gradient");
        console.log(elements);
        for (let element of elements) {
            element.classList.remove("gradient-text-dark");
            element.classList.add("gradient-text");
        }
    }
}

let isOnline = true;
window.addEventListener("load", function () {
    invertSite();

    isOnline = navigator.onLine;
    if (isOnline)
        online();
    else
        offline();

    window.addEventListener("online", online);
    window.addEventListener("offline", offline);

    for (const logo of document.getElementsByTagName("logo")) {
        let img = "/static/images/nebulusCats" + logo.getAttribute("image");
        if ( logo.getAttribute("image") === null)
            img = "/static/images/nebulusCats/v3.gif";

        let size = logo.getAttribute("size");

        if (size === null) {
            logo.style.width = size;
            logo.style.height = size;
        }
        logo.innerHTML = `<img alt="logo" style="` + logo.getAttribute("style") + '" class="' + logo.className + '" src="' + img + '">';

        logo.removeAttribute("style");
        logo.removeAttribute("class");
    }
});

if ('serviceWorker' in navigator) {
    // we are checking here to see if the browser supports the service worker api
    window.addEventListener('load', async function () {
        await navigator.serviceWorker.register(/*'../static/js/sw.js'*/ '../sw.js?2', {scope: "/"}).then(
            function (registration) {
                // Registration was successful
                console.log(
                    'Service Worker registration was successful with scope: ',
                    registration.scope
                );
            },
            function (error) {
                console.log('ServiceWorker registration failed: ', error);
            }
        );
    });
}

let interval = 0;
let shouldGetSpotify = true;
let shouldGetFocus = true;
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
    if (shouldGetSpotify)
        interval = setInterval(navFetchStatus, 1000);

}

function offline() {
    isOnline = false;
    if (shouldGetSpotify)
        clearInterval(interval);
}

setInterval(navFetchFocus, 1000);
function navFetchStatus() {
    if (!document.getElementById("songhere"))
        return;

    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/spotify-status',
    });

    request.done((data) => {
        if (parseInt(data)) {
            document.getElementById("songhere").innerHTML = "";
            shouldGetSpotify = false;
            clearInterval(interval);
            return;
        }

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

        document.getElementById("songhere").innerHTML = `
            <div style="width:150px;float:left;">
                <img style="display: inline-block; margin:20px; border-radius:10px;" class="mb-3 w-20 h-20 shadow-lg" src="${image}" alt="Song Title">
            </div>
            <div style="width: calc(100% - 150px);float:left;">
                <div style="margin-top:20px;">
                <p class="truncate text-lg text-black dark:text-white"><i style="display:inline-block; color:#1BD661; margin-right:10px;" class="fab fa-spotify"></i> ${name} ${explicit} </p>
                    <p class="truncate text-sm text-gray-600 dark:text-gray-300">${artists} - ${album}</p></div>
                <div class="w-full bg-gray-200 rounded-full dark:bg-gray-700 h-1">
                    <div class="bg-white text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full h-1" style="width: ${Math.round(ratio)}%"> </div>
                </div>
                <p class="truncate text-sm text-gray-600 dark:text-gray-300">${timestamp} of ${total}
                    ${playing}
                    <i style="margin-left:20px;color:white;" class="material-icons">skip_next</i>
                </p></div>`;
    });

    request.fail(onFailedRequest);
}
function navFetchFocus() {
    const focus = localStorage.getItem('focus');
    if (focus === "idling" || focus === null){
        localStorage.setItem("focus", "idling");
        document.getElementById("bigFocus").style.visibility = "hidden";
    }else{
        document.getElementById("bigFocus").style.visibility = "visible";
        document.getElementById("focus").innerText = focus;
    }
}

function changeFavicon(){
    const list = [
        "Red",
        "Blue",
        "Green",
        "Blurple",
        "Pink",
        "Jade",
        "Yellow"
    ]
    for (let i = 0; i<list.length; i++){
        list[i] = `${window.location.origin}/static/images/nebulusCats/new${list[i]}.png`
    }

    var link = document.querySelector("link[rel~='icon']");

    //var old = link.href.pathname;
    var old = link.href;
    if (!link) {
        link = document.createElement('link');
        link.rel = 'icon';
        document.getElementsByTagName('head')[0].appendChild(link);
    }
    //let index =(list.findIndex(old) + 1) % list.length;
    let index = (list.indexOf(old) + 1) % list.length;

    link.href = list[index];
}

setInterval(changeFavicon, 250)