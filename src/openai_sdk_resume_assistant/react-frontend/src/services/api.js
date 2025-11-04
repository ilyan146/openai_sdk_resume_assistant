import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

export const sendMessage = async(message) => {
    const response = await api.post('/api/chat/ask', { question: message });
    return response.data;
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

export default api;