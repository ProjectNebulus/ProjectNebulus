window.addEventListener('load', function () {
    // document.getElementById("change1").onclick = change1();
    // document.getElementById("change2").onclick = change2();
    // document.getElementById("change3").onclick = change3();
    let inputs = document.getElementsByTagName("input");
    for (let input = 0; input < 3; input++) {
        inputs[input].classList.remove("bg-gray-50", "dark:border-gray-600", "dark:placeholder-gray-400", "dark:text-white")
        inputs[input].classList.add("bg-gray-100", "cursor-not-allowed", "dark:border-gray-600", "dark:placeholder-gray-500", "dark:text-gray-500")
    }
});