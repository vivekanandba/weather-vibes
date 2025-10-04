import { create } from 'zustand';

interface UIStore {
  isSidebarOpen: boolean;
  isCalendarModalOpen: boolean;
  isVibeModalOpen: boolean;
  setSidebarOpen: (isOpen: boolean) => void;
  setCalendarModalOpen: (isOpen: boolean) => void;
  setVibeModalOpen: (isOpen: boolean) => void;
}

export const useUIStore = create<UIStore>((set) => ({
  isSidebarOpen: true,
  isCalendarModalOpen: false,
  isVibeModalOpen: false,
  setSidebarOpen: (isOpen) => set({ isSidebarOpen: isOpen }),
  setCalendarModalOpen: (isOpen) => set({ isCalendarModalOpen: isOpen }),
  setVibeModalOpen: (isOpen) => set({ isVibeModalOpen: isOpen }),
}));
