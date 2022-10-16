document.getElementById("pageTitle").innerHTML = "App";

keyUpDelay('#search', 1000, searchWithin);
const Default = {
    placement: 'bottom-right',
    triggerType: 'click',
    onShow: () => {
    },
    onHide: () => {
    }
};

for (const button of document.getElementsByClassName('expand')) {
    const parent = button.parentElement;
    let title = "Announcement from " + parent.querySelector('[author-element]').innerHTML;
    try {
        title = parent.querySelector('[title-element]').innerHTML;
    } catch (ignored) {
    }
    button.addEventListener('click', () =>
        openDetailsModal(
            parent.querySelector('[content-element]').innerHTML,
            title,
            parent.querySelector('[author-element]').innerHTML,
            parent.querySelector('[image-element]').src,
            parent.querySelector('[course-name-element]').innerHTML,
            parent.querySelector('[post-time-element]').innerHTML,
            parent.querySelector('[due-time-element]').innerHTML,
            parent.querySelector('[type-element]').innerHTML
        )
    );
}

function openDetailsModal(content, title, author, pic, course, postTime, dueTime, type) {
    if (type === "Announcement") {
        document.getElementById("submissionsBox").style.display = "none";
        document.getElementById("descriptionTitle").innerHTML = "Message";
    } else {
        document.getElementById("commentBox").style.display = "none";
    }
    if (title === author) title = 'Announcement from ' + title;

    if (dueTime === undefined) dueTime = '';

    document.getElementById('header').innerHTML = `
<h3 class="text-xl font-semibold text-gray-900 dark:text-white truncate h-full">${title}</h3>
<div class="flex mt-2">
    <img data-dropdown-toggle="userDropdown-0_0" id="avatar0_0" data-dropdown-placement="bottom-start" class="mr-2 inline-block rounded-full ring-2 ring-gray-300 dark:ring-gray-500 cursor-pointer mt-2 rounded-full
      shadow-lg dark:bg-gray-900 dark:hover:bg-gray-800 w-8 h-8" src="${pic}" alt="${author}'s profile picture">
    
    <div class="flex flex-col text-xs">
        <h4 class="text-lg text-gray-900 dark:text-white truncate cursor-pointer hover:underline" data-dropdown-toggle="userDropdown-0_0">
            ${author}
        </h4>
        <span data-dropdown-toggle="courseDropdown-0_0" class="bg-gray-300 text-gray-800 text-xs font-normal uppercase
         mr-2 px-2.5 py-0.5 rounded dark:bg-gray-600 dark:text-gray-300">${course}</span>
    </div>
</div>`;

    document.getElementById('dueTime').innerHTML = dueTime;
    document.getElementById('announcementBody').innerHTML = content;
    openModal("modal");
}

function replaceURLs(message) {
    if (!message) return message;

    if (!message.includes('http')) {
        console.log('returned. no link detected');
        return message;
    }
    if (message.includes('href="http')) {
        console.log('returned. recursive detected');
        return message;
    }

    const urlRegex = /(((https?:\/\/)|(www\.))\S+)/g;

    return message.replace(urlRegex, function (url) {
        let hyperlink = url;

        if (!hyperlink.match('^https?://')) hyperlink = 'http://' + hyperlink;

        hyperlink = hyperlink.replace('<p>', '');
        hyperlink = hyperlink.replace('</p>', '');

        return `<a target="_blank"
                   class="
                   underline 
                   decoration-yellow-500 decoration-[0.25rem] 
                   motion-safe:transition-all motion-safe:duration-200 
                   hover:decoration-[0.5rem] focus:decoration-[0.5rem] hover:decoration-yellow-500/50 focus:decoration-yellow-500/50 
               " href="${hyperlink}">${hyperlink}</a>`;
    });
}
