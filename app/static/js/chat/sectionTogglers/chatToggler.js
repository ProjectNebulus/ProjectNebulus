function toggleChat() {
    document.getElementById("pageTitle").innerText = "Chat";
    document.getElementById('members-sidebar').style.display = 'block';
    document.getElementById('main-area').style.display = 'block';
    document.getElementById('blocked').style.display = 'none';
    document.getElementById('friends').style.display = 'none';
    document.getElementById('emojis').style.display = 'none';
    document.getElementById('emails').style.display = 'none';
}

export default toggleChat;
