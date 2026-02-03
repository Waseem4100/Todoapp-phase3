import axios from 'axios';

interface User {
  id: string;
  email: string;
  first_name?: string;
  last_name?: string;
  created_at: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

interface RegisterData {
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
}

class AuthService {
  private static readonly BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
  private static readonly AUTH_TOKEN_KEY = 'auth_token';

  // Register a new user
  static async register(userData: RegisterData): Promise<LoginResponse> {
    try {
      const response = await axios.post(`${this.BASE_URL}/auth/register`, userData);
      const { access_token, user } = response.data;

      // Store the token in localStorage
      localStorage.setItem(this.AUTH_TOKEN_KEY, access_token);

      return { access_token, token_type: 'bearer', user };
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Registration failed');
    }
  }

  // Login user
  static async login(email: string, password: string): Promise<LoginResponse> {
    try {
      const response = await axios.post(`${this.BASE_URL}/auth/login`, {
        email,
        password,
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { access_token, user } = response.data;

      // Store the token in localStorage
      localStorage.setItem(this.AUTH_TOKEN_KEY, access_token);

      return { access_token, token_type: 'bearer', user };
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || 'Login failed');
    }
  }

  // Logout user
  static logout(): void {
    localStorage.removeItem(this.AUTH_TOKEN_KEY);
  }

  // Get current user token
  static getToken(): string | null {
    return localStorage.getItem(this.AUTH_TOKEN_KEY);
  }

  // Check if user is authenticated
  static isAuthenticated(): boolean {
    return !!this.getToken();
  }

  // Get API instance with authentication
  static getApiInstance() {
    const instance = axios.create({
      baseURL: this.BASE_URL,
    });

    // Add auth token to requests
    instance.interceptors.request.use(
      (config) => {
        const token = this.getToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Handle token expiration
    instance.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.logout();
        }
        return Promise.reject(error);
      }
    );

    return instance;
  }
}

export default AuthService;