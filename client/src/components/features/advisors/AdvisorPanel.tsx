'use client';

import { Box, VStack, Heading, Text, Button } from '@chakra-ui/react';
import { useState } from 'react';
import { useVibeStore } from '../../../stores/useVibeStore';
import { useLocationStore } from '../../../stores/useLocationStore';
import { useTimeStore } from '../../../stores/useTimeStore';
import { advisorService } from '../../../services/advisorService';
import { AdvisorRequest } from '../../../types/api';
import { toaster } from '../../ui/toaster';

export default function AdvisorPanel() {
  const { selectedVibe, advisorData, setAdvisorData } = useVibeStore();
  const { center } = useLocationStore();
  const { selectedMonth } = useTimeStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleGetAdvice = async () => {
    if (!selectedVibe || selectedVibe.type !== 'advisor') {
      toaster.create({
        title: 'No advisor selected',
        description: 'Please select an AI advisor from the vibe menu',
        type: 'warning',
        duration: 3000,
        closable: true,
      });
      return;
    }

    if (!selectedMonth) {
      toaster.create({
        title: 'No month selected',
        description: 'Please select a month to get recommendations',
        type: 'warning',
        duration: 3000,
        closable: true,
      });
      return;
    }

    setIsLoading(true);

    try {
      // Map vibe ID to advisor type
      const advisorTypeMap: Record<string, string> = {
        fashion_stylist: 'fashion',
        crop_advisor: 'crop',
        mood_predictor: 'mood',
      };

      const advisorType = advisorTypeMap[selectedVibe.id];
      if (!advisorType) {
        throw new Error(`Unknown advisor type: ${selectedVibe.id}`);
      }

      const request: AdvisorRequest = {
        advisor_type: advisorType,
        lat: center[1], // center is [lon, lat]
        lon: center[0],
        month: selectedMonth,
      };

      const response = await advisorService.getRecommendations(request);
      setAdvisorData(response);

      toaster.create({
        title: 'Recommendations ready!',
        description: `Got ${response.recommendations.length} personalized recommendations`,
        type: 'success',
        duration: 5000,
        closable: true,
      });

      // TODO: Display recommendations in the UI
      console.log('Advisor recommendations:', response);
    } catch (error: unknown) {
      console.error('Error fetching recommendations:', error);
      const description =
        (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail ||
        'Failed to get recommendations. Please try again.';
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
      maxH="80vh"
      overflowY="auto"
    >
      <VStack gap={4} alignItems="stretch">
        <Heading size="md" color="gray.500">
          🤖 AI Advisors
        </Heading>
        <Text fontSize="sm" color="gray.600">
          Get personalized recommendations based on weather conditions
        </Text>

        <Box bg="gray.50" p={3} borderRadius="md">
          <Text fontSize="xs" fontWeight="medium" color="gray.600" mb={1}>
            Current Location
          </Text>
          <Text fontSize="sm" color="gray.700">
            {center[1].toFixed(4)}°N, {center[0].toFixed(4)}°E
          </Text>
        </Box>

        {selectedVibe?.type === 'advisor' && (
          <Box bg="brand.50" p={3} borderRadius="md">
            <Text fontSize="sm" fontWeight="medium" color="gray.700">
              {selectedVibe.icon} {selectedVibe.name}
            </Text>
            <Text fontSize="xs" color="gray.600" mt={1}>
              {selectedVibe.description}
            </Text>
          </Box>
        )}

        <Button
          colorScheme="brand"
          onClick={handleGetAdvice}
          loading={isLoading}
          disabled={!selectedVibe || selectedVibe.type !== 'advisor'}
        >
          Get Recommendations
        </Button>

        <Text fontSize="xs" color="gray.500">
          AI advisors provide context-aware suggestions
        </Text>

        {/* Recommendations Display */}
        {advisorData && (
          <Box mt={4} p={3} bg="gray.50" borderRadius="md" border="1px" borderColor="gray.200">
            <Text fontSize="sm" fontWeight="bold" mb={3} color="gray.700">
              🤖 {advisorData.metadata.advisor_name} Recommendations
            </Text>
            <VStack gap={3} alignItems="stretch">
              {advisorData.recommendations.map((rec, index) => (
                <Box key={index} p={3} bg="white" borderRadius="md" border="1px" borderColor="gray.200" boxShadow="sm">
                  <Box display="flex" alignItems="center" mb={2}>
                    <Text fontSize="lg" mr={2}>
                      {rec.icon}
                    </Text>
                    <Text fontSize="sm" fontWeight="bold" color="gray.800">
                      {rec.item}
                    </Text>
                  </Box>
                  <Text fontSize="xs" color="gray.600" lineHeight="1.4">
                    {rec.description}
                  </Text>
                </Box>
              ))}
            </VStack>

            {/* Weather Data Summary */}
            <Box mt={3} p={2} bg="blue.50" borderRadius="sm" border="1px" borderColor="blue.200">
              <Text fontSize="xs" fontWeight="bold" color="blue.700" mb={1}>
                📊 Weather Context
              </Text>
              <Box display="grid" gridTemplateColumns="repeat(2, 1fr)" gap={1} fontSize="xs" color="blue.600">
                <Text>Temp: {(advisorData.raw_data?.T2M as number)?.toFixed(1)}°C</Text>
                <Text>Rain: {(advisorData.raw_data?.PRECTOTCORR as number)?.toFixed(1)}mm</Text>
                <Text>Sun: {(advisorData.raw_data?.ALLSKY_SFC_SW_DWN as number)?.toFixed(1)} MJ/m²</Text>
                <Text>Wind: {(advisorData.raw_data?.WS2M as number)?.toFixed(1)} m/s</Text>
              </Box>
            </Box>
          </Box>
        )}
      </VStack>
    </Box>
  );
}
