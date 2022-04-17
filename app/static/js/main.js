const siteName = window.location.protocol + "//" + window.location.host;

let rightClickElements = null;
let prevRightClickElements = null;

// string as key, function to run as value

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
        if (window.location.href.endsWith("/"))
            document.body.style.backgroundImage = "url(\"/static/images/darkwallpaper.png\")";

        if (banner) banner.style.filter = "invert(0)";

        for (const logo of document.getElementsByTagName("logo")) {
            if (!logo.getAttribute("no-revert"))
                logo.style.filter = "invert(0)";
        }
    } else {
        if (window.location.href.endsWith("/"))
            document.body.style.backgroundImage = "url(\"/static/images/lightwallpaper.png\")";

        if (banner) banner.style.filter = "invert(1)";

        for (const logo of document.getElementsByTagName("logo")) {
            if (logo.getAttribute("no-revert") === null)
                logo.style.filter = "invert(1)";
        }
    }

    if (window.location.href.includes("course")) {
        const frame = document.getElementById("frame");
        const innerDoc = frame.contentDocument || frame.contentWindow.document;

        if (document.documentElement.classList.contains("dark")) {
            innerDoc.documentElement.classList.add("dark");
            innerDoc.body.style.background = "#111926";
        } else {
            innerDoc.documentElement.classList.remove("dark");
            innerDoc.body.style.background = "white";
        }
    }
}

window.addEventListener("load", function () {
    invertSite();

    if (navigator.onLine)
        online();
    else
        offline();

    window.addEventListener("online", online);
    window.addEventListener("offline", offline);

    for (const logo of document.getElementsByTagName("logo")) {
        let img = logo.getAttribute("image");
        if (img === null)
            img = "cat1.png";

        let size = logo.getAttribute("size");

        if (size === null)
            size = "2rem";

        logo.style.width = size;
        logo.style.height = size;
        logo.classList.add("inline-block", "mx-3", "my-3");

        logo.innerHTML = '<img alt="logo" style="' + logo.getAttribute("style") + '" class="' + logo.className + '" src="/static/images/nebulusCats/' + img + '">';

        logo.removeAttribute("style");
        logo.removeAttribute("class");
    }
});

document.onclick = () => (menu.style.visibility = 'hidden');

document.oncontextmenu = (e) => {
    menu.style.visibility = 'hidden';

    if (rightClickElements === null) return;

    e.preventDefault();

    if (Object.keys(rightClickElements).length === 0) return;

    if (rightClickElements !== prevRightClickElements) {
        prevRightClickElements = rightClickElements;
        menu.innerHTML = '';

        const ul = document.createElement('ul');
        for (const [key, value] of Object.entries(rightClickElements)) {
            const li = document.createElement('li');
            li.innerHTML = key;
            li.onclick = rightClickElements[value];
            ul.appendChild(li);
        }

        menu.appendChild(ul);

        rightClickElements = {};
    }

    menu.style.visibility = 'visible';
    menu.style.left = e.pageX + 'px';
    menu.style.top = e.pageY + 'px';
};

if ('serviceWorker' in navigator) {
    // we are checking here to see if the browser supports the service worker api
    window.addEventListener('load', function () {
        navigator.serviceWorker.register('/static/js/sw.js').then(
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

function online() {

}

function offline() {

}