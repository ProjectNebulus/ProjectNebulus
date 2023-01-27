let override = false;

document.addEventListener("click", (e) => {
    if (override) {
        override = false;
        e.preventDefault();
    }
})

bindFunc("[title*=Copy]", courseElement => {
    courseElement = courseElement.parentElement.parentElement.parentElement;
    let id = courseElement.getAttribute("id");

    const header = courseElement.querySelector("div.text-left div.-mt-1");

    if (!confirm('Delete course "' + header.children[0].innerText.trim() + '"? This is irreversible!')) return;
    header.children[1].innerText = "Deleting...";

    let deleteETA = Math.floor(parseInt(courseElement.getAttribute("total-resources")) * 0.4);

    if (deleteETA) {
        let interval = setInterval(() => {
            header.children[1].innerText = "Deleting (ETA: " + (Math.floor(deleteETA / 60) + "").padStart(2, "0") +
                ":" + (deleteETA % 60 + "").padStart(2, "0") + ")";
            deleteETA--;

            if (deleteETA < -1) {
                clearInterval(interval);
                courseElement.parentElement.remove();
            }
        }, 1000);
    } else
        courseElement.parentElement.remove();

    $.ajax({
        type: "POST",
        url: "/api/v1/internal/delete/course",
        data: JSON.stringify({
            course: id,
        }),

        contentType: 'application/json; charset=utf-8',
    });
});

bindFunc("[title*=Delete]", element => {
    const id = element.parentElement.parentElement.parentElement.getAttribute("id");
    element.disabled = true;

    navigator.clipboard.writeText(id).then(
        () => {
            element.style.color = "#00AA00";
            element.innerHTML = "done";

            setTimeout(() => {
                element.innerHTML = "content_copy";
                element.style.color = "";
            }, 2000);
        },
        () => {
            element.style.color = "#FF7777";
            element.innerHTML = "error";

            setTimeout(() => {
                element.innerHTML = "content_copy";
                element.style.color = "";
            }, 2000);
        }
    );
});

bindFunc("[title*=Sync]", element => {
    const id = element.parentElement.parentElement.parentElement.getAttribute("id");
    element.disabled = true;
    element.innerHTML = loadingIcon(5, 5);

    const req = $.ajax({
        url: "/api/v1/internal/sync/course/schoology",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({link: "app.schoology.com/course/" + id})
    });

    req.done(() => {
        element.disabled = false;
        element.style.color = "#00AA00";
        element.innerHTML = "done";

        setTimeout(() => {
            element.innerHTML = "sync";
            element.style.color = "";
        }, 2000);
    });

    req.fail(() => {
        element.disabled = false;
        element.style.color = "#FF7777";
        element.innerHTML = "error";

        setTimeout(() => {
            element.innerHTML = "sync";
            element.style.color = "";
        }, 2000);
    });
});

for (const el of document.getElementsByTagName("img")) {
    if (!validImage(el))
        el.style.display = "none";
}

function validImage(img) {
    return img.naturalWidth > 0 && img.naturalHeight > 0 && img.complete;
}