'use client';

import {
  Box,
  VStack,
  Heading,
  Text,
  Button,
  
} from '@chakra-ui/react';
import { useState } from 'react';
import { useVibeStore } from '../stores/useVibeStore';
import { useLocationStore } from '../stores/useLocationStore';
import { useUIStore } from '../stores/useUIStore';

export default function WhenPanel() {
  const { selectedVibe } = useVibeStore();
  const { center } = useLocationStore();
  const { setCalendarModalOpen } = useUIStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleFindBestTimes = async () => {
    if (!selectedVibe) {
      alert('Please select a vibe to find best times');
      return;
    }

    setIsLoading(true);
    // TODO: Call whenService.getMonthlyScores() with API integration
    console.log('Feature in progress: This will show monthly scores in a calendar');
    setIsLoading(false);
    setCalendarModalOpen(true);
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
      zIndex={10}
    >
      <VStack gap={4} alignItems="stretch">
        <Heading size="md">📅 When</Heading>
        <Text fontSize="sm" color="gray.600">
          Find the best times for your selected vibe at this location
        </Text>

        <Box bg="gray.50" p={3} borderRadius="md">
          <Text fontSize="xs" fontWeight="medium" color="gray.600" mb={1}>
            Current Location
          </Text>
          <Text fontSize="sm">
            {center[1].toFixed(4)}°N, {center[0].toFixed(4)}°E
          </Text>
        </Box>

        <Button
          colorScheme="brand"
          onClick={handleFindBestTimes}
          loading={isLoading}
          disabled={!selectedVibe}
        >
          Find Best Times
        </Button>

        <Text fontSize="xs" color="gray.500">
          View monthly scores for the year to plan your perfect moment
        </Text>
      </VStack>
    </Box>
  );
}
