import sendMessage from './MessageHandlers/sendingMessageHandler.js';
import toggleEmail from "./sectionTogglers/emailToggler.js";

let chatBox;
function keyboardManager(socket){
    chatBox = document.getElementById("msg_content");
    chatBox.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            if (!(e.shiftKey || e.ctrlKey || e.metaKey)) {
                sendMessage(socket);
                e.preventDefault();
            } else
                chatBox.rows = Math.min(3, parseInt(chatBox.rows) + 1) + "";
        } else if (e.key === "Backspace") {
            if (chatBox.value.charAt(chatBox.selectionStart) === "\n")
                chatBox.rows = Math.max(1, parseInt(chatBox.rows))
        }
    });

    if (window.location.search.substring(1).includes("email=ema")) toggleEmail();
}

export default keyboardManager;