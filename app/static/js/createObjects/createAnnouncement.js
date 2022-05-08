function createAnnouncement() {
    const announcement = {
        title: document.getElementById("announcementname").value,
        content: document.getElementById("message").value,
        author: document.getElementById("author").value,
        author_pic: document.querySelector("#navbar trigger logo").getAttribute("image"),
        course: document.getElementById("course_id").innerText,
    };

    $.ajax({
        type: "POST",
        url: "/api/v1/internal/create-announcement",
        data: JSON.stringify(announcement),
        dataType: "json",
        contentType: "application/json",
        done: function (data) {
            alert('Successfully created announcement');
        },
        error: function (error) {
            alert(error);
        }
    });
}