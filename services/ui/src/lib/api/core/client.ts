import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from "axios";

// API configuration
const API_TIMEOUT = 30000; // 30 seconds

// Use empty baseURL to leverage the Vite proxy
const baseURL = import.meta.env.VITE_API_URL || '';

// Create axios instance with default config
export const apiClient: AxiosInstance = axios.create({
  baseURL,
  timeout: API_TIMEOUT,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json"
  },
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // You can add auth tokens here if needed
    // const token = getAuthToken();
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error: AxiosError) => {
    // You can add global error handling here
    // For example, handle 401 unauthorized, refresh tokens, etc.
    if (error.response?.status === 401) {
      // Handle unauthorized access
      // redirectToLogin();
    }

    return Promise.reject(error);
  }
);

// Helper function to make typed API requests
export async function apiRequest<T>(config: AxiosRequestConfig): Promise<T> {
  try {
    const response = await apiClient(config);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // You can add specific error handling here
      const errorMessage = error.response?.data?.message || error.message;
      throw new Error(errorMessage);
    }
    throw error;
  }
}