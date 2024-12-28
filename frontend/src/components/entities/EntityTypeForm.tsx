import React, { useState } from "react";
import { useEntityStore } from "@/stores/entityStore";

interface EntityTypeFormProps {
  entityType?: {
    id: string;
    name: string;
    default_fields: string[];
  };
  onSubmit: () => void;
}

export const EntityTypeForm: React.FC<EntityTypeFormProps> = ({
  entityType,
  onSubmit,
}) => {
  const { createEntityType, updateEntityType } = useEntityStore();

  const [formData, setFormData] = useState({
    name: entityType?.name || "",
    default_fields: entityType?.default_fields || [],
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (entityType) {
      await updateEntityType(entityType.id, formData);
    } else {
      await createEntityType(formData);
    }
    onSubmit();
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="mb-4">
        <label className="block text-sm font-medium">Name</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
      </div>
      <div className="mb-4">
        <label className="block text-sm font-medium">Default Fields</label>
        <input
          type="text"
          value={formData.default_fields.join(", ")}
          onChange={(e) =>
            setFormData({
              ...formData,
              default_fields: e.target.value.split(",").map((f) => f.trim()),
            })
          }
          className="mt-1 block w-full rounded-md border-gray-300"
          placeholder="Enter fields separated by commas"
        />
      </div>
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {entityType ? "Update" : "Create"} Entity Type
      </button>
    </form>
  );
};
