"use client";

import {
  Box,
  VStack,
  HStack,
  Text,
  Badge,
  Button,
  Checkbox,
  Progress,
} from "@chakra-ui/react";
import { useState } from "react";

interface ActionableRecommendation {
  category: string;
  priority: string;
  title: string;
  description: string;
  action: string;
  timeline: string;
}

interface ActionableStepsProps {
  recommendations: ActionableRecommendation[];
  onStepComplete?: (stepIndex: number) => void;
}

const CATEGORY_CONFIG: Record<
  string,
  {
    color: string;
    icon: string;
    bgColor: string;
  }
> = {
  planting: {
    color: "green",
    icon: "🌱",
    bgColor: "green.50",
  },
  temperature: {
    color: "orange",
    icon: "🌡️",
    bgColor: "orange.50",
  },
  irrigation: {
    color: "blue",
    icon: "💧",
    bgColor: "blue.50",
  },
  drainage: {
    color: "purple",
    icon: "🏞️",
    bgColor: "purple.50",
  },
  fertilization: {
    color: "yellow",
    icon: "🌾",
    bgColor: "yellow.50",
  },
  pest_control: {
    color: "red",
    icon: "🐛",
    bgColor: "red.50",
  },
  harvesting: {
    color: "teal",
    icon: "🌾",
    bgColor: "teal.50",
  },
  soil: {
    color: "brown",
    icon: "🌍",
    bgColor: "yellow.50",
  },
  protection: {
    color: "gray",
    icon: "🛡️",
    bgColor: "gray.50",
  },
};

const PRIORITY_CONFIG: Record<
  string,
  {
    color: string;
    icon: string;
    weight: number;
  }
> = {
  high: { color: "red", icon: "🔥", weight: 3 },
  medium: { color: "yellow", icon: "⭐", weight: 2 },
  low: { color: "blue", icon: "💡", weight: 1 },
};

const TIMELINE_CONFIG: Record<
  string,
  {
    color: string;
    icon: string;
  }
> = {
  immediate: { color: "red", icon: "⚡" },
  "within 1-2 weeks": { color: "orange", icon: "📅" },
  weekly: { color: "blue", icon: "🗓️" },
  monthly: { color: "green", icon: "📊" },
  seasonal: { color: "purple", icon: "🌸" },
};

export default function ActionableSteps({
  recommendations,
  onStepComplete,
}: ActionableStepsProps) {
  const [completedSteps, setCompletedSteps] = useState<Set<number>>(new Set());
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set());

  // Sort recommendations by priority and timeline urgency
  const sortedRecommendations = [...recommendations].sort((a, b) => {
    const priorityA = PRIORITY_CONFIG[a.priority]?.weight || 0;
    const priorityB = PRIORITY_CONFIG[b.priority]?.weight || 0;

    if (priorityA !== priorityB) {
      return priorityB - priorityA; // Higher priority first
    }

    // Then by timeline urgency
    const timelineUrgency: Record<string, number> = {
      immediate: 5,
      "within 1-2 weeks": 4,
      weekly: 3,
      monthly: 2,
      seasonal: 1,
    };

    return (
      (timelineUrgency[b.timeline] || 0) - (timelineUrgency[a.timeline] || 0)
    );
  });

  const handleStepToggle = (index: number) => {
    const newCompleted = new Set(completedSteps);
    if (completedSteps.has(index)) {
      newCompleted.delete(index);
    } else {
      newCompleted.add(index);
      onStepComplete?.(index);
    }
    setCompletedSteps(newCompleted);
  };

  const handleStepExpand = (index: number) => {
    const newExpanded = new Set(expandedSteps);
    if (expandedSteps.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedSteps(newExpanded);
  };

  const completedCount = completedSteps.size;
  const totalCount = recommendations.length;
  const progressPercentage =
    totalCount > 0 ? (completedCount / totalCount) * 100 : 0;

  const getTimelineConfig = (timeline: string) => {
    // Find matching timeline config by checking if timeline contains key
    for (const [key, config] of Object.entries(TIMELINE_CONFIG)) {
      if (
        timeline.toLowerCase().includes(key.toLowerCase()) ||
        key === timeline
      ) {
        return config;
      }
    }
    return TIMELINE_CONFIG["weekly"]; // Default fallback
  };

  return (
    <VStack gap={4} alignItems="stretch" p={4} bg="blue.50" borderRadius="lg">
      {/* Header with Progress */}
      <VStack alignItems="stretch" gap={3}>
        <HStack justify="space-between" align="center">
          <Text fontSize="sm" fontWeight="semibold" color="blue.800">
            ✅ Action Plan & Steps
          </Text>

          <Badge colorScheme="blue" variant="solid">
            {completedCount}/{totalCount} completed
          </Badge>
        </HStack>

        {/* Progress Bar */}
        <VStack alignItems="stretch" gap={2}>
          <HStack justify="space-between">
            <Text fontSize="xs" color="blue.600">
              Overall Progress
            </Text>
            <Text fontSize="xs" color="blue.600">
              {Math.round(progressPercentage)}%
            </Text>
          </HStack>

          <Progress.Root
            value={progressPercentage}
            colorScheme="blue"
            size="md"
            borderRadius="full"
            bg="blue.100"
          >
            <Progress.Track>
              <Progress.Range />
            </Progress.Track>
          </Progress.Root>
        </VStack>
      </VStack>

      {/* Action Steps List */}
      <VStack gap={3} alignItems="stretch">
        {sortedRecommendations.map((rec, index) => {
          const categoryConfig =
            CATEGORY_CONFIG[rec.category] || CATEGORY_CONFIG["planting"];
          const priorityConfig =
            PRIORITY_CONFIG[rec.priority] || PRIORITY_CONFIG["medium"];
          const timelineConfig = getTimelineConfig(rec.timeline);
          const isCompleted = completedSteps.has(index);
          const isExpanded = expandedSteps.has(index);

          return (
            <Box
              key={index}
              p={4}
              bg="white"
              borderRadius="lg"
              border="1px solid"
              borderColor={
                isCompleted ? "green.300" : categoryConfig.color + ".200"
              }
              borderLeftWidth="4px"
              borderLeftColor={categoryConfig.color + ".400"}
              opacity={isCompleted ? 0.7 : 1}
              transition="all 0.2s"
            >
              <VStack alignItems="stretch" gap={3}>
                {/* Step Header */}
                <HStack justify="space-between" align="start">
                  <HStack gap={3} flex={1}>
                    {/* Completion Checkbox */}
                    <Checkbox.Root
                      checked={isCompleted}
                      onChange={() => handleStepToggle(index)}
                      colorScheme="green"
                      size="lg"
                    >
                      <Checkbox.Control />
                    </Checkbox.Root>

                    {/* Step Info */}
                    <VStack alignItems="start" gap={1} flex={1}>
                      <HStack flexWrap="wrap" gap={2}>
                        <Text fontSize="lg">{categoryConfig.icon}</Text>
                        <Text
                          fontSize="sm"
                          fontWeight="bold"
                          color="gray.800"
                          textDecoration={isCompleted ? "line-through" : "none"}
                        >
                          {rec.title}
                        </Text>

                        <Badge
                          size="sm"
                          colorScheme={categoryConfig.color}
                          variant="subtle"
                        >
                          {rec.category.replace(/_/g, " ")}
                        </Badge>
                      </HStack>

                      <Text fontSize="xs" color="gray.600">
                        {rec.description}
                      </Text>
                    </VStack>
                  </HStack>

                  {/* Priority & Timeline Badges */}
                  <VStack gap={1} align="end" minWidth="80px">
                    <Badge
                      size="sm"
                      colorScheme={priorityConfig.color}
                      variant="solid"
                    >
                      {priorityConfig.icon} {rec.priority}
                    </Badge>

                    <Badge
                      size="sm"
                      colorScheme={timelineConfig.color}
                      variant="outline"
                    >
                      {timelineConfig.icon} {rec.timeline}
                    </Badge>
                  </VStack>
                </HStack>

                {/* Expandable Action Details */}
                <HStack justify="space-between" align="center">
                  <Button
                    size="xs"
                    variant="ghost"
                    colorScheme="blue"
                    onClick={() => handleStepExpand(index)}
                  >
                    {isExpanded ? "▼ Hide Details" : "▶ Show Action Details"}
                  </Button>
                </HStack>

                {isExpanded && (
                  <Box
                    p={3}
                    bg={categoryConfig.bgColor}
                    borderRadius="md"
                    border="1px"
                    borderColor={categoryConfig.color + ".200"}
                  >
                    <VStack alignItems="stretch" gap={2}>
                      <Text fontSize="xs" fontWeight="medium" color="gray.700">
                        🎯 Detailed Action Plan:
                      </Text>
                      <Text fontSize="xs" color="gray.600" lineHeight="1.5">
                        {rec.action}
                      </Text>

                      {/* Action Checklist (could be expanded in real implementation) */}
                      <Box
                        mt={2}
                        pt={2}
                        borderTop="1px solid"
                        borderColor="gray.200"
                      >
                        <Text
                          fontSize="xs"
                          fontWeight="medium"
                          color="gray.700"
                          mb={1}
                        >
                          📋 Steps to Complete:
                        </Text>
                        <VStack alignItems="start" gap={1}>
                          <Text fontSize="xs" color="gray.600">
                            • Follow the action plan above
                          </Text>
                          <Text fontSize="xs" color="gray.600">
                            • Monitor results and adjust as needed
                          </Text>
                          <Text fontSize="xs" color="gray.600">
                            • Mark as complete when finished
                          </Text>
                        </VStack>
                      </Box>
                    </VStack>
                  </Box>
                )}
              </VStack>
            </Box>
          );
        })}
      </VStack>

      {/* Summary Stats */}
      <Box
        p={3}
        bg="white"
        borderRadius="md"
        border="1px"
        borderColor="blue.200"
      >
        <HStack justify="space-around" gap={4}>
          <VStack gap={1}>
            <Text fontSize="xs" color="blue.600" fontWeight="medium">
              High Priority
            </Text>
            <Text fontSize="sm" fontWeight="bold" color="red.600">
              {recommendations.filter((r) => r.priority === "high").length}
            </Text>
          </VStack>

          <VStack gap={1}>
            <Text fontSize="xs" color="blue.600" fontWeight="medium">
              Medium Priority
            </Text>
            <Text fontSize="sm" fontWeight="bold" color="yellow.600">
              {recommendations.filter((r) => r.priority === "medium").length}
            </Text>
          </VStack>

          <VStack gap={1}>
            <Text fontSize="xs" color="blue.600" fontWeight="medium">
              Low Priority
            </Text>
            <Text fontSize="sm" fontWeight="bold" color="blue.600">
              {recommendations.filter((r) => r.priority === "low").length}
            </Text>
          </VStack>

          <VStack gap={1}>
            <Text fontSize="xs" color="blue.600" fontWeight="medium">
              Completed
            </Text>
            <Text fontSize="sm" fontWeight="bold" color="green.600">
              {completedCount}
            </Text>
          </VStack>
        </HStack>
      </Box>

      {/* Tips */}
      <Box
        p={3}
        bg="yellow.50"
        borderRadius="md"
        border="1px"
        borderColor="yellow.200"
      >
        <Text fontSize="xs" color="yellow.700" fontWeight="medium" mb={1}>
          💡 Action Tips
        </Text>
        <VStack alignItems="start" gap={1}>
          <Text fontSize="xs" color="yellow.600">
            • Focus on high-priority actions first, especially immediate
            timeline items
          </Text>
          <Text fontSize="xs" color="yellow.600">
            • Check weather updates before implementing outdoor actions
          </Text>
          <Text fontSize="xs" color="yellow.600">
            • Document results to improve future farming decisions
          </Text>
          <Text fontSize="xs" color="yellow.600">
            • Consult local agricultural experts for complex issues
          </Text>
        </VStack>
      </Box>
    </VStack>
  );
}
