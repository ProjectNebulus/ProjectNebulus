let openDropdown = null;
let justOpened = false;
let dropdowns = document.getElementsByTagName("dropdown-menu");

window.addEventListener("load", setUpDropdowns);
window.addEventListener("click", function () {
    if (justOpened) {
        justOpened = false;
        return;
    }

    if (openDropdown !== null) {
        openDropdown.style.visibility = "hidden";
        openDropdown = null;
    }
});
window.addEventListener("resize", function () {
    for (const menu of dropdowns) {
        let trigger = menu.getElementsByTagName("trigger")[0].getBoundingClientRect(),
            contents = menu.getElementsByTagName("contents")[0],
            rightAlign = menu.getAttribute("align") !== "left";

        if (rightAlign) {
            contents.style.left = (trigger.left - contents.getBoundingClientRect().width / 2).toString();
            contents.style.top = (trigger.top + trigger.height).toString();
        }
    }
});

function setUpDropdowns() {
    for (const menu of dropdowns) {
        let trigger = menu.getElementsByTagName("trigger")[0],
            contents = menu.getElementsByTagName("contents")[0],
            items = contents.getElementsByTagName("item"),

            rightAlign = menu.getAttribute("align") !== "left";

        for (let item of items) {
            const link = item.getAttribute("href");
            if (link !== null) {
                let target = item.getAttribute("target");
                if (target === null)
                    target = "_self";

                item.addEventListener("click", () => window.open(link, target));
                item.style.cursor = "pointer";
            }
        }

        trigger.addEventListener("click", function () {
            if (contents.style.visibility === "hidden") {
                contents.style.visibility = "visible";
                justOpened = true;
                openDropdown = contents;
            }
            else {
                contents.style.visibility = "hidden";
                openDropdown = null;
            }
        });

        let cRect = contents.getBoundingClientRect();
        let tRect = trigger.getBoundingClientRect();

        if (rightAlign) {
            contents.style.left = (cRect.left - cRect.width + tRect.width * 2).toString();
            contents.style.top = (cRect.top + tRect.height).toString();
        }

        for (let i = 0; i < contents.childElementCount - 1; i++) {
            if (contents.children[i].nodeName === "HR")
                continue;

            i += 1;
            contents.children[i].insertAdjacentHTML("afterend", "<br>");
        }
    }
}