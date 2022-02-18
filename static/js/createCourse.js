// set up templates
let divs = document.getElementsByClassName('scroll');
let screens = document.getElementsByClassName('CourseBtn');

// set up button
let modal = document.getElementById('CourseModal');
let btn = document.getElementById('create');

btn.onclick = function () {
    modal.style.display = 'block';

    for (let screen of screens) screen.style.display = 'none';
    screens[0].style.display = 'block';
};

window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};

// set up close button
for (let close of document.getElementsByClassName('close')) {
    close.className += ' material-icons';
    close.innerHTML = 'close';
    close.onclick = function () {
        modal.style.display = 'none';
    };
}

// set up user
const user = document.getElementById('userinfo').innerHTML;

// set up course stuff
let courseName = document.getElementById('course-name');
let courseTeacher = document.getElementById('course-teacher');

function createCourse(subtemplate) {
    document.getElementById('create-course-status').innerHTML = 'Creating course...';

    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/createCourse', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.send(
        JSON.stringify({
            name: document.getElementById('course-name').value,
            teacher: document.getElementById('course-teacher').value,
            template: subtemplate
        })
    );
}

function skipTemplates() {
    screens[0].style.display = "none";
    customize(null, user + "'s class");
    const h1 = document.getElementById("change-if-skip-templates");
    h1.innerHTML = h1.innerHTML.replace("Step 3: ", "");
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
    button.className = 'button';
    button.onclick = function () {
        chooseTemplate(template);
    };

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
    description.style.color = 'gray';
    description.style.fontSize = '0.8em';
    description.innerHTML = 'Subtemplates: ';

    for (const subtemplate of template.subtemplates) description.innerHTML += subtemplate + ', ';
    description.innerHTML = description.innerHTML.substring(0, description.innerHTML.length - 2);

    button.appendChild(description);

    divs[0].appendChild(button);
}

function chooseTemplate(template) {
    screens[0].style.display = 'none';
    screens[1].style.display = 'block';

    divs[1].innerHTML = '';
    for (const subtemplate of template.subtemplates) {
        let button = document.createElement('span');
        button.className = 'button';
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
        button.appendChild(next);

        divs[1].appendChild(button);
    }
}

function customize(template, subtemplate) {
    screens[1].style.display = 'none';
    screens[2].style.display = 'block';

    courseName.placeholder = subtemplate;
    courseTeacher.placeholder = user;

    document.getElementById('create-course').onsubmit = function () {
        createCourse(subtemplate);
    };

    document.getElementById('import-schoology').onclick = importSchoology;
}

function importSchoology() {
    screens[2].style.display = 'none';
    screens[3].style.display = 'block';

    const status = document.getElementById('create-course-status');
    const input = document.getElementById("schoology-id");
    
    document.getElementById('schoology_import').onsubmit = function () {
        var index = input.value.indexOf(".schoology.com/course/");        
      
        if (index == -1) {
            status.style.color = "red";
            status.innerHTML = "Invalid Course Link!";
            return;
        }

        var endIndex;
        for (var endIndex = index + 22; endIndex < input.value.length; endIndex++) {
          if (isNaN(parseInt(input.value.charAt(i))))
            break
        }

        if (endIndex - index < 1) {
            status.style.color = "red";
            status.innerHTML = "Invalid Course Link!";
            return;
        }
        
        const id = input.value.substring(index, endIndex);

        status.innerHTML
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
