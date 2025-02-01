import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Blocks } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { useEntityStore } from "@/stores/entityStore";
import type { Entity } from "@/types/graphql";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface EntityFormProps {
  entity?: Entity;
  onClose: () => void;
}

export function EntityForm({ entity, onClose }: EntityFormProps) {
  const { entityTypes, loading, createEntity, updateEntity, generateDetails } =
    useEntityStore();

  const [formData, setFormData] = useState({
    name: entity?.name || "",
    typeId: entity?.typeDef.id || "",
    description: entity?.description || "",
    attributes: entity?.attributes || {},
  });

  const selectedType = entityTypes.find((t) => t.id === formData.typeId);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (entity) {
        // We do not change typeId for an existing entity
        const { typeId, ...updateData } = formData;
        await updateEntity(entity.id, updateData);
      } else {
        await createEntity(formData);
      }
      onClose();
    } catch (error) {
      console.error("Error saving entity:", error);
    }
  };

  const handleGenerate = async () => {
    if (entity) {
      try {
        await generateDetails(entity.id);
        onClose();
      } catch (error) {
        console.error("Error generating details:", error);
      }
    }
  };

  const handleGenerateAttribute = async (field: string) => {
    console.log(`Generating content for ${field}`);
    // TODO: Implement attribute generation
  };

  return (
    <div className="py-2">
      <DialogHeader>
        <DialogTitle>
          {entity ? "Edit Entity" : "Create New Entity"}
        </DialogTitle>
      </DialogHeader>

      <form onSubmit={handleSubmit} className="space-y-6 mt-4">
        <div className="grid grid-cols-4 gap-4">
          <Label htmlFor="name">Name</Label>
          <Input
            id="name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
            className="col-span-3"
          />
        </div>

        {!entity && (
          <div className="grid grid-cols-4 gap-4">
            <Label htmlFor="type">Entity Type</Label>
            <Select
              value={formData.typeId}
              onValueChange={(value) =>
                setFormData({ ...formData, typeId: value })
              }
            >
              <SelectTrigger>
                <SelectValue placeholder="Select type..." />
              </SelectTrigger>
              <SelectContent>
                {entityTypes.map((type) => (
                  <SelectItem key={type.id} value={type.id}>
                    {type.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        <div className="space-y-2">
          <Label htmlFor="description">Description</Label>
          <div className="flex gap-2">
            <Textarea
              id="description"
              rows={3}
              value={formData.description}
              onChange={(e) =>
                setFormData({ ...formData, description: e.target.value })
              }
            />
          </div>
        </div>

        {selectedType && (
          <>
            <h3 className="font-medium">Attributes</h3>
            <div className="space-y-4 h-[40vh] overflow-y-auto">
              {selectedType.defaultFields.map((field) => (
                <div key={field} className="grid grid-cols-5 gap-4">
                  <Label htmlFor={field} className="col-span-1">
                    {field}
                  </Label>
                  <div className="col-span-4 flex gap-2">
                    <Textarea
                      id={field}
                      value={formData.attributes[field] || ""}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          attributes: {
                            ...formData.attributes,
                            [field]: e.target.value,
                          },
                        })
                      }
                      rows={4}
                      className="flex-1"
                    />
                    {entity && (
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <Button
                            type="button"
                            variant="outline"
                            size="icon"
                            onClick={() => handleGenerateAttribute(field)}
                          >
                            <Blocks />
                          </Button>
                        </TooltipTrigger>
                        <TooltipContent>
                          {entity.attributes[field] ? (
                            <p>Regenerate {field}</p>
                          ) : (
                            <p>Generate {field}</p>
                          )}
                        </TooltipContent>
                      </Tooltip>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </>
        )}

        <div className="flex justify-end space-x-2 pt-4">
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          {entity && (
            <Button
              type="button"
              variant="secondary"
              onClick={handleGenerate}
              disabled={loading}
            >
              {loading ? "Generating..." : "Generate Details"}
            </Button>
          )}
          <Button type="submit" disabled={loading}>
            {loading
              ? entity
                ? "Updating..."
                : "Creating..."
              : entity
              ? "Update"
              : "Create"}
          </Button>
        </div>
      </form>
    </div>
  );
}
