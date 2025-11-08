import React, {useEffect, useRef} from 'react';
import ChatBubble from './ChatBubble';

const ChatMessages = ({ messages, loading, streaming }) => {
  const messagesEndRef = useRef(null);

// Auto-scroll to bottom when messages change or during streaming
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streaming]);

// const ChatMessages = ({ messages, loading }) => {
  
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
      {streaming && !loading && (
        <div className="streaming-indicator">●</div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatMessages;