import { useContext } from 'react';
import { AuthContext } from '../context/authContextObject';

/**
 * Hook to access the current authentication state.
 *
 * Must be called inside an AuthProvider. Throws if used outside one so a
 * misconfigured tree fails loudly instead of silently returning undefined.
 *
 * @returns {{ user: object|null, isAuthenticated: boolean, loading: boolean, error: string|null, login: Function, logout: Function }}
 */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}