let exitTime;
let loadingModal;
let syncedTime;
window.addEventListener("load", () => {
    for (let i = 0; i < 6; i++)
        addTimePeriod();

    loadingModal = new Modal(document.getElementById("loading"));
    loadingModal.show();
    document.querySelector("#loading p").innerHTML += loadingIcon(30);
    exitTime = Date.now() + 300;

    reloadTable();
});

const times = document.getElementById("timePeriods");

let d, month, year, startDate;

const oneWeek = 1000 * 60 * 60 * 24 * 7;

let page = Math.floor(Date.now() / oneWeek);

const nextPage = document.getElementById("nextPage");
const today = document.getElementById("today");
const prevPage = document.getElementById("prevPage");

const saveState = document.getElementById("savestate");
const error = document.getElementById("error");
const plannerName = document.getElementById("planner_name");

function errorExpire(){
    setTimeout(() => {
        //error.style.display = 'none';
        error.style.visibility = "hidden";
    }, 1500);
}
function errorShow(){
    //error.style.display = 'block';
    error.style.visibility = "visible";
}
function updateDate() {
    d = new Date();
    month = d.getMonth();
    year = d.getFullYear();

    startDate = d.getDate() - d.getDay();
}

function reloadTable() {
    table.innerHTML = "";
    changeDate();
    for (let i = 1; i <= document.querySelectorAll("#configureModal #timePeriods .timePeriod").length; i++) {
        const row = table.insertRow();
        const smallCell = row.insertCell();

        smallCell.innerHTML = i + "";
        smallCell.style.textAlign = "center";
        smallCell.style.width = "2.5rem";

        for (let j = 0; j < 7; j++) {
            const cell = row.insertCell();

            const div = document.createElement("div");
            div.setAttribute("contenteditable", "true");
            div.className = "note";
            div.innerHTML = `
            <ul>
              <li><br></li>
              <li><br></li>
              </ul>      `
            cell.appendChild(div);
        }
    }
}

updateDate();
errorShow();
errorExpire();
const weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
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

changeDate();

let num = 1;

function addTimePeriod() {
    if (num >= 20)
        return

    const roundedText = showIcons ? "" : "rounded-r-lg";
    const hiddenText = showIcons ? "" : "hidden";

    let inputs = document.querySelectorAll("#configureModal #timePeriods .timePeriod input");
    const timePeriods = [];
    for (let a of inputs)
        timePeriods.push(a.value);

    let data = `
            <div class="flex w-full mb-4 timePeriod">
                <span class="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border border-r-0 border-gray-300
                 rounded-l-md dark:bg-gray-500 dark:text-gray-400 dark:border-gray-600">${num}</span>
                <input type="text" class="rounded-none ${roundedText} bg-gray-50 border border-gray-300 text-gray-900
                focus:ring-blue-500 focus:border-blue-500 block flex-1 min-w-0 w-full text-sm border-gray-300 p-2.5
                dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500
                dark:focus:border-blue-500" placeholder="Period ${num}">
                <button class="inline-flex items-center px-3 py-2.5 text-sm bg-red-600 border border-r-0 border-gray-300
     rounded-r-md text-white dark:border-gray-600 material-icons removeIcon hover:bg-red-800 ${hiddenText}"
     onclick="removePeriod(this.parentElement)">close</button>
            </div>
            `;
    times.innerHTML += data;
    times.scrollTo(0, times.scrollHeight)
    num++;

    inputs = document.querySelectorAll("#configureModal #timePeriods .timePeriod input");
    for (let i = 0; i < timePeriods.length; i++)
        inputs[i].value = timePeriods[i];
}

function removePeriod(element) {
    num--;
    element.classList.add("fade-out");
    setTimeout(() => {
        element.parentElement.removeChild(element);

        let inputs = document.querySelectorAll("#configureModal #timePeriods .timePeriod");
        const timePeriods = [];
        for (let a of inputs)
            timePeriods.push(a.value);

        for (let i = parseInt(element.children[0].innerHTML); i <= timePeriods.length; i++) {
            const number = inputs[i - 1].children[0];
            number.innerHTML = (parseInt(number.innerHTML) - 1) + "";
            const input = inputs[i - 1].children[1];
            input.placeholder = "Period " + parseInt(number.innerHTML);
        }
    }, 750);
}

let configSaved = true;

function saveConfig() {
    configSaved = false;
    reloadTable();
    let inputs = document.querySelectorAll("#configureModal #timePeriods .timePeriod input");
    let values = []
    for (const element of inputs)
        values.push(element.value);

    const request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/planner/saveConfig",
        data: JSON.stringify(values)
    });

    request.done(() => {
        errorShow();
        error.innerHTML = "Configuration Saved";
        error.style.color = "green";
        errorExpire();
        configSaved = true;
    });
    request.fail(() => {
        errorShow();
        saveState.innerHTML = "Retrying Configuration Save";
        error.innerHTML = "Configuration Saving Failed";
        error.style.color = "red";
        errorExpire();
    })
}

let showIcons = false;

function toggleRemoveIcons() {
    if (num <= 1)
        return

    showIcons = !showIcons;
    for (const element of document.getElementsByClassName("timePeriod")) {
        element.getElementsByTagName("input")[0].classList.toggle("rounded-r-lg");
        element.getElementsByClassName("removeIcon")[0].classList.toggle("hidden");
    }
}

function settings() {
    document.getElementById("configName").value = document.getElementById("planner_name").value;
}

function changeDate() {
    const daysRow = table.insertRow();
    for (let i = 0; i <= 7; i++)
        daysRow.insertCell();

    document.getElementById("month").innerHTML = months[month] + " " + year;

    for (let i = 1; i <= 7; i++) {
        let day = startDate + i;
        if (day > daysInMonths[month])
            day -= daysInMonths[month];

        table.rows[0].cells[i].innerHTML = day.toString() + " " + weekDays[i - 1];
    }
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
        if (notes[i].innerHTML !== "")
            saveData[page][i] = notes[i].innerHTML.replaceAll("=", ":::::");
    }
}

function load(page) {
    const notes = document.getElementsByClassName("note");
    for (let i = 0; i < notes.length; i++) {
        if (saveData[page] && saveData[page][i])
            notes[i].innerHTML = saveData[page][i].replaceAll(":::::", "=");
        else
            notes[i].innerHTML = `
            <ul>
              <li><br></li>
              <li><br></li>
              </ul>      `;
    }
}

function loadFromServer() {
    const request = $.ajax({
        type: "GET",
        url: "/api/v1/internal/planner/load"
    });

    request.done(data => {
        setTimeout(() => {
                document.getElementById("loading").classList.add("fade-out");
                setTimeout(() => {
                    loadingModal.hide();
                    document.querySelector("[modal-backdrop]").classList.add("fade-out");
                }, 500);
            },
            Math.max(0, exitTime - Date.now()) + 1000
        );

        if (Object.keys(data).length === 0) {
            setTimeout(() => {
                    loadingModal.hide();
                    document.getElementById("openModal").click();
                },
                Math.max(0, exitTime - Date.now()) + 1000);
            return;
        }

        plannerName.value = data["name"];
        saveData = data["saveData"];

        let inputs = document.querySelectorAll("#configureModal #timePeriods .timePeriod input");

        for (let i = 0; i < data["periods"].length - inputs.length; i++)
            addTimePeriod();

        inputs = document.querySelectorAll("#configureModal #timePeriods .timePeriod input");

        for (let i = 0; i < inputs.length; i++)
            inputs[i].value = data["periods"][i];

        for (const key of Object.keys(saveData)) {
            if (page.toString() === key) {
                load(page);
                break;
            }
        }
    });

    request.fail(function (jqXHR, textStatus) {
        errorShow();
        error.innerText = "Error Loading Planner Data!";
        error.style.color = "red";
        errorExpire();
    });
}

let resetRequestNum = true;
let requestInterval;

function recursiveSave(saveDict, count) {
    saveDict["name"] = plannerName.value;
    saveDict["saveData"] = saveData;
    saveDict["lastEdited"] = [year, month + 1, d.getDate()].join("-") + " " + [d.getHours(), d.getMinutes(), d.getSeconds()].join(":");

    saveDict["periods"] = [];
    errorShow();
    saveState.innerHTML = "Edits are being Synced";
    error.innerHTML = "Syncing to Cloud..."
    error.style.color = "lightgray";
    errorExpire();

    const request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/planner/save",
        data: JSON.stringify(saveDict)
    });

    request.done(() => {
        errorShow();
        var currentDateTime = new Date();
        syncedTime= Math.floor(currentDateTime.getTime() / 1000);
        saveState.innerHTML = "Last Edit was seconds ago";
        error.innerHTML = "Synced to Cloud";
        error.style.color = "green";
        errorExpire();
        resetRequestNum = true;
        if (requestInterval) clearInterval(requestInterval);
    });

    request.fail(() => {
        if (count < (resetRequestNum ? 3 : 1)) {
            errorShow();
            saveState.innerHTML = "Sync Unsuccessful | Retrying Sync...";
            error.innerHTML = "Connecting...";
            error.style.color = "lightgray";
            errorExpire();
            recursiveSave(saveDict, count + 1);
        }
        else {
            errorShow();
            saveState.innerHTML = "Sync Unsuccessful | Retrying soon...";
            error.innerHTML = "Could not connect to Nebulus";
            error.style.color = "red";
            errorExpire();
            resetRequestNum = false;

            if (!requestInterval) requestInterval = setInterval(() => recursiveSave(saveDict, 1), 1000 * 60)
        }
    });
}

function saveToServer() {
    save();
    updateDate();

    if (!configSaved)
        saveConfig();

    const saveDict = {};
    saveDict["name"] = plannerName.value;
    saveDict["saveData"] = saveData;
    saveDict["lastEdited"] = [year, month + 1, d.getDate()].join("-") + " " + [d.getHours(), d.getMinutes(), d.getSeconds()].join(":");

    saveDict["periods"] = [];

    recursiveSave(saveDict, 1);
}

function change(id) {
    if (id === "b") {
        document.execCommand('bold');
    }
    if (id === "i") {
        document.execCommand('italic');
    }
    if (id === "u") {
        document.execCommand('underline');
    }
    if (id === "c") {
        document.execCommand('foreColor', false, document.getElementById("changediscolor").style.color);
    }
    if (id === "h") {
        document.execCommand('hiliteColor', false, document.getElementById("changediscolor2").style.color);
    }
    if (id === "al") {
        document.execCommand('justifyLeft');
    }
    if (id === "ar") {
        document.execCommand('justifyRight');
    }
    if (id === "ac") {
        document.execCommand('justifyCenter');
    }
    if (id === "af") {
        document.execCommand('justifyFull');
    }
    if (id === "lb") {
        document.execCommand('insertUnorderedList');
    }
    if (id === "ln") {
        document.execCommand('insertOrderedList');
    }
    if (id === "redo") {
        document.execCommand('redo');
    }
    if (id === "undo") {
        document.execCommand('undo');
    }
    document.getElementById("editor").focus();
    document.getElementById("editor").focus();
}

function color() {
    let dacolor = document.getElementById("colorpicker").value;
    //document.getElementsByClassName("buttonSelect")[10].style.background = dacolor;
    document.getElementById("changediscolor").style.color = dacolor;
    document.execCommand('foreColor', false, dacolor);
}

function hilite() {
    let dacolor = document.getElementById("colorpicker2").value;
    //document.getElementsByClassName("buttonSelect")[10].style.background = dacolor;
    document.getElementById("changediscolor2").style.color = dacolor;
    document.execCommand('hiliteColor', false, dacolor);
}

document.getElementById("colorpicker").onchange = function () {
    color();

}

function checktime(){
    var currentDateTime = new Date();
    var seconds = Math.floor(currentDateTime.getTime() / 1000 - syncedTime);
    let minutes = false;
    if (seconds > 60){
        minutes = true;
        seconds = Math.floor(seconds/60);
    }
    if (saveState.innerHTML.includes("Last Edit")){
        let newmsg = "";
        if (minutes){
            newmsg = `Last Edit was ${seconds} minutes ago`;
        }else{
            newmsg = `Last Edit was ${seconds} seconds ago`;
        }
        saveState.innerHTML = newmsg;
    }
}

setInterval(checktime, 2000);