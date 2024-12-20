import { create } from 'zustand';
import type { Entity } from '@/types/graphql';

interface UIState {
    // Entity management
    selectedEntity: Entity | null;
    isEntityFormOpen: boolean;
    searchQuery: string;

    // UI actions
    setSelectedEntity: (entity: Entity | null) => void;
    openEntityForm: () => void;
    closeEntityForm: () => void;
    setSearchQuery: (query: string) => void;

    // Form state
    isSubmitting: boolean;
    setSubmitting: (isSubmitting: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
    // Entity management
    selectedEntity: null,
    isEntityFormOpen: false,
    searchQuery: '',

    // UI actions
    setSelectedEntity: (entity) => set({ selectedEntity: entity }),
    openEntityForm: () => set({ isEntityFormOpen: true }),
    closeEntityForm: () => set({
        isEntityFormOpen: false,
        selectedEntity: null
    }),
    setSearchQuery: (query) => set({ searchQuery: query }),

    // Form state
    isSubmitting: false,
    setSubmitting: (isSubmitting) => set({ isSubmitting }),
}));