import { create } from 'zustand';

interface TimeStore {
  selectedMonth: number | null;
  selectedYear: number;
  timeRange: { start: Date; end: Date } | null;
  setSelectedMonth: (month: number) => void;
  setSelectedYear: (year: number) => void;
  setTimeRange: (range: { start: Date; end: Date }) => void;
}

export const useTimeStore = create<TimeStore>((set) => ({
  selectedMonth: new Date().getMonth() + 1,
  selectedYear: new Date().getFullYear(),
  timeRange: null,
  setSelectedMonth: (month) => set({ selectedMonth: month }),
  setSelectedYear: (year) => set({ selectedYear: year }),
  setTimeRange: (range) => set({ timeRange: range }),
}));
