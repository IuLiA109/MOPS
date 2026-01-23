import apiClient from './client';

export interface User {
  id: number;
  username: string;
}

export interface LoginPayload {
  email?: string;
  username?: string;
  password: string;
}

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}

interface MessageResponse {
  message: string;
}

export const authApi = {
  login: async (identifier: string, password: string): Promise<MessageResponse> => {
    // Detectează dacă e email sau username
    const isEmail = identifier.includes('@');
    
    const payload: LoginPayload = isEmail
      ? { email: identifier, password }
      : { username: identifier, password };

    console.log('LOGIN PAYLOAD:', payload);
    
    return apiClient.post<MessageResponse>('/auth/login', payload);
  },

  register: async (payload: RegisterPayload): Promise<MessageResponse> => {
    return apiClient.post<MessageResponse>('/auth/register', payload);
  },

  logout: async (): Promise<MessageResponse> => {
    return apiClient.post<MessageResponse>('/auth/logout');
  },

  getMe: async (): Promise<User> => {
    return apiClient.get<User>('/auth/me');
  },
};

export default authApi;