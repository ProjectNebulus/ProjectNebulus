
function replaceURLs(message) {
    console.log(message);
    if(!message) return;

    var urlRegex = /(((https?:\/\/)|(www\.))[^\s]+)/g;
    let result = message.replace(urlRegex, function (url) {
        var hyperlink = url;
        console.log(hyperlink);
        if (!hyperlink.match('^https?:\/\/')) {
          hyperlink = 'http://' + hyperlink;
        }
        return `<a class="
                   underline 
                   decoration-yellow-500 decoration-[0.25rem] 
                   motion-safe:transition-all motion-safe:duration-200 
                   hover:decoration-[0.5rem] focus:decoration-[0.5rem] hover:decoration-yellow-500/50 focus:decoration-yellow-500/50 
               " href="${hyperlink}">${hyperlink}</a>`;
  });
    console.log(result);
  return result;
}
