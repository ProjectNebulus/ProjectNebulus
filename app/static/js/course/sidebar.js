for (const a of document.querySelectorAll("a[target=frame]")) {
    a.href += '?iframe=true';
    a.onclick = () => {
        window.history.pushState(null, '', a.href.replace('?iframe=true', ''));

        for (const link of document.querySelectorAll("a[target=frame]")) {
            if (link === a) continue;

            link.style.pointerEvents = 'auto';
            link.style.cursor = 'pointer';
            link.classList.remove('dark:bg-gray-600', 'light:bg-gray-600');
        }

        let title = a.href
            .substring(a.href.indexOf(document.documentURI))
            .split('/')[5]
            .replace('?iframe=true', '');
        title = title[0].toUpperCase() + title.substring(1);
        pageTitle.innerHTML = title;
        setCreateButton(title);

        a.style.pointerEvents = 'none';
        a.style.cursor = 'default';
        a.classList.add('dark:bg-gray-600', 'light:bg-gray-600');
    };
}

{
    const syncButton = document.getElementById("sync-lms");
    const syncText = syncButton.querySelector("span.ml-3");
    syncButton.addEventListener("click", () => {
        syncButton.disabled = true;
        syncText.innerText = "Syncing...";

        const xhttp = new XMLHttpRequest();
        xhttp.open('POST', '/api/v1/internal/sync/course/' + syncFrom, true);
        xhttp.setRequestHeader('Content-type', 'application/json');
        const data = {link: "app.schoology.com/course/" + syncID};
        xhttp.send(JSON.stringify(data));


        xhttp.addEventListener("readystatechange", () => {
            if (xhttp.readyState !== XMLHttpRequest.DONE)
                return;

            const status = xhttp.status;
            if (status === 0 || (status >= 200 && status < 400))
                syncText.innerText = "Sync Complete!";
            else
                syncText.innerText = "Sync failed!";

            setTimeout(() => syncText.innerText = "LMS Sync", 2000);
            setTimeout(() => syncText.disabled = false, 10000);
        });
    });
}