window.addEventListener('load', function () {
    const bgCards = document.querySelectorAll('.card img');
    const wallpaper = localStorage.getItem('wallpaper');

    for (const card of bgCards) {
        if (card.src === wallpaper) card.parentElement.classList.add('selected_card');

        card.addEventListener('click', () => {
            if (card.classList.contains('selected_card')) return;

            localStorage.setItem('wallpaper', card.src);
            document.body.style.background = `linear-gradient(rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2)), url('${card.src}') no-repeat center center fixed`;
            document.body.style.backgroundSize = 'cover';
            document.querySelector('.selected_card').classList.remove('.selected_card');
        });
    }

    document.getElementById('no-filter').addEventListener('click', () => {
        localStorage.removeItem('wallpaper');
        document.body.style.backgroundImage = '';
        document.body.style.background = document.documentElement.classList.contains('dark')
            ? '#111926'
            : 'white';
    });

    const sidebarOptions = document.querySelectorAll("aside:not(#sidebar_) li > span");
    const search = location.href.split("#");

    for (const option of sidebarOptions) {
        let opensPage = option.getAttribute("onclick").substring(10);
        opensPage = opensPage.substring(0, opensPage.length - 2);

        option.addEventListener("click", () => {
            if (!option.classList.contains("bg-gray-300"))
                window.location = "#" + opensPage;

            for (const op of sidebarOptions)
                op.classList.remove("bg-gray-300", "dark:bg-gray-600");

            option.classList.add("bg-gray-300", "dark:bg-gray-600");
        });

        if (sidebarOptions[0] !== option && search.length > 1 && opensPage === search[1]) {
            sidebarOptions[0].classList.remove("bg-gray-300", "dark:bg-gray-600");
            option.classList.add("bg-gray-300", "dark:bg-gray-600");
            open_pls(opensPage);
        }
    }
});
