
function sendMessage() {
    var messageInput = document.getElementById('message-input');
    var messageText = messageInput.value.trim();
    if (messageText !== '') {
        var chatMessages = document.getElementById('chat-messages');
        var messageDiv = document.createElement('div');
        messageDiv.className = 'message sent'; // 보낸 메시지에 대한 클래스 추가
        messageDiv.innerHTML = `
            <span class="user">사용자:</span>
            <span class="text">${messageText}</span>
            <span class="time">${getCurrentTime()}</span>
        `;
        chatMessages.appendChild(messageDiv);
        messageInput.value = '';
        scrollToBottom();
    }
}

function getCurrentTime() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // 0시일 경우 12시로 변경
    minutes = minutes < 10 ? '0' + minutes : minutes;
    var timeString = hours + ':' + minutes + ' ' + ampm;
    return timeString;
}

function scrollToBottom() {
    var chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
