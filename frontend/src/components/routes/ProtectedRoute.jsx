import { Navigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

/**
 * ProtectedRoute wraps a route element so that only authenticated users can
 * reach it.
 *
 * Behaviour:
 * - While AuthContext is still restoring state from localStorage (loading),
 *   the component renders nothing. This prevents a redirect flash while the
 *   persisted user is being validated.
 * - Once loading is finished, an unauthenticated user is redirected to
 *   /login with a `from` state so the login page can return them afterwards.
 * - An authenticated user renders the wrapped element normally.
 *
 * This component deliberately does NOT handle logout itself — logout clears
 * AuthContext state, and the next navigation through this guard redirects.
 */
export default function ProtectedRoute({ element }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return null;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return element;
}