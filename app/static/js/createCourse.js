let modal = document.getElementById('CourseModal');

// set up templates
let templateLists = modal.getElementsByClassName('scroll');
let screens = modal.getElementsByClassName('CoursePage');

// set up button
let btn = document.getElementById('create');

for (let screen of screens)
    screen.className += " relative px-4 w-full max-w-2xl relative bg-white rounded-lg shadow dark:bg-gray-700 text-black dark:text-white"

for (let h3 of modal.getElementsByTagName("h3"))
    h3.className += " flex justify-between items-start p-5 rounded-t border-b dark:border-gray-600 text-xl font-semibold text-gray-900 lg:text-2xl dark:text-white"

btn.onclick = function () {
    modal.style.display = 'block';

    screens[0].style.top = "-1000px";
    screens[0].style.animation = "0.5s movein";

    for (let screen of screens) {
        screen.style.display = 'none';
        screen.style.animationFillMode = "forwards";
        screen.style.webkitAnimationFillMode = "forwards";
    }

    screens[0].style.display = 'block';
};

window.onclick = function (event) {
    if (event.target === modal)
        modal.style.display = 'none';
};

// set up close button
for (let close of modal.getElementsByClassName('close')) {
    close.className += ' material-icons dark:text-white';
    close.innerHTML = 'close';
    close.onclick = () => modal.style.display = "none";
}

// set up course stuff
let courseName = document.getElementById('course-name');
let courseTeacher = document.getElementById('course-teacher');

for (const element of modal.getElementsByClassName('CoursePage'))
    element.className += ' hidden overflow-visible fixed right-0 left-0 top-4 z-50 justify-center items-center h-72 md:inset-0';

function createCourse(subtemplate) {
    document.getElementById('create-course-status').innerHTML = 'Creating course...';

    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/createCourse', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(
        JSON.stringify({
            username: user,
            name: document.getElementById('course-name').value,
            teacher: document.getElementById('course-teacher').value,
            template: subtemplate
        })
    );
}

function skipTemplates() {
    screens[0].style.display = 'none';
    customize(null, user + "'s class");
    const h1 = modal.getElementById('change-if-skip-templates');
    h1.innerHTML = h1.innerHTML.replace('Step 3: ', '');
}

const pageCounters = modal.getElementsByClassName("pageCount");
for (let i = 0; i < pageCounters.length; i++) {
    pageCounters[i].className += " flex items-center p-6 space-x-2 rounded-b border-t border-gray-200 dark:border-gray-600";
    for (let j = 0; j < 5; j++) {
        if (j <= i)
            pageCounters[i].innerHTML += "<svg width=\"10\" height=\"10\"><circle cx=\"3\" cy=\"3\" r=\"3\" fill=\"lightgray\"></circle></svg>"
        else
            pageCounters[i].innerHTML += "<svg width=\"10\" height=\"10\"><circle cx=\"3\" cy=\"3\" r=\"3\" fill=\"gray\"></circle></svg>"
    }

    pageCounters[i].style.marginLeft = "38%";
    //position: absolute;
    //     bottom: 0;
    pageCounters[i].style.position = "absolute";
    pageCounters[i].style.bottom ="0";

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
    let button = document.createElement('span');
    button.className = 'createSelectButton text-white focus:ring-4 shadow-lg font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2';
    button.onclick = () => chooseTemplate(template);

    // TODO: fix duplicate code fragments
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
    templateName.innerHTML = template.name;
    button.appendChild(templateName);

    let next = document.createElement('span');
    next = document.createElement('img');
    next.style.float = 'right';
    next.height = 20;
    next.width = 20;
    next.src = 'static/images/icons/next.svg';
    button.appendChild(next);

    button.appendChild(document.createElement('br'));

    let description = document.createElement('span');
    description.classList.add('text-gray-600', 'dark:text-gray-300');
    description.style.fontSize = '0.8em';
    description.innerHTML = '';

    for (let i = 0; i < Math.min(template.subtemplates.length, 4); i++)
        description.innerHTML += template.subtemplates[i] + ', ';

    if (template.subtemplates.length > 4)
        description.innerHTML += "etc."
    else
        description.innerHTML = description.innerHTML.substring(0, description.innerHTML.length - 2);

    button.appendChild(description);

    templateLists[0].appendChild(button);
}

function chooseTemplate(template) {
    screens[0].style.display = 'none';
    screens[1].style.display = 'block';

    templateLists[1].innerHTML = '';
    for (const subtemplate of template.subtemplates) {
        let button = document.createElement('span');
        button.className = 'createSelectButton text-white focus:ring-4 shadow-lg font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2';
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
        next.alt = "Next";
        button.appendChild(next);

        templateLists[1].appendChild(button);
    }
}

function customize(template, subtemplate) {
    screens[1].style.display = 'none';
    screens[2].style.display = 'block';

    courseName.placeholder = subtemplate;
    courseTeacher.placeholder = user;

    document.getElementById('create-course').onsubmit = () => createCourse(subtemplate);

    document.getElementById('import-schoology').onclick = importSchoology;
    document.getElementById('import-classroom').onclick = importGClassroom;
    document.getElementById('import-canvas').onclick = importCanvas;
}

function importGClassroom() {
    screens[2].style.display = 'none';
    screens[4].style.display = 'block';
}

function importCanvas() {
    screens[2].style.display = 'none';
    screens[5].style.display = 'block';
}

function importSchoology() {
    screens[2].style.display = 'none';
    screens[3].style.display = 'block';

    const status = document.getElementById('create-course-status');
    const input = document.getElementById('schoology-id');

    document.getElementById('schoology_import').onsubmit = function () {
        // todo: maybe this needs regex instead of whatever this is
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
        xhttp.open('POST', '/createCourseSchoology', true);
        xhttp.setRequestHeader('Content-type', 'application/json');
        xhttp.send(
            JSON.stringify({
                schoology: id
            })
        );
    };
}
