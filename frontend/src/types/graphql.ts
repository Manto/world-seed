export interface GenerationTemplate {
    fields: string[];
    systemPrompt: string;
}

export interface EntityType {
    id: string;  // UUID string
    name: string;
    defaultFields: string[];
}

export interface Entity {
    id: string;  // UUID string
    name: string;
    description: string | null;
    attributes: Record<string, any>;
    generationTemplate: GenerationTemplate;
    typeDef: EntityType;
    createdAt: string;
    updatedAt: string;
}

export interface EntityInput {
    name: string;
    typeId: string;  // UUID string
    description?: string | null;
    attributes?: Record<string, any>;
    generationTemplate?: GenerationTemplate;
    parentIds?: string[];  // UUID strings
}

export interface EntityUpdateInput {
    name?: string;
    description?: string | null;
    attributes?: Record<string, any>;
    generationTemplate?: GenerationTemplate;
    parentIds?: string[];  // UUID strings
}