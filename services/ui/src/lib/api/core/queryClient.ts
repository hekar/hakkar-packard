import { QueryClient, QueryKey } from '@tanstack/react-query';

// Create a singleton QueryClient to be used across the app
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

// Invalidate queries helper
export function invalidateQueries(queryKey: QueryKey) {
  return queryClient.invalidateQueries({ queryKey });
}