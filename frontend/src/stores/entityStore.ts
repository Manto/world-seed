import { create } from "zustand";
import { entityService } from "../services/entityService";
import type {
  Entity,
  EntityType,
  EntityInput,
  EntityUpdateInput,
  EntityTypeInput,
} from "../types/graphql";

interface EntityState {
  entities: Entity[];
  entityTypes: EntityType[];
  loading: boolean;
  searchQuery: string;

  // Fetch operations
  fetchEntities: () => Promise<void>;
  fetchEntityTypes: () => Promise<void>;

  // Entity operations
  createEntity: (input: EntityInput) => Promise<void>;
  updateEntity: (id: string, input: EntityUpdateInput) => Promise<void>;
  generateDetails: (id: string) => Promise<void>;

  // EntityType operations
  createEntityType: (input: EntityTypeInput) => Promise<void>;
  updateEntityType: (id: string, input: EntityTypeInput) => Promise<void>;

  // UI state
  setSearchQuery: (query: string) => void;
  setError: (error: string | null) => void;
}

export const useEntityStore = create<EntityState>((set, get) => ({
  entities: [],
  entityTypes: [],
  loading: false,
  searchQuery: "",

  setSearchQuery: (query) => set({ searchQuery: query }),
  setError: (error) => set({ error }),

  fetchEntities: async () => {
    set({ loading: true });
    try {
      const data = await entityService.getEntities();
      set({ entities: data.entities, loading: false });
    } finally {
      set({ loading: false });
    }
  },

  fetchEntityTypes: async () => {
    set({ loading: true });
    try {
      const data = await entityService.getEntityTypes();
      set({ entityTypes: data.entityTypes, loading: false });
    } finally {
      set({
        loading: false,
      });
    }
  },

  createEntity: async (input) => {
    set({ loading: true });
    try {
      const data = await entityService.createEntity(input);
      set((state) => ({
        entities: [...state.entities, data.createEntity],
        loading: false,
      }));
    } finally {
      set({
        loading: false,
      });
    }
  },

  updateEntity: async (id: string, input) => {
    set({ loading: true });
    try {
      const data = await entityService.updateEntity(id, input);
      set((state) => ({
        entities: state.entities.map((e) =>
          e.id === id ? data.updateEntity : e
        ),
        loading: false,
      }));
    } finally {
      set({
        loading: false,
      });
    }
  },

  createEntityType: async (input) => {
    set({ loading: true });
    try {
      const data = await entityService.createEntityType(input);
      set((state) => ({
        entityTypes: [...state.entityTypes, data.createEntityType],
        loading: false,
      }));
    } finally {
      set({
        loading: false,
      });
    }
  },

  updateEntityType: async (id: string, input) => {
    set({ loading: true });
    try {
      const data = await entityService.updateEntityType(id, input);
      set((state) => ({
        entityTypes: state.entityTypes.map((e) =>
          e.id === id ? data.updateEntityType : e
        ),
        loading: false,
      }));
    } finally {
      set({
        loading: false,
      });
    }
  },

  generateDetails: async (id: string) => {
    set({ loading: true });
    try {
      const data = await entityService.generateDetails(id);
      set((state) => ({
        entities: state.entities.map((e) =>
          e.id === id
            ? { ...e, attributes: data.generateAndUpdateEntity.attributes }
            : e
        ),
        loading: false,
      }));
    } finally {
      set({
        loading: false,
      });
    }
  },
}));
