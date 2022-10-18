document.getElementById("extraWidgets").innerHTML = `
<button id="create" class="hidden sm:flex items-center text-left space-x-3 w-16 h-12 bg-white ring-1
 ring-slate-900/10 hover:ring-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 shadow-sm rounded-lg
  text-slate-400 dark:bg-slate-800/75 dark:ring-0 dark:text-slate-300 dark:highlight-white/5 dark:hover:bg-gray-500
   text-white font-medium rounded-lg text-sm pl-4 py-2.5 text-center">
    <span style="font-size:30px;" class="material-icons">add</span>
</button>`

window.addEventListener('load', () => {
    let modal = document.getElementById('courseModal');

    // set up templates
    let templateLists = modal.getElementsByClassName('scroll');

    let screens = modal.getElementsByClassName('CoursePage');

    // set up button
    let btn = document.getElementById('create');

    for (const screen of screens)
        screen.className +=
            ' relative px-4 w-full max-w-2xl relative bg-gray-200 rounded-lg shadow dark:bg-gray-800 text-black dark:text-white';

    for (const h3 of modal.getElementsByTagName('h3'))
        h3.className +=
            ' flex justify-between items-start p-5 rounded-t border-b border-gray-300 dark:border-gray-600 text-xl font-semibold text-gray-900 lg:text-2xl dark:text-white';

    for (const list of templateLists) list.classList.add('scroll');

    btn.onclick = function () {
        modal.style.display = 'block';

        screens[0].style.top = '-1000px';
        screens[0].style.animation = '0.5s movein';

        for (let screen of screens) {
            screen.style.display = 'none';
            screen.style.animationFillMode = 'forwards';
            screen.style.webkitAnimationFillMode = 'forwards';
        }

        screens[0].style.display = 'block';
    };

    window.onclick = function (event) {
        if (event.target === modal) modal.style.display = 'none';
    };

    // set up close button
    for (let close of modal.getElementsByClassName('close')) {
        close.className += ' material-icons dark:text-white';
        close.innerHTML = 'close';
        close.onclick = () => (modal.style.display = 'none');
    }

    // set up course stuff
    let courseName = document.getElementById('course-name');
    let courseTeacher = document.getElementById('course-teacher');

    for (const element of modal.getElementsByClassName('CoursePage'))
        element.className +=
            ' hidden overflow-visible fixed right-0 left-0 top-4 z-50 justify-center items-center h-72 md:inset-0';

    function lms(subtemplate) {
        document.getElementById('create-course-status').innerHTML = 'Creating course...';

        const xhttp = new XMLHttpRequest();
        xhttp.open('POST', '/lms', true);
        xhttp.setRequestHeader('Content-type', 'application/json');
        xhttp.send(
            JSON.stringify({
                name: document.getElementById('course-name').value,
                teacher: document.getElementById('course-teacher').value,
                avatar: 'https://app.schoology.com/sites/all/themes/schoology_theme/images/course-default.svg',
                template: subtemplate
            })
        );
    }

    function skipTemplates() {
        screens[0].style.display = 'none';
        customize(null, user + "'s class");
        const h1 = document.getElementById('change-if-skip-templates');
        h1.innerHTML = h1.innerHTML.replace('Step 3: ', '');
    }

    document.getElementById('skip-templates').addEventListener('click', skipTemplates);

    const pageCounters = modal.getElementsByClassName('pageCount');

    for (const i in pageCounters) {
        pageCounters[i].className += ' flex items-center p-6 space-x-2 absolute bottom-0';
        for (let j = 0; j < 3; j++) {
            if (j === i)
                pageCounters[i].innerHTML +=
                    "<div class='rounded-full w-2 h-2 bg-gray-400 dark:bg-gray-500'></div>";
            else
                pageCounters[i].innerHTML +=
                    "<div class='rounded-full w-2 h-2 bg-gray-300 dark:bg-gray-400'></div>";
        }

        try {
            pageCounters[i].setAttribute('style', 'transform: translate(300%)');
        } catch (e) {
        }
    }

    /*

    To course a new template, add a new dictionary and put the parameters:

    name (e.g. Science)
    icon (e.g. science.svg)
    description (e.g. Physics, Chemistry, Biology)

    as demonstrated below.

    */
    const templates = [
        {
            name: 'Science',
            icon: 'science.svg',
            subtemplates: [
                'Introduction to Science',
                'Physics',
                'Chemistry',
                'Biology',
                'Astronomy',
                'Life Science',
                'Earth Science',
                'Physical Science',
                'Physical Geography',
                'Computer Science',
                'Programming',
                'Coding'
            ]
        },

        {
            name: 'Mathematics',
            icon: 'math.svg',
            subtemplates: [
                'K-8th Math',
                'Pre-Algebra',
                'Algebra I',
                'Algebra II',
                'Pre-Calculus A/B/AB',
                'Calculus AB/BC',
                'AP Statistics',
                'AP Calculus',
                'Competitive Math'
            ]
        },

        {
            name: 'History',
            icon: 'history.svg',
            subtemplates: [
                'Social Studies',
                'World History I/II',
                'US History',
                'AP World History',
                'AP US History'
            ]
        },

        {
            name: 'Art',
            icon: 'art.svg',
            subtemplates: ['Visual Arts', 'Music', 'Drama']
        },

        {
            name: 'Language',
            icon: 'language.svg',
            subtemplates: ['English', 'Latin', 'Spanish', 'French', 'Mandarin', 'German']
        },

        {
            name: 'Sports',
            icon: 'sport.svg',
            subtemplates: [
                'PE',
                'Basketball',
                'Soccer',
                'Ice Hockey',
                'Volleyball',
                'Track and Field',
                'Football',
                'Tennis',
                'Dance'
            ]
        }
    ];

    for (const template of templates) {
        let button = document.createElement('div');
        button.className =
            'createSelectButton flex justify-between place-items-center text-white bg-gray-500 dark:hover:bg-gray-800 dark:bg-gray-900 font-medium rounded-lg text-lg px-5 py-5 text-center mr-2 mb-2';
        button.onclick = () => chooseTemplate(template);

        let imageSpan = document.createElement('span');

        let image = document.createElement('img');
        image.height = 40;
        image.width = 40;
        image.src = 'static/images/icons/' + template.icon;
        imageSpan.appendChild(image);

        button.appendChild(imageSpan);

        let templateName = document.createElement('span');
        templateName.innerHTML = template.name + "<br>";

        let description = document.createElement('span');
        description.classList.add('text-gray-300', 'text-sm');
        description.innerHTML += 'Includes: ';
        for (let i = 0; i < Math.min(template.subtemplates.length, 4); i++)
            description.innerHTML += template.subtemplates[i] + ', ';

        if (template.subtemplates.length > 4) description.innerHTML += 'etc.';
        else
            description.innerHTML = description.innerHTML.substring(
                0,
                description.innerHTML.length - 2
            );

        templateName.appendChild(description);

        button.appendChild(templateName);

        let next = document.createElement('span');
        next = document.createElement('img');
        next.style.float = 'right';
        next.height = 40;
        next.width = 40;
        next.src = 'static/images/icons/next.svg';
        button.appendChild(next);

        button.appendChild(document.createElement('br'));

        templateLists[0].appendChild(button);
    }

    function chooseTemplate(template) {
        screens[0].style.display = 'none';
        screens[1].style.display = 'block';

        templateLists[1].innerHTML = '';
        for (const subtemplate of template.subtemplates) {
            let button = document.createElement('div');
            button.className =
                'createSelectButton text-white bg-gray-500 dark:hover:bg-gray-800 dark:bg-gray-900 font-medium rounded-lg text-lg px-5 py-5 text-center mr-2 mb-2';
            button.onclick = function () {
                const name = template.name;
                customize(name, subtemplate);
            };

            let imageSpan = document.createElement('span');
            imageSpan.style.float = 'left';

            let image = document.createElement('img');
            image.style.float = 'right';
            image.height = 20;
            image.width = 20;
            image.src = 'static/images/icons/' + template.icon;
            imageSpan.appendChild(image);

            button.appendChild(imageSpan);

            let templateName = document.createElement('span');
            templateName.innerHTML = subtemplate;
            button.appendChild(templateName);

            let next = document.createElement('span');
            next = document.createElement('img');
            next.style.float = 'right';
            next.height = 20;
            next.width = 20;
            next.src = 'static/images/icons/next.svg';
            next.alt = 'Next';
            button.appendChild(next);

            templateLists[1].appendChild(button);
        }
    }

    function customize(template, subtemplate) {
        screens[1].style.display = 'none';
        screens[2].style.display = 'block';

        courseName.placeholder = subtemplate;
        courseTeacher.placeholder = user;

        document.getElementById('create-course').onsubmit = () => lms(subtemplate);

        document.getElementById('import-schoology').onclick = importSchoology;
        document.getElementById('import-classroom').onclick = importGClassroom;
        document.getElementById('import-canvas').onclick = importCanvas;
    }
});

function schoologyCourseReq() {
    const status = document.getElementById('create-course-status2');
    if (this.responseText === '1') {
        status.style.color = 'red';
        status.innerHTML =
            'You have not connected your schoology account! Please connect a schoology account to import courses from Schoology.';
    } else {
        status.style.color = 'green';
        status.innerHTML = 'Course created!';
    }
}

function googleCourseReq() {
    const status = document.getElementById('create-course-status2');
    if (this.responseText === '1') {
        status.style.color = 'red';
        status.innerHTML =
            'You have not connected your google account! Please connect a schoology account to import courses from Schoology.';
    } else {
        status.style.color = 'green';
        status.innerHTML = 'Course created!';
    }
}

function canvasCourseReq() {
    const status = document.getElementById('create-course-status2');
    if (this.responseText === '1') {
        status.style.color = 'red';
        status.innerHTML =
            'You have not connected your canvas account! Please connect a schoology account to import courses from Schoology.';
    } else {
        status.style.color = 'green';
        status.innerHTML = 'Course created!';
    }
}

function importSchoology() {
    let modal = document.getElementById('courseModal');
    let screens = modal.getElementsByClassName('CoursePage');
    screens[2].style.display = 'none';
    screens[3].style.display = 'block';

    const status = document.getElementById('create-course-status2');
    const input = document.getElementById('schoology-course-id');
    const teacher = document.getElementById('schoology-course-teacher');

    const index = input.value.indexOf('.schoology.com/course/');

    if (index === -1) {
        status.style.color = 'red';
        status.innerHTML = 'Invalid Course Link!';
        return;
    }

    let endIndex;
    for (endIndex = index + 22; endIndex < input.value.length; endIndex++) {
        if (isNaN(parseInt(input.value.charAt(endIndex)))) break;
    }

    if (endIndex - index < 1) {
        status.style.color = 'red';
        status.innerHTML = 'Invalid Course Link!';
        return;
    }

    const id = input.value.substring(index, endIndex);

    status.innerHTML;
    status.innerHTML = 'Creating course...';

    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/v1/internal/create/course/schoology', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.addEventListener('load', schoologyCourseReq);
    xhttp.send(
        JSON.stringify({
            link: input.value,
            teacher: teacher.value
        })
    );
}


function importCanvas() {
    screens[2].style.display = 'none';
    screens[5].style.display = 'block';
    const status = document.getElementById('create-course-status2');
    const input = document.getElementById('canvas-course-id');
    const teacher = document.getElementById('canvas-course-teacher');

    const index = input.value.indexOf('/course/');

    if (index === -1) {
        status.style.color = 'red';
        status.innerHTML = 'Invalid Course Link!';
        return;
    }

    let endIndex;
    for (endIndex = index + 22; endIndex < input.value.length; endIndex++) {
        if (isNaN(parseInt(input.value.charAt(endIndex)))) break;
    }

    if (endIndex - index < 1) {
        status.style.color = 'red';
        status.innerHTML = 'Invalid Course Link!';
        return;
    }

    const id = input.value.substring(index, endIndex);

    status.innerHTML;
    status.innerHTML = 'Creating course...';

    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/v1/internal/create/course/canvas', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.addEventListener('load', canvasCourseReq);
    xhttp.send(
        JSON.stringify({
            link: input.value,
            teacher: teacher.value
        })
    );
}


function importGClassroom() {
    screens[2].style.display = 'none';
    screens[4].style.display = 'block';
    const status = document.getElementById('create-course-status2');
    const input = document.getElementById('google-course-id');
    const teacher = document.getElementById('google-course-teacher');

    const index = input.value.indexOf('classroom.google.com/c/');

    if (index === -1) {
        status.style.color = 'red';
        status.innerHTML = 'Invalid Course Link!';
        return;
    }

    let endIndex;
    for (endIndex = index + 22; endIndex < input.value.length; endIndex++) {
        if (isNaN(parseInt(input.value.charAt(endIndex)))) break;
    }

    if (endIndex - index < 1) {
        status.style.color = 'red';
        status.innerHTML = 'Invalid Course Link!';
        return;
    }

    const id = input.value.substring(index, endIndex);

    status.innerHTML;
    status.innerHTML = 'Creating course...';

    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/v1/internal/create/course/google', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.addEventListener('load', googleCourseReq);
    xhttp.send(
        JSON.stringify({
            link: input.value,
            teacher: teacher.value
        })
    );
}


function updateCanvasLink(link) {
    document.getElementById('canvas-course-id').value = link;
    document.getElementById('clist').style.display = 'none';
    document.getElementById('canvas-create-course').style.display = 'block';
}

function updateGoogleLink(link, teacher) {
    document.getElementById('google-course-id').value = link;
    document.getElementById('google-course-teacher').value = teacher;
    document.getElementById('glist').style.display = 'none';
    document.getElementById('google-create-course').style.display = 'block';
}

function updateSchoologyLink(link) {
    document.getElementById('schoology-course-id').value = link;
    document.getElementById('slist').style.display = 'none';
    document.getElementById('schoology-create-course').style.display = 'block';
}

