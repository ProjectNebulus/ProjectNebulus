document.addEventListener("DOMContentLoaded", function (event) {
    import 'flowbite';

    function openModal(object_id) {
        let targetEl = document.getElementById(object_id);
        const options = {
            placement: 'bottom-right',
            backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40',
            onHide: () => {
                console.log('modal is hidden');
            },
            onShow: () => {
                console.log('modal is shown');
            },
            onToggle: () => {
                console.log('modal has been toggled');
            }
        };
        const modal = new Modal(targetEl, options);
        modal.show();
        return true;

    }

    function closeModal(object_id) {
        let targetEl = document.getElementById(object_id);
        const options = {
            placement: 'bottom-right',
            backdropClasses: 'bg-gray-900 bg-opacity-50 dark:bg-opacity-80 fixed inset-0 z-40',
            onHide: () => {
                console.log('modal is hidden');
            },
            onShow: () => {
                console.log('modal is shown');
            },
            onToggle: () => {
                console.log('modal has been toggled');
            }
        };
        const modal = new Modal(targetEl, options);
        modal.hide();
        return true;


    }
});
