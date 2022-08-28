import makeCall from "./sectionLoaders/sidebarLoadingManager.js";
import newMessageHandler from "./MessageHandlers/receivingMessageHandler/recievingMessageHandler.js";
import statusChangeHandler from "./statusChangeHandlers/statusChangeHandler.js";
import chatScrollHandler from "./scrollHandlers/chatScrollHandler.js";
import sidebarScrollHandler from "./scrollHandlers/sidebarScrollHandler.js";
import keyboardManager from "./keyboardUtils.js";
import loadSocket from "./socketManager.js";
import createChat from "./newChatHandlers/createChat.js";

function initializeChat(io){
    console.log('Initialized chat!');
    makeCall();


    let socket = loadSocket(io);
    window["createChat"] = function(members){
        createChat(members, socket);
    }
    socket.on('new_chat', function(data){handleNewChat(data, socket)});
    socket.on('new_message', function(data){newMessageHandler(data)});
    socket.on('user_status_change', function(data){statusChangeHandler(data)});

    window.onunload = function () {
        socket.emit('user_unloaded', {}, function () {
            socket.disconnect();
        });
    };

    $('#chat').on('scroll', chatScrollHandler);
    $('#chat-sidebar').on('scroll', sidebarScrollHandler);
    keyboardManager(socket);
}

export default initializeChat;