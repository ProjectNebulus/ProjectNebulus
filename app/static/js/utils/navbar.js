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

    detectTheme();
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
    if (!search) search = "user"

    let value = document.getElementById('search_input').value;

    if (value.length > 0) {
        document.getElementById('search_items').innerHTML = `
<li>
<div class="py-2.5 rounded-lg mx-auto block px-4 py-2 mx-2 dark:hover:text-white">
                <svg class="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
</svg>
    Searching...
</div>
</li>
            `;
        const request = $.ajax({
            type: 'POST',
            url: '/api/v1/internal/search-within-' + search,
            data: JSON.stringify({search: value}),
            contentType: 'application/json; charset=utf-8'
        });
        request.done((data) => {
            document.getElementById('search_items').innerHTML = '';
            let temp_arr = [];
            if (data === '0') {
                document.getElementById('search_items').innerHTML += `
                    <li>
                            <div class="py-2.5 rounded-lg mx-auto block px-4 py-2 mx-2 dark:hover:text-white">
                        <svg class="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
</svg>
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
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">description</i>`;
                                break;
                            case 'NebDoc':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">draft</i>`;
                                break;
                            case 'event':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">event</i>`;
                                break;
                            case 'assignment':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">assignment</i>`;
                                break;
                            case 'chat':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">forum</i>`;
                                break;
                            case 'announcement':
                                pic = `<i class="material-icons" style="font-size: 40px;vertical-align: middle;margin-right: 20px;">campaign</i>`;
                                break;
                        }

                        document.getElementById('search_items').innerHTML += `
                    <li style="margin:5px;">
                        <div class="truncate py-2.5 rounded-lg mx-auto block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 mx-2 dark:hover:text-white" style="text-align:left;">
                ${pic}
                <div style="display: inline-block; vertical-align: middle;">
                ${temp_arr[1]} <br><span class="text-gray-500">${temp_arr[2]}</span></div>
                </div>
                    </li>`;
                        temp_arr = [];
                    }
                }
            }
        });

        document.getElementById('search_items').innerHTML = '';
    }
}
