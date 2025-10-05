'use client';

import { MapContainer, TileLayer, useMapEvents, useMap } from 'react-leaflet';
import { useLocationStore } from '../../stores/useLocationStore';
import { MAP_CONFIG } from '../../config/mapbox';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in Leaflet with Next.js
import L from 'leaflet';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

// @ts-ignore
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon.src,
  iconRetinaUrl: markerIcon2x.src,
  shadowUrl: markerShadow.src,
});

// Component to handle map events
function MapEvents() {
  const { setCenter, setZoom, setBounds } = useLocationStore();
  const map = useMap();

  useMapEvents({
    moveend: () => {
      const center = map.getCenter();
      const zoom = map.getZoom();
      const bounds = map.getBounds();

      setCenter([center.lng, center.lat]);
      setZoom(zoom);
      setBounds([
        [bounds.getWest(), bounds.getSouth()],
        [bounds.getEast(), bounds.getNorth()],
      ]);
    },
    load: () => {
      // Set initial bounds when map loads
      const center = map.getCenter();
      const zoom = map.getZoom();
      const bounds = map.getBounds();

      setCenter([center.lng, center.lat]);
      setZoom(zoom);
      setBounds([
        [bounds.getWest(), bounds.getSouth()],
        [bounds.getEast(), bounds.getNorth()],
      ]);
    },
  });

  return null;
}

interface MapComponentProps {
  center: [number, number];
  zoom: number;
}

export default function MapComponent({ center, zoom }: MapComponentProps) {
  return (
    <MapContainer
      center={[center[1], center[0]]} // Leaflet uses [lat, lng] format
      zoom={zoom}
      style={{ width: '100%', height: '100%', zIndex: 1 }}
      zoomControl={false} // We'll add custom controls
    >
      <TileLayer
        url={MAP_CONFIG.tileLayer.url}
        attribution={MAP_CONFIG.tileLayer.attribution}
        maxZoom={MAP_CONFIG.tileLayer.maxZoom}
      />
      <MapEvents />
    </MapContainer>
  );
}
