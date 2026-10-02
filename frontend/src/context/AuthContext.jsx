import { useState, useEffect, useContext } from 'react';
import { login } from '../services/api';
import { AuthContext, STORAGE_KEY } from './authContextObject';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize auth state from localStorage on mount
  useEffect(() => {
    const initAuth = async () => {
      try {
        const storedUser = localStorage.getItem(STORAGE_KEY);
        if (storedUser) {
          const parsed = JSON.parse(storedUser);
          // Validate basic structure
          if (parsed && parsed.id && parsed.name && parsed.email) {
            setUser(parsed);
          } else {
            // Invalid data, clear it
            localStorage.removeItem(STORAGE_KEY);
          }
        }
      } catch (err) {
        // If parsing fails, clear corrupted data
        localStorage.removeItem(STORAGE_KEY);
        console.warn('Failed to parse auth data from localStorage', err);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const loginUser = async (email, password) => {
    setError(null);
    try {
      const userData = await login({ email, password });
      setUser(userData);
      // Persist only safe user information
      localStorage.setItem(STORAGE_KEY, JSON.stringify(userData));
      return userData;
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.');
      throw err;
    }
  };

  const logoutUser = () => {
    setUser(null);
    localStorage.removeItem(STORAGE_KEY);
  };

  const updateUser = (updatedData) => {
    setUser(updatedData);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updatedData));
  };

  const isAuthenticated = !!user;

  const value = {
    user,
    isAuthenticated,
    loading,
    error,
    login: loginUser,
    logout: logoutUser,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}

export function useAuthContext() {
  // `createContext()` with no default yields undefined, which is how a call
  // outside the provider is detected -- a hook that silently returned a
  // half-built object would fail much later and much less clearly.
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
}
