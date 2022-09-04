import initializeChat from './chatInitializer.js';
import changeSearch from './searchManager.js';
import getChat from './sectionLoaders/chatLoader.js';
import {openBlocked, openFriends, toggleEmail, toggleEmoji, togglePreview} from './sectionTogglers/importUtil.js';

let io = window.io;
window['getChat'] = getChat;
window['searchWithin'] = changeSearch;
window['toggleEmoji'] = toggleEmoji;
window['openFriends'] = openFriends;
window['openBlocked'] = openBlocked;
window['toggleEmail'] = toggleEmail;
window['togglePreview'] = togglePreview;

keyUpDelay('#search', 1000, changeSearch);
$(document).ready(function () {
    initializeChat(io);
});
