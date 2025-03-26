import React from "react";
import WelcomeSection from "./WelcomeSection";
import DashboardCards from "./DashboardCards";

const DashboardView: React.FC = () => {
  return (
    <div className="w-full px-4 md:px-8 lg:px-12 py-8">
      <h1 className="text-3xl font-bold mb-6 text-primary">Dashboard</h1>
      <WelcomeSection />
      <DashboardCards />
    </div>
  );
};

export default DashboardView;