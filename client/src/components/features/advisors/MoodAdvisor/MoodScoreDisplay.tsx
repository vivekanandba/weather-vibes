"use client";

import {
  Box,
  VStack,
  HStack,
  Text,
  Badge,
  Grid,
  Progress,
} from "@chakra-ui/react";

interface MoodFactor {
  factor: string;
  value: number;
  score: number;
  impact: string;
  description: string;
}

interface MoodPrediction {
  overall_score: number;
  predicted_mood: string;
  confidence: number;
  factors: MoodFactor[];
}

interface MoodScoreDisplayProps {
  moodPrediction: MoodPrediction;
}

const MOOD_SCORE_RANGES: Record<
  string,
  {
    min: number;
    max: number;
    color: string;
    icon: string;
    description: string;
    bgColor: string;
  }
> = {
  excellent: {
    min: 80,
    max: 100,
    color: "green",
    icon: "😊",
    description:
      "Feeling great! Perfect conditions for productivity and happiness",
    bgColor: "green.50",
  },
  good: {
    min: 65,
    max: 79,
    color: "blue",
    icon: "🙂",
    description: "Good mood overall with minor weather influences",
    bgColor: "blue.50",
  },
  neutral: {
    min: 50,
    max: 64,
    color: "yellow",
    icon: "😐",
    description: "Balanced mood, weather has moderate impact",
    bgColor: "yellow.50",
  },
  low: {
    min: 35,
    max: 49,
    color: "orange",
    icon: "😔",
    description: "Weather is affecting your mood negatively",
    bgColor: "orange.50",
  },
  poor: {
    min: 0,
    max: 34,
    color: "red",
    icon: "😞",
    description: "Challenging weather conditions for mood and energy",
    bgColor: "red.50",
  },
};

const FACTOR_ICONS: Record<string, string> = {
  temperature: "🌡️",
  sunlight: "☀️",
  precipitation: "🌧️",
  humidity: "💧",
  wind: "💨",
  pressure: "⭐",
};

const IMPACT_CONFIG: Record<
  string,
  {
    color: string;
    icon: string;
  }
> = {
  positive: { color: "green", icon: "✅" },
  negative: { color: "red", icon: "❌" },
  neutral: { color: "gray", icon: "➖" },
};

export default function MoodScoreDisplay({
  moodPrediction,
}: MoodScoreDisplayProps) {
  const getMoodConfig = (score: number) => {
    for (const [mood, config] of Object.entries(MOOD_SCORE_RANGES)) {
      if (score >= config.min && score <= config.max) {
        return { mood, ...config };
      }
    }
    return { mood: "neutral", ...MOOD_SCORE_RANGES["neutral"] };
  };

  const moodConfig = getMoodConfig(moodPrediction.overall_score);

  const getScoreColor = (score: number) => {
    if (score >= 80) return "green";
    if (score >= 60) return "blue";
    if (score >= 40) return "yellow";
    if (score >= 20) return "orange";
    return "red";
  };

  const getConfidenceText = (confidence: number) => {
    if (confidence >= 0.8) return "Very High";
    if (confidence >= 0.6) return "High";
    if (confidence >= 0.4) return "Medium";
    if (confidence >= 0.2) return "Low";
    return "Very Low";
  };

  const getWeatherDescription = (factor: string, value: number) => {
    switch (factor) {
      case "temperature":
        if (value < 10) return "Very Cold";
        if (value < 20) return "Cool";
        if (value < 25) return "Pleasant";
        if (value < 30) return "Warm";
        return "Hot";
      case "sunlight":
        if (value < 2) return "Very Cloudy";
        if (value < 4) return "Cloudy";
        if (value < 6) return "Partly Sunny";
        if (value < 8) return "Sunny";
        return "Very Sunny";
      case "precipitation":
        if (value < 1) return "Dry";
        if (value < 5) return "Light Rain";
        if (value < 15) return "Moderate Rain";
        return "Heavy Rain";
      case "humidity":
        if (value < 30) return "Very Dry";
        if (value < 50) return "Dry";
        if (value < 70) return "Comfortable";
        if (value < 80) return "Humid";
        return "Very Humid";
      default:
        return value.toFixed(1);
    }
  };

  return (
    <VStack
      gap={4}
      alignItems="stretch"
      p={4}
      bg={moodConfig.bgColor}
      borderRadius="lg"
    >
      {/* Main Mood Score */}
      <Box
        p={6}
        bg="white"
        borderRadius="xl"
        border="2px solid"
        borderColor={moodConfig.color + ".200"}
        boxShadow="lg"
      >
        <VStack gap={4}>
          {/* Score Circle */}
          <VStack gap={2}>
            <Box
              w="120px"
              h="120px"
              borderRadius="full"
              bg={moodConfig.color + ".100"}
              border="8px solid"
              borderColor={moodConfig.color + ".300"}
              display="flex"
              alignItems="center"
              justifyContent="center"
              position="relative"
            >
              <VStack gap={1}>
                <Text
                  fontSize="3xl"
                  fontWeight="bold"
                  color={moodConfig.color + ".600"}
                >
                  {Math.round(moodPrediction.overall_score)}
                </Text>
                <Text
                  fontSize="xs"
                  color={moodConfig.color + ".500"}
                  fontWeight="medium"
                >
                  MOOD SCORE
                </Text>
              </VStack>

              {/* Mood Emoji */}
              <Box
                position="absolute"
                top="-10px"
                right="-10px"
                fontSize="2xl"
                bg="white"
                borderRadius="full"
                p={1}
                border="3px solid"
                borderColor={moodConfig.color + ".200"}
              >
                {moodConfig.icon}
              </Box>
            </Box>

            {/* Mood Category */}
            <VStack gap={1}>
              <Badge
                colorScheme={moodConfig.color}
                variant="solid"
                size="lg"
                borderRadius="full"
                px={4}
                py={1}
              >
                {moodPrediction.predicted_mood.toUpperCase()} MOOD
              </Badge>

              <Text
                fontSize="sm"
                color="gray.600"
                textAlign="center"
                maxW="300px"
              >
                {moodConfig.description}
              </Text>
            </VStack>
          </VStack>

          {/* Confidence Indicator */}
          <HStack gap={3} p={3} bg="gray.50" borderRadius="lg" w="100%">
            <Text fontSize="sm" color="gray.700" fontWeight="medium">
              Prediction Confidence:
            </Text>
            <Badge colorScheme="blue" variant="outline">
              {getConfidenceText(moodPrediction.confidence)} (
              {Math.round(moodPrediction.confidence * 100)}%)
            </Badge>
          </HStack>
        </VStack>
      </Box>

      {/* Weather Factors Analysis */}
      <VStack alignItems="stretch" gap={3}>
        <Text fontSize="sm" fontWeight="semibold" color="gray.800">
          🌦️ Weather Impact on Mood
        </Text>

        <Grid templateColumns="repeat(auto-fit, minmax(250px, 1fr))" gap={3}>
          {moodPrediction.factors.map((factor, index) => {
            const impactConfig =
              IMPACT_CONFIG[factor.impact] || IMPACT_CONFIG["neutral"];
            const factorIcon = FACTOR_ICONS[factor.factor] || "📊";

            return (
              <Box
                key={index}
                p={4}
                bg="white"
                borderRadius="lg"
                border="1px solid"
                borderColor={impactConfig.color + ".200"}
                borderLeftWidth="4px"
                borderLeftColor={impactConfig.color + ".400"}
              >
                <VStack alignItems="stretch" gap={3}>
                  {/* Factor Header */}
                  <HStack justify="space-between" align="center">
                    <HStack>
                      <Text fontSize="lg">{factorIcon}</Text>
                      <VStack alignItems="start" gap={0}>
                        <Text
                          fontSize="sm"
                          fontWeight="bold"
                          color="gray.800"
                          textTransform="capitalize"
                        >
                          {factor.factor}
                        </Text>
                        <Text fontSize="xs" color="gray.600">
                          {getWeatherDescription(factor.factor, factor.value)}
                        </Text>
                      </VStack>
                    </HStack>

                    <Badge
                      colorScheme={impactConfig.color}
                      variant="solid"
                      size="sm"
                    >
                      {impactConfig.icon} {factor.impact}
                    </Badge>
                  </HStack>

                  {/* Current Value */}
                  <HStack justify="space-between">
                    <Text fontSize="xs" color="gray.600">
                      Current Value:
                    </Text>
                    <Text fontSize="xs" fontWeight="bold" color="gray.800">
                      {factor.factor === "temperature"
                        ? `${factor.value.toFixed(1)}°C`
                        : factor.factor === "sunlight"
                        ? `${factor.value.toFixed(1)} kWh/m²`
                        : factor.factor === "precipitation"
                        ? `${factor.value.toFixed(1)}mm`
                        : factor.factor === "humidity"
                        ? `${factor.value.toFixed(1)}%`
                        : factor.value.toFixed(1)}
                    </Text>
                  </HStack>

                  {/* Mood Impact Score */}
                  <VStack alignItems="stretch" gap={2}>
                    <HStack justify="space-between">
                      <Text fontSize="xs" color="gray.600">
                        Mood Impact:
                      </Text>
                      <Text
                        fontSize="xs"
                        fontWeight="bold"
                        color={getScoreColor(factor.score) + ".600"}
                      >
                        {factor.score}/100
                      </Text>
                    </HStack>

                    <Progress.Root
                      value={factor.score}
                      colorScheme={getScoreColor(factor.score)}
                      size="sm"
                      borderRadius="full"
                    >
                      <Progress.Track>
                        <Progress.Range />
                      </Progress.Track>
                    </Progress.Root>
                  </VStack>

                  {/* Description */}
                  <Box p={2} bg="gray.50" borderRadius="sm">
                    <Text fontSize="xs" color="gray.600" lineHeight="1.4">
                      {factor.description}
                    </Text>
                  </Box>
                </VStack>
              </Box>
            );
          })}
        </Grid>
      </VStack>

      {/* Mood Improvement Tips */}
      <Box
        p={4}
        bg="white"
        borderRadius="lg"
        border="1px"
        borderColor="purple.200"
      >
        <VStack alignItems="stretch" gap={3}>
          <HStack>
            <Text fontSize="lg">💡</Text>
            <Text fontSize="sm" fontWeight="semibold" color="purple.800">
              Tips to Improve Your Mood Score
            </Text>
          </HStack>

          <VStack alignItems="start" gap={2}>
            {moodPrediction.overall_score < 50 && (
              <Text fontSize="xs" color="purple.600">
                • Consider spending time in well-lit indoor spaces if weather is
                gloomy
              </Text>
            )}

            {moodPrediction.factors.find(
              (f) => f.factor === "sunlight" && f.score < 60
            ) && (
              <Text fontSize="xs" color="purple.600">
                • Try light therapy or sit near bright windows to boost mood
              </Text>
            )}

            {moodPrediction.factors.find(
              (f) => f.factor === "temperature" && f.impact === "negative"
            ) && (
              <Text fontSize="xs" color="purple.600">
                • Dress appropriately for temperature comfort to improve overall
                wellbeing
              </Text>
            )}

            {moodPrediction.factors.find(
              (f) => f.factor === "precipitation" && f.impact === "negative"
            ) && (
              <Text fontSize="xs" color="purple.600">
                • Engage in cozy indoor activities and focus on comfort during
                rainy weather
              </Text>
            )}

            <Text fontSize="xs" color="purple.600">
              • Regular exercise and social connection can help offset
              weather-related mood impacts
            </Text>

            <Text fontSize="xs" color="purple.600">
              • Practice gratitude and mindfulness to build resilience against
              weather changes
            </Text>
          </VStack>
        </VStack>
      </Box>

      {/* Mood Tracking Note */}
      <Box
        p={3}
        bg="blue.50"
        borderRadius="md"
        border="1px"
        borderColor="blue.200"
      >
        <Text fontSize="xs" color="blue.700" fontWeight="medium" mb={1}>
          📊 Understanding Your Mood Score
        </Text>
        <VStack alignItems="start" gap={1}>
          <Text fontSize="xs" color="blue.600">
            • Scores are based on scientifically-backed weather-mood
            correlations
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Individual sensitivity to weather varies - use this as a general
            guide
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Tracking patterns over time can help you prepare for
            weather-sensitive days
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Consider other factors like sleep, nutrition, and stress levels
            too
          </Text>
        </VStack>
      </Box>
    </VStack>
  );
}
