import { useState, useEffect, useCallback } from 'react';
// import { sendMessage as apiSendMessage } from '../services/api';
import {sendMessageStream, getChatHistory} from '../services/api';

export const useChat = (chatId) => {
  const [messages, setMessages] = useState([]); // Initial value is an empty array
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState(false); // State for streaming
  const [error, setError] = useState(null);

  const loadChatHistory = useCallback(async (id) => {
    if (!id) return;
    
    try {
      setLoading(true);
      setError(null);
      const chatData = await getChatHistory(id);
      if (chatData && chatData.chat_messages) {
        setMessages(chatData.chat_messages.map(msg => ({
          text: msg.content,
          isUser: msg.role === 'user'
        })));
      } else {
        setMessages([]);
      }
    } catch (err) {
      console.error('Failed to load chat history:', err);
      setError('Failed to load chat history: ' +err.message);
      setMessages([]);
    } finally {
      setLoading(false);
    }
  }, []);

  // // optional: to restore history
  // useEffect(() => {
  //   const saved = localStorage.getItem('chatLog'); // If there is a saved chat log in localStorage
  //   if (saved) setMessages(JSON.parse(saved)); // Using setMessages function you can update the state with the new value
  // }, []); // Empty dependency array means this effect runs once on mount only

  // // For storing a chatlog in memory for persistence of history for example
  // const persist = (next) => {
  //   localStorage.setItem('chatLog', JSON.stringify(next)); // localStorage only stores strings, so we convert the array to a JSON string
  // };

  // const clearChat = () => {
  //   setMessages([]);
  //   localStorage.removeItem('chatLog');
  //   };

  const sendChat = async (text) => {
    const trimmed = text.trim();
    if (!trimmed) return;

    if (!chatId) {
      setError('No chat selected');
      return;
    }


    // setMessages(prev => {
    //   const next = [...prev, { text: trimmed, isUser: true }]; // Updating the conversation list of dictionaries the content and user the user
    //   persist(next);
    //   return next;
    // });

    // Add user message (removed persist call)
    setMessages(prev => [...prev, { text: trimmed, isUser: true }]);

    // Create empty assistant message that will be filled in as chunks arrive
    const assistantMessage = { text: 'Getting Assistant response.....\n', isUser: false };
    setMessages(prev => [...prev, assistantMessage]);

    setLoading(true);
    setStreaming(true);
    setError(null);

    await sendMessageStream(
      trimmed,
      chatId,
      // onChunk: Append text to the last message
      (chunk) => {
        setLoading(false); // Hide loading dots once streaming starts
        setMessages(prev => {
          const updated = [...prev];
          const lastIndex = updated.length - 1;
          updated[lastIndex] = {
            ...updated[lastIndex],
            text: updated[lastIndex].text + chunk
          };
          return updated;
        });
      },
      // onComplete: Finalize
      () => {
        setLoading(false);
        setStreaming(false);
        // setMessages(prev => {
        //   persist(prev);
        //   return prev;
        // });
      },
      // onError: Handle errors
      (errorMsg) => {
        setError('Error: ' + errorMsg);
        setLoading(false);
        setStreaming(false);
        // Remove the empty assistant message
        setMessages(prev => prev.slice(0, -1));
      }
    );

  };

  // return { messages, loading, streaming, error, sendChat, clearChat, loadChatHistory };
  return { 
    messages, 
    loading, 
    streaming, 
    error, 
    sendChat, 
    loadChatHistory 
  };
};