import React from 'react';
import { useChat } from '../hooks/useChat';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';
import StatusMessage from './StatusMessage';
import '../styles/ChatPage.css';

const ChatWindow = () => {
  const { messages, loading, streaming,error, sendChat, clearChat} = useChat();

  return (
    <div className="chat-container">
      <ChatMessages messages={messages} loading={loading} streaming={streaming} />
      <StatusMessage loading={loading} error={error} />
      <ChatInput onSend={sendChat} onClear={clearChat} disabled={loading || streaming} />
    </div>
  );
};

export default ChatWindow;