import {
  useQuery,
  UseQueryOptions,
  QueryKey,
} from '@tanstack/react-query';
import { AxiosError } from 'axios';
import { getHealthStatus } from './api';
import { HealthStatus } from './types';
import { ApiError, queryClient } from '../core';

// Typed query hook for health status
export function useHealthStatusQuery(
  options?: UseQueryOptions<HealthStatus, AxiosError<ApiError>, HealthStatus, QueryKey>
) {
  return useQuery({
    queryKey: ['health'],
    queryFn: getHealthStatus,
    ...options,
  });
}

// Prefetch health status data
export async function prefetchHealthStatus() {
  await queryClient.prefetchQuery({
    queryKey: ['health'],
    queryFn: getHealthStatus,
  });
}