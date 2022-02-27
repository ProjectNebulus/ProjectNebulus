const loadingIcon = "<svg class=\"inline mr-2 w-4 h-4 text-gray-200 animate-spin dark:text-gray-600\" viewBox=\"0 0 100 101\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"> <path d=\"M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z\" fill=\"currentColor\"/> <path d=\"M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z\" fill=\"#1C64F2\"/> </svg>";

let rightClickElements = {};
let prevRightClickElements = {};
// string as key, function to run as value

window.onload = function () {
    document.documentElement.lang = "en";

    let details = document.getElementsByTagName("details");
    if (details.length > 0)
        document.addEventListener("click", function () {
            if (event.target !== details[0])
                details[0].open = false;
        });

    if (localStorage.getItem("color-theme") == null) {
        const darkTheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
        localStorage.setItem("color-theme", darkTheme ? "dark" : "light")
    }

    if (localStorage.getItem("color-theme") === "dark")
        document.body.style.background = "#111926";
    else
        document.body.style.background = "#EEEEEE";


    // On page load or when changing themes, best to add inline in `head` to avoid FOUC
    if (localStorage.getItem('color-theme') === 'dark' || !('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
        document.documentElement.classList.add('dark');
    else
        document.documentElement.classList.remove('dark')
}

document.onclick = () => menu.style.visibility = "hidden";

document.oncontextmenu = (e) => {
    menu.style.visibility = "hidden";

    if (rightClickElements == null)
        return;

    e.preventDefault();

    if (Object.keys(rightClickElements).length === 0)
        return;

    if (rightClickElements !== prevRightClickElements) {
        prevRightClickElements = rightClickElements;
        menu.innerHTML = "";

        const ul = document.createElement("ul");
        for (const [key, value] of Object.entries(rightClickElements)) {
            const li = document.createElement("li");
            li.innerHTML = key;
            li.onclick = rightClickElements[value];
            ul.appendChild(li);
        }

        menu.appendChild(ul);

        rightClickElements = {}
    }

    menu.style.visibility = "visible";
    menu.style.left = e.pageX + "px";
    menu.style.top = e.pageY + "px";
}

if ('serviceWorker' in navigator) {
    // we are checking here to see if the browser supports the service worker api
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
            // Registration was successful
            console.log('Service Worker registration was successful with scope: ', registration.scope);
        }, function(error) {
            console.log('ServiceWorker registration failed: ', error);
        });
    });
}
