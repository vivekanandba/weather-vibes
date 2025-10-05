"use client";

import {
  Box,
  VStack,
  HStack,
  Text,
  Badge,
  Grid,
  Button,
} from "@chakra-ui/react";
import { useState } from "react";

interface Activity {
  name: string;
  suitability: string;
  duration: string;
  preparation: string[];
}

interface ActivitySuggestionsProps {
  activities: Activity[];
  energyLevel: string;
  socialRecommendations: string[];
  onActivitySelect?: (activity: Activity) => void;
}

const SUITABILITY_CONFIG: Record<
  string,
  {
    color: string;
    icon: string;
    description: string;
  }
> = {
  high: {
    color: "green",
    icon: "🌟",
    description: "Perfect match for your current mood and weather",
  },
  moderate: {
    color: "yellow",
    icon: "👍",
    description: "Good option, may require some adjustments",
  },
  medium: {
    color: "yellow",
    icon: "👍",
    description: "Good option, may require some adjustments",
  },
  low: {
    color: "red",
    icon: "⚠️",
    description: "Not ideal for current conditions",
  },
};

const ENERGY_LEVEL_CONFIG: Record<
  string,
  {
    color: string;
    icon: string;
    description: string;
    recommendations: string[];
  }
> = {
  high: {
    color: "red",
    icon: "⚡",
    description: "You have lots of energy today!",
    recommendations: [
      "Perfect for physical activities",
      "Try challenging or new activities",
      "Great for social gatherings",
    ],
  },
  moderate: {
    color: "yellow",
    icon: "🌟",
    description: "Good energy levels for most activities",
    recommendations: [
      "Balanced mix of active and relaxing",
      "Good for planned activities",
      "Moderate social engagement",
    ],
  },
  low: {
    color: "blue",
    icon: "😌",
    description: "Take it easy and focus on gentle activities",
    recommendations: [
      "Prioritize rest and relaxation",
      "Choose low-energy activities",
      "Small social groups or solo time",
    ],
  },
};

const ACTIVITY_ICONS: Record<string, string> = {
  // Physical activities
  running: "🏃‍♂️",
  cycling: "🚴‍♀️",
  hiking: "🥾",
  exercise: "💪",
  yoga: "🧘‍♀️",
  swimming: "🏊‍♀️",
  dancing: "💃",

  // Indoor activities
  reading: "📚",
  cooking: "👨‍🍳",
  baking: "👨‍🍳",
  movies: "🎬",
  music: "🎵",
  art: "🎨",
  writing: "✍️",
  gaming: "🎮",

  // Social activities
  friends: "👥",
  family: "👨‍👩‍👧‍👦",
  party: "🎉",
  coffee: "☕",
  restaurant: "🍽️",

  // Outdoor activities
  park: "🌳",
  beach: "🏖️",
  garden: "🌻",
  photography: "📸",
  picnic: "🧺",

  // Relaxation
  meditation: "🧘‍♂️",
  spa: "💆‍♀️",
  bath: "🛁",
  nap: "😴",
  massage: "💆‍♀️",
};

export default function ActivitySuggestions({
  activities,
  energyLevel,
  socialRecommendations,
  onActivitySelect,
}: ActivitySuggestionsProps) {
  const [selectedActivities, setSelectedActivities] = useState<Set<number>>(
    new Set()
  );
  const [filterBySuitability, setFilterBySuitability] = useState<string | null>(
    null
  );

  const energyConfig =
    ENERGY_LEVEL_CONFIG[energyLevel] || ENERGY_LEVEL_CONFIG["moderate"];

  const getActivityIcon = (activityName: string) => {
    const name = activityName.toLowerCase();

    // Find matching icon by checking if activity name contains key
    for (const [key, icon] of Object.entries(ACTIVITY_ICONS)) {
      if (name.includes(key)) {
        return icon;
      }
    }

    // Default icon based on activity type
    if (
      name.includes("outdoor") ||
      name.includes("exercise") ||
      name.includes("sport")
    )
      return "🏃‍♂️";
    if (
      name.includes("indoor") ||
      name.includes("home") ||
      name.includes("relax")
    )
      return "🏠";
    if (
      name.includes("social") ||
      name.includes("gather") ||
      name.includes("meet")
    )
      return "👥";
    if (
      name.includes("creative") ||
      name.includes("art") ||
      name.includes("craft")
    )
      return "🎨";

    return "🎯"; // Default activity icon
  };

  const handleActivityToggle = (index: number) => {
    const newSelected = new Set(selectedActivities);
    if (selectedActivities.has(index)) {
      newSelected.delete(index);
    } else {
      newSelected.add(index);
      onActivitySelect?.(activities[index]);
    }
    setSelectedActivities(newSelected);
  };

  const filteredActivities = filterBySuitability
    ? activities.filter(
        (activity) => activity.suitability === filterBySuitability
      )
    : activities;

  const sortedActivities = [...filteredActivities].sort((a, b) => {
    const suitabilityOrder = { high: 3, moderate: 2, medium: 2, low: 1 };
    return (
      (suitabilityOrder[b.suitability as keyof typeof suitabilityOrder] || 0) -
      (suitabilityOrder[a.suitability as keyof typeof suitabilityOrder] || 0)
    );
  });

  return (
    <VStack gap={4} alignItems="stretch" p={4} bg="purple.50" borderRadius="lg">
      {/* Energy Level Header */}
      <Box
        p={4}
        bg="white"
        borderRadius="lg"
        border="1px"
        borderColor="purple.200"
      >
        <VStack alignItems="stretch" gap={3}>
          <HStack justify="space-between" align="center">
            <HStack>
              <Text fontSize="lg">{energyConfig.icon}</Text>
              <VStack alignItems="start" gap={0}>
                <Text fontSize="sm" fontWeight="bold" color="gray.800">
                  Your Energy Level Today
                </Text>
                <Text fontSize="xs" color="gray.600">
                  {energyConfig.description}
                </Text>
              </VStack>
            </HStack>

            <Badge colorScheme={energyConfig.color} variant="solid" size="lg">
              {energyLevel.toUpperCase()}
            </Badge>
          </HStack>

          <VStack alignItems="start" gap={1}>
            {energyConfig.recommendations.map((rec, index) => (
              <Text key={index} fontSize="xs" color="gray.600">
                • {rec}
              </Text>
            ))}
          </VStack>
        </VStack>
      </Box>

      {/* Activity Filter */}
      <HStack gap={2} flexWrap="wrap">
        <Text fontSize="xs" color="gray.600" fontWeight="medium">
          Filter by suitability:
        </Text>

        <Button
          size="xs"
          variant={filterBySuitability === null ? "solid" : "outline"}
          colorScheme="purple"
          onClick={() => setFilterBySuitability(null)}
        >
          All ({activities.length})
        </Button>

        {Object.entries(SUITABILITY_CONFIG).map(([level, config]) => {
          const count = activities.filter(
            (a) => a.suitability === level
          ).length;
          if (count === 0) return null;

          return (
            <Button
              key={level}
              size="xs"
              variant={filterBySuitability === level ? "solid" : "outline"}
              colorScheme={config.color}
              onClick={() => setFilterBySuitability(level)}
            >
              {config.icon} {level} ({count})
            </Button>
          );
        })}
      </HStack>

      {/* Activity Suggestions Grid */}
      <Grid templateColumns="repeat(auto-fit, minmax(280px, 1fr))" gap={4}>
        {sortedActivities.map((activity, index) => {
          const originalIndex = activities.indexOf(activity);
          const suitabilityConfig =
            SUITABILITY_CONFIG[activity.suitability] ||
            SUITABILITY_CONFIG["moderate"];
          const isSelected = selectedActivities.has(originalIndex);
          const activityIcon = getActivityIcon(activity.name);

          return (
            <Box
              key={originalIndex}
              p={4}
              bg="white"
              borderRadius="lg"
              border="2px solid"
              borderColor={
                isSelected ? suitabilityConfig.color + ".400" : "gray.200"
              }
              cursor="pointer"
              onClick={() => handleActivityToggle(originalIndex)}
              _hover={{
                borderColor: suitabilityConfig.color + ".300",
                transform: "translateY(-2px)",
                boxShadow: "lg",
              }}
              transition="all 0.2s"
              position="relative"
            >
              {/* Selection Indicator */}
              {isSelected && (
                <Box
                  position="absolute"
                  top="-8px"
                  right="-8px"
                  bg={suitabilityConfig.color + ".400"}
                  color="white"
                  borderRadius="full"
                  w="24px"
                  h="24px"
                  display="flex"
                  alignItems="center"
                  justifyContent="center"
                  fontSize="sm"
                  fontWeight="bold"
                >
                  ✓
                </Box>
              )}

              <VStack alignItems="stretch" gap={3}>
                {/* Activity Header */}
                <HStack justify="space-between" align="start">
                  <HStack>
                    <Text fontSize="xl">{activityIcon}</Text>
                    <VStack alignItems="start" gap={0}>
                      <Text fontSize="sm" fontWeight="bold" color="gray.800">
                        {activity.name}
                      </Text>
                      <Badge
                        size="sm"
                        colorScheme={suitabilityConfig.color}
                        variant="subtle"
                      >
                        {suitabilityConfig.icon} {activity.suitability} match
                      </Badge>
                    </VStack>
                  </HStack>
                </HStack>

                {/* Duration */}
                <HStack>
                  <Text fontSize="xs" color="gray.600" fontWeight="medium">
                    ⏱️ Suggested duration:
                  </Text>
                  <Text fontSize="xs" color="gray.700">
                    {activity.duration}
                  </Text>
                </HStack>

                {/* Preparation */}
                {activity.preparation.length > 0 && (
                  <VStack alignItems="stretch" gap={2}>
                    <Text fontSize="xs" color="gray.600" fontWeight="medium">
                      🎒 What you&apos;ll need:
                    </Text>
                    <VStack alignItems="start" gap={1}>
                      {activity.preparation
                        .slice(0, 3)
                        .map((prep, prepIndex) => (
                          <Text key={prepIndex} fontSize="xs" color="gray.600">
                            • {prep}
                          </Text>
                        ))}
                      {activity.preparation.length > 3 && (
                        <Text fontSize="xs" color="gray.500">
                          +{activity.preparation.length - 3} more items
                        </Text>
                      )}
                    </VStack>
                  </VStack>
                )}

                {/* Suitability Note */}
                <Box
                  p={2}
                  bg={suitabilityConfig.color + ".50"}
                  borderRadius="sm"
                >
                  <Text fontSize="xs" color={suitabilityConfig.color + ".700"}>
                    💭 {suitabilityConfig.description}
                  </Text>
                </Box>
              </VStack>
            </Box>
          );
        })}
      </Grid>

      {/* Social Recommendations */}
      {socialRecommendations.length > 0 && (
        <Box
          p={4}
          bg="blue.50"
          borderRadius="lg"
          border="1px"
          borderColor="blue.200"
        >
          <VStack alignItems="stretch" gap={2}>
            <Text fontSize="sm" fontWeight="semibold" color="blue.800">
              👥 Social Activity Recommendations
            </Text>

            {socialRecommendations.map((rec, index) => (
              <Text key={index} fontSize="xs" color="blue.700">
                • {rec}
              </Text>
            ))}
          </VStack>
        </Box>
      )}

      {/* Selected Activities Summary */}
      {selectedActivities.size > 0 && (
        <Box
          p={3}
          bg="green.50"
          borderRadius="md"
          border="1px"
          borderColor="green.200"
        >
          <HStack justify="space-between" align="center">
            <Text fontSize="sm" fontWeight="medium" color="green.800">
              🎯 Selected Activities: {selectedActivities.size}
            </Text>

            <Button
              size="sm"
              colorScheme="green"
              variant="solid"
              onClick={() => {
                const selectedActivityList = Array.from(selectedActivities).map(
                  (i) => activities[i]
                );
                console.log("Planning activities:", selectedActivityList);
              }}
            >
              Plan My Day
            </Button>
          </HStack>
        </Box>
      )}

      {/* Activity Tips */}
      <Box
        p={3}
        bg="yellow.50"
        borderRadius="md"
        border="1px"
        borderColor="yellow.200"
      >
        <Text fontSize="xs" color="yellow.700" fontWeight="medium" mb={1}>
          💡 Activity Tips for Today
        </Text>
        <VStack alignItems="start" gap={1}>
          <Text fontSize="xs" color="yellow.600">
            • Choose activities that match your energy level and weather
            conditions
          </Text>
          <Text fontSize="xs" color="yellow.600">
            • Have backup indoor options ready in case weather changes
          </Text>
          <Text fontSize="xs" color="yellow.600">
            • Listen to your body and adjust activities as needed
          </Text>
          <Text fontSize="xs" color="yellow.600">
            • Consider combining high and low suitability activities for variety
          </Text>
        </VStack>
      </Box>
    </VStack>
  );
}
