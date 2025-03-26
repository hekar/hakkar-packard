import React from "react";
import { 
  Card, 
  CardHeader, 
  CardTitle, 
  CardDescription, 
  CardContent 
} from "@/components/ui/card";

const DashboardCards: React.FC = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
      <Card>
        <CardHeader>
          <CardTitle className="text-primary">Overview</CardTitle>
          <CardDescription>A summary of your dashboard</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="dark:text-gray-300">This card demonstrates the shadcn/ui Card component.</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-primary">Features</CardTitle>
          <CardDescription>Key capabilities</CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="list-disc pl-5 space-y-2 dark:text-gray-300">
            <li>React + TypeScript</li>
            <li>Tailwind CSS</li>
            <li>shadcn/ui components</li>
            <li>Feature-based architecture</li>
          </ul>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-primary">Getting Started</CardTitle>
          <CardDescription>Next steps</CardDescription>
        </CardHeader>
        <CardContent>
          <p className="dark:text-gray-300">This template follows a best-practice architecture with:</p>
          <ul className="list-disc pl-5 mt-2 space-y-1 dark:text-gray-300">
            <li>Pages for routes</li>
            <li>Features for business logic</li>
            <li>Components for UI elements</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  );
};

export default DashboardCards;