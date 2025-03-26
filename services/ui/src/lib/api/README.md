# API Integration Guide

This directory contains the API client and related utilities for making requests to the backend.

## Architecture

The API layer is organized as follows:

- `client.ts` - Core Axios client setup with interceptors and error handling
- `types.ts` - TypeScript interfaces for API responses and data models
- `queries.ts` - TanStack React Query hooks for data fetching
- `endpoints/` - Domain-specific API endpoints (organized by feature)

## Using API Endpoints

### Setting Up

The API client is pre-configured to connect to the Go backend via a Vite proxy. In development, 
the requests are proxied to the Go server (default port 8003).

### Making API Calls

All API calls should use the provided React Query hooks for data fetching and mutations.

Example:

```tsx
import { useHealthStatusQuery } from '@/lib/api';

function MyComponent() {
  const { data, isLoading, isError } = useHealthStatusQuery();
  
  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error loading health data</div>;
  
  return (
    <div>
      <p>Status: {data?.status}</p>
      <p>Version: {data?.version}</p>
    </div>
  );
}
```

### Adding New Endpoints

1. Create a new file in the `endpoints/` directory for your domain (e.g., `users.ts`)
2. Define types and function wrappers for API calls
3. Add corresponding React Query hooks in `queries.ts`
4. Export your endpoints and hooks from `index.ts`

Example:

```typescript
// endpoints/users.ts
import { apiRequest } from '../client';

export interface User {
  id: string;
  name: string;
  email: string;
}

export async function getUsers(): Promise<User[]> {
  return apiRequest<User[]>({
    method: 'GET',
    url: '/api/v1/users',
  });
}

// queries.ts
export function useUsersQuery() {
  return useQuery({
    queryKey: ['users'],
    queryFn: getUsers,
  });
}
```

## Best Practices

1. Always use the `apiRequest` helper for type safety
2. Group related endpoints in a single file
3. Create dedicated React Query hooks for each endpoint
4. Use the `invalidateQueries` helper to refresh data
5. Handle loading and error states in your components