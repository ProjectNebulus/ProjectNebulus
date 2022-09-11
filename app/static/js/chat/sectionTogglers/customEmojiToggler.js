function toggleEmoji() {
    document.getElementById("pageTitle").innerText = "Emojis";
    document.getElementById('members-sidebar').style.display = 'none';
    document.getElementById('main-area').style.display = 'none';
    document.getElementById('blocked').style.display = 'none';
    document.getElementById('friends').style.display = 'none';
    document.getElementById('emojis').style.display = 'block';
    document.getElementById('emails').style.display = 'none';
}

export default toggleEmoji;
