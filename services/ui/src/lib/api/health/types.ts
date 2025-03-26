// Health related types
export interface HealthStatus {
  status: "healthy" | "unhealthy";
  server?: boolean;
  database?: boolean;
  version?: string;
}