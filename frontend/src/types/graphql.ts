export interface EntityType {
  id: string; // UUID string
  name: string;
  defaultFields: string[];
}

export interface EntityTypeInput {
  name: string;
  defaultFields?: string[];
}

export interface Entity {
  id: string; // UUID string
  name: string;
  description: string | null;
  attributes: Record<string, any>;
  typeDef: EntityType;
  createdAt: string;
  updatedAt: string;
}

export interface EntityInput {
  name: string;
  typeId: string; // UUID string
  description?: string | null;
  attributes?: Record<string, any>;
  // parentIds?: string[]; // UUID strings
}

export interface EntityUpdateInput {
  name?: string;
  description?: string | null;
  attributes?: Record<string, any>;
  // parentIds?: string[]; // UUID strings
}

export interface GetEntitiesData {
  entities: Entity[];
}

export interface GetEntityTypesData {
  entityTypes: EntityType[];
}

export interface CreateEntityData {
  createEntity: Entity;
}

export interface UpdateEntityData {
  updateEntity: Entity;
}

export interface GenerateDetailsData {
  generateAndUpdateEntity: Entity;
}
