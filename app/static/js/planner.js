let exitTime;
let loadingModal;

window.addEventListener("load", () => {
    addTimePeriod();
    addTimePeriod();
    loadingModal = new Modal(document.getElementById("loading"));
    loadingModal.show();
    document.querySelector("#loading p").innerHTML += loadingIcon(30);
    exitTime = Date.now() + 300;
});

const times = document.getElementById("timePeriods");

let d, month, year, page, startDate;

const nextPage = document.getElementById("nextpage");
const today = document.getElementById("today");
const prevPage = document.getElementById("prevpage");

const saveState = document.getElementById("savestate");
const error = document.getElementById("error");
const plannerName = document.getElementById("planner_name");

const oneWeek = 1000 * 60 * 60 * 24 * 7;

function updateDate() {
    d = new Date();
    month = d.getMonth();
    year = d.getFullYear();
    page = Math.floor(Date.now() / oneWeek);

    startDate = d.getDate() - d.getDay();
}

updateDate();

const weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const daysInMonths = [31, d.getFullYear() % 4 === 0 ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

const table = document.getElementsByTagName("table")[0];

let saveData = {};

keyUpDelay("table", 500, saveToServer);
keyUpDelay("#planner_name", 500, saveToServer);

document.addEventListener("keyup", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.shiftKey) {
        if (e.key === "ArrowLeft")
            prevPage.click();
        else if (e.key === "ArrowRight")
            nextPage.click();
        else if (e.key === "ArrowUp")
            today.click();
    }
});

loadFromServer();

nextPage.onclick = function () {
    save()

    page++;
    load(page);

    nextPage.disabled = year >= 2030 && month === 11 && startDate >= daysInMonths[month] - 7;
    prevPage.disabled = false;

    startDate += 7;
    if (startDate > daysInMonths[month]) {
        startDate -= daysInMonths[month]
        month++;

        if (month > 11) {
            month = 0;
            year++;
        }
    }

    changeDate();
}

prevPage.onclick = function () {
    save();

    page--;
    load(page);

    prevPage.disabled = year <= 1970 && month === 0 && startDate <= 7;
    nextPage.disabled = false;

    startDate -= 7;
    if (startDate < 0) {
        month--;

        if (month < 0) {
            year--;
            month = 11;
        }

        startDate += daysInMonths[month];
    }

    changeDate();
}

today.onclick = function () {
    page = Math.floor(Date.now() / oneWeek);
    load(page);
    startDate = d.getDate() - d.getDay();
    year = d.getFullYear();
    month = d.getMonth();
    changeDate();
    nextPage.disabled = false;
    prevPage.disabled = false;
}

document.getElementById("month").innerHTML = months[month] + " " + d.getFullYear();

const daysRow = table.insertRow();
for (let i = 0; i < 7; i++)
    daysRow.insertCell();

changeDate();

for (let i = 1; i <= 8; i++) {
    const row = table.insertRow();
    const smallCell = row.insertCell();

    let textarea = document.createElement("textarea");
    textarea.innerHTML = i + "";
    textarea.style.fontsize = "1.5rem";
    smallCell.appendChild(textarea);

    for (let j = 0; j < 6; j++) {
        const cell = row.insertCell();

        textarea = document.createElement("textarea");
        textarea.className = "note";
        //textarea.placeholder = "_".repeat(105);
        cell.appendChild(textarea);
    }
}

function addTimePeriod() {
    let data = `
            <div class="flex w-full mb-4">
                <span onclick="addTimePeriod()" class="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border
                border-r-0 border-gray-300 rounded-l-md dark:bg-gray-500 dark:text-gray-400 dark:border-gray-600">+</span>
                <input type="text" class="rounded-none rounded-r-lg bg-gray-50 border border-gray-300 text-gray-900
                focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5 dark:bg-gray-700
                dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
            </div>
            `;
    times.innerHTML += data;
    times.scrollTo(0, times.scrollHeight)
}

function changeDate() {
    document.getElementById("month").innerHTML = months[month] + " " + year;

    let day;
    for (let i = 1; i < 7; i++) {
        day = startDate + i;
        if (day > daysInMonths[month])
            day -= daysInMonths[month];

        table.rows[0].cells[i].innerHTML = day.toString() + " " + weekDays[i - 1];
    }

    day = startDate + 7;
    if (day > daysInMonths[month])
        day -= daysInMonths[month];
    table.rows[0].cells[6].innerHTML += "/" + day.toString() + " Sunday";
}

function save(e) {
    if (e) {
        const code = String.fromCharCode(e.keyCode);

        if (!(/[a-zA-Z0-9-_ ]/.test(code) && code === code.toUpperCase()))
            return;
    }

    const notes = document.getElementsByClassName("note");
    saveData[page] = {};
    for (let i = 0; i < notes.length; i++) {
        if (notes[i].value !== "")
            saveData[page][i] = notes[i].value.replaceAll("=", ":::::");
    }
}

function load(page) {
    const notes = document.getElementsByClassName("note");
    for (let i in notes) {
        if (saveData[page] && saveData[page][i])
            notes[i].value = saveData[page][i].replaceAll(":::::", "=");
        else
            notes[i].value = "";
    }
}

function fadeOut(func) {
    setTimeout(() => {
            document.getElementById("loading").classList.add("fade-out");
            document.querySelector("[modal-backdrop]").classList.add("fade-out");
            setTimeout(func, 500);
        },
        Math.max(0, exitTime - Date.now()) + 1000
    );
}

function loadFromServer() {
    const request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/planner/load"
    });

    request.done(data => {
        fadeOut(() => loadingModal.hide());

        if (Object.keys(data).length === 0) {
            setTimeout(() => {
                loadingModal.hide();
                setTimeout(() => document.getElementById("openModal").click(), 200);
            }, Math.max(0, exitTime - Date.now()) + 1000);
            return;
        }

        document.getElementById("planner_name").value = data["name"];

        saveData = data["saveData"];

        for (const key of Object.keys(saveData)) {
            if (page.toString() === key) {
                load(page);
                break;
            }
        }
    });

    request.fail(function (jqXHR, textStatus) {
        error.innerText = "Error Loading Planner Data!";
        error.style.color = "red";
    });
}

let resetRequestNum = true;
let requestInterval;

function recursiveRequest(saveDict, count) {
    saveState.innerHTML = "Syncing... | Please wait...";

    const request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/planner/save",
        data: JSON.stringify(saveDict)
    });

    request.done(ignored => {
        saveState.innerHTML = "Synced to Cloud | Last Edit was seconds ago";
        error.innerHTML = "Connected to Nebulus";
        error.style.color = "green";
        resetRequestNum = true;
        if (requestInterval) clearInterval(requestInterval);
    });

    request.fail((ignored, ignored2) => {
        if (count < (resetRequestNum ? 3 : 1)) {
            saveState.innerHTML = "Sync Unsuccessful | Retrying Sync...";
            error.innerHTML = "Connecting...";
            error.style.color = "lightgray";
            recursiveRequest(saveDict, count + 1);
        }
        else {
            saveState.innerHTML = "Sync Unsuccessful | Retrying soon...";
            error.innerHTML = "Could not connect to Nebulus";
            error.style.color = "red";
            resetRequestNum = false;

            if (!requestInterval) requestInterval = setInterval(() => recursiveRequest(saveDict, 1), 1000 * 60)
        }
    });
}

function saveToServer() {
    save();

    updateDate();

    const saveDict = {};
    saveDict["name"] = document.getElementById("planner_name").value;
    saveDict["saveData"] = saveData;
    saveDict["lastEdited"] = [year, month, d.getDate(), d.getHours(), d.getMinutes()];

    recursiveRequest(saveDict, 1);
}