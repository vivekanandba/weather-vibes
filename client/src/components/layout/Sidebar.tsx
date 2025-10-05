"use client";

import {
  Box,
  VStack,
  Text,
  Button,
  Separator,
} from "@chakra-ui/react";
import { TooltipRoot, TooltipTrigger, TooltipContent } from "@chakra-ui/react";
import { useUIStore } from "../../stores/useUIStore";
import { useVibeStore } from "../../stores/useVibeStore";
import VibeSelector from "@/components/vibe/VibeSelector";

export default function Sidebar() {
  const { isSidebarOpen } = useUIStore();
  const { selectedVibe, activeFeature, setActiveFeature } = useVibeStore();

  if (!isSidebarOpen) return null;

  return (
    <Box
      as="aside"
      w="320px"
      flexShrink={0}
      bg="white"
      borderRight="1px"
      borderColor="gray.200"
      p={4}
      overflowY="auto"
      h="100%"
    >
      <VStack gap={4} alignItems="stretch">
        <Box>
          <Text fontSize="sm" fontWeight="bold" mb={2} color="gray.600">
            SELECT A VIBE
          </Text>
          <VibeSelector />
        </Box>

        <Separator />

        <Box>
          <Text fontSize="sm" fontWeight="bold" mb={2} color="gray.600">
            FEATURES
          </Text>
          <VStack gap={2}>
            <TooltipRoot>
              <TooltipTrigger asChild>
                <Button
                  width="full"
                  variant={activeFeature === "where" ? "solid" : "outline"}
                  colorPalette="brand"
                  disabled={selectedVibe?.type === "advisor"}
                  onClick={() => {
                    if (selectedVibe?.type === "advisor") {
                      setActiveFeature("advisor");
                    } else {
                      setActiveFeature(activeFeature === "where" ? null : "where");
                    }
                  }}
                >
                  📍 Where
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                {selectedVibe?.type === "advisor" ? "Use Advisors feature for AI advisors" : "Find best locations for this vibe"}
              </TooltipContent>
            </TooltipRoot>
            <TooltipRoot>
              <TooltipTrigger asChild>
                <Button
                  width="full"
                  variant={activeFeature === "when" ? "solid" : "outline"}
                  colorPalette="brand"
                  disabled={selectedVibe?.type === "advisor"}
                  onClick={() => {
                    if (selectedVibe?.type === "advisor") {
                      setActiveFeature("advisor");
                    } else {
                      setActiveFeature(activeFeature === "when" ? null : "when");
                    }
                  }}
                >
                  📅 When
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                {selectedVibe?.type === "advisor" ? "Use Advisors feature for AI advisors" : "Find best times for this vibe"}
              </TooltipContent>
            </TooltipRoot>
            <TooltipRoot>
              <TooltipTrigger asChild>
                <Button
                  width="full"
                  variant={activeFeature === "advisor" ? "solid" : "outline"}
                  colorPalette="brand"
                  disabled={selectedVibe?.type !== "advisor"}
                  onClick={() =>
                    setActiveFeature(activeFeature === "advisor" ? null : "advisor")
                  }
                >
                  🤖 Advisors
                </Button>
              </TooltipTrigger>
              <TooltipContent>
                {selectedVibe?.type !== "advisor" ? "Select an AI advisor to use this feature" : "Get personalized recommendations"}
              </TooltipContent>
            </TooltipRoot>
          </VStack>
        </Box>

        <Separator />

        <Box>
          <Text fontSize="xs" color="gray.500">
            Powered by NASA POWER API
          </Text>
        </Box>
      </VStack>
    </Box>
  );
}
