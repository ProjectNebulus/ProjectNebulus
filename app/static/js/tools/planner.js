let exitTime;
let loadingModal;
let empty = false;

const times = document.getElementById('timePeriods');

let d = new Date(),
    month,
    year,
    startDate;

const oneWeek = 1000 * 60 * 60 * 24 * 7;

let page = Math.floor(Date.now() / oneWeek);

const nextPage = document.getElementById('nextPage');
const today = document.getElementById('today');
const prevPage = document.getElementById('prevPage');

const saveState = document.getElementById('savestate');
const error = document.getElementById('error');
const plannerName = document.getElementById('planner_name');

const weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
const months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
];
const daysInMonths = [
    31,
    d.getFullYear() % 4 === 0 ? 29 : 28,
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31
];

const table = document.getElementsByTagName('table')[0];

let saveData = {};

window.addEventListener('load', () => {
    if (empty) {
        for (let i = 0; i < 6; i++) addTimePeriod();
    }

    loadingModal = new Modal(document.getElementById('loading'));
    loadingModal.show();
    document.querySelector('#loading p').innerHTML += loadingIcon(30);
    exitTime = Date.now() + 300;

    reloadTable();
});

// if(typeof escapeHtmlEntities == 'undefined') {
//     escapeHtmlEntities = function (text) {
//         return text.replace(":","&colon;").replace(/[\u00A0-\u2666<>\&]/g, function(c) {
//             return '&' +
//                 (escapeHtmlEntities.entityTable[c.charCodeAt(0)] || '#'+c.charCodeAt(0)) + ';';
//         });
//     };
//
//     // all HTML4 entities as defined here: http://www.w3.org/TR/html4/sgml/entities.html
//     // added: amp, lt, gt, quot and apos
//     escapeHtmlEntities.entityTable = {
//         34 : 'quot',
//         38 : 'amp',
//         39 : 'apos',
//         60 : 'lt',
//         62 : 'gt',
//         160 : 'nbsp',
//         161 : 'iexcl',
//         162 : 'cent',
//         163 : 'pound',
//         164 : 'curren',
//         165 : 'yen',
//         166 : 'brvbar',
//         167 : 'sect',
//         168 : 'uml',
//         169 : 'copy',
//         170 : 'ordf',
//         171 : 'laquo',
//         172 : 'not',
//         173 : 'shy',
//         174 : 'reg',
//         175 : 'macr',
//         176 : 'deg',
//         177 : 'plusmn',
//         178 : 'sup2',
//         179 : 'sup3',
//         180 : 'acute',
//         181 : 'micro',
//         182 : 'para',
//         183 : 'middot',
//         184 : 'cedil',
//         185 : 'sup1',
//         186 : 'ordm',
//         187 : 'raquo',
//         188 : 'frac14',
//         189 : 'frac12',
//         190 : 'frac34',
//         191 : 'iquest',
//         192 : 'Agrave',
//         193 : 'Aacute',
//         194 : 'Acirc',
//         195 : 'Atilde',
//         196 : 'Auml',
//         197 : 'Aring',
//         198 : 'AElig',
//         199 : 'Ccedil',
//         200 : 'Egrave',
//         201 : 'Eacute',
//         202 : 'Ecirc',
//         203 : 'Euml',
//         204 : 'Igrave',
//         205 : 'Iacute',
//         206 : 'Icirc',
//         207 : 'Iuml',
//         208 : 'ETH',
//         209 : 'Ntilde',
//         210 : 'Ograve',
//         211 : 'Oacute',
//         212 : 'Ocirc',
//         213 : 'Otilde',
//         214 : 'Ouml',
//         215 : 'times',
//         216 : 'Oslash',
//         217 : 'Ugrave',
//         218 : 'Uacute',
//         219 : 'Ucirc',
//         220 : 'Uuml',
//         221 : 'Yacute',
//         222 : 'THORN',
//         223 : 'szlig',
//         224 : 'agrave',
//         225 : 'aacute',
//         226 : 'acirc',
//         227 : 'atilde',
//         228 : 'auml',
//         229 : 'aring',
//         230 : 'aelig',
//         231 : 'ccedil',
//         232 : 'egrave',
//         233 : 'eacute',
//         234 : 'ecirc',
//         235 : 'euml',
//         236 : 'igrave',
//         237 : 'iacute',
//         238 : 'icirc',
//         239 : 'iuml',
//         240 : 'eth',
//         241 : 'ntilde',
//         242 : 'ograve',
//         243 : 'oacute',
//         244 : 'ocirc',
//         245 : 'otilde',
//         246 : 'ouml',
//         247 : 'divide',
//         248 : 'oslash',
//         249 : 'ugrave',
//         250 : 'uacute',
//         251 : 'ucirc',
//         252 : 'uuml',
//         253 : 'yacute',
//         254 : 'thorn',
//         255 : 'yuml',
//         402 : 'fnof',
//         913 : 'Alpha',
//         914 : 'Beta',
//         915 : 'Gamma',
//         916 : 'Delta',
//         917 : 'Epsilon',
//         918 : 'Zeta',
//         919 : 'Eta',
//         920 : 'Theta',
//         921 : 'Iota',
//         922 : 'Kappa',
//         923 : 'Lambda',
//         924 : 'Mu',
//         925 : 'Nu',
//         926 : 'Xi',
//         927 : 'Omicron',
//         928 : 'Pi',
//         929 : 'Rho',
//         931 : 'Sigma',
//         932 : 'Tau',
//         933 : 'Upsilon',
//         934 : 'Phi',
//         935 : 'Chi',
//         936 : 'Psi',
//         937 : 'Omega',
//         945 : 'alpha',
//         946 : 'beta',
//         947 : 'gamma',
//         948 : 'delta',
//         949 : 'epsilon',
//         950 : 'zeta',
//         951 : 'eta',
//         952 : 'theta',
//         953 : 'iota',
//         954 : 'kappa',
//         955 : 'lambda',
//         956 : 'mu',
//         957 : 'nu',
//         958 : 'xi',
//         959 : 'omicron',
//         960 : 'pi',
//         961 : 'rho',
//         962 : 'sigmaf',
//         963 : 'sigma',
//         964 : 'tau',
//         965 : 'upsilon',
//         966 : 'phi',
//         967 : 'chi',
//         968 : 'psi',
//         969 : 'omega',
//         977 : 'thetasym',
//         978 : 'upsih',
//         982 : 'piv',
//         8226 : 'bull',
//         8230 : 'hellip',
//         8242 : 'prime',
//         8243 : 'Prime',
//         8254 : 'oline',
//         8260 : 'frasl',
//         8472 : 'weierp',
//         8465 : 'image',
//         8476 : 'real',
//         8482 : 'trade',
//         8501 : 'alefsym',
//         8592 : 'larr',
//         8593 : 'uarr',
//         8594 : 'rarr',
//         8595 : 'darr',
//         8596 : 'harr',
//         8629 : 'crarr',
//         8656 : 'lArr',
//         8657 : 'uArr',
//         8658 : 'rArr',
//         8659 : 'dArr',
//         8660 : 'hArr',
//         8704 : 'forall',
//         8706 : 'part',
//         8707 : 'exist',
//         8709 : 'empty',
//         8711 : 'nabla',
//         8712 : 'isin',
//         8713 : 'notin',
//         8715 : 'ni',
//         8719 : 'prod',
//         8721 : 'sum',
//         8722 : 'minus',
//         8727 : 'lowast',
//         8730 : 'radic',
//         8733 : 'prop',
//         8734 : 'infin',
//         8736 : 'ang',
//         8743 : 'and',
//         8744 : 'or',
//         8745 : 'cap',
//         8746 : 'cup',
//         8747 : 'int',
//         8756 : 'there4',
//         8764 : 'sim',
//         8773 : 'cong',
//         8776 : 'asymp',
//         8800 : 'ne',
//         8801 : 'equiv',
//         8804 : 'le',
//         8805 : 'ge',
//         8834 : 'sub',
//         8835 : 'sup',
//         8836 : 'nsub',
//         8838 : 'sube',
//         8839 : 'supe',
//         8853 : 'oplus',
//         8855 : 'otimes',
//         8869 : 'perp',
//         8901 : 'sdot',
//         8968 : 'lceil',
//         8969 : 'rceil',
//         8970 : 'lfloor',
//         8971 : 'rfloor',
//         9001 : 'lang',
//         9002 : 'rang',
//         9674 : 'loz',
//         9824 : 'spades',
//         9827 : 'clubs',
//         9829 : 'hearts',
//         9830 : 'diams',
//         338 : 'OElig',
//         339 : 'oelig',
//         352 : 'Scaron',
//         353 : 'scaron',
//         376 : 'Yuml',
//         710 : 'circ',
//         732 : 'tilde',
//         8194 : 'ensp',
//         8195 : 'emsp',
//         8201 : 'thinsp',
//         8204 : 'zwnj',
//         8205 : 'zwj',
//         8206 : 'lrm',
//         8207 : 'rlm',
//         8211 : 'ndash',
//         8212 : 'mdash',
//         8216 : 'lsquo',
//         8217 : 'rsquo',
//         8218 : 'sbquo',
//         8220 : 'ldquo',
//         8221 : 'rdquo',
//         8222 : 'bdquo',
//         8224 : 'dagger',
//         8225 : 'Dagger',
//         8240 : 'permil',
//         8249 : 'lsaquo',
//         8250 : 'rsaquo',
//         8364 : 'euro'
//     };
// }
function updateDate() {
    d = new Date();
    month = d.getMonth();
    year = d.getFullYear();

    startDate = d.getDate() - d.getDay();

    if (startDate < 1) {
        month--;
        if (month < 0) {
            month = 11;
            year--;
        }
        startDate = daysInMonths[month] + startDate;
    }
}

function reloadTable() {
    table.innerHTML = '';
    changeDate(true);
    for (
        let i = 1;
        i <= document.querySelectorAll('#configureModal #timePeriods .timePeriod').length;
        i++
    ) {
        const row = table.insertRow();
        row.classList.add(
            "bg-white/75", "border-b", "dark:bg-gray-800/75", "dark:border-gray-700",
        )
        const smallCell = row.insertCell();

        smallCell.innerHTML = i + '';
        smallCell.style.textAlign = 'center';
        smallCell.style.width = '2.5rem';

        for (let j = 0; j < 7; j++) {
            const cell = row.insertCell();

            const div = document.createElement('div');
            div.setAttribute('contenteditable', 'true');
            div.className = 'note';

            if (saveData[page] && saveData[page][i])
                div.innerHTML = saveData[page][i].replaceAll(':::::', '=');
            else div.innerHTML = `
            <ul>
              <li><br></li>
              <li><br></li>
              </ul>      `;

            cell.appendChild(div);
        }
    }
}

updateDate();

keyUpDelay('table', 500, saveToServer);
keyUpDelay('#planner_name', 500, saveToServer);

document.addEventListener('keyup', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.shiftKey) {
        if (e.key === 'ArrowLeft') prevPage.click();
        else if (e.key === 'ArrowRight') nextPage.click();
        else if (e.key === 'ArrowUp') today.click();
    }
});
window.onload = function () {
    loadFromServer();
}


nextPage.onclick = function () {
    save();

    page++;
    load(page);

    nextPage.disabled = year >= 2030 && month === 11 && startDate >= daysInMonths[month] - 7;
    prevPage.disabled = false;

    startDate += 7;
    if (startDate > daysInMonths[month]) {
        startDate -= daysInMonths[month];
        month++;

        if (month > 11) {
            month = 0;
            year++;
        }
    }

    changeDate(false);
};

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

    changeDate(false);
};

today.onclick = function () {
    page = Math.floor(Date.now() / oneWeek);
    load(page);
    startDate = d.getDate() - d.getDay();
    year = d.getFullYear();
    month = d.getMonth();
    changeDate(false);
    nextPage.disabled = false;
    prevPage.disabled = false;
};

document.getElementById('month').innerHTML = months[month] + ' ' + d.getFullYear();

changeDate(true);

let num = 1;

function addTimePeriod() {
    if (num >= 20) return;

    const roundedText = showIcons ? '' : 'rounded-r-lg';
    const hiddenText = showIcons ? '' : 'hidden';

    let inputs = document.querySelectorAll('#configureModal #timePeriods .timePeriod input');
    const timePeriods = [];
    for (let a of inputs) timePeriods.push(a.value);

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
    times.scrollTo(0, times.scrollHeight);
    num++;

    inputs = document.querySelectorAll('#configureModal #timePeriods .timePeriod input');
    for (let i = 0; i < timePeriods.length; i++) inputs[i].value = timePeriods[i];
}

function removePeriod(element) {
    num--;
    element.classList.add('fade-out');
    setTimeout(() => {
        element.parentElement.removeChild(element);

        let inputs = document.querySelectorAll('#configureModal #timePeriods .timePeriod');
        const timePeriods = [];
        for (let a of inputs) timePeriods.push(a.value);

        for (let i = parseInt(element.children[0].innerHTML); i <= timePeriods.length; i++) {
            const number = inputs[i - 1].children[0];
            number.innerHTML = parseInt(number.innerHTML) - 1 + '';
            const input = inputs[i - 1].children[1];
            input.placeholder = 'Period ' + parseInt(number.innerHTML);
        }
    }, 750);
}

let configSaved = true;

function saveConfig() {
    configSaved = false;
    reloadTable();
    let inputs = document.querySelectorAll('#configureModal #timePeriods .timePeriod input');
    let values = [];
    for (const element of inputs) values.push(element.value);

    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/planner/saveConfig',
        data: JSON.stringify(values)
    });

    request.done(() => {
        saveState.innerHTML = 'Configuration Saved';
        configSaved = true;
    });
    request.fail(() => (saveState.innerHTML = 'Configuration Saving Failed | Retrying soon...'));
}

let showIcons = false;

function toggleRemoveIcons() {
    if (num <= 1) return;

    showIcons = !showIcons;
    for (const element of document.getElementsByClassName('timePeriod')) {
        element.getElementsByTagName('input')[0].classList.toggle('rounded-r-lg');
        element.getElementsByClassName('removeIcon')[0].classList.toggle('hidden');
    }
}

function settings() {
    document.getElementById('configName').value = document.getElementById('planner_name').value;
}

function changeDate(insert) {
    if (insert === true) {
        const daysRow = table.insertRow();
        daysRow.classList.add(
            "text-xs", "text-gray-700", "uppercase", "bg-gray-50", "dark:bg-gray-700", "dark:text-gray-400",
        )
        for (let i = 0; i <= 7; i++) daysRow.insertCell();
    }

    document.getElementById('month').innerHTML = months[month] + ' ' + year;

    for (let i = 1; i <= 7; i++) {
        let day = startDate + i;
        if (day > daysInMonths[month]) day -= daysInMonths[month];

        table.rows[0].cells[i].innerHTML = day.toString() + ' ' + weekDays[i - 1];
    }
}

function save(e) {
    if (e) {
        const code = String.fromCharCode(e.keyCode);

        if (!(/[a-zA-Z0-9-_ ]/.test(code) && code === code.toUpperCase())) return;
    }

    const notes = document.getElementsByClassName('note');
    saveData[page] = {};
    for (let i = 0; i < notes.length; i++) {
        if (notes[i].innerHTML !== '')

            saveData[page][i] = (notes[i].innerHTML.replaceAll('=', ':::::'));
    }
}

function load(page) {
    const notes = document.getElementsByClassName('note');
    for (let i = 0; i < notes.length; i++) {
        if (saveData[page] && saveData[page][i])
            notes[i].innerHTML = saveData[page][i].replaceAll(':::::', '=');
        else notes[i].innerHTML = `
            <ul>
              <li><br></li>
              <li><br></li>
              </ul>      `;
    }
}

function loadFromServer() {
    const request = $.ajax({
        type: 'GET',
        url: '/api/v1/internal/planner/load'
    });

    request.done((data) => {
        setTimeout(() => {
            document.getElementById('loading').classList.add('fade-out');
            document.querySelector('[modal-backdrop]').classList.add('fade-out');
            setTimeout(() => loadingModal.hide(), 500);
        }, Math.max(0, exitTime - Date.now()) + 1000);

        if (Object.keys(data).length === 0) {
            setTimeout(() => {
                loadingModal.hide();
                document.getElementById('openModal').click();
                empty = true;
            }, Math.max(0, exitTime - Date.now()) + 1000);
            return;
        }

        plannerName.value = data['name'];
        saveData = data['saveData'];

        for (let i = 0; i < data['periods'].length; i++) addTimePeriod();

        let inputs = document.querySelectorAll('#configureModal #timePeriods .timePeriod input');

        for (let i = 0; i < inputs.length; i++) inputs[i].value = data['periods'][i];

        reloadTable();

        for (const key of Object.keys(saveData)) {
            if (page.toString() === key) {
                load(page);
                break;
            }
        }
    });

    request.fail(() => {
        error.innerText = 'Error Loading Planner Data!';
        error.style.color = 'red';
    });
}

let resetRequestNum = true;
let requestInterval;

function recursiveSave(saveDict, count) {
    saveState.innerHTML = 'Syncing... | Please wait...';

    const request = $.ajax({
        type: 'POST',
        url: '/api/v1/internal/planner/save',
        data: JSON.stringify(saveDict)
    });

    request.done(() => {
        saveState.innerHTML = 'Last Edit was seconds ago';
        error.innerHTML = 'Synced to Cloud';
        error.style.color = 'skyblue';
        resetRequestNum = true;
        if (requestInterval) clearInterval(requestInterval);
    });

    request.fail(() => {
        if (count < (resetRequestNum ? 3 : 1)) {
            saveState.innerHTML = 'Retrying Sync...';
            error.innerHTML = 'Syncing Failed';
            error.style.color = 'lightgray';
            recursiveSave(saveDict, count + 1);
        } else {
            saveState.innerHTML = 'Retrying soon...';
            error.innerHTML = 'Syncing Failed, Cannot Connect to Nebulus';
            error.style.color = 'red';
            resetRequestNum = false;

            if (!requestInterval)
                requestInterval = setInterval(() => recursiveSave(saveDict, 1), 1000 * 60);
        }
    });
}

function saveToServer() {
    save();
    updateDate();

    if (!configSaved) saveConfig();

    const saveDict = {};
    saveDict['name'] = plannerName.value;
    saveDict['saveData'] = saveData;
    saveDict['lastEdited'] =
        [year, month + 1, d.getDate()].join('-') +
        ' ' +
        [d.getHours(), d.getMinutes(), d.getSeconds()].join(':');

    saveDict['periods'] = [];

    recursiveSave(saveDict, 1);
}
