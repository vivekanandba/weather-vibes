"use client";

import { useEffect, useRef, useState } from "react";
import { Box, Spinner, Center, Text } from "@chakra-ui/react";
import Map, {
  MapRef,
  NavigationControl,
  GeolocateControl,
} from "react-map-gl/mapbox";
import { useLocationStore } from "../../stores/useLocationStore";
import { MAPBOX_CONFIG } from "../../config/mapbox";
import "mapbox-gl/dist/mapbox-gl.css";

export default function MapView() {
  const mapRef = useRef<MapRef>(null);
  const { center, zoom, setCenter, setZoom, setBounds } = useLocationStore();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if Mapbox token is configured
    if (
      !MAPBOX_CONFIG.token ||
      MAPBOX_CONFIG.token === "your_mapbox_token_here"
    ) {
      setError(
        "Mapbox token not configured. Please add NEXT_PUBLIC_MAPBOX_TOKEN to .env.local"
      );
      setIsLoading(false);
    }
  }, []);

  const handleMapLoad = () => {
    setIsLoading(false);
  };

  const handleMapMove = () => {
    if (mapRef.current) {
      const map = mapRef.current.getMap();
      const newCenter = map.getCenter();
      const newZoom = map.getZoom();
      const newBounds = map.getBounds();

      setCenter([newCenter.lng, newCenter.lat]);
      setZoom(newZoom);

      if (newBounds) {
        setBounds([
          [newBounds.getWest(), newBounds.getSouth()],
          [newBounds.getEast(), newBounds.getNorth()],
        ]);
      }
    }
  };

  if (error) {
    return (
      <Center h="100%" w="100%" bg="gray.100">
        <Box textAlign="center" p={4}>
          <Text fontSize="xl" fontWeight="bold" color="red.500" mb={2}>
            Map Configuration Error
          </Text>
          <Text color="gray.600">{error}</Text>
          <Text fontSize="sm" color="gray.500" mt={4}>
            Get your token from: https://account.mapbox.com/
          </Text>
        </Box>
      </Center>
    );
  }

  return (
    <Box position="relative" w="100%" h="100%">
      {isLoading && (
        <Center
          position="absolute"
          top={0}
          left={0}
          right={0}
          bottom={0}
          bg="white"
          zIndex={10}
        >
          <Spinner size="xl" color="brand.500" />
        </Center>
      )}

      <Map
        ref={mapRef}
        initialViewState={{
          longitude: center[0],
          latitude: center[1],
          zoom: zoom,
        }}
        style={{ width: "100%", height: "100%" }}
        mapStyle={MAPBOX_CONFIG.style}
        mapboxAccessToken={MAPBOX_CONFIG.token}
        onLoad={handleMapLoad}
        onMove={handleMapMove}
      >
        <NavigationControl position="top-right" />
        <GeolocateControl
          position="top-right"
          trackUserLocation
          onGeolocate={(e) => {
            setCenter([e.coords.longitude, e.coords.latitude]);
          }}
        />
      </Map>
    </Box>
  );
}
