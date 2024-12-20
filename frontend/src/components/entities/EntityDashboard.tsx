import React from 'react';
import { Button } from '@/components/ui/button';
import { EntityList } from './EntityList';
import { EntityForm } from './EntityForm';
import { Plus } from 'lucide-react';
import { useUIStore } from '@/stores/uiStore';
import type { Entity } from '@/types/graphql';

export function EntityDashboard() {
    const {
        isEntityFormOpen,
        selectedEntity,
        setSelectedEntity,
        openEntityForm,
        closeEntityForm
    } = useUIStore();

    const handleEditEntity = (entity: Entity) => {
        setSelectedEntity(entity);
        openEntityForm();
    };

    return (
        <div className="p-6">
            {!isEntityFormOpen ? (
                <div className="space-y-4">
                    <div className="flex justify-between items-center">
                        <h1 className="text-2xl font-bold">Entities</h1>
                        <Button onClick={() => {
                            setSelectedEntity(null);
                            openEntityForm();
                        }}>
                            <Plus className="w-4 h-4 mr-2" />
                            New Entity
                        </Button>
                    </div>
                    <EntityList onEditEntity={handleEditEntity} />
                </div>
            ) : (
                <EntityForm entity={selectedEntity} onClose={closeEntityForm} />
            )}
        </div>
    );
}