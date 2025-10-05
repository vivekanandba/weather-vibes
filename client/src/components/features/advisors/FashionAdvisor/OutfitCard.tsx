"use client";

import { Box, VStack, HStack, Text, Badge } from "@chakra-ui/react";
import { useState } from "react";

interface OutfitItem {
  type: string;
  name: string;
  category: string;
  weather_suitability: string;
  style_match: string;
  fabric: string;
}

interface OutfitRecommendation {
  name: string;
  priority: string;
  items: OutfitItem[];
  comfort_score: number;
  style_score: number;
  weather_appropriateness: number;
  notes: string[];
}

interface OutfitCardProps {
  outfit: OutfitRecommendation;
  isExpanded?: boolean;
  onToggle?: () => void;
}

export default function OutfitCard({
  outfit,
  isExpanded = false,
  onToggle,
}: OutfitCardProps) {
  const [expanded, setExpanded] = useState(isExpanded);

  const handleToggle = () => {
    setExpanded(!expanded);
    onToggle?.();
  };

  const getSuitabilityColor = (suitability: string) => {
    switch (suitability) {
      case "excellent":
        return "green";
      case "good":
        return "blue";
      case "fair":
        return "yellow";
      case "poor":
        return "red";
      default:
        return "gray";
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case "weather":
        return "🌤️";
      case "style":
        return "✨";
      case "layering":
        return "🧥";
      default:
        return "👔";
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "green";
    if (score >= 60) return "yellow";
    return "red";
  };

  return (
    <Box
      p={4}
      bg="white"
      borderRadius="lg"
      border="1px"
      borderColor="gray.200"
      boxShadow="sm"
      cursor="pointer"
      onClick={handleToggle}
      _hover={{ boxShadow: "md", borderColor: "brand.300" }}
      transition="all 0.2s"
    >
      <VStack gap={3} alignItems="stretch">
        {/* Header */}
        <HStack justify="space-between" align="center">
          <HStack>
            <Text fontSize="lg" fontWeight="bold" color="gray.800">
              {getPriorityIcon(outfit.priority)} {outfit.name}
            </Text>
            <Badge colorScheme="brand" variant="subtle">
              {outfit.priority}
            </Badge>
          </HStack>
          <Text fontSize="sm" color="gray.500">
            {expanded ? "▼" : "▶"}
          </Text>
        </HStack>

        {/* Score Summary */}
        <HStack justify="space-between" gap={4}>
          <VStack flex={1} gap={1}>
            <Text fontSize="xs" color="gray.600">
              Comfort
            </Text>
            <Box
              w="100%"
              h="8px"
              bg="gray.200"
              borderRadius="full"
              overflow="hidden"
            >
              <Box
                h="100%"
                w={`${outfit.comfort_score}%`}
                bg={`${getScoreColor(outfit.comfort_score)}.400`}
                borderRadius="full"
                transition="width 0.3s ease"
              />
            </Box>
            <Text fontSize="xs" color="gray.700" fontWeight="medium">
              {outfit.comfort_score}%
            </Text>
          </VStack>

          <VStack flex={1} gap={1}>
            <Text fontSize="xs" color="gray.600">
              Style
            </Text>
            <Box
              w="100%"
              h="8px"
              bg="gray.200"
              borderRadius="full"
              overflow="hidden"
            >
              <Box
                h="100%"
                w={`${outfit.style_score}%`}
                bg={`${getScoreColor(outfit.style_score)}.400`}
                borderRadius="full"
                transition="width 0.3s ease"
              />
            </Box>
            <Text fontSize="xs" color="gray.700" fontWeight="medium">
              {outfit.style_score}%
            </Text>
          </VStack>

          <VStack flex={1} gap={1}>
            <Text fontSize="xs" color="gray.600">
              Weather
            </Text>
            <Box
              w="100%"
              h="8px"
              bg="gray.200"
              borderRadius="full"
              overflow="hidden"
            >
              <Box
                h="100%"
                w={`${outfit.weather_appropriateness}%`}
                bg={`${getScoreColor(outfit.weather_appropriateness)}.400`}
                borderRadius="full"
                transition="width 0.3s ease"
              />
            </Box>
            <Text fontSize="xs" color="gray.700" fontWeight="medium">
              {outfit.weather_appropriateness}%
            </Text>
          </VStack>
        </HStack>

        {/* Expanded Content */}
        {expanded && (
          <>
            <Box h="1px" bg="gray.200" />

            {/* Clothing Items */}
            <VStack gap={3} alignItems="stretch">
              <Text fontSize="sm" fontWeight="semibold" color="gray.700">
                👔 Outfit Items
              </Text>

              {outfit.items.map((item, index) => (
                <Box
                  key={index}
                  p={3}
                  bg="gray.50"
                  borderRadius="md"
                  border="1px"
                  borderColor="gray.100"
                >
                  <HStack justify="space-between" align="start">
                    <VStack alignItems="start" gap={1} flex={1}>
                      <HStack>
                        <Text
                          fontSize="sm"
                          fontWeight="medium"
                          color="gray.800"
                        >
                          {item.name}
                        </Text>
                        <Badge size="sm" colorScheme="gray">
                          {item.type}
                        </Badge>
                      </HStack>

                      <Text fontSize="xs" color="gray.600">
                        Material: {item.fabric}
                      </Text>
                    </VStack>

                    <VStack gap={1} align="end">
                      <Badge
                        size="sm"
                        colorScheme={getSuitabilityColor(
                          item.weather_suitability
                        )}
                      >
                        {item.weather_suitability}
                      </Badge>
                      <Text fontSize="xs" color="gray.500">
                        weather match
                      </Text>
                    </VStack>
                  </HStack>
                </Box>
              ))}
            </VStack>

            {/* Notes */}
            {outfit.notes.length > 0 && (
              <VStack gap={2} alignItems="stretch">
                <Text fontSize="sm" fontWeight="semibold" color="gray.700">
                  💡 Style Notes
                </Text>
                {outfit.notes.map((note, index) => (
                  <Box
                    key={index}
                    p={2}
                    bg="blue.50"
                    borderRadius="sm"
                    border="1px"
                    borderColor="blue.200"
                  >
                    <Text fontSize="xs" color="blue.700">
                      • {note}
                    </Text>
                  </Box>
                ))}
              </VStack>
            )}
          </>
        )}
      </VStack>
    </Box>
  );
}
