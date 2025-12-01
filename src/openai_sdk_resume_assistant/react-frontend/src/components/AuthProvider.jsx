import React, { createContext, useState, useEffect } from 'react';
import { getCurrentUser, isAuthenticated, setToken, logoutUser } from '../services/authApi';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        if (isAuthenticated()) {
            try {
                const userData = await getCurrentUser();
                setUser(userData);
            } catch (error) {
                console.error('Auth check failed:', error);
                localStorage.removeItem('access_token');
            }
        }
        setLoading(false);
    };

    const login = async (token) => {
        setToken(token);
        const userData = await getCurrentUser();
        setUser(userData);
    };

    const logout = async () => {
        await logoutUser();
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, logout, isAuthenticated: !!user }}>
            {children}
        </AuthContext.Provider>
    );
};