import React, { useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import {
  LayoutDashboard,
  Menu,
  X,
  ChevronLeft,
  ChevronRight,
  Moon,
  Sun,
  MessageSquare,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useLayoutStore } from "../stores/useLayoutStore";
import HealthStatus from "./HealthStatus";

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const appTitle = "Postgres Project";
  const location = useLocation();

  // Use the layout store instead of local state
  const {
    sidebarOpen,
    sidebarCollapsed,
    theme,
    toggleSidebar,
    setSidebarOpen,
    toggleSidebarCollapse,
    setSidebarCollapsed,
    toggleTheme,
  } = useLayoutStore();

  // Check if screen is large enough to show expanded sidebar by default
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 1024) {
        setSidebarCollapsed(false); // On smaller screens, don't collapse
      }
    };

    // Set initial state
    handleResize();

    // Add event listener
    window.addEventListener("resize", handleResize);

    // Clean up
    return () => window.removeEventListener("resize", handleResize);
  }, [setSidebarCollapsed]);

  // Ensure theme is applied correctly when component mounts
  useEffect(() => {
    // This ensures the theme is applied to the document when the component mounts
    const currentTheme = theme;
    document.documentElement.classList.remove("light", "dark");
    document.documentElement.classList.add(currentTheme);
  }, [theme]);

  const navItems = [
    {
      name: "Dashboard",
      path: "/",
      icon: <LayoutDashboard className="w-5 h-5" />,
    },
    {
      name: "ChatGPT",
      path: "/chat",
      icon: <MessageSquare className="w-5 h-5" />,
    },
  ];

  return (
    <div className="flex h-screen overflow-hidden bg-background transition-colors duration-200">
      {/* Sidebar overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={toggleSidebar}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`fixed lg:relative z-50 h-full bg-card shadow-xl transform transition-all duration-300 ease-in-out ${
          sidebarOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        } ${sidebarCollapsed ? "lg:w-20" : "w-64"}`}
      >
        <div className="flex flex-col h-full">
          {/* Header with logo */}
          <div
            className={`px-4 py-6 border-b border-border ${
              sidebarCollapsed ? "flex justify-center" : ""
            }`}
          >
            <Link to="/" className="flex items-center">
              {sidebarCollapsed ? (
                <span className="text-2xl font-bold text-primary">A</span>
              ) : (
                <h1 className="text-xl font-bold text-primary">{appTitle}</h1>
              )}
            </Link>
          </div>

          <nav className="flex-1 px-2 py-4 space-y-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center ${
                  sidebarCollapsed ? "justify-center" : ""
                } px-4 py-3 rounded-md transition-colors
                  ${
                    location.pathname === item.path
                      ? "bg-accent dark:bg-accent/30 text-primary"
                      : "text-gray-600 dark:text-gray-300 hover:bg-accent dark:hover:bg-accent/20"
                  }`}
                onClick={() => setSidebarOpen(false)}
              >
                <span
                  className={`${sidebarCollapsed ? "" : "mr-3"} ${
                    location.pathname === item.path
                      ? "text-primary"
                      : "text-gray-500 dark:text-gray-400"
                  }`}
                >
                  {item.icon}
                </span>
                {!sidebarCollapsed && (
                  <span className="font-medium">{item.name}</span>
                )}
              </Link>
            ))}
          </nav>

          <div className="mt-auto">
            {/* Footer sections with outlined buttons */}
            <div className="border-t border-b dark:border-slate-700 py-3">
              <div
                className={`flex flex-col items-center justify-center ${
                  sidebarCollapsed ? "space-y-3" : "space-y-4"
                }`}
              >
                {/* Health status */}
                <div
                  className={
                    sidebarCollapsed
                      ? "w-full flex justify-center"
                      : "w-full px-3"
                  }
                >
                  <HealthStatus collapsed={sidebarCollapsed} />
                </div>

                {/* Separator - full width in both collapsed and expanded states */}
                <div className="w-full h-px bg-gray-200 dark:bg-slate-700"></div>

                {/* Theme toggle */}
                <div
                  className={
                    sidebarCollapsed
                      ? "w-full flex justify-center"
                      : "w-full px-3"
                  }
                >
                  {sidebarCollapsed ? (
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={toggleTheme}
                      className="h-9 w-9 bg-transparent hover:bg-accent border border-border rounded-md"
                    >
                      {theme === "light" ? (
                        <Moon className="h-5 w-5 text-primary" />
                      ) : (
                        <Sun className="h-5 w-5 text-yellow-500" />
                      )}
                    </Button>
                  ) : (
                    <Button
                      variant="ghost"
                      onClick={toggleTheme}
                      className="h-9 flex justify-start items-center w-full px-3 bg-transparent border border-border hover:bg-accent rounded-md"
                    >
                      {theme === "light" ? (
                        <Moon className="h-5 w-5 text-primary mr-2" />
                      ) : (
                        <Sun className="h-5 w-5 text-yellow-500 mr-2" />
                      )}
                      <span className="text-sm text-gray-700 dark:text-gray-300">
                        {theme === "light" ? "Dark Mode" : "Light Mode"}
                      </span>
                    </Button>
                  )}
                </div>

                {/* Collapse/expand toggle */}
                <div
                  className={
                    sidebarCollapsed
                      ? "w-full flex justify-center"
                      : "w-full px-3"
                  }
                >
                  {sidebarCollapsed ? (
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={toggleSidebarCollapse}
                      className="h-9 w-9 bg-transparent hover:bg-accent border border-border rounded-md"
                      aria-label="Expand sidebar"
                    >
                      <ChevronRight className="h-5 w-5 text-primary" />
                    </Button>
                  ) : (
                    <Button
                      variant="ghost"
                      onClick={toggleSidebarCollapse}
                      className="h-9 flex justify-start items-center w-full px-3 bg-transparent border border-border hover:bg-accent rounded-md"
                      aria-label="Collapse sidebar"
                    >
                      <ChevronLeft className="h-5 w-5 text-primary mr-2" />
                      <span className="text-sm text-gray-700 dark:text-gray-300">
                        Collapse Sidebar
                      </span>
                    </Button>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-y-auto transition-all duration-300">
        <header
          className="lg:hidden sticky top-0 z-30 bg-card shadow-md"
          style={{ height: "80px" }}
        >
          <div className="h-full w-full flex items-center justify-between px-6">
            <Button
              variant="ghost"
              size="default"
              onClick={toggleSidebar}
              className="p-2"
            >
              {sidebarOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </Button>
            <h1 className="text-2xl font-bold text-primary">{appTitle}</h1>
            <div className="w-10"></div> {/* Spacer to center the title */}
          </div>
        </header>

        <main className="flex-1 w-full h-full">
          <div className="w-full h-full">{children}</div>
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
