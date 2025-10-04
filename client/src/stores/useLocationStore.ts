import { create } from 'zustand';

interface LocationStore {
  center: [number, number];
  zoom: number;
  bounds: [[number, number], [number, number]] | null;
  setCenter: (center: [number, number]) => void;
  setZoom: (zoom: number) => void;
  setBounds: (bounds: [[number, number], [number, number]]) => void;
}

export const useLocationStore = create<LocationStore>((set) => ({
  center: [77.5946, 12.9716], // Default to Bangalore [lng, lat]
  zoom: 10,
  bounds: null,
  setCenter: (center) => set({ center }),
  setZoom: (zoom) => set({ zoom }),
  setBounds: (bounds) => set({ bounds }),
}));
