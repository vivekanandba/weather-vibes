'use client';

import { Box, VStack, Heading, Text, Button } from '@chakra-ui/react';
import { useState } from 'react';
import { useVibeStore } from '../../../stores/useVibeStore';
import { useLocationStore } from '../../../stores/useLocationStore';
import { whereService } from '../../../services/whereService';
import { WhereRequest } from '../../../types/api';
import { toaster } from '../../ui/toaster';
import DateRangePicker from '../../ui/DateRangePicker';

export default function WherePanel() {
  const { selectedVibe, whereData, setWhereData } = useVibeStore();
  const { center } = useLocationStore();
  const [isLoading, setIsLoading] = useState(false);
  const [dateRange, setDateRange] = useState<{
    startDate?: string;
    endDate?: string;
    month?: number;
  }>({});

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

    // Check if we have either month or date range selected
    if (!dateRange.month && !dateRange.startDate && !dateRange.endDate) {
      toaster.create({
        title: 'No time period selected',
        description: 'Please select a month or date range to find locations',
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
        month: dateRange.month,
        start_date: dateRange.startDate,
        end_date: dateRange.endDate,
        center_lat: center[1], // center is [lon, lat]
        center_lon: center[0],
        radius_km: 100, // Default radius
        resolution: 5, // Default resolution
      };

      const response = await whereService.getHeatmap(request);
      setWhereData(response);

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
      maxH="80vh"
      overflowY="auto"
      zIndex={1000}
    >
      <VStack gap={4} alignItems="stretch">
        <Heading size="md" color="gray.500">
          📍 Where
        </Heading>
        <Text fontSize="sm" color="gray.600">
          Find the best locations for your selected vibe
        </Text>

        <DateRangePicker
          onDateRangeChange={(startDate, endDate, month) => {
            setDateRange({ startDate, endDate, month });
          }}
          selectedMonth={dateRange.month}
          selectedStartDate={dateRange.startDate}
          selectedEndDate={dateRange.endDate}
        />

        <Button colorScheme="brand" onClick={handleFindLocations} loading={isLoading} disabled={!selectedVibe}>
          Find Best Locations
        </Button>

        <Text fontSize="xs" color="gray.500">
          A heatmap will appear on the map showing the best locations
        </Text>

        {/* Results Display */}
        {whereData && (
          <Box mt={4} p={3} bg="gray.50" borderRadius="md" border="1px" borderColor="gray.200">
            <Text fontSize="sm" fontWeight="bold" mb={2} color="gray.700">
              📊 Results Summary
            </Text>
            <VStack gap={2} alignItems="stretch">
              <Text fontSize="xs" color="gray.600">
                <strong>Locations Found:</strong> {whereData.scores.length}
              </Text>
              <Text fontSize="xs" color="gray.600">
                <strong>Score Range:</strong> {whereData.min_score.toFixed(1)} - {whereData.max_score.toFixed(1)}
              </Text>
              <Text fontSize="xs" color="gray.600">
                <strong>Search Radius:</strong> {whereData.metadata.radius_km}km
              </Text>
              <Text fontSize="xs" color="gray.600">
                <strong>Resolution:</strong> {whereData.metadata.resolution_km}km
              </Text>
              {whereData.month && (
                <Text fontSize="xs" color="gray.600">
                  <strong>Month:</strong>{' '}
                  {new Date(2024, whereData.month - 1).toLocaleString('default', { month: 'long' })}
                </Text>
              )}
              {whereData.start_date && whereData.end_date && (
                <Text fontSize="xs" color="gray.600">
                  <strong>Date Range:</strong> {whereData.start_date} to {whereData.end_date}
                </Text>
              )}
            </VStack>
          </Box>
        )}
      </VStack>
    </Box>
  );
}
