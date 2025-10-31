import axios from "axios";
import create from "zustand";

const apiBase = import.meta.env.VITE_API_BASE || "/api";

const api = axios.create({
  baseURL: apiBase
});

let interceptorsAttached = false;

const useApiStore = create((set) => ({
  refreshToken: null,
  accessToken: null,
  setTokens: (access, refresh) => set({ accessToken: access, refreshToken: refresh })
}));

export function attachInterceptors(accessToken, refreshToken, onLogout) {
  useApiStore.getState().setTokens(accessToken, refreshToken);

  if (interceptorsAttached) {
    return;
  }
  interceptorsAttached = true;
  api.interceptors.request.use((config) => {
    const { accessToken: currentAccess } = useApiStore.getState();
    if (currentAccess) {
      config.headers.Authorization = `Bearer ${currentAccess}`;
    }
    return config;
  });

  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const { refreshToken: storeRefresh } = useApiStore.getState();
      if (error.response?.status === 401 && storeRefresh) {
        try {
          const refreshUrl = `${apiBase.replace(/\/$/, "")}/auth/refresh`;
          const refreshResponse = await axios.post(refreshUrl, null, {
            headers: { Authorization: `Bearer ${storeRefresh}` }
          });
          const newAccess = refreshResponse.data.access_token;
          useApiStore.getState().setTokens(newAccess, storeRefresh);
          error.config.headers.Authorization = `Bearer ${newAccess}`;
          return api.request(error.config);
        } catch (refreshError) {
          if (onLogout) onLogout();
        }
      }
      return Promise.reject(error);
    }
  );
}

export default api;
