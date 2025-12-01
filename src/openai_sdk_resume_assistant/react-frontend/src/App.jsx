// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'

// // Starting edits from here
import React from 'react';
// import ChatWindow from './components/ChatWindow';
// import {Route, Routes} from 'react-router-dom';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import AuthPage from './pages/AuthPage';
import { AuthProvider } from './components/AuthProvider';
import ChatListPage from './pages/ChatListPage';
import ChatPage from './pages/ChatPage';
import Header from './components/Header';
import UploadPage from './pages/UploadPage';

// const App = () => {
//   return <ChatWindow />;
// };

// export default App;

// const App = () => (
//   <>
//     <Header />
//     <Routes>
//       <Route path="/" element={<ChatListPage />} />
//       <Route path="/chat/:chatId" element={<ChatPage />} />
//       <Route path="/upload" element={<UploadPage />} />
//     </Routes>
//   </>
// );
// export default App;

const App = () => {
    return (
        <AuthProvider>
            <Router>
                <Routes>
                    {/* Public Route */}
                    <Route path="/auth" element={<AuthPage />} />

                    {/* Protected Routes */}
                    <Route
                        path="/"
                        element={
                            <ProtectedRoute>
                                <ChatListPage />
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/chat/:chatId"
                        element={
                            <ProtectedRoute>
                                <ChatPage />
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/upload"
                        element={
                            <ProtectedRoute>
                                <UploadPage />
                            </ProtectedRoute>
                        }
                    />
                </Routes>
            </Router>
        </AuthProvider>
    );
};

export default App;


// From the internet for example
// import React, { useState, useEffect } from 'react';
// import './App.css';

// function App() {
//     const [userInput, setUserInput] = useState('');
//     const [chatLog, setChatLog] = useState([]);
//     const [loading, setLoading] = useState(false);

//     // Effect to load chat history from local storage when the app starts
//     useEffect(() => {
//         const storedChatLog = localStorage.getItem('chatLog');
//         if (storedChatLog) {
//             setChatLog(JSON.parse(storedChatLog));
//         }
//     }, []);

//     const handleSubmit = async (event) => {
//         event.preventDefault();
//         if (!userInput.trim()) return; // Don't send empty messages

//         const userMessage = { type: 'user', text: userInput };
//         const newChatLog = [...chatLog, userMessage];
//         setChatLog(newChatLog);
//         setUserInput('');
//         setLoading(true);

//         try {
//             // The API call to our FastAPI backend
//             const response = await fetch('http://localhost:8000/api/v1/chat/ask', {
//                 method: 'POST',
//                 headers: { 'Content-Type': 'application/json' },
//                 body: JSON.stringify({ question: userInput }),
//             });

//             if (!response.ok) {
//                 throw new Error(`HTTP error! status: ${response.status}`);
//             }

//             const data = await response.json();
//             const botMessage = { type: 'bot', text: data.response };

//             // Update the chat log with the bot's response
//             const finalChatLog = [...newChatLog, botMessage];
//             setChatLog(finalChatLog);

//             // Save the updated chat log to local storage for persistence
//             localStorage.setItem('chatLog', JSON.stringify(finalChatLog));

//         } catch (error) {
//             console.error('Error fetching chat response:', error);
//             const errorMessage = { type: 'error', text: 'Sorry, something went wrong. Please try again.' };
//             setChatLog(prev => [...prev, errorMessage]);
//         } finally {
//             setLoading(false);
//         }
//     };

//     return (
//         <div className="App">
//             <h1>AI Chatbot</h1>
//             <div className="chat-window">
//                 {chatLog.map((message, index) => (
//                     <div key={index} className={`message ${message.type}`}>
//                         {message.text}
//                     </div>
//                 ))}
//                 {loading && <div className="message bot">Loading...</div>}
//             </div>
//             <form onSubmit={handleSubmit} className="chat-form">
//                 <input
//                     type="text"
//                     value={userInput}
//                     onChange={(e) => setUserInput(e.target.value)}
//                     placeholder="Type your message..."
//                     disabled={loading}
//                 />
//                 <button type="submit" disabled={loading}>Send</button>
//             </form>
//         </div>
//     );
// }

// export default App;
