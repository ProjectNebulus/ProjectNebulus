const dropdownTitle = document.getElementById("pageTitle");

if (document.title.includes("Nebulus - "))
    dropdownTitle.innerHTML = document.title.replace("Nebulus - ", "");

const pageTitleRect = dropdownTitle.getBoundingClientRect();
if (pageTitleRect.width < 175)
    dropdownTitle.style.width = (pageTitleRect.width + 30) + "px";

for (const element of document.querySelectorAll("#changePage li[href] span"))
    element.classList.add("material-icons", 'mr-3', "text-gray-600", "dark:text-gray-300")

for (const element of document.querySelectorAll("#changePage li[href]")) {
    const list = ['py-2', 'pl-2', 'pr-10', 'mx-2', 'hover:bg-gray-100', 'dark:hover:bg-gray-600', 'dark:hover:text-white', 'flex', 'place-items-center', 'cursor-pointer', 'rounded'];
    element.innerHTML = "<a href='" + element.getAttribute("href") + "' class='" + list.join(" ") + "'>" + element.innerHTML + "</a>";
    element.removeAttribute("href");
}

const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');

// Change the icons inside the button based on previous settings
if (
    localStorage.getItem('color-theme') === 'dark' ||
    (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)
)
    themeToggleLightIcon.classList.remove('hidden');
else themeToggleDarkIcon.classList.remove('hidden');

const themeToggleBtn = document.getElementById('theme-toggle');

themeToggleBtn.addEventListener('click', function () {
    // toggle icons inside button
    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    // if set via local storage previously
    if (localStorage.getItem('color-theme') === 'light')
        localStorage.setItem('color-theme', 'dark');
    else localStorage.setItem('color-theme', 'light');

    toggleTheme();
    invertSite();
});

for (const a of document.getElementsByClassName('nav-link'))
    a.className +=
        ' hover:underline block py-2 px-1 text-sm text-gray-700 dark:text-gray-200 dark:hover:text-white';

for (const a of document.getElementsByClassName('nav-link-2'))
    a.className +=
        ' block py-2 pr-4 pl-3 text-sm text-black bg-black-700 rounded md:bg-transparent md:p-0 dark:text-white';

for (const element of document.getElementsByClassName('changeable-gradient')) {
    element.classList.toggle('gradient-text-dark');
    element.classList.toggle('gradient-text');
}

document.querySelector("#navbar [data-dropdown-toggle='control-center']").oncontextmenu = (e) =>
    e.preventDefault();

function searchWithin(search) {
    if (search !== "course") search = "user"

    let value = document.getElementById('search_input').value;
    let searchItems = document.getElementById('search_items');
    if (/\w+/.test(value)) {
        searchItems.innerHTML = `
                    <li>
                        <div class="flex gap-2 place-items-center py-2.5 rounded-lg mx-auto block px-4 py-2 mx-2 dark:hover:text-white">
                            ${loadingIcon(8)} Searching...
                        </div>
                    </li>`;

        const request = $.ajax({
            type: 'POST',
            url: '/api/v1/internal/search-within-user',
            data: JSON.stringify({search: value}),
            contentType: 'application/json; charset=utf-8'
        });
        request.done((data) => {
            let string = '';
            let temp_arr = [];
            if (data === '0') {
                string = `
                    <li>
                        <div class="py-2.5 rounded-lg mx-auto block px-4 py-2 mx-2 dark:hover:text-white">
                            No Results Found
                        </div>
                    </li>`;
            } else {
                let datas = data.split('•');
                for (let i = 0; i < datas.length; i++) {
                    temp_arr.push(datas[i]);
                    if (i % 4 === 3) {
                        let pic = `<img src="${temp_arr[3]}" style="margin-right: 20px;" class="inline-block w-10 h-10 rounded-md">`;
                        switch (temp_arr[0]) {
                            case 'document':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">description</i><img src="https://api.schoology.com/sites/all/themes/schoology_theme/images/course-default.svg" style="margin-left: -40px;margin-top: 20px;" class="inline-block w-6 h-6 rounded-md">`;
                                break;
                            case 'NebDoc':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">draft</i><img src="https://api.schoology.com/sites/all/themes/schoology_theme/images/course-default.svg" style="margin-left: -40px;margin-top: 20px;" class="inline-block w-6 h-6 rounded-md">`;
                                break;
                            case 'event':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">event</i><img src="https://api.schoology.com/sites/all/themes/schoology_theme/images/course-default.svg" style="margin-left: -40px;margin-top: 20px;" class="inline-block w-6 h-6 rounded-md">`;
                                break;
                            case 'assignment':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">assignment</i><img src="https://api.schoology.com/sites/all/themes/schoology_theme/images/course-default.svg" style="margin-left: -40px;margin-top: 20px;" class="inline-block w-6 h-6 rounded-md">`;
                                break;
                            case 'chat':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">forum</i><img src="https://api.schoology.com/sites/all/themes/schoology_theme/images/course-default.svg" style="margin-left: -40px;margin-top: 20px;" class="inline-block w-6 h-6 rounded-md">`;
                                break;
                            case 'announcement':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">campaign</i><img src="https://api.schoology.com/sites/all/themes/schoology_theme/images/course-default.svg" style="margin-left: -40px;margin-top: 20px;" class="inline-block w-6 h-6 rounded-md">`;
                                break;
                        }

                        string += `
                    <li style="margin:5px;">
                        <div class="truncate py-2.5 rounded-lg mx-auto block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 mx-2 dark:hover:text-white">
                ${pic}
                <div style="display: inline-block; vertical-align: middle;">
                ${temp_arr[1]} <br><span class="text-gray-500">${temp_arr[2]}</span></div>
                </div>
                    </li>`;
                        temp_arr = [];
                    }
                }
            }
            searchItems.innerHTML = string;
        });

    }
}
