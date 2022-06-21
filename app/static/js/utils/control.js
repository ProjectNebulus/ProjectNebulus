const controlCenter = document.getElementById("control-center");
const focus = document.getElementById("focus");
const focusText = document.getElementById("focusText");

setInterval(() => {
    let original = localStorage.getItem("originalTimer");

    if (!original) {
        focus.classList.add("hidden");
        return;
    }
    original = original.split(" ");

    focus.classList.remove("hidden");
    const current = localStorage.getItem("currentTimer").split(" ");

    focusText.innerHTML = "Focusing on " + current[0]

}, 1000);

for (const div of controlCenter.querySelectorAll("div > div > div"))
    div.className += " bg-gray-300/30 dark:bg-gray-900/60 mx-2 text-left flex flex-col rounded-lg";

for (const icon of controlCenter.getElementsByTagName("i"))
    icon.className += " material-icons text-center text-sm text-white rounded-full bg-blue-600 w-5 h-5 mr-1";

for (const a of controlCenter.getElementsByTagName("a"))
    a.className += " text-gray-500 dark:text-gray-400 focus:outline-none hover:bg-blue-200 dark:hover:bg-blue-700 text-left text-sm rounded-lg p-2.5 w-36 cursor-pointer";