import getStatusColor from "./getStatusColor.js";

// This function is ran when someone's status changes (socket receives "user_status_change" event)
function statusChangeHandler(data) {
    /* data:
        {
            userID: The user's whose status has changed,
            status: The user's new status, if they have a new one (Do Not Disturb, Idle, Invisibile, None)
            offline: Whether the user is offline or online ( changing this also counts as a status change )
        }
    */

    let user = $(`member_${data['userID']}`); // Find the div that holds the specified user in the member list
    let user_img = user.children('span')[0]; // Get the user's profile picture status circle
    let color = getStatusColor(data);
    user_img.classList.add(color)

}

export default statusChangeHandler;




