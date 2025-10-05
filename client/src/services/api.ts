import axios from 'axios';

// Determine API base URL based on environment
const getApiBaseUrl = () => {
  // In production (static export), use the Azure backend
  if (typeof window !== 'undefined' && window.location.hostname !== 'localhost') {
    return 'https://weather-vibes-api.whitewave-6eaae7b5.eastus.azurecontainerapps.io';
  }
  // For local development
  return process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
};

const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Debug logging
console.log('API Base URL:', getApiBaseUrl());

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
