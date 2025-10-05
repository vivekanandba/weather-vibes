// Backend API Types - matching server models

export interface WhereRequest {
  vibe: string;
  month?: number;
  year?: number;
  start_date?: string; // YYYY-MM-DD format
  end_date?: string; // YYYY-MM-DD format
  center_lat: number;
  center_lon: number;
  radius_km: number;
  resolution?: number;
}

export interface LocationScore {
  lat: number;
  lon: number;
  score: number;
}

export interface WhereResponse {
  vibe: string;
  month?: number;
  year?: number;
  start_date?: string;
  end_date?: string;
  scores: LocationScore[];
  max_score: number;
  min_score: number;
  metadata: {
    center: { lat: number; lon: number };
    radius_km: number;
    resolution_km: number;
    num_points: number;
    vibe_name: string;
    date_range?: {
      start: string;
      end: string;
    };
  };
}

export interface WhenRequest {
  vibe: string;
  lat: number;
  lon: number;
  year?: number;
  start_date?: string; // YYYY-MM-DD format
  end_date?: string; // YYYY-MM-DD format
  analysis_type?: 'monthly' | 'daily' | 'hourly'; // New field for analysis type
}

export interface MonthlyScore {
  month: number;
  month_name: string;
  score: number;
}

export interface DailyScore {
  date: string; // YYYY-MM-DD format
  score: number;
}

export interface HourlyScore {
  hour: number;
  score: number;
}

export interface WhenResponse {
  vibe: string;
  location: { lat: number; lon: number };
  monthly_scores?: MonthlyScore[];
  daily_scores?: DailyScore[];
  hourly_scores?: HourlyScore[];
  best_month?: number;
  worst_month?: number;
  best_date?: string;
  worst_date?: string;
  best_hour?: number;
  worst_hour?: number;
  analysis_type: 'monthly' | 'daily' | 'hourly';
  metadata: {
    year?: number;
    num_months?: number;
    num_days?: number;
    num_hours?: number;
    vibe_name: string;
    date_range?: {
      start: string;
      end: string;
    };
  };
}

export interface AdvisorRequest {
  advisor_type: string;
  lat: number;
  lon: number;
  month: number;
  year?: number;
  additional_params?: Record<string, unknown>;
}

export interface Recommendation {
  item: string;
  icon: string;
  description?: string;
}

export interface AdvisorResponse {
  advisor_type: string;
  location: { lat: number; lon: number };
  recommendations: Recommendation[];
  metadata: {
    month: number;
    year?: number;
    advisor_name: string;
  };
  raw_data?: Record<string, unknown>;
}
