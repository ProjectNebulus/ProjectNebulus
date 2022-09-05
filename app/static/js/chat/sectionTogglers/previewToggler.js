function togglePreview() {
    let preview = document.getElementById('preview_border');
    console.log(preview.style.display);
    let chat = document.getElementById('chat');
    if (preview.style.display === 'none') {
        preview.style.display = 'block';
        chat.style.height = '64%';
    } else {
        preview.style.display = 'none';
        chat.style.height = '80%';
    }
}

export default togglePreview;
