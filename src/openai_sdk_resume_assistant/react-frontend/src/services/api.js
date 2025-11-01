import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

export const sendMessage = async(message) => {
    const response = await api.post('/api/v1/chat/ask', { question: message });
    return response.data;
};

export default api;