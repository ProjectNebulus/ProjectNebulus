//import 'flowbite';
function openModal(object_id) {
    let targetEl = document.getElementById(object_id);
    const options = {
        placement: 'bottom-right',
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
    return true;
}

$("#search").click(function () {
    openModal("searchModal");
});

$("")