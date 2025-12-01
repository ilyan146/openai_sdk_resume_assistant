import axios from 'axios';


// Debug: Log the API URL
console.log('VITE_API_URL:', import.meta.env.VITE_API_URL);

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Create new chat
export const createChat = async (chatName) => {
    const response = await api.post('/api/chat/create_chat_memory', null, {
        params: { chat_name: chatName }
    });
    return response.data;
};

// Get all chats
export const getAllChats = async () => {
    const response = await api.get('/api/chat/all_chats');
    return response.data;
};

// Get specific chat with history
export const getChatHistory = async (chatId) => {
    const response = await api.get(`/api/chat/chat_memory/${chatId}`);
    return response.data;
};

export const deleteChatMemory = async (chatId) => {
    const response = await api.delete(`/api/chat/chat_memory/${chatId}`);
    return response.data;
};

export const sendMessage = async(message) => {
    const response = await api.post('/api/chat/ask', { question: message });
    return response.data;
};

// New function to send message and receive streaming response
export const sendMessageStream = async(message, chatId, onChunk, onComplete, onError) => {
    try {
        const response = await fetch(`${api.defaults.baseURL}/api/chat/ask_stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: message, chat_id: chatId}),
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');

        while (true) { // Read the stream until done 
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));
                    if (data.error) {
                        onError(data.error);
                        return;
                    }
                    if (data.done) {
                        onComplete();
                        return;
                    }
                    if (data.chunk) {
                        onChunk(data.chunk);
                    }
                }
            }

        }
    } catch (error) {
        onError(error.message);
    }
};


// New function to upload files
export const uploadFiles = async(files) => {
    const formData = new FormData();    
    files.forEach(file => {
        formData.append('files', file);
    });
    const response = await api.post('/api/chat/upload_files', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    return response.data;
}

export const listCollectionItems = async() => {
    const response = await api.get('/api/chat/list_collection_items');
    return response.data;
}

export default api;