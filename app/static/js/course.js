//import 'flowbite';
function openModal(object_id) {
    let targetEl = document.getElementById(object_id);
    const options = {
        placement: 'center',
        backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40'
    };
    const modal = new Modal(targetEl, options);
    modal.show();
    return true;
}

function closeModal(object_id) {
    let targetEl = document.getElementById(object_id);
    const options = {
        placement: 'bottom-right',
        backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40'
    };
    const modal = new Modal(targetEl, options);
    modal.hide();

    for (const element of document.querySelectorAll("[modal-backdrop]"))
        element.parentElement.removeChild(element);

    return true;
}

$("#search").click(function () {
    openModal("searchModal");
});

$("#upload-file").click(function () {
    alert('Uploaded');
    var formData = new FormData();
    let fileupload = document.getElementById("file");
    formData.append("file", fileupload.files[0]);
    formData.append("course", document.getElementById("course_id").innerText);
    formData.append("folder", "0");
    let request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/upload_file",
        processData: false,
        contentType: false,
        data: formData
    });

    request.done(function (data) {
        alert('Uploaded :)');
        alert(data);
    });
});