"use client";

import {
  Box,
  VStack,
  HStack,
  Text,
  Badge,
  Grid,
  Tooltip,
} from "@chakra-ui/react";

interface FabricRecommendation {
  fabric: string;
  reason: string;
  priority: string;
}

interface FabricRecommendationsProps {
  fabricRecommendations: FabricRecommendation[];
}

const FABRIC_PROPERTIES: Record<
  string,
  {
    description: string;
    icon: string;
    properties: string[];
    bestFor: string[];
  }
> = {
  cotton: {
    description: "Natural, breathable fiber",
    icon: "🌱",
    properties: ["breathable", "comfortable", "absorbent"],
    bestFor: ["casual wear", "everyday comfort"],
  },
  linen: {
    description: "Lightweight natural cooling",
    icon: "🍃",
    properties: ["very breathable", "quick-drying", "lightweight"],
    bestFor: ["hot weather", "summer clothing"],
  },
  wool: {
    description: "Natural insulating fiber",
    icon: "🐑",
    properties: ["insulating", "moisture-wicking", "odor-resistant"],
    bestFor: ["cold weather", "layering"],
  },
  cashmere: {
    description: "Luxury warm and soft",
    icon: "✨",
    properties: ["very soft", "lightweight", "warm"],
    bestFor: ["luxury items", "cold weather"],
  },
  fleece: {
    description: "Synthetic insulation",
    icon: "🧥",
    properties: ["warm", "lightweight", "quick-drying"],
    bestFor: ["outdoor activities", "layering"],
  },
  polyester: {
    description: "Durable synthetic",
    icon: "🔧",
    properties: ["durable", "wrinkle-resistant", "easy-care"],
    bestFor: ["activewear", "professional wear"],
  },
  bamboo: {
    description: "Eco-friendly moisture-wicking",
    icon: "🎋",
    properties: ["moisture-wicking", "antibacterial", "soft"],
    bestFor: ["activewear", "sensitive skin"],
  },
  gore_tex: {
    description: "Waterproof and breathable",
    icon: "☔",
    properties: ["waterproof", "breathable", "windproof"],
    bestFor: ["rain gear", "outdoor activities"],
  },
  nylon: {
    description: "Water-resistant synthetic",
    icon: "💧",
    properties: ["water-resistant", "durable", "lightweight"],
    bestFor: ["rain protection", "windbreakers"],
  },
  windproof_materials: {
    description: "Wind-resistant fabrics",
    icon: "💨",
    properties: ["wind-resistant", "durable"],
    bestFor: ["windy conditions", "outdoor activities"],
  },
  denim: {
    description: "Durable cotton weave",
    icon: "👖",
    properties: ["durable", "versatile", "classic"],
    bestFor: ["casual wear", "everyday use"],
  },
  silk: {
    description: "Natural luxury fiber",
    icon: "🦋",
    properties: ["smooth", "temperature-regulating", "elegant"],
    bestFor: ["formal wear", "delicate items"],
  },
  leather: {
    description: "Natural animal hide",
    icon: "🦌",
    properties: ["durable", "wind-resistant", "classic"],
    bestFor: ["outerwear", "accessories"],
  },
};

export default function FabricRecommendations({
  fabricRecommendations,
}: FabricRecommendationsProps) {
  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case "high":
        return "red";
      case "medium":
        return "yellow";
      case "low":
        return "blue";
      default:
        return "gray";
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority.toLowerCase()) {
      case "high":
        return "🔥";
      case "medium":
        return "⭐";
      case "low":
        return "💡";
      default:
        return "📝";
    }
  };

  return (
    <VStack gap={4} alignItems="stretch" p={4} bg="gray.50" borderRadius="lg">
      <Text fontSize="sm" fontWeight="semibold" color="gray.700">
        🧵 Fabric Recommendations
      </Text>

      <Grid templateColumns="repeat(auto-fit, minmax(280px, 1fr))" gap={3}>
        {fabricRecommendations.map((recommendation, index) => {
          const fabricInfo = FABRIC_PROPERTIES[
            recommendation.fabric.toLowerCase()
          ] || {
            description: "Recommended fabric",
            icon: "🧵",
            properties: ["suitable for current weather"],
            bestFor: ["current conditions"],
          };

          return (
            <Box
              key={index}
              p={4}
              bg="white"
              borderRadius="lg"
              border="1px"
              borderColor="gray.200"
              boxShadow="sm"
              _hover={{ boxShadow: "md", borderColor: "brand.300" }}
              transition="all 0.2s"
            >
              <VStack alignItems="stretch" gap={3}>
                {/* Header */}
                <HStack justify="space-between" align="center">
                  <HStack>
                    <Text fontSize="xl">{fabricInfo.icon}</Text>
                    <VStack alignItems="start" gap={0}>
                      <Text
                        fontSize="sm"
                        fontWeight="bold"
                        color="gray.800"
                        textTransform="capitalize"
                      >
                        {recommendation.fabric.replace(/_/g, " ")}
                      </Text>
                      <Text fontSize="xs" color="gray.600">
                        {fabricInfo.description}
                      </Text>
                    </VStack>
                  </HStack>

                  <VStack gap={1} align="end">
                    <Badge
                      colorScheme={getPriorityColor(recommendation.priority)}
                      variant="solid"
                      size="sm"
                    >
                      {getPriorityIcon(recommendation.priority)}{" "}
                      {recommendation.priority}
                    </Badge>
                  </VStack>
                </HStack>

                {/* Reason */}
                <Box
                  p={2}
                  bg="blue.50"
                  borderRadius="md"
                  border="1px"
                  borderColor="blue.200"
                >
                  <Text fontSize="xs" color="blue.700" fontWeight="medium">
                    Why it&apos;s recommended:
                  </Text>
                  <Text fontSize="xs" color="blue.600" mt={1}>
                    {recommendation.reason}
                  </Text>
                </Box>

                {/* Properties */}
                <VStack alignItems="stretch" gap={2}>
                  <Text fontSize="xs" fontWeight="semibold" color="gray.700">
                    Key Properties:
                  </Text>
                  <HStack flexWrap="wrap" gap={1}>
                    {fabricInfo.properties.map((property, propIndex) => (
                      <Badge
                        key={propIndex}
                        size="sm"
                        colorScheme="green"
                        variant="subtle"
                      >
                        {property}
                      </Badge>
                    ))}
                  </HStack>
                </VStack>

                {/* Best For */}
                <VStack alignItems="stretch" gap={2}>
                  <Text fontSize="xs" fontWeight="semibold" color="gray.700">
                    Best for:
                  </Text>
                  <VStack alignItems="start" gap={1}>
                    {fabricInfo.bestFor.map((use, useIndex) => (
                      <Text key={useIndex} fontSize="xs" color="gray.600">
                        • {use}
                      </Text>
                    ))}
                  </VStack>
                </VStack>
              </VStack>
            </Box>
          );
        })}
      </Grid>

      {/* General Fabric Care Tips */}
      <Box
        p={3}
        bg="purple.50"
        borderRadius="md"
        border="1px"
        borderColor="purple.200"
      >
        <Text fontSize="xs" color="purple.700" fontWeight="medium" mb={2}>
          🧼 Fabric Care Tips for Current Weather
        </Text>
        <VStack alignItems="start" gap={1}>
          {fabricRecommendations.some((f) => f.fabric.includes("water")) && (
            <Text fontSize="xs" color="purple.600">
              • Pre-treat waterproof fabrics with appropriate care products
            </Text>
          )}
          {fabricRecommendations.some((f) => f.priority === "high") && (
            <Text fontSize="xs" color="purple.600">
              • High-priority fabrics are essential for comfort in current
              conditions
            </Text>
          )}
          <Text fontSize="xs" color="purple.600">
            • Always check care labels before washing
          </Text>
          <Text fontSize="xs" color="purple.600">
            • Consider fabric blends for optimal comfort and durability
          </Text>
        </VStack>
      </Box>
    </VStack>
  );
}
