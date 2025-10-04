export const MAPBOX_CONFIG = {
  token: process.env.NEXT_PUBLIC_MAPBOX_TOKEN || '',
  style: 'mapbox://styles/mapbox/streets-v12',
  defaultCenter: {
    lng: Number(process.env.NEXT_PUBLIC_DEFAULT_LNG) || 77.5946,
    lat: Number(process.env.NEXT_PUBLIC_DEFAULT_LAT) || 12.9716,
  },
  defaultZoom: Number(process.env.NEXT_PUBLIC_DEFAULT_ZOOM) || 10,
};
