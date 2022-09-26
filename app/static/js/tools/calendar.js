window.onload = function () {
    const nowdate = new Date();
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const dateElement = document.getElementById('date');
    dateElement.innerHTML = months[nowdate.getMonth()] + ' ' + nowdate.getFullYear();
    document.getElementById("monthID").value = nowdate.getMonth() + nowdate.getFullYear() * 12;
    document.getElementById("prevPage").onclick = function () {
        let monthID = document.getElementById("monthID").value - 1;
        document.getElementById("monthID").value = monthID;
        let month_number = monthID % 12;
        let year = Math.floor((monthID - month_number) / 12);
        dateElement.innerHTML = months[month_number] + ' ' + year;

    };
    document.getElementById("today").onclick = function () {
        dateElement.innerHTML = months[nowdate.getMonth()] + ' ' + nowdate.getFullYear();
        document.getElementById("monthID").value = nowdate.getMonth() + nowdate.getFullYear() * 12;
    };
    document.getElementById("nextPage").onclick = function () {
        let monthID = document.getElementById("monthID").value + 1;
        document.getElementById("monthID").value = monthID;
        document.getElementById("monthID").value = monthID;
        let month_number = monthID % 12;
        let year = (monthID - month_number) / 12;
        dateElement.innerHTML = months[month_number] + ' ' + year;

    };
}