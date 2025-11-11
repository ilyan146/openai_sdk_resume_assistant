import React from 'react';
import { useParams } from 'react-router-dom';
import ChatWindow from '../components/ChatWindow';
import '../styles/ChatPage.css';

const ChatPage = () => {
  const { chatId } = useParams(); // Get chatId from URL

  // const ChatPage = () => (
  return (
    <div className="chat-page-background">
      <div className="chat-page-center">
        <ChatWindow chatId={chatId} />
      </div>
    </div>
  );
};

export default ChatPage;
