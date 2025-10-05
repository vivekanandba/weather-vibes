"use client";

import { Box, VStack, HStack, Text, Grid, Badge } from "@chakra-ui/react";

interface PlantingWindow {
  optimal_months: number[];
  planting_window: string;
  confidence: number;
  notes: string;
}

interface PlantingCalendarProps {
  plantingWindow: PlantingWindow;
  cropType: string;
  currentMonth: number;
}

const MONTH_NAMES = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];

const SEASON_COLORS: Record<string, string> = {
  spring: "#22c55e",
  summer: "#eab308",
  monsoon: "#3b82f6",
  winter: "#64748b",
  optimal: "#16a34a",
  good: "#65a30d",
  poor: "#dc2626",
};

export default function PlantingCalendar({
  plantingWindow,
  cropType,
  currentMonth,
}: PlantingCalendarProps) {
  const getMonthStatus = (monthIndex: number) => {
    const month = monthIndex + 1; // Convert 0-based to 1-based

    if (plantingWindow.optimal_months.includes(month)) {
      return "optimal";
    }

    // Extended planting window (within 1 month of optimal)
    const isNearOptimal = plantingWindow.optimal_months.some(
      (optMonth) =>
        Math.abs(month - optMonth) <= 1 || Math.abs(month - optMonth) >= 11 // Handle year wraparound
    );

    if (isNearOptimal) {
      return "good";
    }

    return "poor";
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return "green";
    if (confidence >= 0.6) return "yellow";
    return "red";
  };

  const isCurrentMonth = (monthIndex: number) => {
    return monthIndex + 1 === currentMonth;
  };

  const getSeasonIcon = (monthIndex: number) => {
    const month = monthIndex + 1;
    if ([12, 1, 2].includes(month)) return "❄️";
    if ([3, 4, 5].includes(month)) return "🌸";
    if ([6, 7, 8].includes(month)) return "☀️";
    if ([9, 10, 11].includes(month)) return "🍂";
    return "📅";
  };

  return (
    <VStack gap={4} alignItems="stretch" p={4} bg="green.50" borderRadius="lg">
      <HStack justify="space-between" align="center">
        <Text fontSize="sm" fontWeight="semibold" color="green.800">
          📅 Planting Calendar for{" "}
          {cropType.charAt(0).toUpperCase() + cropType.slice(1)}
        </Text>

        <Badge
          colorScheme={getConfidenceColor(plantingWindow.confidence)}
          variant="solid"
        >
          {Math.round(plantingWindow.confidence * 100)}% confidence
        </Badge>
      </HStack>

      {/* Monthly Calendar Grid */}
      <Grid templateColumns="repeat(6, 1fr)" gap={2}>
        {MONTH_NAMES.map((monthName, index) => {
          const status = getMonthStatus(index);
          const isCurrent = isCurrentMonth(index);
          const statusColor = SEASON_COLORS[status];

          return (
            <Box
              key={monthName}
              p={3}
              borderRadius="lg"
              bg={statusColor}
              color="white"
              textAlign="center"
              position="relative"
              cursor="pointer"
              opacity={status === "poor" ? 0.4 : 1}
              border={isCurrent ? "3px solid" : "1px solid"}
              borderColor={isCurrent ? "orange.400" : "transparent"}
              _hover={{ transform: "scale(1.05)" }}
              transition="all 0.2s"
              title={`${monthName}: ${
                status === "optimal"
                  ? "Best time to plant"
                  : status === "good"
                  ? "Good planting window"
                  : "Not recommended"
              }`}
            >
              {/* Current month indicator */}
              {isCurrent && (
                <Box
                  position="absolute"
                  top="-8px"
                  right="-8px"
                  bg="orange.400"
                  borderRadius="full"
                  w="20px"
                  h="20px"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                  fontSize="xs"
                >
                  📍
                </Box>
              )}

              <VStack gap={1}>
                <Text fontSize="xs" fontWeight="bold">
                  {monthName}
                </Text>

                <Text fontSize="lg">{getSeasonIcon(index)}</Text>

                <Text fontSize="xs" fontWeight="medium">
                  {status === "optimal" && "★ Best"}
                  {status === "good" && "✓ Good"}
                  {status === "poor" && "✗ Poor"}
                </Text>
              </VStack>
            </Box>
          );
        })}
      </Grid>

      {/* Planting Window Summary */}
      <Box
        p={3}
        bg="white"
        borderRadius="md"
        border="1px"
        borderColor="green.200"
      >
        <VStack alignItems="stretch" gap={2}>
          <HStack justify="space-between">
            <Text fontSize="sm" fontWeight="semibold" color="green.800">
              🌱 Optimal Planting Window
            </Text>
            <Badge colorScheme="green" variant="outline">
              {plantingWindow.planting_window}
            </Badge>
          </HStack>

          <Text fontSize="xs" color="green.700">
            {plantingWindow.notes}
          </Text>

          {plantingWindow.optimal_months.length > 0 && (
            <HStack flexWrap="wrap" gap={2}>
              <Text fontSize="xs" color="green.600" fontWeight="medium">
                Best months:
              </Text>
              {plantingWindow.optimal_months.map((month) => (
                <Badge
                  key={month}
                  size="sm"
                  colorScheme="green"
                  variant="solid"
                >
                  {MONTH_NAMES[month - 1]}
                </Badge>
              ))}
            </HStack>
          )}
        </VStack>
      </Box>

      {/* Legend */}
      <HStack gap={4} justify="center" fontSize="xs">
        <HStack>
          <Box w="12px" h="12px" bg={SEASON_COLORS.optimal} borderRadius="sm" />
          <Text color="gray.600">Optimal</Text>
        </HStack>
        <HStack>
          <Box w="12px" h="12px" bg={SEASON_COLORS.good} borderRadius="sm" />
          <Text color="gray.600">Good</Text>
        </HStack>
        <HStack>
          <Box
            w="12px"
            h="12px"
            bg={SEASON_COLORS.poor}
            borderRadius="sm"
            opacity="0.4"
          />
          <Text color="gray.600">Poor</Text>
        </HStack>
        <HStack>
          <Box
            w="12px"
            h="12px"
            border="2px solid"
            borderColor="orange.400"
            borderRadius="sm"
          />
          <Text color="gray.600">Current</Text>
        </HStack>
      </HStack>

      {/* Quick Tips */}
      <Box
        p={3}
        bg="blue.50"
        borderRadius="md"
        border="1px"
        borderColor="blue.200"
      >
        <Text fontSize="xs" color="blue.700" fontWeight="medium" mb={1}>
          💡 Planting Tips
        </Text>
        <VStack alignItems="start" gap={1}>
          <Text fontSize="xs" color="blue.600">
            • Plant during optimal months for best yield
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Good months may require extra care and attention
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Avoid poor months unless you have greenhouse/controlled
            environment
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Consider local climate variations and micro-climates
          </Text>
        </VStack>
      </Box>
    </VStack>
  );
}
