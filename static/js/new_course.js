function setUpStuff() {}

function newCourse() {
    const xhttp = new XMLHttpRequest();
    xhttp.open('POST', '/new', true);
    xhttp.setRequestHeader('Content-type', 'application/json');
    xhttp.addEventListener('load', reqListener);
    xhttp.send(
        JSON.stringify({
            name: document.getElementById('name').value,
            teacher: document.getElementById('teacher').value
        })
    );
}

function reqListener() {
    let text = document.getElementById('result');
    text.innerHTML = 'Course Created!';
    text.style.color = 'greenyellow';
    window.location.href = '/dashboard';
}
