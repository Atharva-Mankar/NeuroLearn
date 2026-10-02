import { createContext } from 'react';

/**
 * The authentication context object itself.
 *
 * It lives in its own module (rather than inside AuthContext.jsx) so that
 * AuthProvider and the useAuth hook can both import it without either file
 * exporting non-components alongside a component export.
 */
export const AuthContext = createContext();

/** localStorage key holding the persisted, non-sensitive user object. */
export const STORAGE_KEY = 'neurolearn_user';
