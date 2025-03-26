import { ActivitySquare, ServerOff } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useHealthStatusQuery } from '@/lib/api';

interface HealthStatusProps {
  collapsed?: boolean;
}

export const HealthStatus = ({ collapsed = false }: HealthStatusProps) => {
  const { data, isLoading, isError } = useHealthStatusQuery();

  // Determine status and style
  let icon = <ActivitySquare />;
  let iconColor = "text-gray-400";
  let indicatorColor = "bg-gray-400";
  let label = "Checking...";
  let textColor = "text-gray-500";
  let statusTextColor = "text-gray-400";
  
  if (isError) {
    icon = <ServerOff />;
    iconColor = "text-red-500 dark:text-red-400";
    indicatorColor = "bg-red-500 dark:bg-red-400";
    label = "Server";
    textColor = "text-red-500 dark:text-red-400";
    statusTextColor = "text-red-400 dark:text-red-300";
  } else if (!isLoading) {
    // Check if data has status field and it's 'healthy', or if server field is true
    const isHealthy = data?.status === 'healthy' || data?.server === true;
    
    icon = <ActivitySquare />;
    iconColor = isHealthy 
      ? "text-success" 
      : "text-amber-500 dark:text-amber-400";
    indicatorColor = isHealthy 
      ? "bg-success" 
      : "bg-amber-500 dark:bg-amber-400";
    label = "Server";
    textColor = isHealthy 
      ? "text-success" 
      : "text-amber-500 dark:text-amber-400";
    statusTextColor = isHealthy 
      ? "text-gray-600 dark:text-gray-300" 
      : "text-amber-400 dark:text-amber-300";
  }

  if (collapsed) {
    // Collapsed version - with consistent height
    return (
      <div className="flex justify-center items-center h-9">
        <div className={cn(
          "relative",
          "w-auto h-auto"
        )}>
          {/* Icon with status indicator dot */}
          <div className={cn("w-5 h-5", iconColor)}>
            {icon}
          </div>
          <span className={cn(
            "absolute top-0 right-0 w-2 h-2 rounded-full",
            indicatorColor
          )}></span>
          
          {/* Tooltip content - using absolute positioning relative to the parent */}
          <div className="absolute left-full ml-3 top-1/2 -translate-y-1/2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-[9999] pointer-events-none">
            <div className="relative bg-white dark:bg-slate-800 shadow-lg rounded-md py-2 px-3 whitespace-nowrap text-xs border dark:border-slate-700 min-w-[140px] text-center">
              <div className="flex flex-col items-center gap-1">
                <span className={cn("font-medium", textColor)}>Server Status</span>
                <span className={cn("font-bold", statusTextColor)}>
                  {isLoading ? "Checking..." : isError ? "Unavailable" : ((data?.status === 'healthy' || data?.server === true) ? "Online" : "Issue detected")}
                </span>
                {data?.version && (
                  <span className="text-xs text-gray-400 mt-1">v{data.version}</span>
                )}
              </div>
              
              {/* Left-pointing arrow */}
              <div className="absolute top-1/2 -translate-y-1/2 left-[-6px] w-3 h-3 bg-white dark:bg-slate-800 transform rotate-45 border-l border-b dark:border-slate-700"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Expanded version (full status)
  return (
    <div className="bg-card rounded-md px-3 py-2 shadow-sm border border-border w-full">
      <div className="flex items-center justify-between w-full">
        <div className="flex items-center space-x-4">
          <div className="relative flex-shrink-0">
            <div className={cn("w-5 h-5", iconColor)}>
              {icon}
            </div>
            <span className={cn(
              "absolute top-0 right-0 w-2 h-2 rounded-full",
              indicatorColor
            )}></span>
          </div>
          <div className="flex flex-col">
            <span className={cn("text-xs font-semibold", textColor)}>
              {label}
            </span>
            <span className={cn("text-xs", statusTextColor)}>
              {isLoading ? "Checking..." : isError ? "Unavailable" : ((data?.status === 'healthy' || data?.server === true) ? "Online" : data?.status || "Issue detected")}
            </span>
          </div>
        </div>
        {data?.version && (
          <span className="text-xs text-gray-400 dark:text-gray-500 ml-2">v{data.version}</span>
        )}
      </div>
    </div>
  );
};

export default HealthStatus;