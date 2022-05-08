$(window).scroll(function(){

    // get the bottom position
    var bottom_position = $(document).height() - ($(window).scrollTop() + $(window).height());
    var scroll_data = {
            action: 'user_scroll',
            container_id: container_id
        };
    $.ajax({
             url: wdm_url,
             data: scroll_data,
             context: document.body
           }).done(function(response) {
                // do stuff here
              });
});