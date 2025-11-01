import React from 'react';


const ChatBubble = ({message, isUser}) =>
{
    return (
        <div className={`chat-bubble ${isUser ? 'user' : 'bot'}`}>
            {message}
        </div>
    );
}
export default ChatBubble;