"use client";

import { Box, VStack, HStack, Text, Badge, Progress } from "@chakra-ui/react";

interface Risk {
  type: string;
  level: string;
  probability: number;
  message: string;
}

interface RiskAssessment {
  overall: string;
  factors: Risk[];
  risk_summary: string;
}

interface AlertItem {
  type: string;
  message: string;
  action: string;
  urgency: string;
}

interface RiskAlertsProps {
  riskAssessment: RiskAssessment;
  alerts: AlertItem[];
}

const RISK_LEVEL_CONFIG: Record<
  string,
  {
    color: string;
    icon: string;
    bgColor: string;
    borderColor: string;
  }
> = {
  low: {
    color: "green",
    icon: "✅",
    bgColor: "green.50",
    borderColor: "green.200",
  },
  medium: {
    color: "yellow",
    icon: "⚠️",
    bgColor: "yellow.50",
    borderColor: "yellow.200",
  },
  high: {
    color: "red",
    icon: "🚨",
    bgColor: "red.50",
    borderColor: "red.200",
  },
};

const RISK_TYPE_ICONS: Record<string, string> = {
  frost: "🧊",
  heat_stress: "🌡️",
  drought: "🏜️",
  excessive_rain: "🌊",
  pest: "🐛",
  disease: "🦠",
  wind: "💨",
  hail: "🧊",
};

const URGENCY_CONFIG: Record<
  string,
  {
    color: string;
    icon: string;
  }
> = {
  immediate: { color: "red", icon: "🚨" },
  high: { color: "orange", icon: "⚡" },
  medium: { color: "yellow", icon: "⚠️" },
  low: { color: "blue", icon: "💡" },
};

export default function RiskAlerts({
  riskAssessment,
  alerts,
}: RiskAlertsProps) {
  const overallRiskConfig =
    RISK_LEVEL_CONFIG[riskAssessment.overall] || RISK_LEVEL_CONFIG["medium"];

  const getProbabilityText = (probability: number) => {
    if (probability >= 0.8) return "Very High";
    if (probability >= 0.6) return "High";
    if (probability >= 0.4) return "Medium";
    if (probability >= 0.2) return "Low";
    return "Very Low";
  };

  const sortedAlerts = alerts.sort((a, b) => {
    const urgencyOrder = { immediate: 4, high: 3, medium: 2, low: 1 };
    return (
      (urgencyOrder[b.urgency as keyof typeof urgencyOrder] || 0) -
      (urgencyOrder[a.urgency as keyof typeof urgencyOrder] || 0)
    );
  });

  return (
    <VStack gap={4} alignItems="stretch" p={4} bg="red.50" borderRadius="lg">
      {/* Overall Risk Assessment */}
      <Box
        p={4}
        bg={overallRiskConfig.bgColor}
        borderRadius="lg"
        border="2px solid"
        borderColor={overallRiskConfig.borderColor}
      >
        <VStack alignItems="stretch" gap={3}>
          <HStack justify="space-between" align="center">
            <HStack>
              <Text fontSize="xl">{overallRiskConfig.icon}</Text>
              <VStack alignItems="start" gap={0}>
                <Text fontSize="sm" fontWeight="bold" color="gray.800">
                  Overall Risk Assessment
                </Text>
                <Text fontSize="xs" color="gray.600">
                  Current farming conditions
                </Text>
              </VStack>
            </HStack>

            <Badge
              size="lg"
              colorScheme={overallRiskConfig.color}
              variant="solid"
              borderRadius="full"
              px={3}
              py={1}
            >
              {riskAssessment.overall.toUpperCase()} RISK
            </Badge>
          </HStack>

          <Text fontSize="sm" color="gray.700">
            {riskAssessment.risk_summary}
          </Text>
        </VStack>
      </Box>

      {/* Individual Risk Factors */}
      {riskAssessment.factors.length > 0 && (
        <VStack alignItems="stretch" gap={3}>
          <Text fontSize="sm" fontWeight="semibold" color="gray.700">
            🔍 Risk Factors Analysis
          </Text>

          {riskAssessment.factors.map((risk, index) => {
            const riskConfig =
              RISK_LEVEL_CONFIG[risk.level] || RISK_LEVEL_CONFIG["medium"];
            const riskIcon = RISK_TYPE_ICONS[risk.type] || "⚠️";

            return (
              <Box
                key={index}
                p={3}
                bg="white"
                borderRadius="md"
                border="1px solid"
                borderColor={riskConfig.borderColor}
                borderLeftWidth="4px"
                borderLeftColor={`${riskConfig.color}.400`}
              >
                <VStack alignItems="stretch" gap={2}>
                  <HStack justify="space-between" align="center">
                    <HStack>
                      <Text fontSize="lg">{riskIcon}</Text>
                      <VStack alignItems="start" gap={0}>
                        <Text
                          fontSize="sm"
                          fontWeight="medium"
                          color="gray.800"
                          textTransform="capitalize"
                        >
                          {risk.type.replace(/_/g, " ")}
                        </Text>
                        <Badge
                          size="sm"
                          colorScheme={riskConfig.color}
                          variant="subtle"
                        >
                          {risk.level} risk
                        </Badge>
                      </VStack>
                    </HStack>
                  </HStack>

                  <Text fontSize="xs" color="gray.600">
                    {risk.message}
                  </Text>

                  {/* Probability Bar */}
                  <VStack alignItems="stretch" gap={1}>
                    <HStack justify="space-between">
                      <Text fontSize="xs" color="gray.600">
                        Probability: {getProbabilityText(risk.probability)}
                      </Text>
                      <Text fontSize="xs" color="gray.600">
                        {Math.round(risk.probability * 100)}%
                      </Text>
                    </HStack>

                    <Progress.Root
                      value={risk.probability * 100}
                      colorScheme={riskConfig.color}
                      size="sm"
                      borderRadius="full"
                    >
                      <Progress.Track>
                        <Progress.Range />
                      </Progress.Track>
                    </Progress.Root>
                  </VStack>
                </VStack>
              </Box>
            );
          })}
        </VStack>
      )}

      {/* Immediate Alerts */}
      {sortedAlerts.length > 0 && (
        <VStack alignItems="stretch" gap={3}>
          <Text fontSize="sm" fontWeight="semibold" color="red.700">
            🚨 Active Alerts & Actions Required
          </Text>

          {sortedAlerts.map((alert, index) => {
            const urgencyConfig =
              URGENCY_CONFIG[alert.urgency] || URGENCY_CONFIG["medium"];

            return (
              <Box
                key={index}
                p={4}
                bg={`${urgencyConfig.color}.50`}
                borderRadius="lg"
                border="1px solid"
                borderColor={`${urgencyConfig.color}.200`}
                borderLeftWidth="4px"
                borderLeftColor={`${urgencyConfig.color}.400`}
              >
                <VStack alignItems="stretch" gap={2}>
                  <HStack justify="space-between" align="start">
                    <VStack alignItems="start" gap={1} flex={1}>
                      <HStack>
                        <Text fontSize="lg">{urgencyConfig.icon}</Text>
                        <Text fontSize="sm" fontWeight="bold">
                          {alert.message}
                        </Text>
                        <Badge
                          size="sm"
                          colorScheme={urgencyConfig.color}
                          variant="solid"
                        >
                          {alert.urgency}
                        </Badge>
                      </HStack>

                      <Box p={2} bg="gray.100" borderRadius="md" w="100%">
                        <Text
                          fontSize="xs"
                          fontWeight="medium"
                          color="gray.700"
                          mb={1}
                        >
                          🎯 Recommended Action:
                        </Text>
                        <Text fontSize="xs" color="gray.600">
                          {alert.action}
                        </Text>
                      </Box>
                    </VStack>
                  </HStack>
                </VStack>
              </Box>
            );
          })}
        </VStack>
      )}

      {/* No Alerts Message */}
      {alerts.length === 0 && riskAssessment.overall === "low" && (
        <Box
          p={4}
          bg="green.100"
          borderRadius="md"
          border="1px"
          borderColor="green.300"
        >
          <HStack>
            <Text fontSize="lg">✅</Text>
            <VStack alignItems="start" gap={1}>
              <Text fontSize="sm" fontWeight="medium" color="green.800">
                No Active Alerts
              </Text>
              <Text fontSize="xs" color="green.600">
                Current conditions are favorable for your crops. Continue with
                regular farming practices.
              </Text>
            </VStack>
          </HStack>
        </Box>
      )}

      {/* Risk Monitoring Tips */}
      <Box
        p={3}
        bg="purple.50"
        borderRadius="md"
        border="1px"
        borderColor="purple.200"
      >
        <Text fontSize="xs" color="purple.700" fontWeight="medium" mb={2}>
          📊 Risk Monitoring Tips
        </Text>
        <VStack alignItems="start" gap={1}>
          <Text fontSize="xs" color="purple.600">
            • Check weather updates regularly during high-risk periods
          </Text>
          <Text fontSize="xs" color="purple.600">
            • Have emergency supplies ready (covers, irrigation, drainage tools)
          </Text>
          <Text fontSize="xs" color="purple.600">
            • Monitor plants closely for early signs of stress or disease
          </Text>
          <Text fontSize="xs" color="purple.600">
            • Consider crop insurance for high-risk periods
          </Text>
        </VStack>
      </Box>
    </VStack>
  );
}
