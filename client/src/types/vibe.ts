export interface VibeParameter {
  id: string;
  weight: number;
  scoring: 'low_is_better' | 'high_is_better' | 'optimal_range';
  range?: [number, number];
}

export interface Vibe {
  id: string;
  name: string;
  description?: string;
  icon?: string;
  type?: 'standard' | 'advisor';
  parameters: VibeParameter[];
  logic?: string;
}

export interface VibeScore {
  vibeId: string;
  score: number;
  location?: [number, number];
  month?: number;
  details?: Record<string, unknown>;
}
