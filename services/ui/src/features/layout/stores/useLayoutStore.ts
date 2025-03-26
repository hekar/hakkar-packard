import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

export type Theme = 'light' | 'dark';

// Helper function to safely update the DOM theme
const updateDocumentTheme = (theme: Theme) => {
  if (typeof window === 'undefined') return;
  
  const root = document.documentElement;
  root.classList.remove('light', 'dark');
  root.classList.add(theme);
  localStorage.setItem('theme', theme); // Also update localStorage directly
};

interface LayoutState {
  // Sidebar state
  sidebarOpen: boolean;
  sidebarCollapsed: boolean;
  
  // Theme state
  theme: Theme;
  
  // Actions
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  toggleSidebarCollapse: () => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

// Detect initial theme from localStorage or system preference
const getInitialTheme = (): Theme => {
  if (typeof window === 'undefined') return 'light';
  
  const savedTheme = localStorage.getItem('theme') as Theme;
  if (savedTheme) return savedTheme;
  
  // If no saved theme, try to detect system preference
  const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  return systemTheme;
};

export const useLayoutStore = create<LayoutState>()(
  persist(
    (set) => ({
      // Initial state
      sidebarOpen: false,
      sidebarCollapsed: false,
      theme: getInitialTheme(),
      
      // Actions
      toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      
      toggleSidebarCollapse: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
      
      toggleTheme: () => 
        set((state) => {
          const newTheme = state.theme === 'light' ? 'dark' : 'light';
          updateDocumentTheme(newTheme);
          return { theme: newTheme };
        }),
      setTheme: (theme) => {
        updateDocumentTheme(theme);
        set({ theme });
      },
    }),
    {
      name: 'layout-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ 
        sidebarCollapsed: state.sidebarCollapsed,
        theme: state.theme 
      }),
    }
  )
);

// Initialize theme when the module loads
if (typeof window !== 'undefined') {
  // Apply the theme from the store
  const theme = useLayoutStore.getState().theme;
  updateDocumentTheme(theme);
  
  // Also set up a listener for system theme changes
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    if (!localStorage.getItem('theme')) { // Only update if user hasn't explicitly set a preference
      const newTheme = event.matches ? 'dark' : 'light';
      useLayoutStore.getState().setTheme(newTheme);
    }
  });
}