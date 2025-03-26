import { useTheme } from "@/lib/theme-provider";
import { Button } from "@/components/ui/button";
import { Moon, Sun } from "lucide-react";

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <Button 
      variant="ghost" 
      onClick={toggleTheme}
      className="h-9 flex justify-start items-center w-full px-3 bg-transparent border border-border hover:bg-accent rounded-md text-foreground"
    >
      {theme === "light" ? (
        <Moon className="h-5 w-5 text-primary mr-2" />
      ) : (
        <Sun className="h-5 w-5 text-yellow-500 mr-2" />
      )}
      <span className="text-sm">{theme === "light" ? "Dark Mode" : "Light Mode"}</span>
    </Button>
  );
}