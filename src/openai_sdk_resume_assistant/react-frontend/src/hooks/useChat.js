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
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // optional: restore history
  useEffect(() => {
    const saved = localStorage.getItem('chatLog');
    if (saved) setMessages(JSON.parse(saved));
  }, []);

  const persist = (next) => {
    localStorage.setItem('chatLog', JSON.stringify(next));
  };

  const sendChat = async (text) => {
    const trimmed = text.trim();
    if (!trimmed) return;
    setMessages(prev => {
      const next = [...prev, { text: trimmed, isUser: true }];
      persist(next);
      return next;
    });
    setLoading(true);
    setError(null);
    try {
      const response = await apiSendMessage(trimmed);
      setMessages(prev => {
        const next = [...prev, { text: response.answer, isUser: false }];
        persist(next);
        return next;
      });
    } catch (e) {
      setError('Error sending message');
    } finally {
      setLoading(false);
    }
  };

  return { messages, loading, error, sendChat };
};