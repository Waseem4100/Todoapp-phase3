import axios from 'axios';
import AuthService from './auth';

interface Todo {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface CreateTodoData {
  title: string;
  description?: string;
  is_completed?: boolean;
}

interface UpdateTodoData {
  title?: string;
  description?: string;
  is_completed?: boolean;
}

class TodoApiService {
  private static readonly BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

  // Get all todos for the current user
  static async getTodos(): Promise<Todo[]> {
    try {
      const response = await AuthService.getApiInstance().get('/todos');
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch todos');
    }
  }

  // Create a new todo
  static async createTodo(todoData: CreateTodoData): Promise<Todo> {
    try {
      const response = await AuthService.getApiInstance().post('/todos', todoData);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to create todo');
    }
  }

  // Get a specific todo by ID
  static async getTodoById(id: string): Promise<Todo> {
    try {
      const response = await AuthService.getApiInstance().get(`/todos/${id}`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch todo');
    }
  }

  // Update a specific todo
  static async updateTodo(id: string, todoData: UpdateTodoData): Promise<Todo> {
    try {
      const response = await AuthService.getApiInstance().put(`/todos/${id}`, todoData);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to update todo');
    }
  }

  // Delete a specific todo
  static async deleteTodo(id: string): Promise<void> {
    try {
      await AuthService.getApiInstance().delete(`/todos/${id}`);
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to delete todo');
    }
  }

  // Toggle todo completion status
  static async toggleTodoCompletion(id: string): Promise<Todo> {
    try {
      const response = await AuthService.getApiInstance().patch(`/todos/${id}/toggle-complete`);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Failed to toggle todo completion');
    }
  }
}

export { TodoApiService, type Todo, type CreateTodoData, type UpdateTodoData };