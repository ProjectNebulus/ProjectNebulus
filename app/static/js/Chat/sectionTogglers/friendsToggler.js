function openFriends() {
    $.ajax({
        url: '/api/v1/internal/get-friends',
        type: 'GET',
        contentType: 'application/json',
        data: JSON.stringify({})
    }).done((data) => {
        document.getElementById('members-sidebar').style.display = 'none';
        document.getElementById('main-area').style.display = 'none';
        document.getElementById('blocked').style.display = 'none';
        document.getElementById('friends').style.display = 'block';
        document.getElementById('emojis').style.display = 'none';
        document.getElementById('emails').style.display = 'none';
    });
}

export default openFriends;