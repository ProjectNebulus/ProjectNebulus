function change1() {
    let inputs = document.getElementsByTagName("input");
    inputs[0].classList.remove("bg-gray-100", "cursor-not-allowed", "dark:border-gray-600", "dark:placeholder-gray-500", "dark:text-gray-500")
    inputs[0].classList.add("bg-gray-50", "dark:border-gray-600", "dark:placeholder-gray-400", "dark:text-white")
    inputs[0].disabled = false;
    document.getElementById("change1").innerText = "Change Username"
}

function change2() {
    let inputs = document.getElementsByTagName("input");
    inputs[1].classList.remove("bg-gray-100", "cursor-not-allowed", "dark:border-gray-600", "dark:placeholder-gray-500", "dark:text-gray-500")
    inputs[1].classList.add("bg-gray-50", "dark:border-gray-600", "dark:placeholder-gray-400", "dark:text-white")
    inputs[1].disabled = false;
    document.getElementById("change2").innerText = "Change Password"
}

function change3() {
    let inputs = document.getElementsByTagName("input");
    inputs[2].classList.remove("bg-gray-100", "cursor-not-allowed", "dark:border-gray-600", "dark:placeholder-gray-500", "dark:text-gray-500")
    inputs[2].classList.add("bg-gray-50", "dark:border-gray-600", "dark:placeholder-gray-400", "dark:text-white")
    inputs[2].disabled = false;
    document.getElementById("change3").innerText = "Change Email"
}

window.addEventListener('load', function () {
    document.getElementById("change1").addEventListener("click", change1(), false);
    document.getElementById("change2").addEventListener("click", change2(), false);
    document.getElementById("change3").addEventListener("click", change3(), false);
    let inputs = document.getElementsByTagName("input");
    for (let input = 0; input < inputs.length; input++) {
        inputs[input].classList.remove("bg-gray-50", "dark:border-gray-600", "dark:placeholder-gray-400", "dark:text-white")
        inputs[input].classList.add("bg-gray-100", "cursor-not-allowed", "dark:border-gray-600", "dark:placeholder-gray-500", "dark:text-gray-500")
    }

});