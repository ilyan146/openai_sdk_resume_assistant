import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useChat } from '../hooks/useChat';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';
import StatusMessage from './StatusMessage';
import '../styles/ChatPage.css';

const ChatWindow = ({ chatId }) => {
  const navigate = useNavigate();
  // const { messages, loading, streaming,error, sendChat, clearChat, loadChatHistory} = useChat(chatId);
  const { messages, loading, streaming,error, sendChat, loadChatHistory} = useChat(chatId);

  useEffect(() => {
    // If no chatId, redirect to chat list
    if (!chatId) {
      navigate('/');
    } else {
      // Load chat history when component mounts
      loadChatHistory(chatId);
    }
  }, [chatId, navigate, loadChatHistory]);

  const handleBackToList = () => {
    navigate('/');
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <button onClick={handleBackToList} className="back-button">
          ← Back to Chats
        </button>
      </div>
      <ChatMessages messages={messages} loading={loading} streaming={streaming} />
      <StatusMessage loading={loading} error={error} />
      {/* <ChatInput onSend={sendChat} onClear={clearChat} disabled={loading || streaming} /> */}
      <ChatInput onSend={sendChat} disabled={loading || streaming} />
    </div>
  );
};

export default ChatWindow;