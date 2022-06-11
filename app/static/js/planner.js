let exitTime;
let loadingModal;

window.addEventListener("load", () => {
    addTimePeriod(1);
    addTimePeriod(2);
    loadingModal = new Modal(document.getElementById("loading"));
    loadingModal.show();
    document.querySelector("#loading p").innerHTML += loadingIcon(30);
    exitTime = Date.now() + 500;
});

function init_table(){
    document.getElementsByTagName("table")[0].innerHTML = "";
    const times = document.getElementById("timePeriods");

    let d, month, year, page, startDate;

    const nextPage = document.getElementById("nextpage");
    const today = document.getElementById("today");
    const prevPage = document.getElementById("prevpage");

    const saveState = document.getElementById("savestate");
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

    keyUpDelay("table", 500, save);
    keyUpDelay("#planner_name", 500, save);

    loadFromServer();

    nextPage.onclick = function () {
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
        save();
    }

    prevPage.onclick = function () {
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
        save();
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

}

function init_table_with_periods(periods){
    document.getElementsByTagName("table")[0].innerHTML = "";
    const times = document.getElementById("timePeriods");

    let d, month, year, page, startDate;

    const nextPage = document.getElementById("nextpage");
    const today = document.getElementById("today");
    const prevPage = document.getElementById("prevpage");

    const saveState = document.getElementById("savestate");
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

    keyUpDelay("table", 500, save);
    keyUpDelay("#planner_name", 500, save);

    loadFromServer();

    nextPage.onclick = function () {
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
        save();
    }

    prevPage.onclick = function () {
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
        save();
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

    for (let i = 0; i < 8; i++) {
        const row = table.insertRow();
        const smallCell = row.insertCell();

        let textarea = document.createElement("textarea");
        textarea.innerHTML = periods[i] + "";
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

}
init_table();
function addTimePeriod() {
    let periods = document.getElementById("numberOfPeriods").value;
    document.getElementById("numberOfPeriods").value = parseInt(periods)+1;
    let data = `
            <div class="flex w-full mb-4">
                <span onclick="addTimePeriod()" class="inline-flex items-center px-3 text-sm text-gray-900 bg-gray-200 border
                border-r-0 border-gray-300 rounded-l-md dark:bg-gray-500 dark:text-gray-400 dark:border-gray-600">+</span>
                <input type="text" name="period${periods}"  class="rounded-none rounded-r-lg bg-gray-50 border border-gray-300 text-gray-900
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
    const code = String.fromCharCode(e.keyCode);

    if (!(/[a-zA-Z0-9-_ ]/.test(code) && code === code.toUpperCase()))
        return;

    const notes = document.getElementsByClassName("note");
    saveData[page] = {};
    for (let i = 0; i < notes.length; i++) {
        if (notes[i].value !== "")
            saveData[page][i] = notes[i].value;
    }

    saveToServer();
}

function load(page) {
    const notes = document.getElementsByClassName("note");
    for (let i = 0; i < notes.length; i++) {
        if (saveData[page] && saveData[page][i])
            notes[i].value = saveData[page][i];
        else
            notes[i].value = "";
    }
}

function loadFromServer() {
    const request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/planner/load"
    });

    request.done(data => {
        setTimeout(() => {
                document.getElementById("loading").classList.add("fade-out");
                document.querySelector("[modal-backdrop]").classList.add("fade-out");
                setTimeout(() => loadingModal.hide(), 500);
            },
            Math.max(0, exitTime - Date.now()) + 1000
        );

        if (data === "0") {
            new Modal(document.getElementById("configureModal")).show();
            return;
        }

        document.getElementById("planner_name").value = data["name"];
        let periods = data["periods"];
        // let table = document.getElementsByTagName("table")[0]
        // table.innerHTML = "";
        // for (let i = 0; i < periods.length; i++) {
        //     const row = table.insertRow();
        //     const smallCell = row.insertCell();
        //
        //     let textarea = document.createElement("textarea");
        //     textarea.innerHTML = periods[i] + "";
        //     textarea.style.fontsize = "1.5rem";
        //     smallCell.appendChild(textarea);
        //
        //     for (let j = 0; j < 6; j++) {
        //         const cell = row.insertCell();
        //
        //         textarea = document.createElement("textarea");
        //         textarea.className = "note";
        //         //textarea.placeholder = "_".repeat(105);
        //         cell.appendChild(textarea);
        //     }
        // }


        //init_table_with_periods(periods);
        saveData = data["data"];

        for (const key of Object.keys(saveData)) {
            if (page.toString() === key) {
                load(page);
                break;
            }
        }
    });

    request.fail(function (jqXHR, textStatus) {
        document.getElementById("error").innerText = "Error Loading Planner Data!";
        document.getElementById("error").style.color = "red";
    });
}

function saveToServer() {
    updateDate();

    const save = {};
    save["name"] = document.getElementById("planner_name").value;
    save["saveData"] = saveData;
    save["lastEdited"] = [year, month, d.getDate(), d.getHours(), d.getMinutes()];

    saveState.innerHTML = "Syncing... | Please wait...";

    const request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/planner/save",
        data: JSON.stringify(save)
    });

    request.done(function (ignored) {
        saveState.innerHTML = "Synced to Cloud | Last Edit was seconds ago";
    });

    request.fail(function (ignored, alsoignored) {
        saveState.innerHTML = "Sync Unsuccessful | Retrying Sync...";
    });
}

function createPlanner(){
    let daplannerName = document.getElementById('configName').value;
    plannerName.value = daplannerName;
    let arr = [];
    let count = 0;
    while (true){
        let name = "period"+count.toString();
        if (document.body.contains(document.getElementsByName(name)[0])){
            arr.push(document.getElementsByName(name)[0].value);
            count+=1;
        }else{
            break;
        }
    }
    const save = {};
    save["name"] = daplannerName;
    save["periods"] = arr;
    const request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/planner/create",
        data: JSON.stringify(save)
    });

    request.done(function (ignored) {
        location.reload();
    });

}