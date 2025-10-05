'use client';

import { useEffect, useState } from 'react';
import { Box, Spinner, Center } from '@chakra-ui/react';
import dynamic from 'next/dynamic';
import { useLocationStore } from '../../stores/useLocationStore';

// Dynamically import the actual map component to avoid SSR issues
const DynamicMap = dynamic(() => import('./MapComponent'), {
  ssr: false,
  loading: () => (
    <Center h="100%" w="100%" bg="gray.100">
      <Spinner size="xl" color="brand.500" />
    </Center>
  ),
});

export default function MapView() {
  const { center, zoom } = useLocationStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading time for better UX
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  return (
    <Box position="relative" w="100%" h="100%" minH="100%" minW="100%">
      {isLoading && (
        <Center position="absolute" top={0} left={0} right={0} bottom={0} bg="white" zIndex={10}>
          <Spinner size="xl" color="brand.500" />
        </Center>
      )}

      <DynamicMap center={center} zoom={zoom} />
    </Box>
  );
}
