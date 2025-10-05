'use client';

import { MapContainer, TileLayer, useMapEvents, useMap } from 'react-leaflet';
import { useEffect, useRef } from 'react';
import { useLocationStore } from '../../stores/useLocationStore';
import { useVibeStore } from '../../stores/useVibeStore';
import { MAP_CONFIG } from '../../config/mapbox';
import MapVisualization from './MapVisualization';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in Leaflet with Next.js
import L from 'leaflet';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

// @ts-expect-error - Leaflet icon fix
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon.src,
  iconRetinaUrl: markerIcon2x.src,
  shadowUrl: markerShadow.src,
});

// Component to handle map events
function MapEvents() {
  const { setCenter, setZoom, setBounds, center, zoom } = useLocationStore();
  const map = useMap();

  useMapEvents({
    moveend: () => {
      const newCenter = map.getCenter();
      const newZoom = map.getZoom();
      const bounds = map.getBounds();

      // Only update if values have actually changed to prevent infinite loops
      const newCenterArray: [number, number] = [newCenter.lng, newCenter.lat];
      const currentCenterArray = center;

      const centerChanged =
        Math.abs(newCenterArray[0] - currentCenterArray[0]) > 0.0001 ||
        Math.abs(newCenterArray[1] - currentCenterArray[1]) > 0.0001;

      const zoomChanged = Math.abs(newZoom - zoom) > 0.1;

      if (centerChanged || zoomChanged) {
        setCenter(newCenterArray);
        setZoom(newZoom);
        setBounds([
          [bounds.getWest(), bounds.getSouth()],
          [bounds.getEast(), bounds.getNorth()],
        ]);
      }
    },
    load: () => {
      // Set initial bounds when map loads (only once)
      const newCenter = map.getCenter();
      const newZoom = map.getZoom();
      const bounds = map.getBounds();

      setCenter([newCenter.lng, newCenter.lat]);
      setZoom(newZoom);
      setBounds([
        [bounds.getWest(), bounds.getSouth()],
        [bounds.getEast(), bounds.getNorth()],
      ]);
    },
  });

  return null;
}

// Component to handle map updates from store
function MapUpdater({ center, zoom }: { center: [number, number]; zoom: number }) {
  const map = useMap();
  const isUpdatingRef = useRef(false);

  useEffect(() => {
    if (isUpdatingRef.current) return;

    const currentCenter = map.getCenter();
    const currentZoom = map.getZoom();

    // Only update if the values are significantly different
    const centerChanged =
      Math.abs(currentCenter.lng - center[0]) > 0.0001 || Math.abs(currentCenter.lat - center[1]) > 0.0001;

    const zoomChanged = Math.abs(currentZoom - zoom) > 0.1;

    if (centerChanged || zoomChanged) {
      isUpdatingRef.current = true;
      map.setView([center[1], center[0]], zoom);
      setTimeout(() => {
        isUpdatingRef.current = false;
      }, 100);
    }
  }, [center, zoom, map]);

  return null;
}

interface MapComponentProps {
  center: [number, number];
  zoom: number;
}

export default function MapComponent({ center, zoom }: MapComponentProps) {
  const { whereData, whenData, advisorData } = useVibeStore();

  // Ensure we're on the client side
  if (typeof window === 'undefined') {
    return null;
  }

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
      <MapUpdater center={center} zoom={zoom} />
      <MapVisualization whereData={whereData} whenData={whenData} advisorData={advisorData} />
    </MapContainer>
  );
}
