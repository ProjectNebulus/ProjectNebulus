// Function to get the status color based on the user's status
function getStatusColor(data) {
    /*
        data:
          {
               status: The status (Do Not Disturb, Idle, Invisibile, None)
               offline: Whether the user is offline or online
          }
    */

    if (!data['offline'] && data['status'] === 'None') color = 'bg-green-400';
    else if (data['status'] === 'Do Not Disturb') color = 'bg-red-500';
    else if (data['status'] === 'Idle') color = 'bg-amber-500';
    else color = 'bg-gray-700';
    return color;
}

export default getStatusColor;
