'use client';

import { Box, VStack, Heading, Text, Button } from '@chakra-ui/react';
import { useState } from 'react';
import { useVibeStore } from '../../../stores/useVibeStore';
import { useLocationStore } from '../../../stores/useLocationStore';
import { useUIStore } from '../../../stores/useUIStore';
import { whenService } from '../../../services/whenService';
import { WhenRequest } from '../../../types/api';
import { toaster } from '../../ui/toaster';

export default function WhenPanel() {
  const { selectedVibe } = useVibeStore();
  const { center } = useLocationStore();
  const { setCalendarModalOpen } = useUIStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleFindBestTimes = async () => {
    if (!selectedVibe) {
      toaster.create({
        title: 'No vibe selected',
        description: 'Please select a vibe to find best times',
        type: 'warning',
        duration: 3000,
        closable: true,
      });
      return;
    }

    setIsLoading(true);

    try {
      const request: WhenRequest = {
        vibe: selectedVibe.id,
        lat: center[1], // center is [lon, lat]
        lon: center[0],
      };

      const response = await whenService.getMonthlyScores(request);

      toaster.create({
        title: 'Best times found!',
        description: `Best month: ${
          response.monthly_scores.find((m) => m.month === response.best_month)?.month_name
        } (score: ${response.monthly_scores.find((m) => m.month === response.best_month)?.score.toFixed(2)})`,
        type: 'success',
        duration: 5000,
        closable: true,
      });

      // TODO: Update calendar modal with monthly scores
      console.log('Monthly scores:', response);
      setCalendarModalOpen(true);
    } catch (error: unknown) {
      console.error('Error fetching monthly scores:', error);
      const description =
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
        'Failed to find best times. Please try again.';
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
          📅 When
        </Heading>
        <Text fontSize="sm" color="gray.600">
          Find the best times for your selected vibe at this location
        </Text>

        <Box bg="gray.50" p={3} borderRadius="md">
          <Text fontSize="xs" fontWeight="medium" color="gray.600" mb={1}>
            Current Location
          </Text>
          <Text fontSize="sm" color="gray.700">
            {center[1].toFixed(4)}°N, {center[0].toFixed(4)}°E
          </Text>
        </Box>

        <Button colorScheme="brand" onClick={handleFindBestTimes} loading={isLoading} disabled={!selectedVibe}>
          Find Best Times
        </Button>

        <Text fontSize="xs" color="gray.500">
          View monthly scores for the year to plan your perfect moment
        </Text>
      </VStack>
    </Box>
  );
}
