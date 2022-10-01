document.addEventListener('load', function () {
    const datepicker = document.getElementsByClassName('datepicker')[0];
    datepicker.classList.remove('z-20');
    datepicker.classList.add('z-50');
});

function createAssignment() {
    const dateString = document.getElementById('duedate').value + ' ' + document.getElementById('duetime').value;

    if (new Date(dateString).getTime() - Date.now() <= 0 && !confirm("The entered due date is in the past. Continue?"))
        return;

    let assignment = {
        title: document.getElementById('assignmentname').value,
        points: document.getElementById('points').value,
        due: dateString,
        course: course_id,
        description: document.getElementById('description').value
    };
    $.ajax({
        type: 'POST',
        url: '/api/v1/internal/create/assignment',
        data: JSON.stringify(assignment),
        dataType: 'json',
        contentType: 'application/json',
        done() {
            alert('Successfully created assignment');
        }
    });
}
