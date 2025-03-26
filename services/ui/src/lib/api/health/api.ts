import { apiClient } from "../core/client";
import { HealthStatus } from "./types";

/**
 * Get the current health status of the API
 *
 * @returns Health status information
 */
export async function getHealthStatus(): Promise<HealthStatus> {
  // Use the api/v1/health endpoint through the Vite proxy
  const response = await apiClient.get("/api/v1/health");
  return response.data;
}