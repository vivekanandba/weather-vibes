export interface Coordinates {
  lat: number;
  lng: number;
}

export interface Bounds {
  north: number;
  south: number;
  east: number;
  west: number;
}

export interface Location {
  name: string;
  coordinates: [number, number];
  score?: number;
}
