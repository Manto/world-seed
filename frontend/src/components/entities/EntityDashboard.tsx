import { useState } from "react";
import { Button } from "@/components/ui/button";
import { EntityList } from "./EntityList";
import { EntityForm } from "./EntityForm";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Plus } from "lucide-react";
import { useEntityStore } from "@/stores/entityStore";
import type { Entity } from "@/types/graphql";

export function EntityDashboard() {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedEntity, setSelectedEntity] = useState<Entity | undefined>();

  const handleEditEntity = (entity: Entity) => {
    setSelectedEntity(entity);
    setIsFormOpen(true);
  };

  const handleCreateEntity = () => {
    setSelectedEntity(undefined);
    setIsFormOpen(true);
  };

  const handleCloseForm = () => {
    setIsFormOpen(false);
    setSelectedEntity(undefined);
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Entities</h1>
        <Button onClick={handleCreateEntity}>
          <Plus className="w-4 h-4 mr-2" />
          New Entity
        </Button>
      </div>

      <EntityList onEditEntity={handleEditEntity} />

      <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
        <DialogContent className="max-w-4xl">
          <EntityForm entity={selectedEntity} onClose={handleCloseForm} />
        </DialogContent>
      </Dialog>
    </div>
  );
}
