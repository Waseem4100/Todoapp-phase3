import React from 'react';
import Link from 'next/link';
import AuthService from '../services/auth';
import '../styles/global.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const isLoggedIn = AuthService.isAuthenticated();

  const handleLogout = () => {
    AuthService.logout();
    window.location.href = '/login'; // Redirect to login after logout
  };

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <Link href="/" className="nav-brand">
            Todo App
          </Link>

          <div className="nav-links">
            {isLoggedIn ? (
              <>
                <Link href="/todos" className="nav-link">
                  My Todos
                </Link>
                <button onClick={handleLogout} className="logout-btn">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="nav-link">
                  Login
                </Link>
                <Link href="/signup" className="nav-link">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      <main className="main-content">
        {children}
      </main>

      <footer className="footer">
        <div className="footer-container">
          <p>&copy; 2026 Todo App. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;