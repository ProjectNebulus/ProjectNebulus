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

function updateExpand() {
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
                parent.querySelector('[type-element]').innerHTML,
                parent.querySelector('[image-element2]').src
            )
        );
    }
}

updateExpand();

{
    const recActivity = document.getElementById("recent-activity-div");
    recActivity.style.scrollBehavior = "smooth";
    let announcementStart = 8;
    let eventStart = 15;
    let waiting = false;
    let endMessageAdded = false;

    recActivity.addEventListener("scroll", () => {
        if ($(recActivity).scrollTop() + $(recActivity).innerHeight() < $(recActivity)[0].scrollHeight - 5)
            return;

        if (announcementStart >= announcementEnd) {
            if (!endMessageAdded) {
                endMessageAdded = true;
                recActivity.innerHTML += `
                <div class="flex gap-4 justify-center place-items-center mb-4">
                    <img src="${randomCat()}" class="w-8 h-10">
                    <p class="text-gray-500 dark:text-gray-400 text-2xl">This is the end...</p>
                </div>`
            }

            return;
        }

        if (waiting)
            return;

        recActivity.innerHTML += `
        <div class="flex gap-4 justify-center place-items-center mb-4">
            <img src="${v3Image}" class="w-10 h-12">
            <p class="text-gray-500 dark:text-gray-400 text-2xl">Loading...</p>
        </div>
        `
        recActivity.scrollTop = recActivity.scrollHeight;

        waiting = true;
        const req = $.ajax({
            url: "/api/v1/internal/get/recent-activity",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({load: announcementStart})
        });
        req.done(data => {
            recActivity.children[recActivity.children.length - 1].remove();
            announcementStart += 8;
            waiting = false;

            recActivity.innerHTML += data;
            updateExpand();
        });
    });
}

function openDetailsModal(content, title, author, pic, course, postTime, dueTime, type, coursepic) {
    if (type === "Announcement") {
        document.getElementById("submissionsBox").style.display = "none";
        document.getElementById("descriptionTitle").innerHTML = "Message";
        document.getElementById("commentBox").style.display = "block";

    } else {
        document.getElementById("descriptionTitle").innerHTML = "Description";
        document.getElementById("commentBox").style.display = "none";
        document.getElementById("submissionsBox").style.display = "block";
    }
    if (title === author) title = 'Announcement from ' + title;

    if (dueTime === undefined) dueTime = '';

    document.getElementById('header').innerHTML = `
<h3 class="text-xl font-semibold text-gray-900 dark:text-white truncate h-full">${title}</h3>
<div class="flex mt-2">
     <img class="inline-block mt-2 rounded-lg dark:bg-gray-900 w-12 h-12" src="${pic}" alt="
                                                        ${author}'s profile picture" style="
    margin-right: 10px;
">
                            <img src="${coursepic}" style="margin-left: -30px;margin-top: 40px;margin-right: 10px;" class="inline-block w-6 h-6 rounded-md">

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
    document.getElementById("courseNameForSubmission").innerText = course;
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
