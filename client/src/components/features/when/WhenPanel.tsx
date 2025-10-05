'use client';

import { Box, VStack, Heading, Text, Button } from '@chakra-ui/react';
import { NativeSelectRoot, NativeSelectField } from '@chakra-ui/react';
import { useState } from 'react';
import { useVibeStore } from '../../../stores/useVibeStore';
import { useLocationStore } from '../../../stores/useLocationStore';
import { useUIStore } from '../../../stores/useUIStore';
import { whenService } from '../../../services/whenService';
import { WhenRequest } from '../../../types/api';
import { toaster } from '../../ui/toaster';
import DateRangePicker from '../../ui/DateRangePicker';

export default function WhenPanel() {
  const { selectedVibe, whenData, setWhenData } = useVibeStore();
  const { center } = useLocationStore();
  const { setCalendarModalOpen, isSidebarOpen } = useUIStore();
  const [isLoading, setIsLoading] = useState(false);
  const [analysisType, setAnalysisType] = useState<'monthly' | 'daily' | 'hourly'>('monthly');
  const [dateRange, setDateRange] = useState<{
    startDate?: string;
    endDate?: string;
    month?: number;
  }>({});

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

    // Check if we have either month or date range selected
    if (!dateRange.month && !dateRange.startDate && !dateRange.endDate) {
      toaster.create({
        title: 'No time period selected',
        description: 'Please select a month or date range to find best times',
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
        start_date: dateRange.startDate,
        end_date: dateRange.endDate,
        analysis_type: analysisType,
      };

      const response = await whenService.getMonthlyScores(request);
      setWhenData(response);

      toaster.create({
        title: 'Best times found!',
        description: `Best month: ${
          response.monthly_scores?.find((m) => m.month === response.best_month)?.month_name
        } (score: ${response.monthly_scores?.find((m) => m.month === response.best_month)?.score.toFixed(2)})`,
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
      right={isSidebarOpen ? 4 : 4}
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

        {/* Analysis Type Selection */}
        <Box>
          <Text fontSize="sm" fontWeight="medium" mb={2} color="gray.500">
            Analysis Type
          </Text>
          <NativeSelectRoot>
            <NativeSelectField
              value={analysisType}
              onChange={(e) => setAnalysisType(e.target.value as 'monthly' | 'daily' | 'hourly')}
              color="gray.700"
            >
              <option value="monthly">Monthly Analysis</option>
              <option value="daily">Daily Analysis</option>
              <option value="hourly">Hourly Analysis</option>
            </NativeSelectField>
          </NativeSelectRoot>
        </Box>

        <DateRangePicker
          onDateRangeChange={(startDate, endDate, month) => {
            setDateRange({ startDate, endDate, month });
          }}
          selectedMonth={dateRange.month}
          selectedStartDate={dateRange.startDate}
          selectedEndDate={dateRange.endDate}
        />

        <Button colorScheme="brand" onClick={handleFindBestTimes} loading={isLoading} disabled={!selectedVibe}>
          Find Best Times
        </Button>

        <Text fontSize="xs" color="gray.500">
          View monthly scores for the year to plan your perfect moment
        </Text>

        {/* Monthly Scores Visualization */}
        {whenData && (
          <Box
            mt={4}
            p={3}
            bg="gray.50"
            borderRadius="md"
            border="1px"
            borderColor="gray.200"
            maxH="400px"
            overflowY="auto"
          >
            <Text fontSize="sm" fontWeight="bold" mb={2} color="gray.700">
              📊 Monthly Scores
            </Text>
            <VStack gap={1} alignItems="stretch">
              {whenData.monthly_scores?.map((month) => {
                const isBest = month.month === whenData.best_month;
                const isWorst = month.month === whenData.worst_month;
                const scoreColor = month.score >= 80 ? 'green.500' : month.score >= 70 ? 'yellow.500' : 'red.500';

                return (
                  <Box
                    key={month.month}
                    p={2}
                    bg={isBest ? 'green.50' : isWorst ? 'red.50' : 'white'}
                    borderRadius="sm"
                    border={isBest ? '2px solid' : isWorst ? '2px solid' : '1px solid'}
                    borderColor={isBest ? 'green.200' : isWorst ? 'red.200' : 'gray.200'}
                  >
                    <Box display="flex" justifyContent="space-between" alignItems="center">
                      <Text fontSize="xs" fontWeight={isBest || isWorst ? 'bold' : 'medium'} color="gray.700">
                        {month.month_name}
                        {isBest && ' 🏆'}
                        {isWorst && ' ⚠️'}
                      </Text>
                      <Text fontSize="xs" fontWeight="bold" color={scoreColor}>
                        {month.score.toFixed(1)}
                      </Text>
                    </Box>
                    <Box mt={1} h={2} bg="gray.200" borderRadius="full" overflow="hidden">
                      <Box h="100%" bg={scoreColor} width={`${(month.score / 100) * 100}%`} borderRadius="full" />
                    </Box>
                  </Box>
                );
              })}
            </VStack>
          </Box>
        )}
      </VStack>
    </Box>
  );
}
