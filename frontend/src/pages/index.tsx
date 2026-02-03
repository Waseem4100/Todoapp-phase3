import React from 'react';
import Link from 'next/link';
import Layout from '../components/Layout';
import AuthService from '../services/auth';
import '../styles/global.css';

const HomePage: React.FC = () => {
  const isLoggedIn = AuthService.isAuthenticated();

  return (
    <Layout>
      <div className="home-page">
        <div className="hero-section">
          <h1>Welcome to Todo App</h1>
          <p>Manage your tasks efficiently and boost your productivity</p>

          {isLoggedIn ? (
            <Link href="/todos" className="cta-button">
              View My Todos
            </Link>
          ) : (
            <div className="auth-options">
              <Link href="/signup" className="cta-button">
                Get Started
              </Link>
              <span className="or-separator">or</span>
              <Link href="/login" className="secondary-button">
                Log In
              </Link>
            </div>
          )}
        </div>

        <div className="features-section">
          <div className="feature-card">
            <h3>Create Tasks</h3>
            <p>Easily add new tasks with titles and descriptions</p>
          </div>
          <div className="feature-card">
            <h3>Track Progress</h3>
            <p>Mark tasks as complete to track your progress</p>
          </div>
          <div className="feature-card">
            <h3>Stay Organized</h3>
            <p>Keep all your tasks organized in one place</p>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default HomePage;