// import {useState} from 'react';
// import {sendMessage} from '../services/api';



// export const useChat = () => {
//   const [messages, setMessages] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState(null);

//   const sendMessage = async (text) => {
//     const trimmed = text.trim();
//     if (!trimmed) return;

//     // add user message
//     setMessages(prev => [...prev, { text: trimmed, isUser: true }]);
//     setLoading(true);
//     setError(null);

//     try {
//       const response = await sendMessage(trimmed);
//       setMessages(prev => [...prev, { text: response.answer, isUser: false }]);
//     } catch (err) {
//       setError('Error sending message');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return {
//     messages,
//     loading,
//     error,
//     sendMessage
//   };
// }

import { useState, useEffect } from 'react';
import { sendMessage as apiSendMessage } from '../services/api';

export const useChat = () => {
  const [messages, setMessages] = useState([]); // Initial value is an empty array
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // optional: to restore history
  useEffect(() => {
    const saved = localStorage.getItem('chatLog'); // If there is a saved chat log in localStorage
    if (saved) setMessages(JSON.parse(saved)); // Using setMessages function you can update the state with the new value
  }, []); // Empty dependency array means this effect runs once on mount only

  // For storing a chatlog in memory for persistence of history for example
  const persist = (next) => {
    localStorage.setItem('chatLog', JSON.stringify(next)); // localStorage only stores strings, so we convert the array to a JSON string
  };

  const clearChat = () => {
    setMessages([]);
    localStorage.removeItem('chatLog');
    };

  const sendChat = async (text) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    setMessages(prev => {
      const next = [...prev, { text: trimmed, isUser: true }]; // Updating the conversation list of dictionaries the content and user the user
      persist(next);
      return next;
    });
    
    setLoading(true);
    setError(null);
    try {
      const response = await apiSendMessage(trimmed);
      console.log
      setMessages(prev => {
        const next = [...prev, { text: response.response, isUser: false }];
        persist(next);
        return next;
      });
    } catch (e) {
      setError('Error sending message');
    } finally {
      setLoading(false);
    }
  };

  return { messages, loading, error, sendChat, clearChat };
};