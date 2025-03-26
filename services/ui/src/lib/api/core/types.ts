// General API response type
export interface ApiResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

// Paginated response type
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Error response from API
export interface ApiError {
  message: string;
  code?: string;
  details?: unknown;
}