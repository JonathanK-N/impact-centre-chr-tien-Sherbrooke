import axios from 'axios';
import * as SecureStore from 'expo-secure-store';

const API_BASE_URL = __DEV__ 
  ? 'http://localhost:3000/api' 
  : 'https://impact-centre-backend-production.up.railway.app/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use(
  async (config) => {
    const token = await SecureStore.getItemAsync('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Intercepteur pour gérer les erreurs d'authentification
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await SecureStore.deleteItemAsync('authToken');
      await SecureStore.deleteItemAsync('userData');
      // Rediriger vers login si nécessaire
    }
    return Promise.reject(error);
  }
);

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  phone?: string;
}

export interface User {
  _id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone?: string;
  role: string;
  membershipStatus: string;
  isActive: boolean;
}

export interface AuthResponse {
  token: string;
  user: User;
  message: string;
}

// Services d'authentification
export const authService = {
  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },

  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  getMe: async (): Promise<{ user: User }> => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Services des départements
export const departmentService = {
  getAll: async () => {
    const response = await api.get('/departments');
    return response.data;
  },

  join: async (departmentId: string) => {
    const response = await api.post(`/departments/${departmentId}/join`);
    return response.data;
  },
};

// Services des événements
export const eventService = {
  getAll: async (params?: { startDate?: string; endDate?: string; eventType?: string }) => {
    const response = await api.get('/events', { params });
    return response.data;
  },

  register: async (eventId: string) => {
    const response = await api.post(`/events/${eventId}/register`);
    return response.data;
  },
};

// Services des familles
export const familyService = {
  getAll: async () => {
    const response = await api.get('/families');
    return response.data;
  },

  getNearby: async (latitude: number, longitude: number, maxDistance?: number) => {
    const response = await api.get('/families/nearby', {
      params: { latitude, longitude, maxDistance }
    });
    return response.data;
  },

  requestJoin: async (familyId: string) => {
    const response = await api.post(`/families/${familyId}/request-join`);
    return response.data;
  },
};

export default api;