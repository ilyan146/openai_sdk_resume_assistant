import React from 'react';
import ChatBubble from './ChatBubble';

const ChatMessages = ({ messages, loading }) => {
  return (
    <div className="chat-messages">
      {messages.map((m, i) => (
        <ChatBubble key={i} message={m.text} isUser={m.isUser} />
      ))}
      {loading && (
        <div className="loading-bubble">
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
        </div>
      )}
    </div>
  );
};

export default ChatMessages;