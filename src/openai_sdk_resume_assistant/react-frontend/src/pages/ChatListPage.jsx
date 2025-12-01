import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createChat, getAllChats, deleteChatMemory } from '../services/api';
import '../styles/ChatListPage.css';

const ChatListPage = () => {
  const [chats, setChats] = useState([]);
  const [newChatName, setNewChatName] = useState('');
  const [loading, setLoading] = useState(false);
  const [deleting, setDeleting] = useState(null);
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

  const handleDeleteChat = async (e, chatId) => {
    e.stopPropagation(); // Prevent navigation when clicking delete
    if (!window.confirm('Are you sure you want to delete this chat?')) return;

    setDeleting(chatId);
    try {
      await deleteChatMemory(chatId);
      setChats(chats.filter(chat => chat.id !== chatId));
    } catch (err) {
      setError('Failed to delete chat');
    } finally {
      setDeleting(null);
    }
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
                className="chat-card group relative"
                onClick={() => handleSelectChat(chat.id)}
              >
                <button
                  onClick={(e) => handleDeleteChat(e, chat.id)}
                  disabled={deleting === chat.id}
                  className="absolute top-2 right-2 p-2 rounded-full bg-gradient-to-br from-gray-100 to-gray-300 text-gray-500 shadow-md hover:from-red-100 hover:to-red-300 hover:text-red-600 hover:shadow-lg opacity-0 group-hover:opacity-100 transition-all duration-200 focus:opacity-100 disabled:opacity-50"
                  aria-label="Delete chat"
                >
                  {deleting === chat.id ? (
                    <svg className="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                    </svg>
                  ) : (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  )}
                </button>
                <h3>{chat.chat_name}</h3>
                <p className="chat-info">
                  {chat.chat_messages.length} message{chat.chat_messages.length !== 1 ? 's' : ''}
                </p>
                {chat.created_at && (
                  <p className="chat-date">
                    {new Date(chat.created_at).toLocaleDateString()}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatListPage;