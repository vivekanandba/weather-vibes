'use client';

import {
  Box,
  VStack,
  Heading,
  Text,
  Button,
} from '@chakra-ui/react';
import { NativeSelectRoot, NativeSelectField } from '@chakra-ui/react';
import { useState } from 'react';
import { useVibeStore } from '../stores/useVibeStore';
import { useTimeStore } from '../stores/useTimeStore';
import { useLocationStore } from '../stores/useLocationStore';

export default function WherePanel() {
  const { selectedVibe } = useVibeStore();
  const { selectedMonth, setSelectedMonth } = useTimeStore();
  const { bounds } = useLocationStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleFindLocations = async () => {
    if (!selectedVibe) {
      alert('Please select a vibe to find locations');
      return;
    }

    if (!bounds) {
      alert('Please wait for the map to load');
      return;
    }

    setIsLoading(true);
    // TODO: Call whereService.getHeatmap() with API integration
    console.log('Feature in progress: This will show a heatmap of best locations');
    setIsLoading(false);
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
        <Heading size="md">📍 Where</Heading>
        <Text fontSize="sm" color="gray.600">
          Find the best locations for your selected vibe
        </Text>

        <Box>
          <Text fontSize="sm" fontWeight="medium" mb={2}>
            Month
          </Text>
          <NativeSelectRoot>
            <NativeSelectField
              value={selectedMonth || ''}
              onChange={(e) => setSelectedMonth(Number(e.target.value))}
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

        <Button
          colorScheme="brand"
          onClick={handleFindLocations}
          loading={isLoading}
          disabled={!selectedVibe}
        >
          Find Best Locations
        </Button>

        <Text fontSize="xs" color="gray.500">
          A heatmap will appear on the map showing the best locations
        </Text>
      </VStack>
    </Box>
  );
}
