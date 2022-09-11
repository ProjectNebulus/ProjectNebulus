function openBlocked() {
    $.ajax({
        url: '/api/v1/internal/get/blocks',
        type: 'GET',
        contentType: 'application/json',
        data: JSON.stringify({})
    }).done((data) => {
        document.getElementById("pageTitle").innerText = "Blocked";
        document.getElementById('members-sidebar').style.display = 'none';
        document.getElementById('main-area').style.display = 'none';
        document.getElementById('blocked').style.display = 'block';
        document.getElementById('friends').style.display = 'none';
        document.getElementById('emojis').style.display = 'none';
        document.getElementById('emails').style.display = 'none';
    });
}

export default openBlocked;
