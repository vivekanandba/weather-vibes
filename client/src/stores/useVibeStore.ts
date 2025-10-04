import { create } from 'zustand';
import { Vibe } from '../types/vibe';

interface VibeStore {
  selectedVibe: Vibe | null;
  setSelectedVibe: (vibe: Vibe | null) => void;
  activeFeature: 'where' | 'when' | 'advisor' | null;
  setActiveFeature: (feature: 'where' | 'when' | 'advisor' | null) => void;
}

export const useVibeStore = create<VibeStore>((set) => ({
  selectedVibe: null,
  setSelectedVibe: (vibe) => set({ selectedVibe: vibe }),
  activeFeature: null,
  setActiveFeature: (feature) => set({ activeFeature: feature }),
}));
