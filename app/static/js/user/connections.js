{
    let lastOpenTime = 0, lastShowTime = 0, key, name;

    function setContents(data) {
        data = data.split("\n");

        document.getElementById("key-name").value = key;
        document.getElementById("api-key").value = data[0];
        document.getElementById("api-secret").value = data[1];
    }

    bindFunc("[key]", el => {
        openModal('key-modal')

        if (Date.now() - lastOpenTime < 1000 * 60 * 60)
            return;

        setContents("Loading...\nLoading...")

        lastOpenTime = Date.now();
        key = el.getAttribute("key");
        name = el.parentElement.querySelector("div > div > h5").innerText;

        const req = $.ajax({
            type: "GET",
            url: "/api/v1/internal/get/api-keys/" + key.toLowerCase(),
            contentType: "application/json",
            data: {name: name, hide: true}
        });

        req.done(setContents);
        req.fail((req, status, error) => setContents(req.status + " " + error.toLowerCase() + "\n"))
    });

    bindFunc("#show", el => {
        const secret = document.getElementById("api-secret");
        if (secret.type === "password") {
            secret.type = "text";
            el.innerText = "visibility_off";
        } else {
            secret.type = "password";
            el.innerText = "visibility";
        }

        if (Date.now() - lastShowTime < 1000 * 60 * 60)
            return;

        secret.value = "Loading...";

        lastShowTime = Date.now();

        const req = $.ajax({
            type: "GET",
            url: "/api/v1/internal/get/api-keys/" + key.toLowerCase(),
            contentType: "application/json",
            data: JSON.stringify({name: name})
        });

        req.done(setContents);
        req.fail((req, status, error) => setContents(req.status + " " + error.toLowerCase() + "\n"))
    });

    bindFunc("#key-modal .button-styling:not(#show)", el => {
        const siblings = $(el).siblings();
        const input = siblings[siblings.length - 1];
        if (input.type === "text")
            copy(el, input.value);
    });

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
}