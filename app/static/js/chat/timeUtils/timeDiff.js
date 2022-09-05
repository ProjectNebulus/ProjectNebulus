// Find the time difference of 2 ISO strings and check if it is less than 10 minutes (Used for grouping messages)
function timeDiff(t1, t2) {
    return (
        new Date(t1['send_date'].replaceAll(' ', 'T')).getTime() -
        new Date(t2['send_date'].replaceAll(' ', 'T')).getTime() >
        1000 * 60 * 10
    );
}

export default timeDiff;
