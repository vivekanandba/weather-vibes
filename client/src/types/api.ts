export interface WhereRequest {
  vibeId: string;
  month: number;
  year?: number;
  bounds: {
    north: number;
    south: number;
    east: number;
    west: number;
  };
}

export interface WhereResponse {
  heatmapData: {
    type: 'FeatureCollection';
    features: Array<{
      type: 'Feature';
      geometry: {
        type: 'Point';
        coordinates: [number, number];
      };
      properties: {
        score: number;
      };
    }>;
  };
  topLocations: Array<{
    name: string;
    coordinates: [number, number];
    score: number;
  }>;
}

export interface WhenRequest {
  vibeId: string;
  location: [number, number];
  year?: number;
}

export interface WhenResponse {
  monthlyScores: Array<{
    month: number;
    score: number;
    details?: Record<string, unknown>;
  }>;
}

export interface AdvisorRequest {
  advisorId: string;
  location: [number, number];
  date?: string;
}

export interface AdvisorResponse {
  type: string;
  recommendations: Array<{
    item: string;
    icon?: string;
    description?: string;
  }>;
}
