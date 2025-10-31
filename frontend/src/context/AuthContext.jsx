import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

const STORAGE_KEY = "impact-auth";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [tokens, setTokens] = useState(null);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const parsed = JSON.parse(stored);
      setTokens({ access: parsed.access_token, refresh: parsed.refresh_token });
      setUser(parsed.user);
    }
    setLoading(false);
  }, []);

  const persist = useCallback((payload) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  }, []);

  const login = useCallback(
    (data) => {
      persist(data);
      setTokens({ access: data.access_token, refresh: data.refresh_token });
      setUser(data.user);
    },
    [persist]
  );

  const logout = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setTokens(null);
    setUser(null);
  }, []);

  const updateUser = useCallback(
    (updated) => {
      if (!tokens) return;
      const payload = {
        access_token: tokens.access,
        refresh_token: tokens.refresh,
        user: updated
      };
      persist(payload);
      setUser(updated);
    },
    [tokens, persist]
  );

  const value = useMemo(
    () => ({
      accessToken: tokens?.access,
      refreshToken: tokens?.refresh,
      user,
      login,
      logout,
      updateUser,
      loading
    }),
    [tokens, user, login, logout, updateUser, loading]
  );

  return <AuthContext.Provider value={value}>{!loading && children}</AuthContext.Provider>;
}

export function useAuthContext() {
  return useContext(AuthContext);
}
