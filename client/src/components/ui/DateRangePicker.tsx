'use client';

import { Box, VStack, Text, NativeSelectRoot, NativeSelectField, Button, Input } from '@chakra-ui/react';
import { useState } from 'react';

interface DateRangePickerProps {
  onDateRangeChange: (startDate?: string, endDate?: string, month?: number) => void;
  selectedMonth?: number;
  selectedStartDate?: string;
  selectedEndDate?: string;
}

export default function DateRangePicker({
  onDateRangeChange,
  selectedMonth,
  selectedStartDate,
  selectedEndDate,
}: DateRangePickerProps) {
  const [dateMode, setDateMode] = useState<'month' | 'range'>('month');
  const [month, setMonth] = useState(selectedMonth || new Date().getMonth() + 1);
  const [startDate, setStartDate] = useState(selectedStartDate || '');
  const [endDate, setEndDate] = useState(selectedEndDate || '');

  const handleModeChange = (mode: 'month' | 'range') => {
    setDateMode(mode);
    if (mode === 'month') {
      onDateRangeChange(undefined, undefined, month);
    } else {
      onDateRangeChange(startDate || undefined, endDate || undefined);
    }
  };

  const handleMonthChange = (newMonth: number) => {
    setMonth(newMonth);
    if (dateMode === 'month') {
      onDateRangeChange(undefined, undefined, newMonth);
    }
  };

  const handleDateChange = (type: 'start' | 'end', value: string) => {
    if (type === 'start') {
      setStartDate(value);
      if (dateMode === 'range') {
        onDateRangeChange(value || undefined, endDate || undefined);
      }
    } else {
      setEndDate(value);
      if (dateMode === 'range') {
        onDateRangeChange(startDate || undefined, value || undefined);
      }
    }
  };

  const getCurrentMonth = () => new Date().getMonth() + 1;

  return (
    <VStack gap={3} alignItems="stretch">
      <Text fontSize="sm" fontWeight="medium" color="gray.700">
        📅 Time Selection
      </Text>

      {/* Mode Selection */}
      <Box>
        <Text fontSize="xs" fontWeight="medium" mb={2} color="gray.600">
          Analysis Type
        </Text>
        <NativeSelectRoot>
          <NativeSelectField
            value={dateMode}
            onChange={(e) => handleModeChange(e.target.value as 'month' | 'range')}
            color="gray.700"
          >
            <option value="month">Single Month</option>
            <option value="range">Date Range</option>
          </NativeSelectField>
        </NativeSelectRoot>
      </Box>

      {/* Month Selection */}
      {dateMode === 'month' && (
        <Box>
          <Text fontSize="xs" fontWeight="medium" mb={2} color="gray.600">
            Month
          </Text>
          <NativeSelectRoot>
            <NativeSelectField
              value={month}
              onChange={(e) => handleMonthChange(Number(e.target.value))}
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
      )}

      {/* Date Range Selection */}
      {dateMode === 'range' && (
        <VStack gap={2} alignItems="stretch">
          <Box>
            <Text fontSize="xs" fontWeight="medium" mb={2} color="gray.600">
              Start Date
            </Text>
            <Input
              type="date"
              value={startDate}
              onChange={(e) => handleDateChange('start', e.target.value)}
              color="gray.700"
            />
          </Box>

          <Box>
            <Text fontSize="xs" fontWeight="medium" mb={2} color="gray.600">
              End Date
            </Text>
            <Input
              type="date"
              value={endDate}
              onChange={(e) => handleDateChange('end', e.target.value)}
              color="gray.700"
              min={startDate}
            />
          </Box>
        </VStack>
      )}

      {/* Quick Presets */}
      <Box>
        <Text fontSize="xs" fontWeight="medium" mb={2} color="gray.600">
          Quick Presets
        </Text>
        <VStack gap={1} alignItems="stretch">
          <Button
            size="xs"
            variant="outline"
            onClick={() => {
              const currentMonth = getCurrentMonth();
              handleModeChange('month');
              handleMonthChange(currentMonth);
            }}
          >
            This Month
          </Button>
          <Button
            size="xs"
            variant="outline"
            onClick={() => {
              const today = new Date();
              const startOfYear = new Date(today.getFullYear(), 0, 1);
              const endOfYear = new Date(today.getFullYear(), 11, 31);
              handleModeChange('range');
              handleDateChange('start', startOfYear.toISOString().split('T')[0]);
              handleDateChange('end', endOfYear.toISOString().split('T')[0]);
            }}
          >
            This Year
          </Button>
          <Button
            size="xs"
            variant="outline"
            onClick={() => {
              const today = new Date();
              const startOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
              const endOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
              handleModeChange('range');
              handleDateChange('start', startOfMonth.toISOString().split('T')[0]);
              handleDateChange('end', endOfMonth.toISOString().split('T')[0]);
            }}
          >
            This Month Range
          </Button>
        </VStack>
      </Box>
    </VStack>
  );
}
