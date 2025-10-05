import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Debug logging
console.log('API Base URL:', process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000');

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed in the future
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle errors globally
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default api;
