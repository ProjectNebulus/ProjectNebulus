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

        sessionStorage.setItem('{{ course_id }}', title);
    };
}
