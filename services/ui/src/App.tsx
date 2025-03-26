import { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";

// Layout from features
import { MainLayout, ThemeInitializer } from "@/features/layout";

// Pages
import Dashboard from "@/pages/Dashboard";
import ChatGPT from "@/pages/ChatGPT";

function App() {
  // Any app initialization logic can go here
  useEffect(() => {
    console.log("App initialized");
  }, []);

  return (
    <Router>
      {/* ThemeInitializer to ensure theme is applied early */}
      <ThemeInitializer />
      
      <MainLayout>
        <Routes>
          {/* Main dashboard route */}
          <Route path="/" element={<Dashboard />} />
          
          {/* ChatGPT route */}
          <Route path="/chat" element={<ChatGPT />} />
        </Routes>
      </MainLayout>
    </Router>
  );
}

export default App;