window.addEventListener('load', function () {
    let inputs = document.getElementsByTagName("input");
    for (let input = 0; input < inputs.length; input++) {
        inputs[input].classList.remove("bg-gray-50", "pl-10", "dark:border-gray-600", "dark:placeholder-gray-400", "dark:text-white")
        inputs[input].classList.add("bg-gray-100", "cursor-not-allowed", "dark:border-gray-600", "dark:placeholder-gray-500", "dark:text-gray-500")
    }
});