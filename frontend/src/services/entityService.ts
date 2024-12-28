import { graphqlRequest } from "../lib/graphql-client";
import type {
  Entity,
  EntityType,
  EntityInput,
  EntityTypeInput,
  EntityUpdateInput,
  GetEntitiesData,
  GetEntityTypesData,
} from "../types/graphql";

export const entityService = {
  async getEntities() {
    return graphqlRequest<GetEntitiesData>(`
      query GetEntities {
        entities {
          id
          name
          description
          attributes
          typeDef {
            id
            name
            defaultFields
          }
          createdAt
          updatedAt
        }
      }
    `);
  },

  async getEntityTypes() {
    return graphqlRequest<GetEntityTypesData>(`
      query GetEntityTypes {
        entityTypes {
          id
          name
          defaultFields
        }
      }
    `);
  },

  async createEntityType(input: EntityTypeInput) {
    return graphqlRequest<{ createEntityType: EntityType }>(
      `
      mutation CreateEntityType($input: EntityTypeInput!) {
        createEntityType(input: $input) {
          id
          name
          defaultFields
        }
      }
    `,
      { input }
    );
  },

  async updateEntityType(id: string, input: Partial<EntityTypeInput>) {
    return graphqlRequest<{ updateEntityType: EntityType }>(
      `
      mutation UpdateEntityType($id: String!, $input: EntityTypeUpdateInput!) {
        updateEntityType(id: $id, input: $input) {
          id
          name
          defaultFields
        }
      }
    `,
      { id, input }
    );
  },

  async createEntity(input: EntityInput) {
    return graphqlRequest<{ createEntity: Entity }>(
      `
      mutation CreateEntity($input: EntityInput!) {
        createEntity(input: $input) {
          id
          name
          description
          attributes
          typeDef {
            id
            name
            defaultFields
          }
        }
      }
    `,
      { input }
    );
  },

  async updateEntity(id: string, input: EntityUpdateInput) {
    return graphqlRequest<{ updateEntity: Entity }>(
      `
      mutation UpdateEntity($id: String!, $input: EntityUpdateInput!) {
        updateEntity(id: $id, input: $input) {
          id
          name
          description
          attributes
          typeDef {
            id
            name
            defaultFields
          }
        }
      }
    `,
      { id, input }
    );
  },

  async generateDetails(id: string) {
    return graphqlRequest<{ generateAndUpdateEntity: Entity }>(
      `
      mutation GenerateDetails($id: String!) {
        generateAndUpdateEntity(entityId: $id) {
          id
          attributes
        }
      }
    `,
      { id }
    );
  },
};
