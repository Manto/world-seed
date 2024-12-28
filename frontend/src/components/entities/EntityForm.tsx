import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { EntityFormSkeleton } from './EntityFormSkeleton';
import { useEntityStore } from '@/stores/entityStore';
import type { Entity } from '@/types/graphql';

interface EntityFormProps {
    entity?: Entity;
    onClose: () => void;
}

export function EntityForm({ entity, onClose }: EntityFormProps) {
    const { entityTypes, loading, createEntity, updateEntity, generateDetails } = useEntityStore();

    const [formData, setFormData] = useState({
        name: entity?.name || '',
        typeId: entity?.typeDef.id || '',  // UUID string
        description: entity?.description || '',
        attributes: entity?.attributes || {},
    });

    if (loading) return <EntityFormSkeleton />;

    const selectedType = entityTypes.find(t => t.id === formData.typeId);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            if (entity) {
                await updateEntity(entity.id, formData);
            } else {
                await createEntity(formData);
            }
            onClose();
        } catch (error) {
            console.error('Error saving entity:', error);
        }
    };


    const handleGenerate = async () => {
        if (entity) {
            try {
                await generateDetails(entity.id);
                onClose();
            } catch (error) {
                console.error('Error generating details:', error);
            }
        }
    };

    return (
        <Card className="w-full max-w-2xl mx-auto">
            <CardHeader>
                <CardTitle>{entity ? 'Edit Entity' : 'Create New Entity'}</CardTitle>
            </CardHeader>
            <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                        <Label htmlFor="name">Name</Label>
                        <Input
                            id="name"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            required
                        />
                    </div>

                    {!entity && (
                        <div className="space-y-2">
                            <Label htmlFor="type">Entity Type</Label>
                            <Select
                                value={formData.typeId}  // No need to toString() since it's already a string
                                onValueChange={(value) => setFormData({ ...formData, typeId: value })}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select type..." />
                                </SelectTrigger>
                                <SelectContent>
                                    {entityTypes.map(type => (
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
                        <Textarea
                            id="description"
                            value={formData.description}
                            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                            className="h-32"
                        />
                    </div>

                    {selectedType && (
                        <div className="space-y-4">
                            <h3 className="font-medium">Attributes</h3>
                            {selectedType.defaultFields.map(field => (
                                <div key={field} className="space-y-2">
                                    <Label htmlFor={field}>{field}</Label>
                                    <Input
                                        id={field}
                                        value={formData.attributes[field] || ''}
                                        onChange={(e) => setFormData({
                                            ...formData,
                                            attributes: {
                                                ...formData.attributes,
                                                [field]: e.target.value
                                            }
                                        })}
                                    />
                                </div>
                            ))}
                        </div>
                    )}

                    <div className="flex justify-end space-x-2">
                        <Button type="button" variant="outline" onClick={onClose}>
                            Cancel
                        </Button>
                        {entity && (
                            <Button type="button" onClick={handleGenerate} disabled={loading}>
                                {loading ? 'Generating...' : 'Generate Details'}
                            </Button>
                        )}
                        <Button type="submit" disabled={loading}>
                            {loading ? (entity ? 'Updating...' : 'Creating...') : (entity ? 'Update' : 'Create')}
                        </Button>
                    </div>
                </form>
            </CardContent>
        </Card>
    );
}