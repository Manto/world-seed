import { useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { EntityListSkeleton } from "./EntitySkeleton";
import { ErrorMessage } from "@/components/ErrorMessage";
import { useEntityStore } from "@/stores/entityStore";
import type { EntityType } from "@/types/graphql";

interface EntityTypeListProps {
  onEditType: (type: EntityType) => void;
}

export function EntityTypeList({ onEditType }: EntityTypeListProps) {
  const { entityTypes, loading, error, fetchEntityTypes } = useEntityStore();

  useEffect(() => {
    fetchEntityTypes();
  }, [fetchEntityTypes]);

  if (loading) return <EntityListSkeleton />;
  if (error) return <ErrorMessage message={error} onRetry={fetchEntityTypes} />;

  return (
    <div className="grid gap-4">
      {entityTypes.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          No entity types created yet
        </div>
      ) : (
        entityTypes.map((type) => (
          <Card
            key={type.id}
            className="hover:bg-gray-50 cursor-pointer transition-colors"
            onClick={() => onEditType(type)}
          >
            <CardHeader>
              <CardTitle className="text-lg">{type.name}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {type.defaultFields.map((field) => (
                  <span
                    key={field}
                    className="px-2 py-1 bg-gray-100 rounded-md text-sm"
                  >
                    {field}
                  </span>
                ))}
              </div>
            </CardContent>
          </Card>
        ))
      )}
    </div>
  );
}
