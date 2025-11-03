import React from 'react';
import ChatWindow from '../components/ChatWindow';
import '../styles/ChatPage.css';

const ChatPage = () => (
    <div className="chat-page-background">
    <div className="chat-page-center">
      <ChatWindow />
    </div>
  </div>
)

export default ChatPage;