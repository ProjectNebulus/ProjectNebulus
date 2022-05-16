
function replaceURLs(message) {
    if(!message) return message;//return;
    console.log(message);
    // if (!message.includes("\"http\"")) {
    if (!message.includes("http")) {
        console.log("returned. no link detected");
        return message;//return;
    }
    if (message.includes("href=\"http")){
        console.log("returned. recursive detected");
        return message;//return;
    }
    var urlRegex = /(((https?:\/\/)|(www\.))[^\s]+)/g;

    let result = message.replace(urlRegex, function (url) {
        var hyperlink = url;
        console.log(hyperlink);
        if (!hyperlink.match('^https?:\/\/')) {
          hyperlink = 'http://' + hyperlink;
        }
        hyperlink.replace("<p>","");
        hyperlink.replace("</p>","")
        return `<a 
                   target="_blank"
                   class="
                   underline 
                   decoration-yellow-500 decoration-[0.25rem] 
                   motion-safe:transition-all motion-safe:duration-200 
                   hover:decoration-[0.5rem] focus:decoration-[0.5rem] hover:decoration-yellow-500/50 focus:decoration-yellow-500/50 
               " href="${hyperlink}">${hyperlink}</a>`;
  });
    console.log(result);
  return result;
}
