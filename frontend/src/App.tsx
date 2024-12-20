import React, { useEffect } from 'react';
import { EntityDashboard } from './components/entities/EntityDashboard';
import { useEntityStore } from './stores/entityStore';
import { ErrorMessage } from './components/ErrorMessage';

export default function App() {
  const { fetchEntityTypes, error } = useEntityStore();

  useEffect(() => {
    // Fetch entity types on app initialization
    fetchEntityTypes();
  }, [fetchEntityTypes]);

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-bold">Worldbuilding Assistant</h1>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && <ErrorMessage message={error} />}
        <EntityDashboard />
      </main>

      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-4 text-center text-sm text-gray-500">
            Built with FastAPI, React, and Claude
          </div>
        </div>
      </footer>
    </div>
  );
}