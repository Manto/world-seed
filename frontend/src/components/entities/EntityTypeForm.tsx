import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { useEntityStore } from "@/stores/entityStore";
import type { EntityType } from "@/types/graphql";

interface EntityTypeFormProps {
  entityType?: EntityType;
  onClose: () => void;
}

export function EntityTypeForm({ entityType, onClose }: EntityTypeFormProps) {
  const { createEntityType, updateEntityType, loading } = useEntityStore();

  const [formData, setFormData] = useState({
    name: entityType?.name || "",
    defaultFields: entityType?.defaultFields.join("\n") || "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const fields = formData.defaultFields
      .split("\n")
      .map((f) => f.trim())
      .filter(Boolean);

    if (entityType) {
      await updateEntityType(entityType.id, {
        name: formData.name,
        defaultFields: fields,
      });
    } else {
      await createEntityType({
        name: formData.name,
        defaultFields: fields,
      });
    }
    onClose();
  };

  return (
    <div className="py-2">
      <DialogHeader>
        <DialogTitle>
          {entityType ? "Edit Entity Type" : "Create Entity Type"}
        </DialogTitle>
      </DialogHeader>

      <form onSubmit={handleSubmit} className="space-y-6 mt-4">
        <div className="space-y-2">
          <Label htmlFor="name">Name</Label>
          <Input
            id="name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="fields">Default Fields (one per line)</Label>
          <Textarea
            id="fields"
            value={formData.defaultFields}
            onChange={(e) =>
              setFormData({ ...formData, defaultFields: e.target.value })
            }
            className="min-h-[200px]"
            placeholder="Enter fields, one per line"
            required
          />
        </div>

        <div className="flex justify-end space-x-2 pt-4">
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" disabled={loading}>
            {loading
              ? entityType
                ? "Updating..."
                : "Creating..."
              : entityType
              ? "Update"
              : "Create"}
          </Button>
        </div>
      </form>
    </div>
  );
}
