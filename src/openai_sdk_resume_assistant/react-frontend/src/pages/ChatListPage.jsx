import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createChat, getAllChats } from '../services/api';
import '../styles/ChatListPage.css';

const ChatListPage = () => {
  const [chats, setChats] = useState([]);
  const [newChatName, setNewChatName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    loadChats();
  }, []);

  const loadChats = async () => {
    try {
      setLoading(true);
      const allChats = await getAllChats();
      setChats(allChats);
    } catch (err) {
      setError('Failed to load chats');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateChat = async () => {
    if (!newChatName.trim()) {
      setError('Please enter a chat name');
      return;
    }

    try {
      setLoading(true);
      const newChat = await createChat(newChatName);
      setNewChatName('');
      // Navigate to the chat page with the new chat ID
      navigate(`/chat/${newChat.id}`);
    } catch (err) {
      setError('Failed to create chat');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectChat = (chatId) => {
    navigate(`/chat/${chatId}`);
  };

  return (
    <div className="chat-list-page">
      <div className="chat-list-container">
        <h1>Your Chats</h1>
        
        <div className="new-chat-section">
          <h2>Create New Chat</h2>
          <div className="new-chat-input">
            <input
              type="text"
              placeholder="Enter chat name..."
              value={newChatName}
              onChange={(e) => setNewChatName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleCreateChat()}
              disabled={loading}
            />
            <button onClick={handleCreateChat} disabled={loading || !newChatName.trim()}>
              Create
            </button>
          </div>
        </div>

        {error && <div className="error-message">{error}</div>}

        <div className="chats-section">
          <h2>Recent Chats</h2>
          {loading && <div className="loading">Loading chats...</div>}
          
          {!loading && chats.length === 0 && (
            <div className="no-chats">No chats yet. Create one to get started!</div>
          )}

          <div className="chats-grid">
            {chats.map((chat) => (
              <div
                key={chat.id}
                className="chat-card"
                onClick={() => handleSelectChat(chat.id)}
              >
                <h3>{chat.chat_name}</h3>
                <p className="chat-info">
                  {chat.chat_messages.length} message{chat.chat_messages.length !== 1 ? 's' : ''}
                </p>
                <p className="chat-date">
                  {new Date(chat.created_at).toLocaleDateString()}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatListPage;