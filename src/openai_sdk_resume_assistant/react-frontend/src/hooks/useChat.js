import { useState, useEffect } from 'react';
import { sendMessage as apiSendMessage } from '../services/api';
import {sendMessageStream} from '../services/api';

export const useChat = () => {
  const [messages, setMessages] = useState([]); // Initial value is an empty array
  const [loading, setLoading] = useState(false);
  const [streaming, setStreaming] = useState(false); // State for streaming
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

    // Create empty assistant message that will be filled in as chunks arrive
    const assistantMessage = { text: '', isUser: false };
    setMessages(prev => [...prev, assistantMessage]);

    setLoading(true);
    setStreaming(true);
    setError(null);

    // // Track index of assistant message 
    // let assistantIndex;
    // setMessages(prev => { // Getting the latest messages array and get the index of it
    //   assistantIndex = prev.length - 1;
    //   return prev;
    // });
    
    // try {
    //   const response = await apiSendMessage(trimmed);
    //   console.log
    //   setMessages(prev => {
    //     const next = [...prev, { text: response.response, isUser: false }];
    //     persist(next);
    //     return next;
    //   });
    // } catch (e) {
    //   setError('Error sending message');
    // } finally {
    //   setLoading(false);
    // }
    await sendMessageStream(
      trimmed,
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
        setStreaming(false);
        setMessages(prev => {
          persist(prev);
          return prev;
        });
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

  return { messages, loading, streaming, error, sendChat, clearChat };
};