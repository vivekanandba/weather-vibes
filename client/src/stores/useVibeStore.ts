import { create } from 'zustand';
import { Vibe } from '../types/vibe';
import { WhereResponse, WhenResponse, AdvisorResponse } from '../types/api';

interface VibeStore {
  selectedVibe: Vibe | null;
  setSelectedVibe: (vibe: Vibe | null) => void;
  activeFeature: 'where' | 'when' | 'advisor' | null;
  setActiveFeature: (feature: 'where' | 'when' | 'advisor' | null) => void;
  whereData: WhereResponse | null;
  setWhereData: (data: WhereResponse | null) => void;
  whenData: WhenResponse | null;
  setWhenData: (data: WhenResponse | null) => void;
  advisorData: AdvisorResponse | null;
  setAdvisorData: (data: AdvisorResponse | null) => void;
}

export const useVibeStore = create<VibeStore>((set) => ({
  selectedVibe: null,
  setSelectedVibe: (vibe) => set({ selectedVibe: vibe }),
  activeFeature: null,
  setActiveFeature: (feature) => set({ activeFeature: feature }),
  whereData: null,
  setWhereData: (data) => set({ whereData: data }),
  whenData: null,
  setWhenData: (data) => set({ whenData: data }),
  advisorData: null,
  setAdvisorData: (data) => set({ advisorData: data }),
}));
