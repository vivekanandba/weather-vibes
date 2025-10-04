import type { Vibe } from '../types/vibe';

export const VIBES: Record<string, Vibe> = {
  stargazing: {
    id: 'stargazing',
    name: 'Perfect Stargazing',
    description: 'Clear skies and low humidity for optimal stargazing',
    icon: '🌟',
    type: 'standard',
    parameters: [
      { id: 'CLOUD_AMT', weight: 0.6, scoring: 'low_is_better' },
      { id: 'RH2M', weight: 0.4, scoring: 'low_is_better' },
    ],
  },
  beach_day: {
    id: 'beach_day',
    name: 'Ideal Beach Day',
    description: 'Sunny, warm, and minimal rain',
    icon: '🏖️',
    type: 'standard',
    parameters: [
      { id: 'ALLSKY_SFC_SW_DWN', weight: 0.4, scoring: 'high_is_better' },
      { id: 'T2M', weight: 0.4, scoring: 'optimal_range', range: [24, 32] },
      { id: 'PRECTOTCORR', weight: 0.2, scoring: 'low_is_better' },
    ],
  },
  cozy_rain: {
    id: 'cozy_rain',
    name: 'Cozy Rainy Day',
    description: 'Perfect for indoor activities with steady rain',
    icon: '🌧️',
    type: 'standard',
    parameters: [
      { id: 'PRECTOTCORR', weight: 0.7, scoring: 'high_is_better' },
      { id: 'T2M', weight: 0.3, scoring: 'optimal_range', range: [18, 24] },
    ],
  },
  kite_flying: {
    id: 'kite_flying',
    name: 'Ideal Kite Flying',
    description: 'Moderate winds and clear skies',
    icon: '🪁',
    type: 'standard',
    parameters: [
      { id: 'WS2M', weight: 0.5, scoring: 'optimal_range', range: [10, 25] },
      { id: 'CLOUD_AMT', weight: 0.3, scoring: 'low_is_better' },
      { id: 'PRECTOTCORR', weight: 0.2, scoring: 'low_is_better' },
    ],
  },
  hiking: {
    id: 'hiking',
    name: 'Perfect Hiking Weather',
    description: 'Cool, dry, and comfortable for outdoor activities',
    icon: '🥾',
    type: 'standard',
    parameters: [
      { id: 'T2M', weight: 0.4, scoring: 'optimal_range', range: [15, 25] },
      { id: 'PRECTOTCORR', weight: 0.3, scoring: 'low_is_better' },
      { id: 'WS2M', weight: 0.2, scoring: 'low_is_better' },
      { id: 'RH2M', weight: 0.1, scoring: 'optimal_range', range: [40, 70] },
    ],
  },
  photography: {
    id: 'photography',
    name: 'Golden Hour Photography',
    description: 'Optimal lighting and atmospheric conditions',
    icon: '📸',
    type: 'standard',
    parameters: [
      { id: 'ALLSKY_SFC_SW_DWN', weight: 0.5, scoring: 'high_is_better' },
      { id: 'CLOUD_AMT', weight: 0.3, scoring: 'optimal_range', range: [20, 50] },
      { id: 'RH2M', weight: 0.2, scoring: 'optimal_range', range: [50, 80] },
    ],
  },
  // Advisors
  fashion_stylist: {
    id: 'fashion_stylist',
    name: 'AI Fashion Stylist',
    description: 'Weather-appropriate outfit recommendations',
    icon: '👔',
    type: 'advisor',
    parameters: [
      { id: 'T2M', weight: 0.4, scoring: 'high_is_better' },
      { id: 'ALLSKY_SFC_SW_DWN', weight: 0.3, scoring: 'high_is_better' },
      { id: 'PRECTOTCORR', weight: 0.2, scoring: 'low_is_better' },
      { id: 'WS2M', weight: 0.1, scoring: 'low_is_better' },
    ],
    logic: 'fashion_rules',
  },
  crop_advisor: {
    id: 'crop_advisor',
    name: 'Crop & Farming Advisor',
    description: 'Optimal planting and growing conditions',
    icon: '🌾',
    type: 'advisor',
    parameters: [
      { id: 'T2M', weight: 0.3, scoring: 'optimal_range', range: [15, 30] },
      { id: 'PRECTOTCORR', weight: 0.4, scoring: 'optimal_range', range: [50, 150] },
      { id: 'T2M_MIN', weight: 0.3, scoring: 'optimal_range', range: [10, 20] },
    ],
    logic: 'crop_rules',
  },
  mood_predictor: {
    id: 'mood_predictor',
    name: 'Climate Mood Predictor',
    description: 'Wellness suggestions based on weather',
    icon: '😊',
    type: 'advisor',
    parameters: [
      { id: 'ALLSKY_SFC_SW_DWN', weight: 0.4, scoring: 'high_is_better' },
      { id: 'T2M', weight: 0.3, scoring: 'optimal_range', range: [20, 26] },
      { id: 'RH2M', weight: 0.3, scoring: 'optimal_range', range: [40, 60] },
    ],
    logic: 'mood_rules',
  },
};

export const getVibeById = (id: string): Vibe | undefined => {
  return VIBES[id];
};

export const getStandardVibes = (): Vibe[] => {
  return Object.values(VIBES).filter((v) => v.type !== 'advisor');
};

export const getAdvisorVibes = (): Vibe[] => {
  return Object.values(VIBES).filter((v) => v.type === 'advisor');
};

export const getAllVibes = (): Vibe[] => {
  return Object.values(VIBES);
};
