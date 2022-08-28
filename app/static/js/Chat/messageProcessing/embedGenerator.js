// Function to generate an embed from a url
// This function returns a Promise, because the embed needs to load asynchronously, while the other messages load.
function getEmbed(hyperlink) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: 'http://url-metadata.herokuapp.com/api/metadata?url=' + hyperlink, // POST request to url-metadata API to get metadata about URL
            type: 'GET',
            success: function (data) {
                resolve(data);
            },
            error: function (data) {
                reject(data);
            }
        });
    });
}

export default getEmbed;