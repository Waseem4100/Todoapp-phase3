import React, { useEffect } from 'react';
import Layout from '../components/Layout';
import TodoList from '../components/TodoList';
import AuthService from '../services/auth';
import '../styles/global.css';

const TodosPage: React.FC = () => {
  useEffect(() => {
    // Check if user is authenticated
    if (!AuthService.isAuthenticated()) {
      window.location.href = '/login';
    }
  }, []);

  // If not authenticated, don't render the content
  if (!AuthService.isAuthenticated()) {
    return <div>Redirecting...</div>;
  }

  return (
    <Layout>
      <div className="page-container">
        <TodoList />
      </div>
    </Layout>
  );
};

export default TodosPage;