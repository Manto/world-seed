import { useState } from "react";
import { Button } from "@/components/ui/button";
import { EntityTypeList } from "./EntityTypeList";
import { EntityTypeForm } from "./EntityTypeForm";
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Plus } from "lucide-react";
import type { EntityType } from "@/types/graphql";

export function EntityTypeDashboard() {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedType, setSelectedType] = useState<EntityType | undefined>();

  const handleEditType = (type: EntityType) => {
    setSelectedType(type);
    setIsFormOpen(true);
  };

  const handleCreateType = () => {
    setSelectedType(undefined);
    setIsFormOpen(true);
  };

  const handleCloseForm = () => {
    setIsFormOpen(false);
    setSelectedType(undefined);
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Entity Types</h1>
        <Button onClick={handleCreateType}>
          <Plus className="w-4 h-4 mr-2" />
          New Type
        </Button>
      </div>

      <EntityTypeList onEditType={handleEditType} />

      <Dialog open={isFormOpen} onOpenChange={setIsFormOpen}>
        <DialogContent className="max-w-2xl">
          <EntityTypeForm entityType={selectedType} onClose={handleCloseForm} />
        </DialogContent>
      </Dialog>
    </div>
  );
}
