import { useEffect } from 'react';
import { useLayoutStore } from '../stores/useLayoutStore';

/**
 * ThemeInitializer component ensures the theme is properly applied
 * when the application initially loads.
 * 
 * It doesn't render any UI, just applies the theme class to the document.
 */
export const ThemeInitializer = () => {
  const { theme } = useLayoutStore();
  
  useEffect(() => {
    // Apply theme class to document element
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(theme);
  }, [theme]);
  
  // This component doesn't render anything
  return null;
};

export default ThemeInitializer;