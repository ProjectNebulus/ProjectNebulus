function toggleEmail() {
    document.getElementById('members-sidebar').style.display = 'none';
    document.getElementById('main-area').style.display = 'none';
    document.getElementById('blocked').style.display = 'none';
    document.getElementById('friends').style.display = 'none';
    document.getElementById('emojis').style.display = 'none';
    document.getElementById('emails').style.display = 'block';
    document.getElementById('email_iframe').src = '/chat/email';
}

export default toggleEmail;