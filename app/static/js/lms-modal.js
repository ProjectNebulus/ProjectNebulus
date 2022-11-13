document.getElementById("extraWidgets").innerHTML = `
<button id="create" class="hidden sm:flex items-center text-left space-x-3 w-16 h-12 bg-gray-300 ring-1
 ring-slate-900/10 hover:ring-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 shadow-sm rounded-lg
 dark:bg-slate-800/75 dark:ring-0 dark:text-slate-300 dark:highlight-white/5 dark:hover:bg-gray-500
   text-gray-600 font-medium rounded-lg text-sm pl-4 py-2.5 text-center">
    <span style="font-size:30px;" class="material-icons">add</span>
</button>`

window.addEventListener("load", setUpFunc);

let setup = false;

function setUpFunc() {
    let modal = document.getElementById('courseModal');
    let templateLists = modal.getElementsByClassName('scroll');

    let screens = modal.getElementsByClassName('CoursePage');

    // set up button
    let btn = document.getElementById('create');

    for (const screen of screens)
        screen.className +=
            ' relative w-full max-w-2xl relative bg-gray-200 rounded-lg shadow dark:bg-gray-800 text-black dark:text-white';

    for (const h3 of modal.getElementsByTagName('h3'))
        h3.className +=
            ' flex justify-between items-start pb-4 rounded-t border-b border-gray-300 dark:border-gray-600 text-xl font-semibold text-gray-900 text-2xl dark:text-white';

    for (const list of templateLists) list.classList.add('scroll');

    btn.onclick = function () {
        if (modal.style.display === "block")
            return;

        modal.style.display = 'block';
        for (let screen of [...screens, ...document.querySelectorAll("#courseModal form:not(#create-course)")])
            screen.style.display = 'none';

        for (let screen of document.querySelectorAll("#course-list, #glist, #clist"))
            screen.style.display = 'block';

        screens[0].style.display = 'block';

        if (setup)
            return;

        setup = true;

        const req = $.ajax({
            url: '/import-course',
            type: 'POST',
            contentType: 'application/json',
        })

        req.done(data => {
            document.getElementById("courseModal").innerHTML += data;
            setUpFunc();
        });

        req.fail(() => setup = false);
    };

    // set up close button
    for (let close of modal.getElementsByClassName('close')) {
        close.className += ' material-icons dark:text-white';
        close.innerHTML = 'close';
        close.onclick = () => modal.style.display = 'none';
    }

    // set up course stuff
    let courseName = document.getElementById('course-name');
    let courseTeacher = document.getElementById('course-teacher');

    for (const element of modal.getElementsByClassName('CoursePage'))
        element.className +=
            ' hidden overflow-visible fixed right-0 left-0 top-4 z-50 justify-center items-center h-72 md:inset-0 duration-500';

    function lms(subtemplate) {
        for (const el of document.getElementsByClassName("create-course-status"))
            el.innerHTML = "Creating course...";

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
        xhttp.addEventListener("load", () => {
            for (const el of document.getElementsByClassName("create-course-status"))
                el.innerHTML = "Course created!";
        })
    }

    function skipTemplates() {
        screens[0].style.display = 'none';
        customize(null, user + "'s class");
        const h1 = document.getElementById('change-if-skip-templates');
        h1.innerHTML = h1.innerHTML.replace('Step 3: ', '');
        h1.querySelector(".close").addEventListener("click", () => modal.style.display = "none");
    }

    document.getElementById('skip-templates').addEventListener('click', skipTemplates);

    const pageCounters = modal.getElementsByClassName('pageCount');
    if (pageCounters[0].classList.length === 0) {
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
    }

    /*

    To create a new template, add a new dictionary and put the parameters:

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
            'cursor-pointer flex justify-between place-items-center text-white bg-gray-500 dark:hover:bg-gray-700 dark:bg-gray-900 font-medium rounded-lg text-lg px-5 py-3 text-center mr-2 mb-2';
        button.addEventListener("click", () => chooseTemplate(template));

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
                'cursor-pointer text-white bg-gray-500 dark:hover:bg-gray-700 dark:bg-gray-900 font-medium rounded-lg text-lg px-5 py-3 text-center mr-2 mb-2';
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

        document.getElementById('create-course').onsubmit = () => {
            lms(subtemplate);
            return false;
        };
    }
}


function createSchoologyCourse() {
    const input = document.getElementById('schoology-course-id');
    const teacher = document.getElementById('schoology-course-teacher');
    const status = document.getElementById("schoology-import-status");
    const submitButton = document.querySelector("#schoology-create-course button[type=submit]");
    status.style.color = "gray";
    status.innerHTML = "Creating course...";
    submitButton.disabled = true;

    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/v1/internal/create/course/schoology', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(
        JSON.stringify({
            link: input.value,
            teacher: teacher.value,
            profile_url: schoologyCoursePic,
        })
    );
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState === 4) {
            if (xhttp.status === 200) {
                status.style.color = "greenyellow";
                status.innerHTML = "Course created!";
                window.location.href = xhttp.responseText;
            } else {
                status.style.color = "red";
                status.innerHTML = "An error occurred!";
                submitButton.disabled = false;
            }
        }
    }
}

function createGoogleCourse() {
    const input = document.getElementById('google-course-id');
    const teacher = document.getElementById('google-course-teacher');

    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/v1/internal/create/course/google', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(
        JSON.stringify({
            link: input.value,
            teacher: teacher.value,
        })
    );
}


function createCanvasCourse() {
    const input = document.getElementById('canvas-course-id');
    const teacher = document.getElementById('canvas-course-teacher');

    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/v1/internal/create/course/canvas', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(
        JSON.stringify({
            link: input.value,
            teacher: teacher.value,
        })
    );
    xhttp.addEventListener("load", () => window.location.href = xhttp.response);
}

function importSchoologyAll() {
    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/api/v1/internal/create/course/schoology/all', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
}

function importSchoology() {
    let modal = document.getElementById('courseModal');
    let screens = modal.getElementsByClassName('CoursePage');

    if (screens.length < 4)
        return;

    screens[2].style.display = 'none';
    screens[3].style.display = 'block';
}

function importCanvas() {
    let modal = document.getElementById('courseModal');
    let screens = modal.getElementsByClassName('CoursePage');

    if (screens.length < 4)
        return;

    screens[2].style.display = 'none';
    screens[5].style.display = 'block';
}


function importGClassroom() {
    let modal = document.getElementById('courseModal');
    let screens = modal.getElementsByClassName('CoursePage');

    if (screens.length < 4)
        return;

    screens[2].style.display = 'none';
    screens[4].style.display = 'block';
}


function updateCanvasLink(link) {
    document.getElementById('active-course-header').innerHTML = "Create Course";
    document.getElementById('canvas-course-id').value = link;
    document.getElementById('clist').style.display = 'none';
    document.getElementById('canvas-create-course').style.display = 'block';
}

function updateGoogleLink(link, teacher) {
    document.getElementById('active-course-header').innerHTML = "Create Course";
    document.getElementById('google-course-id').value = link;
    document.getElementById('google-course-teacher').value = teacher;
    document.getElementById('glist').style.display = 'none';
    document.getElementById('google-create-course').style.display = 'block';
}

let schoologyCoursePic;

function updateSchoologyLink(link, coursePic) {
    schoologyCoursePic = coursePic;
    document.getElementById('active-course-header').innerHTML = "Create Course";
    document.getElementById('schoology-course-id').value = link;
    document.getElementById('course-list').style.display = 'none';
    document.getElementById('schoology-create-course').style.display = 'block';
}

