"use client";

import { Box, VStack, HStack, Heading, Text, Button } from "@chakra-ui/react";
import { useState } from "react";
import { useVibeStore } from "../../../stores/useVibeStore";
import { useLocationStore } from "../../../stores/useLocationStore";
import { useTimeStore } from "../../../stores/useTimeStore";
import { advisorService } from "../../../services/advisorService";
import { AdvisorRequest } from "../../../types/api";
import { toaster } from "../../ui/toaster";

// Specialized advisor components
import {
  OutfitCard,
  ColorPalette,
  FabricRecommendations,
} from "./FashionAdvisor";
import { PlantingCalendar, RiskAlerts, ActionableSteps } from "./CropAdvisor";
import {
  ActivitySuggestions,
  WellnessTips,
  MoodScoreDisplay,
} from "./MoodAdvisor";

export default function AdvisorPanel() {
  const { selectedVibe, advisorData, setAdvisorData } = useVibeStore();
  const { center } = useLocationStore();
  const { selectedMonth } = useTimeStore();
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState(0);

  const handleGetAdvice = async () => {
    if (!selectedVibe || selectedVibe.type !== "advisor") {
      toaster.create({
        title: "No advisor selected",
        description: "Please select an AI advisor from the vibe menu",
        type: "warning",
        duration: 3000,
        closable: true,
      });
      return;
    }

    if (!selectedMonth) {
      toaster.create({
        title: "No month selected",
        description: "Please select a month to get recommendations",
        type: "warning",
        duration: 3000,
        closable: true,
      });
      return;
    }

    setIsLoading(true);

    try {
      // Map vibe ID to advisor type
      const advisorTypeMap: Record<string, string> = {
        fashion_stylist: "fashion",
        crop_advisor: "crop",
        mood_predictor: "mood",
      };

      const advisorType = advisorTypeMap[selectedVibe.id];
      if (!advisorType) {
        throw new Error(`Unknown advisor type: ${selectedVibe.id}`);
      }

      const request: AdvisorRequest = {
        advisor_type: advisorType,
        lat: center[1], // center is [lon, lat]
        lon: center[0],
        month: selectedMonth,
      };

      const response = await advisorService.getRecommendations(request);
      setAdvisorData(response);

      toaster.create({
        title: "Recommendations ready!",
        description: `Got ${response.recommendations.length} personalized recommendations`,
        type: "success",
        duration: 5000,
        closable: true,
      });

      console.log("Advisor recommendations:", response);
    } catch (error: unknown) {
      console.error("Error fetching recommendations:", error);
      const description =
        (error as { response?: { data?: { detail?: string } } })?.response?.data
          ?.detail || "Failed to get recommendations. Please try again.";
      toaster.create({
        title: "Error",
        description,
        type: "error",
        duration: 5000,
        closable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const renderSpecializedAdvisorContent = () => {
    if (!advisorData) {
      return (
        <Box p={3} bg="gray.50" borderRadius="md">
          <Text fontSize="sm" color="gray.600">
            Select an advisor and get recommendations to see results here.
          </Text>
        </Box>
      );
    }

    // Show basic recommendations if no raw_data or if raw_data doesn't have specialized content
    if (!advisorData.raw_data || !advisorData.raw_data.outfit_recommendations) {
      return (
        <Box
          p={3}
          bg="gray.50"
          borderRadius="md"
          border="1px"
          borderColor="gray.200"
        >
          <Text fontSize="sm" fontWeight="bold" mb={3} color="gray.700">
            🤖 {advisorData?.metadata.advisor_name} Recommendations
          </Text>
          <VStack gap={3} alignItems="stretch">
            {advisorData?.recommendations.map((rec, index) => (
              <Box
                key={index}
                p={3}
                bg="white"
                borderRadius="md"
                border="1px"
                borderColor="gray.200"
                boxShadow="sm"
              >
                <Box display="flex" alignItems="center" mb={2}>
                  <Text fontSize="lg" mr={2}>
                    {rec.icon}
                  </Text>
                  <Text fontSize="sm" fontWeight="bold" color="gray.800">
                    {rec.item}
                  </Text>
                </Box>
                <Text fontSize="xs" color="gray.600" lineHeight="1.4">
                  {rec.description}
                </Text>
              </Box>
            ))}
          </VStack>
        </Box>
      );
    }

    const rawData = advisorData.raw_data as Record<string, unknown>;

    switch (advisorData.advisor_type) {
      case "fashion":
        return renderFashionAdvisor(rawData);
      case "crop":
        return renderCropAdvisor(rawData);
      case "mood":
        return renderMoodAdvisor(rawData);
      default:
        return (
          <Box p={3} bg="gray.50" borderRadius="md">
            <Text fontSize="sm" color="gray.600">
              Advisor type not yet supported with specialized UI.
            </Text>
          </Box>
        );
    }
  };

  const renderFashionAdvisor = (data: Record<string, unknown>) => {
    return (
      <Box>
        <Text fontSize="lg" fontWeight="bold" mb={4} color="gray.800">
          👗 {advisorData?.metadata.advisor_name} Recommendations
        </Text>

        <HStack gap={2} mb={4}>
          <Button
            size="sm"
            variant={activeTab === 0 ? "solid" : "outline"}
            colorScheme="brand"
            onClick={() => setActiveTab(0)}
          >
            👔 Outfits
          </Button>
          <Button
            size="sm"
            variant={activeTab === 1 ? "solid" : "outline"}
            colorScheme="brand"
            onClick={() => setActiveTab(1)}
          >
            🎨 Colors
          </Button>
          <Button
            size="sm"
            variant={activeTab === 2 ? "solid" : "outline"}
            colorScheme="brand"
            onClick={() => setActiveTab(2)}
          >
            🧵 Fabrics
          </Button>
        </HStack>

        <Box mt={4}>
          {activeTab === 0 && data.outfit_recommendations ? (
            <VStack gap={4} alignItems="stretch">
              {/* eslint-disable-next-line @typescript-eslint/no-explicit-any */}
              {(data.outfit_recommendations as any[]).map(
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                (outfit: any, index: number) => (
                  <OutfitCard
                    key={index}
                    outfit={outfit}
                    isExpanded={index === 0}
                  />
                )
              )}
            </VStack>
          ) : null}

          {activeTab === 1 && data.color_suggestions ? (
            <ColorPalette
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              colorSuggestions={data.color_suggestions as any}
            />
          ) : null}

          {activeTab === 2 && data.fabric_recommendations ? (
            <FabricRecommendations
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              fabricRecommendations={data.fabric_recommendations as any}
            />
          ) : null}
        </Box>
      </Box>
    );
  };

  const renderCropAdvisor = (data: Record<string, unknown>) => {
    return (
      <Box>
        <Text fontSize="lg" fontWeight="bold" mb={4} color="gray.800">
          🌱 {advisorData?.metadata.advisor_name} Recommendations
        </Text>

        <HStack gap={2} mb={4}>
          <Button
            size="sm"
            variant={activeTab === 0 ? "solid" : "outline"}
            colorScheme="green"
            onClick={() => setActiveTab(0)}
          >
            📅 Calendar
          </Button>
          <Button
            size="sm"
            variant={activeTab === 1 ? "solid" : "outline"}
            colorScheme="green"
            onClick={() => setActiveTab(1)}
          >
            ⚠️ Risks
          </Button>
          <Button
            size="sm"
            variant={activeTab === 2 ? "solid" : "outline"}
            colorScheme="green"
            onClick={() => setActiveTab(2)}
          >
            ✅ Actions
          </Button>
        </HStack>

        <Box mt={4}>
          {activeTab === 0 && data.planting_window ? (
            <PlantingCalendar
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              plantingWindow={data.planting_window as any}
              cropType={(data.crop_type as string) || "crop"}
              currentMonth={selectedMonth || new Date().getMonth() + 1}
            />
          ) : null}

          {activeTab === 1 && data.risk_assessment && data.alerts ? (
            <RiskAlerts
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              riskAssessment={data.risk_assessment as any}
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              alerts={data.alerts as any}
            />
          ) : null}

          {activeTab === 2 && data.recommendations ? (
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            <ActionableSteps recommendations={data.recommendations as any} />
          ) : null}
        </Box>
      </Box>
    );
  };

  const renderMoodAdvisor = (data: Record<string, unknown>) => {
    return (
      <Box>
        <Text fontSize="lg" fontWeight="bold" mb={4} color="gray.800">
          🧠 {advisorData?.metadata.advisor_name} Recommendations
        </Text>

        <HStack gap={2} mb={4}>
          <Button
            size="sm"
            variant={activeTab === 0 ? "solid" : "outline"}
            colorScheme="purple"
            onClick={() => setActiveTab(0)}
          >
            📊 Mood Score
          </Button>
          <Button
            size="sm"
            variant={activeTab === 1 ? "solid" : "outline"}
            colorScheme="purple"
            onClick={() => setActiveTab(1)}
          >
            🎯 Activities
          </Button>
          <Button
            size="sm"
            variant={activeTab === 2 ? "solid" : "outline"}
            colorScheme="purple"
            onClick={() => setActiveTab(2)}
          >
            🌟 Wellness
          </Button>
        </HStack>

        <Box mt={4}>
          {activeTab === 0 && data.mood_prediction ? (
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            <MoodScoreDisplay moodPrediction={data.mood_prediction as any} />
          ) : null}

          {activeTab === 1 && data.activity_suggestions ? (
            <ActivitySuggestions
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              activities={data.activity_suggestions as any}
              energyLevel={
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                (data.wellness_recommendations as any)?.energy_level ||
                "moderate"
              }
              socialRecommendations={
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                (data.wellness_recommendations as any)
                  ?.social_recommendations || []
              }
            />
          ) : null}

          {activeTab === 2 &&
          data.wellness_recommendations &&
          data.daily_tips ? (
            <WellnessTips
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              wellnessRecommendations={data.wellness_recommendations as any}
              // eslint-disable-next-line @typescript-eslint/no-explicit-any
              dailyTips={data.daily_tips as any}
            />
          ) : null}
        </Box>
      </Box>
    );
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
      w={advisorData ? "800px" : "300px"}
      zIndex={1000}
      maxH="80vh"
      overflowY="auto"
      transition="width 0.3s ease"
    >
      <VStack gap={4} alignItems="stretch">
        <Heading size="md" color="gray.500">
          🤖 AI Advisors
        </Heading>
        <Text fontSize="sm" color="gray.600">
          Get personalized recommendations based on weather conditions
        </Text>
        <Box bg="gray.50" p={3} borderRadius="md">
          <Text fontSize="xs" fontWeight="medium" color="gray.600" mb={1}>
            Current Location
          </Text>
          <Text fontSize="sm" color="gray.700">
            {center[1].toFixed(4)}°N, {center[0].toFixed(4)}°E
          </Text>
        </Box>
        {selectedVibe?.type === "advisor" && (
          <Box bg="brand.50" p={3} borderRadius="md">
            <Text fontSize="sm" fontWeight="medium" color="gray.700">
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
        {/* Detailed Recommendations Display */}
        {advisorData && <Box mt={4}>{renderSpecializedAdvisorContent()}</Box>}s
      </VStack>
    </Box>
  );
}
