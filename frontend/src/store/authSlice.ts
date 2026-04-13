import { create } from 'zustand';
import api from '@/lib/api';
import { setTokens, clearTokens, getAccessToken, getUserFromToken } from '@/lib/auth';

interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  preferred_language: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  hydrate: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: typeof window !== 'undefined' && !!getAccessToken(),

  login: async (email: string, password: string) => {
    const res = await api.post('/auth/login/', { email, password });
    const { access, refresh } = res.data;
    setTokens(access, refresh);
    const decoded = getUserFromToken();
    set({
      user: decoded
        ? {
            id: decoded.user_id,
            email: decoded.email,
            full_name: decoded.full_name,
            role: decoded.role,
            preferred_language: decoded.preferred_language,
          }
        : null,
      isAuthenticated: true,
    });
  },

  logout: () => {
    clearTokens();
    set({ user: null, isAuthenticated: false });
  },

  hydrate: () => {
    const token = getAccessToken();
    if (token) {
      const decoded = getUserFromToken();
      set({
        user: decoded
          ? {
              id: decoded.user_id,
              email: decoded.email,
              full_name: decoded.full_name,
              role: decoded.role,
              preferred_language: decoded.preferred_language,
            }
          : null,
        isAuthenticated: true,
      });
    }
  },
}));
