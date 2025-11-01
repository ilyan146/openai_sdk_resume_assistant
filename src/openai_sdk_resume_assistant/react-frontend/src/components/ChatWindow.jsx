import React, { useState } from 'react';
import { useChat } from '../hooks/useChat';
import ChatBubble from './ChatBubble';
import '../styles/chat.css';

const ChatWindow = () => {
  const { messages, sendMessage, loading, error } = useChat();
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    sendMessage(input);
    setInput('');
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((m, i) => (
          <ChatBubble key={i} message={m.text} isUser={m.isUser} />
        ))}
        {loading && <div className="status">Thinking...</div>}
        {error && <div className="error">{error}</div>}
      </div>
      <div className="chat-input-row">
        <textarea
          className="chat-textarea"
          placeholder="Type your question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKey}
        />
        <button
          className="chat-send-button"
          onClick={handleSend}
          disabled={loading || !input.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;