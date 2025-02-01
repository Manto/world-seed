import React, { useEffect } from "react";
import { Github } from "lucide-react";
import { Toaster } from "@/components/ui/toaster";
import { EntityDashboard } from "@/components/entities/EntityDashboard";
import { EntityTypeDashboard } from "@/components/entities/EntityTypeDashboard";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useEntityStore } from "./stores/entityStore";
import { TooltipProvider } from "@/components/ui/tooltip";

export default function App() {
  const { fetchEntityTypes } = useEntityStore();

  useEffect(() => {
    // Fetch entity types on app initialization
    fetchEntityTypes();
  }, [fetchEntityTypes]);

  return (
    <TooltipProvider>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <h1 className="text-xl font-bold">Worldbuilding Assistant</h1>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Tabs defaultValue="entities">
            <TabsList className="mb-4">
              <TabsTrigger value="entities">Entities</TabsTrigger>
              <TabsTrigger value="types">Entity Types</TabsTrigger>
            </TabsList>
            <TabsContent value="entities">
              <EntityDashboard />
            </TabsContent>
            <TabsContent value="types">
              <EntityTypeDashboard />
            </TabsContent>
          </Tabs>
        </main>
        <footer className="bg-white border-t mt-auto">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="py-4 text-center text-sm text-gray-500">
              <div className="flex justify-center items-center space-x-2">
                <a
                  href="https://github.com/manto/llm-world-builder"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-gray-300 hover:text-white transition-colors duration-200"
                >
                  <Github className="w-5 h-5 mr-2" />
                  <span className="text-sm font-medium">llm-world-builder</span>
                </a>
              </div>
            </div>
          </div>
        </footer>
        <Toaster />
      </div>
    </TooltipProvider>
  );
}
