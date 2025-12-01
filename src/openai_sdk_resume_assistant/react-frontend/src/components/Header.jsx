import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import '../styles/Header.css';

const Header = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const handleLogout = async () => {
    await logout();
    navigate('/auth');
  };

  return (
    <header className="app-header">
      <div className="header-content">
        <h1 className="header-title">Personal Assistant</h1>
        <nav className="header-nav">
          <Link 
            to="/" 
            className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
          >
            Chat
          </Link>
          <Link 
            to="/upload" 
            className={`nav-link ${location.pathname === '/upload' ? 'active' : ''}`}
          >
            Upload
          </Link>
        </nav>

        {user && (
          <div className="header-user">
            <span className="user-email">{user.email}</span>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;