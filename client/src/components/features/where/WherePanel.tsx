'use client';

import { Box, VStack, Heading, Text, Button } from '@chakra-ui/react';
import { NativeSelectRoot, NativeSelectField } from '@chakra-ui/react';
import { useState } from 'react';
import { useVibeStore } from '../../../stores/useVibeStore';
import { useTimeStore } from '../../../stores/useTimeStore';
import { useLocationStore } from '../../../stores/useLocationStore';
import { whereService } from '../../../services/whereService';
import { WhereRequest } from '../../../types/api';
import { toaster } from '../../ui/toaster';

export default function WherePanel() {
  const { selectedVibe } = useVibeStore();
  const { selectedMonth, setSelectedMonth } = useTimeStore();
  const { center } = useLocationStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleFindLocations = async () => {
    if (!selectedVibe) {
      toaster.create({
        title: 'No vibe selected',
        description: 'Please select a vibe to find locations',
        type: 'warning',
        duration: 3000,
        closable: true,
      });
      return;
    }

    if (!selectedMonth) {
      toaster.create({
        title: 'No month selected',
        description: 'Please select a month to find locations',
        type: 'warning',
        duration: 3000,
        closable: true,
      });
      return;
    }

    setIsLoading(true);

    try {
      const request: WhereRequest = {
        vibe: selectedVibe.id,
        month: selectedMonth,
        center_lat: center[1], // center is [lon, lat]
        center_lon: center[0],
        radius_km: 100, // Default radius
        resolution: 5, // Default resolution
      };

      const response = await whereService.getHeatmap(request);

      toaster.create({
        title: 'Locations found!',
        description: `Found ${response.scores.length} locations with scores ranging from ${response.min_score.toFixed(
          2
        )} to ${response.max_score.toFixed(2)}`,
        type: 'success',
        duration: 5000,
        closable: true,
      });

      // TODO: Update map with heatmap data
      console.log('Heatmap data:', response);
    } catch (error: unknown) {
      console.error('Error fetching locations:', error);
      const description =
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
        'Failed to find locations. Please try again.';
      toaster.create({
        title: 'Error',
        description,
        type: 'error',
        duration: 5000,
        closable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box
      position="absolute"
      top={4}
      right={4}
      bg="white"
      p={4}
      borderRadius="md"
      boxShadow="lg"
      w="300px"
      zIndex={1000}
    >
      <VStack gap={4} alignItems="stretch">
        <Heading size="md" color="gray.500">
          📍 Where
        </Heading>
        <Text fontSize="sm" color="gray.600">
          Find the best locations for your selected vibe
        </Text>

        <Box>
          <Text fontSize="sm" fontWeight="medium" mb={2} color="gray.500">
            Month
          </Text>
          <NativeSelectRoot>
            <NativeSelectField
              value={selectedMonth || ''}
              onChange={(e) => setSelectedMonth(Number(e.target.value))}
              color="gray.700"
            >
              <option value="1">January</option>
              <option value="2">February</option>
              <option value="3">March</option>
              <option value="4">April</option>
              <option value="5">May</option>
              <option value="6">June</option>
              <option value="7">July</option>
              <option value="8">August</option>
              <option value="9">September</option>
              <option value="10">October</option>
              <option value="11">November</option>
              <option value="12">December</option>
            </NativeSelectField>
          </NativeSelectRoot>
        </Box>

        <Button colorScheme="brand" onClick={handleFindLocations} loading={isLoading} disabled={!selectedVibe}>
          Find Best Locations
        </Button>

        <Text fontSize="xs" color="gray.500">
          A heatmap will appear on the map showing the best locations
        </Text>
      </VStack>
    </Box>
  );
}
