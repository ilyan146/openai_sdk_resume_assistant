import React, { useState } from 'react';

const ChatInput = ({ onSend, onClear, disabled }) => {
  const [value, setValue] = useState('');

  const handleSend = () => {
    const trimmed = value.trim();
    if (!trimmed) return;
    onSend(trimmed);
    setValue('');
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-input-row">
      <button
        className="chat-clear-button"
        onClick={onClear}
        disabled={disabled}
      >
        Clear
      </button>
      <textarea
        className="chat-textarea"
        placeholder="Type your question..."
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKey}
        disabled={disabled}
      />
      <button
        className="chat-send-button"
        onClick={handleSend}
        disabled={disabled || !value.trim()}
      >
        submit
      </button>
    </div>
  );
};

export default ChatInput;