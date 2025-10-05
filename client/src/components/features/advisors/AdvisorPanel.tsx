"use client";

import { Box, VStack, Heading, Text, Button } from "@chakra-ui/react";
import { useState } from "react";
import { useVibeStore } from "../../../stores/useVibeStore";
import { useLocationStore } from "../../../stores/useLocationStore";

export default function AdvisorPanel() {
  const { selectedVibe } = useVibeStore();
  const { center } = useLocationStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleGetAdvice = async () => {
    if (!selectedVibe || selectedVibe.type !== "advisor") {
      alert("Please select an AI advisor from the vibe menu");
      return;
    }

    setIsLoading(true);
    // TODO: Call advisorService.getRecommendations() with API integration
    console.log(
      "Feature in progress: This will show AI-powered recommendations"
    );
    setIsLoading(false);
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
      zIndex={10}
      maxH="80vh"
      overflowY="auto"
    >
      <VStack gap={4} alignItems="stretch">
        <Heading size="md">🤖 AI Advisors</Heading>
        <Text fontSize="sm" color="gray.600">
          Get personalized recommendations based on weather conditions
        </Text>

        <Box bg="gray.50" p={3} borderRadius="md">
          <Text fontSize="xs" fontWeight="medium" color="gray.600" mb={1}>
            Current Location
          </Text>
          <Text fontSize="sm">
            {center[1].toFixed(4)}°N, {center[0].toFixed(4)}°E
          </Text>
        </Box>

        {selectedVibe?.type === "advisor" && (
          <Box bg="brand.50" p={3} borderRadius="md">
            <Text fontSize="sm" fontWeight="medium">
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
          disabled={!selectedVibe || selectedVibe.type !== "advisor"}
        >
          Get Recommendations
        </Button>

        <Text fontSize="xs" color="gray.500">
          AI advisors provide context-aware suggestions
        </Text>

        {/* TODO: Render recommendations here after API integration */}
      </VStack>
    </Box>
  );
}
