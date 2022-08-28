import changeTimezone from "./changeTimezone.js";
import formatAMPM from "./formatAMPM.js";

// Format a ISO time string into a proper datetime string
function formatTime(time_input, short=false) {
    console.log(time_input);
    let date = new Date(time_input.replaceAll(" ", "T"));

    var timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    let new_date = changeTimezone(date, timezone);
    const today_date = new Date();
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);

    let date_str = '';
    let time_str = '';

    if (today_date.toDateString() === new_date.toDateString()) {
        date_str = 'Today';
    } else if (yesterday.toDateString() === new_date.toDateString()) {
        date_str = 'Yesterday';
    } else {
        date_str = new_date.toDateString();
    }
    console.log(date_str);

    let time = '';
    if (!(date_str === new_date.toString())) {
        time_str = formatAMPM(new_date);
        time = date_str + ' at ' + time_str;
    } else {
        time = date_str;
    }
    if (short){
        return time_str
    } else {
        return time;
    }
}

export default formatTime;