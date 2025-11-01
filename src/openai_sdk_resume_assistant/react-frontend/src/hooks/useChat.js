import {useState} from 'react';
import {sendMessage} from '../services/api';



export const useChat = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = async (text) => {
    const trimmed = text.trim();
    if (!trimmed) return;

    // add user message
    setMessages(prev => [...prev, { text: trimmed, isUser: true }]);
    setLoading(true);
    setError(null);

    try {
      const response = await sendMessage(trimmed);
      setMessages(prev => [...prev, { text: response.answer, isUser: false }]);
    } catch (err) {
      setError('Error sending message');
    } finally {
      setLoading(false);
    }
  };

  return {
    messages,
    loading,
    error,
    sendMessage
  };
}