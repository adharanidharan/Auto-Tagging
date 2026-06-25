import axios from 'axios';

const resolveBaseUrl = () => {
  const envUrl = import.meta.env.VITE_API_URL;
  if (!envUrl) return 'http://localhost:8000/api';
  // Ensure the base URL ends with /api so client requests go to the correct routes
  try {
    const url = new URL(envUrl);
    // preserve any trailing path, append /api if missing
    if (url.pathname.endsWith('/api')) return url.toString().replace(/\/$/, '');
    // remove trailing slash then append /api
    url.pathname = url.pathname.replace(/\/$/, '') + '/api';
    return url.toString().replace(/\/$/, '');
  } catch (e) {
    // Fallback for relative or malformed values: naive string handling
    let u = envUrl.replace(/\/$/, '');
    if (!u.endsWith('/api')) u = `${u}/api`;
    return u;
  }
};

const api = axios.create({
  baseURL: resolveBaseUrl(),
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear storage
      localStorage.removeItem('token');
      localStorage.removeItem('user');

      // Auto-redirect to login screen if not already there
      const path = window.location.pathname;
      if (path !== '/login' && path !== '/register') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export default api;
