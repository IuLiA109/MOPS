import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
} from 'react';
import { authApi, User } from '../api/auth';

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  register: (username: string, email: string, password: string) => Promise<boolean>;
  logout: () => Promise<void>;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true); // true inițial pentru verificare sesiune
  const [error, setError] = useState<string | null>(null);

  // Verifică sesiunea existentă la mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const currentUser = await authApi.getMe();
        setUser(currentUser);
      } catch {
        // Nu e logat sau cookie expirat - e ok, nu e eroare
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = useCallback(async (identifier: string, password: string): Promise<boolean> => {
  setIsLoading(true);
  setError(null);

  try {
    await authApi.login(identifier, password);  // trimite direct identifier
    
    const currentUser = await authApi.getMe();
    setUser(currentUser);
    return true;
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Login failed';
    setError(message);
    return false;
  } finally {
    setIsLoading(false);
  }
}, []);

  const register = useCallback(
    async (username: string, email: string, password: string): Promise<boolean> => {
      setIsLoading(true);
      setError(null);

      try {
        await authApi.register({ username, email, password });
        
        // După register, fă login automat
        await authApi.login(email, password)
        const currentUser = await authApi.getMe();
        setUser(currentUser);
        return true;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Registration failed';
        setError(message);
        return false;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const logout = useCallback(async () => {
    try {
      await authApi.logout();
    } catch {
      // Chiar dacă request-ul eșuează, curățăm starea locală
    } finally {
      setUser(null);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        error,
        login,
        register,
        logout,
        clearError,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};