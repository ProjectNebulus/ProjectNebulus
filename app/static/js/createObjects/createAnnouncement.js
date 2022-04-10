function createAnnouncement(){
    var announcement = {
        title: document.getElementById("announcementname").value,
        content: document.getElementById("message").value,
        author: document.getElementById("author").value,
        course: document.getElementById("course_id").innerText,
    }
    let request = $.ajax({
        type: "POST",
        url: "/api/v1/internal/create-announcement",
        data: JSON.stringify(announcement),
        dataType: "json",
        contentType: "application/json",
        done: function(data){
            alert('Successfully created announcement');
        },
        error: function(error){
            alert(error);
        }
    });
}