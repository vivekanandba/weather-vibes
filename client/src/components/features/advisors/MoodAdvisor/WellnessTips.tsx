"use client";

import { Box, VStack, HStack, Text, Badge, Grid } from "@chakra-ui/react";

interface WellnessRecommendations {
  mood_category: string;
  activities: string[];
  wellness_tips: string[];
  energy_level: string;
  social_recommendations: string[];
}

interface WellnessTipsProps {
  wellnessRecommendations: WellnessRecommendations;
  dailyTips: string[];
}

const MOOD_CATEGORY_CONFIG: Record<
  string,
  {
    color: string;
    icon: string;
    description: string;
    bgColor: string;
  }
> = {
  energetic: {
    color: "red",
    icon: "⚡",
    description: "High energy and motivation levels",
    bgColor: "red.50",
  },
  refreshed: {
    color: "green",
    icon: "🌱",
    description: "Feeling renewed and clear-minded",
    bgColor: "green.50",
  },
  calm: {
    color: "blue",
    icon: "🧘‍♂️",
    description: "Peaceful and centered state",
    bgColor: "blue.50",
  },
  cozy: {
    color: "orange",
    icon: "🏠",
    description: "Comfortable and content indoors",
    bgColor: "orange.50",
  },
  lethargic: {
    color: "yellow",
    icon: "😴",
    description: "Low energy, need for gentle activities",
    bgColor: "yellow.50",
  },
  withdrawn: {
    color: "purple",
    icon: "🌙",
    description: "Introspective and seeking solitude",
    bgColor: "purple.50",
  },
  neutral: {
    color: "gray",
    icon: "⚖️",
    description: "Balanced emotional state",
    bgColor: "gray.50",
  },
};

const TIP_CATEGORIES: Record<
  string,
  {
    icon: string;
    color: string;
    keywords: string[];
  }
> = {
  physical: {
    icon: "💪",
    color: "red",
    keywords: [
      "exercise",
      "movement",
      "stretch",
      "walk",
      "activity",
      "physical",
    ],
  },
  mental: {
    icon: "🧠",
    color: "blue",
    keywords: [
      "focus",
      "concentrate",
      "think",
      "mental",
      "cognitive",
      "brain",
      "memory",
    ],
  },
  emotional: {
    icon: "❤️",
    color: "pink",
    keywords: [
      "feel",
      "emotion",
      "mood",
      "heart",
      "connect",
      "relationship",
      "social",
    ],
  },
  spiritual: {
    icon: "🕊️",
    color: "purple",
    keywords: [
      "meditat",
      "mindful",
      "spiritual",
      "peace",
      "gratitude",
      "reflect",
      "inner",
    ],
  },
  environmental: {
    icon: "🌿",
    color: "green",
    keywords: [
      "nature",
      "outdoor",
      "fresh air",
      "sunlight",
      "environment",
      "natural",
    ],
  },
  nutrition: {
    icon: "🥗",
    color: "orange",
    keywords: [
      "eat",
      "food",
      "nutrition",
      "vitamin",
      "hydrat",
      "drink",
      "diet",
    ],
  },
  rest: {
    icon: "😴",
    color: "indigo",
    keywords: [
      "rest",
      "sleep",
      "relax",
      "break",
      "recover",
      "recharge",
      "calm",
    ],
  },
  creative: {
    icon: "🎨",
    color: "yellow",
    keywords: ["creative", "art", "music", "craft", "express", "hobby", "play"],
  },
};

export default function WellnessTips({
  wellnessRecommendations,
  dailyTips,
}: WellnessTipsProps) {
  const moodConfig =
    MOOD_CATEGORY_CONFIG[wellnessRecommendations.mood_category] ||
    MOOD_CATEGORY_CONFIG["neutral"];

  const categorizeTip = (
    tip: string
  ): { category: string; config: (typeof TIP_CATEGORIES)[string] } => {
    const tipLower = tip.toLowerCase();

    for (const [category, config] of Object.entries(TIP_CATEGORIES)) {
      if (config.keywords.some((keyword) => tipLower.includes(keyword))) {
        return { category, config };
      }
    }

    return {
      category: "general",
      config: { icon: "💡", color: "gray", keywords: [] },
    };
  };

  const categorizedTips = wellnessRecommendations.wellness_tips.map((tip) => ({
    text: tip,
    ...categorizeTip(tip),
  }));

  const categorizedDailyTips = dailyTips.map((tip) => ({
    text: tip,
    ...categorizeTip(tip),
  }));

  const getEnergyLevelConfig = (level: string) => {
    switch (level) {
      case "high":
        return {
          color: "red",
          icon: "🔥",
          description: "Perfect for active pursuits",
        };
      case "moderate":
        return {
          color: "yellow",
          icon: "⭐",
          description: "Good for balanced activities",
        };
      case "low":
        return {
          color: "blue",
          icon: "🌙",
          description: "Focus on gentle activities",
        };
      default:
        return {
          color: "gray",
          icon: "⚖️",
          description: "Balanced energy level",
        };
    }
  };

  const energyConfig = getEnergyLevelConfig(
    wellnessRecommendations.energy_level
  );

  return (
    <VStack gap={4} alignItems="stretch" p={4} bg="teal.50" borderRadius="lg">
      {/* Mood Category Header */}
      <Box
        p={4}
        bg={moodConfig.bgColor}
        borderRadius="lg"
        border="2px solid"
        borderColor={moodConfig.color + ".200"}
      >
        <VStack alignItems="stretch" gap={3}>
          <HStack justify="space-between" align="center">
            <HStack>
              <Text fontSize="2xl">{moodConfig.icon}</Text>
              <VStack alignItems="start" gap={0}>
                <Text fontSize="sm" fontWeight="bold" color="gray.800">
                  Current Mood Category
                </Text>
                <Text fontSize="xs" color="gray.600">
                  {moodConfig.description}
                </Text>
              </VStack>
            </HStack>

            <Badge colorScheme={moodConfig.color} variant="solid" size="lg">
              {wellnessRecommendations.mood_category.toUpperCase()}
            </Badge>
          </HStack>

          {/* Energy Level Indicator */}
          <HStack
            p={2}
            bg="white"
            borderRadius="md"
            border="1px"
            borderColor="gray.200"
          >
            <Text fontSize="lg">{energyConfig.icon}</Text>
            <VStack alignItems="start" gap={0} flex={1}>
              <Text fontSize="xs" fontWeight="medium" color="gray.700">
                Energy Level: {wellnessRecommendations.energy_level}
              </Text>
              <Text fontSize="xs" color="gray.600">
                {energyConfig.description}
              </Text>
            </VStack>
            <Badge size="sm" colorScheme={energyConfig.color} variant="outline">
              {wellnessRecommendations.energy_level}
            </Badge>
          </HStack>
        </VStack>
      </Box>

      {/* Wellness Tips Grid */}
      <VStack alignItems="stretch" gap={3}>
        <Text fontSize="sm" fontWeight="semibold" color="teal.800">
          🌟 Personalized Wellness Tips
        </Text>

        <Grid templateColumns="repeat(auto-fit, minmax(300px, 1fr))" gap={3}>
          {categorizedTips.map((tip, index) => (
            <Box
              key={index}
              p={4}
              bg="white"
              borderRadius="lg"
              border="1px solid"
              borderColor={tip.config.color + ".200"}
              borderLeftWidth="4px"
              borderLeftColor={tip.config.color + ".400"}
              _hover={{ boxShadow: "md", transform: "translateY(-2px)" }}
              transition="all 0.2s"
            >
              <HStack alignItems="start" gap={3}>
                <Box
                  fontSize="lg"
                  p={2}
                  bg={tip.config.color + ".100"}
                  borderRadius="md"
                >
                  {tip.config.icon}
                </Box>

                <VStack alignItems="start" gap={2} flex={1}>
                  <Badge
                    size="sm"
                    colorScheme={tip.config.color}
                    variant="subtle"
                  >
                    {tip.category}
                  </Badge>

                  <Text fontSize="sm" color="gray.700" lineHeight="1.5">
                    {tip.text}
                  </Text>
                </VStack>
              </HStack>
            </Box>
          ))}
        </Grid>
      </VStack>

      {/* Daily Tips Section */}
      {categorizedDailyTips.length > 0 && (
        <VStack alignItems="stretch" gap={3}>
          <Text fontSize="sm" fontWeight="semibold" color="teal.800">
            📅 Today&apos;s Special Tips
          </Text>

          <VStack gap={2} alignItems="stretch">
            {categorizedDailyTips.map((tip, index) => (
              <Box
                key={index}
                p={3}
                bg="white"
                borderRadius="md"
                border="1px solid"
                borderColor="teal.200"
                borderLeftWidth="3px"
                borderLeftColor="teal.400"
              >
                <HStack alignItems="start" gap={3}>
                  <Text fontSize="md">{tip.config.icon}</Text>

                  <VStack alignItems="start" gap={1} flex={1}>
                    <HStack>
                      <Badge
                        size="xs"
                        colorScheme={tip.config.color}
                        variant="outline"
                      >
                        {tip.category}
                      </Badge>
                      <Text fontSize="xs" color="gray.500">
                        Weather-specific
                      </Text>
                    </HStack>

                    <Text fontSize="sm" color="gray.700" lineHeight="1.4">
                      {tip.text}
                    </Text>
                  </VStack>
                </HStack>
              </Box>
            ))}
          </VStack>
        </VStack>
      )}

      {/* Recommended Activities Summary */}
      <Box
        p={4}
        bg="white"
        borderRadius="lg"
        border="1px"
        borderColor="teal.200"
      >
        <VStack alignItems="stretch" gap={3}>
          <Text fontSize="sm" fontWeight="semibold" color="teal.800">
            🎯 Recommended Activities for Today
          </Text>

          <Grid templateColumns="repeat(auto-fit, minmax(200px, 1fr))" gap={2}>
            {wellnessRecommendations.activities
              .slice(0, 6)
              .map((activity, index) => (
                <Box
                  key={index}
                  p={2}
                  bg="teal.50"
                  borderRadius="md"
                  border="1px solid"
                  borderColor="teal.100"
                  textAlign="center"
                >
                  <Text fontSize="xs" color="teal.700" fontWeight="medium">
                    {activity}
                  </Text>
                </Box>
              ))}
          </Grid>

          {wellnessRecommendations.activities.length > 6 && (
            <Text fontSize="xs" color="gray.600" textAlign="center">
              +{wellnessRecommendations.activities.length - 6} more activities
              recommended
            </Text>
          )}
        </VStack>
      </Box>

      {/* Social Wellness */}
      {wellnessRecommendations.social_recommendations.length > 0 && (
        <Box
          p={4}
          bg="pink.50"
          borderRadius="lg"
          border="1px"
          borderColor="pink.200"
        >
          <VStack alignItems="stretch" gap={2}>
            <HStack>
              <Text fontSize="lg">👥</Text>
              <Text fontSize="sm" fontWeight="semibold" color="pink.800">
                Social Wellness Recommendations
              </Text>
            </HStack>

            {wellnessRecommendations.social_recommendations.map(
              (rec, index) => (
                <HStack key={index} alignItems="start" gap={2}>
                  <Text fontSize="xs" color="pink.500">
                    •
                  </Text>
                  <Text fontSize="xs" color="pink.700" lineHeight="1.4">
                    {rec}
                  </Text>
                </HStack>
              )
            )}
          </VStack>
        </Box>
      )}

      {/* Wellness Categories Summary */}
      <Box
        p={3}
        bg="gray.50"
        borderRadius="md"
        border="1px"
        borderColor="gray.200"
      >
        <Text fontSize="xs" color="gray.700" fontWeight="medium" mb={2}>
          🏷️ Tip Categories in Your Plan
        </Text>

        <HStack flexWrap="wrap" gap={2}>
          {Array.from(
            new Set([
              ...categorizedTips.map((t) => t.category),
              ...categorizedDailyTips.map((t) => t.category),
            ])
          ).map((category) => {
            const config = TIP_CATEGORIES[category] || {
              icon: "💡",
              color: "gray",
            };
            return (
              <Badge
                key={category}
                size="sm"
                colorScheme={config.color}
                variant="subtle"
              >
                {config.icon} {category}
              </Badge>
            );
          })}
        </HStack>
      </Box>

      {/* Wellness Action Note */}
      <Box
        p={3}
        bg="blue.50"
        borderRadius="md"
        border="1px"
        borderColor="blue.200"
      >
        <Text fontSize="xs" color="blue.700" fontWeight="medium" mb={1}>
          🎯 Taking Action on Wellness Tips
        </Text>
        <VStack alignItems="start" gap={1}>
          <Text fontSize="xs" color="blue.600">
            • Start with tips that match your current energy level
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Focus on 2-3 categories rather than trying everything at once
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Adjust recommendations based on how you feel throughout the day
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Weather-specific tips are tailored to current conditions
          </Text>
        </VStack>
      </Box>
    </VStack>
  );
}
