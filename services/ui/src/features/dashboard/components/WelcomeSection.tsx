import React from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const WelcomeSection: React.FC = () => {
  return (
    <Card className="mb-8">
      <CardContent className="pt-6">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4 text-gray-900 dark:text-white">
            Welcome to Postgres Project
          </h2>
          <p className="text-gray-600 dark:text-gray-300 mb-6 max-w-3xl mx-auto">
            This is a simple hello world dashboard built with best practices. It
            uses React, Tailwind CSS, and shadcn/ui components with a sidebar
            layout.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button
              onClick={() => alert("Hello World!")}
              className="bg-primary hover:bg-primary/80 text-primary-foreground"
            >
              Click Me
            </Button>
            <Button
              variant="outline"
              className="border-primary text-primary hover:bg-accent dark:hover:bg-accent/30"
            >
              Learn More
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default WelcomeSection;
