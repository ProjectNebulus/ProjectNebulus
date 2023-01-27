{
    let lastCallTime = 0, key;

    function setContents(data) {
        data = data.split("\n");

        document.getElementById("key-name").value = key;
        document.getElementById("api-key").value = data[0];
        document.getElementById("api-secret").value = data[1];
    }

    bindFunc("[key]", el => {
        openModal('key-modal');

        if (Date.now() - lastCallTime < 1000 * 60 * 60)
            return;

        lastCallTime = Date.now();
        key = el.getAttribute("key");
        setContents(key, "Loading...\nLoading...")

        const req = $.ajax({
            type: "GET",
            url: "/api/v1/internal/get/api-keys/" + key.toLowerCase(),
            contentType: "application/json",
            data: JSON.stringify({name: el.parentElement.querySelector("div > div > h5").innerText})
        });

        req.done(setContents);
        req.fail((req, status, error) => setContents(req.status + " " + error.toLowerCase() + "\n"))
    });
}

keyUpDelay("#graderoom-key", 1000, () => {
    let data = document.getElementById("graderoom-key").value;
    const fail = document.getElementById("graderoom-pair-fail");
    fail.innerHTML = "<br>";

    if (data.length === 6) {
        $.ajax({
            type: 'GET',
            url: '/api/v1/internal/oauth/graderoom/connect',
            data: {
                graderoom_key: data
            }
        }).done(info => {
            if (info.includes("pairing key"))
                fail.innerText = info;
            else
                location.reload()
        });
    }
});