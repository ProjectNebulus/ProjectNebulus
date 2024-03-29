const siteName = window.location.protocol + '//' + window.location.host;
const startLoad = Date.now();
let loadTime;
let screenTime;

const modals = new Set();


window.addEventListener("unload", function (e) {
    for (const blob of list)
        URL.revokeObjectURL(blob);

    screenTime = Date.now() - startLoad;
    $.ajax({
        url: '/screenTime',
        type: 'GET',
        contentType: 'application/json',
        data: {
            "data": screenTime,
            "location": window.location.pathname,
        }
    })
});


if (localStorage.getItem("customCursor") !== null && !window.location.search.includes("iframe=true")) {
    document.documentElement.classList.add("custom-cursor");

    $(document).ready(function () {
        $(document).on('mousemove', function (e) {
            $('#customCursor').css({
                left: e.pageX - 20,
                top: e.pageY - 20,
                display: "block"
            });
        })
    });

    $("a").on("mouseover", function () {
        $('#customCursor').css({
            borderWidth: 4,
            borderColor: "black",
        });
    });

    $("button").on("mouseover", function () {
        $('#customCursor').css({
            borderWidth: 4,
            borderColor: "black",
        });
    });
    $("a").on("mouseout", function () {
        $('#customCursor').css({
            borderWidth: 1,
            borderColor: "#4B5563",
        });
    });

    $("button").on("mouseout", function () {
        $('#customCursor').css({
            borderWidth: 1,
            borderColor: "#4B5563",
        });
    });
}


window.addEventListener('load', () => {
    loadTime = Date.now() - startLoad;
    console.log(loadTime);

    for (const el in document.querySelectorAll("[data-modal-toggle]"))
        try {
            modals.add(el.getAttribute("data-modal-toggle"));
        } catch {
        }
});


document.addEventListener("keydown", e => {
    if ((e.ctrlKey || e.metaKey) && e.key === "k") {
        if (document.getElementById('searchModal').classList.contains("hidden")) openModal('searchModal');
        else closeModal('searchModal');
    }

    if (e.key === "Escape") {
        for (const modal of modals)
            closeModal(modal);
    }
});


setInterval(changeFavicon, 3000);
Array.prototype.insert = (index, item) => this.splice(index, 0, item);

if (!localStorage.getItem('color-theme')) {
    const darkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
    localStorage.setItem('color-theme', darkTheme ? 'dark' : 'light');
}

if (localStorage.getItem('color-theme') === 'dark') document.documentElement.classList.add('dark');
else document.documentElement.classList.remove('dark');

/** Returns a string containing a loading icon, with the parameters defining length and width. */
function loadingIcon(length, width, fill) {
    if (width === undefined) width = length;
    if (fill === undefined) fill = 'blue-600';

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
        if (this.elements.length === 0)
            console.error("WARNING: KeyUpTime query selector does not match any elements.");

        this.onKeyUp = e => {
            if (e.key && e.key.length > 1 && e.key !== "Enter" && e.key !== "Backspace")
                return;

            this.lastKeyUpTime = Date.now();
            this.recheck = true;
            this.lastKeyEvent = e;
        };

        this.onClick = el => {
            if (Date.now() - this.lastKeyUpTime >= 2000 && el.value && el === document.activeElement)
                this.func(el);

            this.lastKeyUpTime = Date.now();
        }

        for (const element of this.elements) {
            element.addEventListener('keyup', this.onKeyUp);
            element.addEventListener('click', () => this.onClick(element));
        }

        this.interval = setInterval(() => {
            if (!this.recheck) return;

            if (Date.now() - this.lastKeyUpTime > this.duration) {
                this.recheck = false;
                this.func(this.lastKeyEvent);
            }
        }, 100);
    }

    disable() {
        for (const element of this.elements) element.removeEventListener('keyup', this.onKeyUp);
        clearInterval(this.interval);
    }
}

function toggleTheme() {
    if (!localStorage.getItem('color-theme')) {
        const darkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;
        localStorage.setItem('color-theme', darkTheme ? 'dark' : 'light');
    }

    if (localStorage.getItem('color-theme') === 'dark')
        document.documentElement.classList.add('dark');
    else document.documentElement.classList.remove('dark');
}

document.addEventListener("DOMContentLoaded", () => {
    let wallpaper = localStorage.getItem("wallpaper");
    // choose random wallpaper if `/signin` or `/signup`
    if (wallpaper === null && (window.location.pathname === "/signin" || window.location.pathname === "/signup")) {
        let wallpapers = [
            "/static/images/wallpaper/northernLights1.jpeg",
            "/static/images/wallpaper/craterlake2.jpeg",
            "/static/images/wallpaper/northernLights3.jpeg",
            "/static/images/wallpaper/jtree.jpeg",
            "/static/images/wallpaper/olympic1.jpeg",
            "/static/images/wallpaper/deathValley.jpeg",
            "/static/images/wallpaper/grandCanyon.jpeg",
            "/static/images/wallpaper/shanghai1.jpeg",
            "/static/images/wallpaper/costaRica.jpeg"
        ]
        wallpaper = wallpapers[Math.floor(Math.random() * wallpapers.length)];
    }
    if (window.location.search.includes("iframe=true")) document.body.style.background = "transparent";
    else if (wallpaper && !(window.location.pathname === "/")) {
        const brightness = document.documentElement.classList.contains("dark") ? 0 : 255;
        document.body.style.background = `linear-gradient( rgba(${brightness}, ${brightness}, ${brightness}, 0.6), rgba(${brightness}, ${brightness}, ${brightness}, 0.6) ), url('${wallpaper}') no-repeat center center fixed`;
        document.body.style.backgroundSize = 'cover';
    }

    for (const el of document.querySelectorAll("input.textarea-styling"))
        el.classList.add('bg-gray-50/75', 'border', 'border-gray-300', 'text-gray-900', 'text-sm', 'rounded-lg', 'focus:ring-blue-500', 'focus:border-blue-500', 'block', 'dark:bg-gray-800/50', 'dark:border-gray-600', 'dark:focus:border-blue-500', 'dark:placeholder-gray-400', 'dark:text-white', 'w-full', 'pl-10', 'p-2.5', 'dark:focus:ring-blue-500')

    for (const el of document.getElementsByClassName("button-styling"))
        el.classList.add('absolute', 'p-1', 'material-icons', 'top-0', 'right-0', 'hover:bg-gray-200', 'dark:hover:bg-gray-600', 'rounded-lg', 'cursor-pointer', 'text-gray-400', 'dark:text-gray-500')
});

function invertSite() {
    if (window.location.search.includes("iframe=true"))
        return;

    const banner = document.getElementById('homeBanner');

    if (localStorage.getItem('color-theme') === 'dark') {
        if (banner) banner.style.filter = 'brightness(100%)';
        if (window.location.pathname === "/") {
            document.getElementById("homeBanner").style.background = `linear-gradient(45deg, rgba(0, 0,0, 0.5), rgba(0, 0, 0, 0.5)), url('/static/images/nebulusCats/IMG_1134.png')`;
            document.getElementById("homeBanner").style.backgroundSize = "cover";
        }
        for (const logo of document.getElementsByTagName('logo'))
            if (!logo.getAttribute('no-revert'))
                logo.style.filter = 'brightness(100%)';
    } else {
        if (banner) banner.style.filter = 'brightness(70%)';
        if (window.location.pathname === "/") {
            document.getElementById("homeBanner").style.background = `linear-gradient(45deg, rgba(0, 0,0, 0.5), rgba(0, 0, 0, 0.5)), url('/static/images/nebulusCats/IMG_1131.png')`;
            document.getElementById("homeBanner").style.backgroundSize = "cover";
        }
        for (const logo of document.getElementsByTagName('logo')) {
            if (logo.getAttribute('no-revert') === null) logo.style.filter = 'brightness(70%)';
        }
    }

    for (const frame of document.getElementsByTagName('iframe')) {
        if (frame && (frame.src.includes(siteName) || !frame.src.includes('http'))) {
            const innerDoc = frame.contentDocument || frame.contentWindow.document;
            innerDoc.addEventListener('click', () => window.dispatchEvent(new Event('click')));
        }
    }

    if (localStorage.getItem('color-theme') === 'dark') {
        let elements = document.getElementsByClassName('changeable-gradient');
        for (let element of elements) {
            element.classList.remove('gradient-text');
            element.classList.add('gradient-text-dark');
        }
    } else {
        let elements = document.getElementsByClassName('changeable-gradient');
        for (let element of elements) {
            element.classList.remove('gradient-text-dark');
            element.classList.add('gradient-text');
        }
    }
    const wallpaper = localStorage.getItem("wallpaper");
    if (window.location.search.includes("iframe=true")) document.body.style.background = "transparent";
    else if (wallpaper && !(window.location.pathname === "/")) {
        const brightness = document.documentElement.classList.contains("dark") ? 0 : 255;
        document.body.style.background = `linear-gradient( rgba(${brightness}, ${brightness}, ${brightness}, 0.6), rgba(${brightness}, ${brightness}, ${brightness}, 0.6) ), url('${wallpaper}') no-repeat center center fixed`;
        document.body.style.backgroundSize = 'cover';
    }
}

function copy(el, text) {
    el.disabled = true;

    navigator.clipboard.writeText(text).then(
        () => {
            el.style.color = "#00AA00";
            el.innerHTML = "done";
            el.disabled = false;

            setTimeout(() => {
                el.innerHTML = "content_copy";
                el.style.color = "";
            }, 2000);
        },
        () => {
            el.style.color = "#FF7777";
            el.innerHTML = "error";
            el.disabled = false;

            setTimeout(() => {
                el.innerHTML = "content_copy";
                el.style.color = "";
            }, 2000);
        }
    );
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

        let size = logo.getAttribute('size');

        if (size === null) {
            logo.style.width = size;
            logo.style.height = size;
        }
        logo.innerHTML = `<img alt="logo" style="${logo.getAttribute('style')}" class="${
            logo.className
        }" src="${img}">`;

        logo.removeAttribute('style');
        logo.removeAttribute('class');
    }
});

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
    shouldGetSpotify = true;
    navFetchStatus();

    document.getElementById('wifi').innerHTML = 'wifi';
    document.getElementById('wifi').classList.add('bg-blue-600');
    document.getElementById('wifi').classList.remove('bg-red-600');
}

function offline() {
    isOnline = false;
    shouldGetSpotify = false;

    document.getElementById('wifi').innerHTML = 'wifi_off';
    document.getElementById('wifi').classList.remove('bg-blue-600');
    document.getElementById('wifi').classList.add('bg-red-600');
}

function navFetchStatus() {
    if (!document.getElementById('spotifyStatus')) return;

    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/get/spotify'
    });

    request.done((data) => {
        if (data === "2") {
            document.getElementById('spotifyStatus').style.display = 'none';
            shouldGetSpotify = false;
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
        document.getElementById('spotifyStatus').style.display = 'block';
        document.getElementById('spotifyStatus').innerHTML = `
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <div style="width:110px;vertical-align: middle; display:inline-block;">
                <img style="display: inline-block; margin:20px; border-radius:10px;" class="mb-3 w-20 h-20 shadow-lg" src="${image}" alt="Song Title">
            </div>
            <div style="width: calc(90% - 110px);vertical-align: middle;display:inline-block;">
                <div style="margin-top:20px;">
                <p class="truncate text-lg text-black"><i class="fa fa-spotify" style="display:inline-block; color:#1DB954;margin-right:10px;"></i> ${name} ${explicit} </p>
                    <p class="truncate text-sm text-gray-600">${artists} - ${album}</p></div>
               
                
                <div class="w-full bg-gray-200 rounded-full dark:bg-gray-700 h-3" style="
    margin: 10px;
">
                    <div class="text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full h-3" style="width: ${Math.round(
            ratio
        )}%;background: linear-gradient(45deg, green, orange);"> </div>
                </div>
                <p class="truncate text-sm text-gray-600">${timestamp} of ${total}
                    ${playing}
                    <i style="margin-left:20px;color:white;" class="material-icons">skip_next</i>
                </p></div>`;

        navFetchStatus();
    });

    request.fail(onFailedRequest);
}


const list = ['Red', 'Blue', 'Green', 'Blurple', 'Pink', 'Jade', 'Yellow'];
let v3Image;

let index = 0;

for (let i = 0; i < list.length; i++) {
    fetch(`/static/images/nebulusCats/new${list[i]}.png`)
        .then((response) => response.blob())
        .then((imageBlob) => (list[i] = URL.createObjectURL(imageBlob)));
}


fetch(`/static/images/nebulusCats/v3.gif`)
    .then((response) => response.blob())
    .then((imageBlob) => (v3Image = URL.createObjectURL(imageBlob)));


function changeFavicon() {
    let link = document.querySelector("link[rel*='icon']");
    index = (index + 1) % list.length;
    link.href = list[index];
}


function openModal(object_id) {
    let targetEl = document.getElementById(object_id);

    if (!targetEl.classList.contains("hidden")) return;
    targetEl.classList.add("pointer-events-none");
    targetEl.children[0].classList.add("pointer-events-auto");

    for (const el of document.querySelectorAll("#" + object_id + " [step]"))
        el.classList.add("hidden");

    const step1 = document.querySelector("#" + object_id + " [step='1']")
    if (step1)
        step1.classList.remove("hidden");

    modals.add(object_id);

    const modal = new Modal(targetEl);
    modal.show();

    document.querySelector("[modal-backdrop]").addEventListener("click", () => closeModal(object_id));

    targetEl.style.scale = "75%";
    targetEl.style.opacity = "50%";
    targetEl.style.transition = "0.2s";

    if (object_id === "searchModal")
        document.getElementById("search_input").focus();

    setTimeout(function () {
        targetEl.style.scale = "100%";
        targetEl.style.opacity = "100%";
    }, 25)
}


function closeModal(object_id) {
    let targetEl = document.getElementById(object_id);
    targetEl.style.scale = "0";
    targetEl.style.opacity = "50%";
    targetEl.style.transition = "0.2s";

    for (const el of document.querySelectorAll("[modal-backdrop]")) {
        el.style.transition = "0.2s";
        el.style.opacity = "0";
    }

    setTimeout(() => {
        const modal = new Modal(targetEl);
        modal.hide();

        for (const el of document.querySelectorAll('[modal-backdrop]'))
            el.remove();
    }, 200);
}

function bindFunc(query, func) {
    let valid = false;
    for (let el of document.querySelectorAll(query)) {
        el.addEventListener("click", () => func(el));
        valid = true;
    }

    if (!valid)
        console.warn("Query " + query + " did not match any elements");
}

function randomCat() {
    return list[Math.floor(Math.random() * list.length)];
}

function linkProxy(onChange) {
    return new Proxy(location, {
        set: (target, p, value, receiver) => {
            console.log(target, p, value, receiver);
            if (p === "pathname")
                onChange(value);

            return Reflect.set(target, p, value, receiver);
        }
    });
}
