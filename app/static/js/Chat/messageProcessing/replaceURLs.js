import getEmbed from './embedGenerator.js';

// This function is applied on every message that is loaded
// It checks for URLS
function replaceURLs(message, message_id) {
    if (!message) return message;

    if (!message.includes('http')) {
        console.log('returned. no link detected');
        return message;
    }
    if (message.includes('href="http')) {
        console.log('returned. recursive detected');
        return message;
    }
    if (message.includes('src="http')) {
        console.log('returned. recursive detected');
        return message;
    }

    const urlRegex = /(((https?:\/\/)|(www\.))[^\s]+)/g;

    return message.replace(urlRegex, function (url) {
        let hyperlink = url;

        if (!hyperlink.match('^https?://')) hyperlink = 'http://' + hyperlink;

        hyperlink = hyperlink.replace('<p>', '');
        hyperlink = hyperlink.replace('</p>', '');
        hyperlink = hyperlink.replace('<br>', '');

        let result = ``;

        if (hyperlink)
            getEmbed(hyperlink).then((data) => {
                data = data['data'];

                data['themeColor'] = data["themeColor"] || '#534F4E';
                let site = data['siteName'] || siteName;

                result += `<div style="border-style: none none none solid; border-width:8px; border-color:${data['themeColor']}"
                     class="block p-6 max-w-sm bg-white rounded-lg border border-gray-200 shadow-md hover:bg-gray-100/75 dark:bg-gray-800/50 dark:border-gray-700 dark:hover:bg-gray-700/75">
                    <a href="${hyperlink}"><h5
                        class="mb-2 text-md hover:underline font-bold tracking-tight text-black dark:text-white">${site}</h5>
                    </a>
                    <a href="${hyperlink}"><h5
                        class="mb-2 text-xl hover:underline font-bold tracking-tight text-sky-500">${data['title']}</h5></a>
                    <p class="font-normal text-gray-700 dark:text-gray-400">${data['description']}</p>
                    `;

                if (data['image'] != null) result += `<img src="${data['image']}" style="width:90%; margin:auto; margin-top:10px;" class="rounded-md">`;

                result += `</div>`;

                document
                    .getElementById(`content_${message_id}`)
                    .insertAdjacentHTML('beforeend', result);
            });

        return `<a class="underline text-blue-600 hover:text-blue-800 visited:text-purple-600" href="${hyperlink}">${hyperlink}</a>${result}`;
    });

    //youtube iframe / embed for everything else
}

export default replaceURLs;

