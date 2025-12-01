import api from './apiClient';

// Register a new user
export const registerUser = async (email, username, password) => {
    const response = await api.post('/auth/register', {
        email,
        username,
        password,
    });
    return response.data;
};

// Login user
export const loginUser = async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email); // OAuth2 uses 'username' field for email
    formData.append('password', password);

    const response = await api.post('/auth/jwt/login', formData, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    });
    return response.data;
};

// Logout user
export const logoutUser = async () => {
    try {
        await api.post('/auth/jwt/logout');
    } finally {
        localStorage.removeItem('access_token');
    }
};

// Get current user
export const getCurrentUser = async () => {
    const response = await api.get('/users/me');
    return response.data;
};

// Store token
export const setToken = (token) => {
    localStorage.setItem('access_token', token);
};

// Get token
export const getToken = () => {
    return localStorage.getItem('access_token');
};

// Check if user is authenticated
export const isAuthenticated = () => {
    return !!localStorage.getItem('access_token');
};