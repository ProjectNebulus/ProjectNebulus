import makeCall from '../sectionLoaders/sidebarLoadingManager.js';

function sidebarScrollHandler() {
    let div = $(this).get(0);

    console.log(div.scrollTop + div.clientHeight + 1, div.scrollHeight);
    if (div.scrollTop + div.clientHeight + 1 >= div.scrollHeight) {
        makeCall(false);
        div.scrollTop = div.scrollHeight;
    }
}

export default sidebarScrollHandler;

