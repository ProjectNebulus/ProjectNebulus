let menu;
let rightClickElements = {};
let prevRightClickElements = {"format: string here": "function to run if clicked here"};

window.onload = function () {
    menu = document.getElementById("context-menu");
    document.documentElement.lang = "en";

    let details = document.getElementsByTagName("details");
    if (details.length > 0)
        document.addEventListener("click", function () {
            if (event.target !== details[0])
                details[0].open = false;
        });


    if (localStorage.getItem("color-theme") == null) {
        const darkTheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
        localStorage.setItem("color-theme", darkTheme ? "dark" : "light");
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
}