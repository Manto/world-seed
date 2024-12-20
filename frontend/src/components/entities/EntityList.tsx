import React, { useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Search } from 'lucide-react';
import { ErrorMessage } from '@/components/ErrorMessage';
import { EntityListSkeleton } from './EntitySkeleton';
import { useEntityStore } from '@/stores/entityStore';
import type { Entity } from '@/types/graphql';

interface EntityListProps {
    onEditEntity: (entity: Entity) => void;
}

export function EntityList({ onEditEntity }: EntityListProps) {
    const {
        entities,
        loading,
        error,
        searchQuery,
        setSearchQuery,
        fetchEntities
    } = useEntityStore();

    useEffect(() => {
        fetchEntities();
    }, [fetchEntities]);

    if (loading) return <EntityListSkeleton />;
    if (error) return <ErrorMessage message={error} onRetry={fetchEntities} />;

    const filteredEntities = entities.filter(entity =>
        entity.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        entity.description?.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="space-y-4">
            <div className="flex items-center space-x-2">
                <Search className="w-4 h-4 text-gray-400" />
                <Input
                    placeholder="Search entities..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="flex-1"
                />
            </div>

            <div className="grid gap-4">
                {filteredEntities.length === 0 ? (
                    <div className="text-center text-gray-500 py-8">
                        {searchQuery ? 'No entities found for your search' : 'No entities created yet'}
                    </div>
                ) : (
                    filteredEntities.map((entity) => (
                        <Card
                            key={entity.id}
                            className="hover:bg-gray-50 cursor-pointer transition-colors"
                            onClick={() => onEditEntity(entity)}
                        >
                            <CardHeader className="pb-2">
                                <CardTitle className="text-lg flex justify-between items-center">
                                    {entity.name}
                                    <span className="text-sm text-gray-500">{entity.typeDef.name}</span>
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-gray-600 text-sm">
                                    {entity.description || 'No description'}
                                </p>
                            </CardContent>
                        </Card>
                    ))
                )}
            </div>
        </div>
    );
}