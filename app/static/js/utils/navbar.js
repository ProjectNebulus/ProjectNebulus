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

    if (frame && frame.src.includes(siteName)) {
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

const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');

// Change the icons inside the button based on previous settings
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches))
    themeToggleLightIcon.classList.remove('hidden');
else
    themeToggleDarkIcon.classList.remove('hidden');

const themeToggleBtn = document.getElementById('theme-toggle');

themeToggleBtn.addEventListener('click', function () {
    // toggle icons inside button
    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    // if set via local storage previously
    if (localStorage.getItem('color-theme') === 'light')
        localStorage.setItem('color-theme', 'dark');
    else
        localStorage.setItem('color-theme', 'light');

    detectTheme();
    invertSite();
});

for (const a of document.getElementsByClassName("nav-link"))
    a.className += " block py-2 px-4 text-sm text-gray-700 dark:text-gray-200 dark:hover:text-white";

for (const a of document.getElementsByClassName("nav-link-2"))
    a.className += " block py-2 pr-4 pl-3 text-black bg-black-700 rounded md:bg-transparent md:text-black md:p-0 dark:text-white";

if (localStorage.getItem("color-theme") === "dark") {
    let daelements = document.getElementsByClassName("changeable-gradient");
    console.log(daelements);
    for (let element of daelements) {
        element.classList.remove("gradient-text");
        element.classList.add("gradient-text-dark");

    }
}
else {
    let gradient = document.getElementsByClassName("changeable-gradient");
    console.log(gradient);
    for (const element of gradient) {
        element.classList.remove("gradient-text-dark");
        element.classList.add("gradient-text");
    }
}
// setInterval(navFetchStatus, 500);

document.querySelector("#navbar [data-dropdown-toggle='control-center']").oncontextmenu = (e) => e.preventDefault();

const resize = () => document.getElementById("mobile-navbar-scroll").style.height = (window.innerHeight -
    document.getElementById("logo").getBoundingClientRect().height - 48) + "px";

window.addEventListener("load", resize)
window.addEventListener("resize", resize);
