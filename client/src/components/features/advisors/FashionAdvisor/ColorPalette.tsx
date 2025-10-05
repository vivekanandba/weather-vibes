"use client";

import { Box, VStack, HStack, Text } from "@chakra-ui/react";

interface ColorSuggestions {
  primary: string[];
  accent: string[];
  avoid: string[];
}

interface ColorPaletteProps {
  colorSuggestions: ColorSuggestions;
}

const COLOR_MAP: Record<string, string> = {
  // Neutrals
  navy: "#1e3a8a",
  black: "#000000",
  charcoal: "#374151",
  gray: "#6b7280",
  white: "#ffffff",
  cream: "#fef3c7",
  beige: "#d6d3d1",

  // Warm colors
  burgundy: "#991b1b",
  brown: "#92400e",
  camel: "#d2691e",
  coral: "#f87171",
  yellow: "#fbbf24",

  // Cool colors
  forest_green: "#065f46",
  sage_green: "#84cc16",
  mint_green: "#6ee7b7",
  light_blue: "#7dd3fc",
  khaki: "#a3a3a3",

  // Pastels
  pastels: "#fecaca",
  olive: "#65a30d",

  // Patterns/Textures
  waterproof_fabrics: "#1f2937",
  dark_colors: "#374151",
  light_colors: "#f9fafb",
};

export default function ColorPalette({ colorSuggestions }: ColorPaletteProps) {
  const renderColorSwatch = (colorName: string, isPrimary: boolean = true) => {
    const colorValue = COLOR_MAP[colorName] || "#9ca3af";
    const isLightColor = ["white", "cream", "light_colors", "pastels"].includes(
      colorName
    );

    return (
      <Box
        key={colorName}
        w="40px"
        h="40px"
        bg={colorValue}
        borderRadius="md"
        border={isLightColor ? "1px solid" : "none"}
        borderColor="gray.300"
        cursor="pointer"
        position="relative"
        _hover={{ transform: "scale(1.1)", boxShadow: "lg" }}
        transition="all 0.2s"
        title={colorName
          .replace(/_/g, " ")
          .replace(/\b\w/g, (l) => l.toUpperCase())}
      >
        {/* Priority indicator */}
        {isPrimary && (
          <Box
            position="absolute"
            top="-2px"
            right="-2px"
            w="12px"
            h="12px"
            bg="gold"
            borderRadius="full"
            border="2px solid white"
            fontSize="8px"
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            ⭐
          </Box>
        )}
      </Box>
    );
  };

  return (
    <VStack gap={4} alignItems="stretch" p={4} bg="gray.50" borderRadius="lg">
      <Text fontSize="sm" fontWeight="semibold" color="gray.700">
        🎨 Recommended Color Palette
      </Text>

      {/* Primary Colors */}
      {colorSuggestions.primary.length > 0 && (
        <VStack alignItems="stretch" gap={2}>
          <Text fontSize="xs" color="gray.600" fontWeight="medium">
            PRIMARY COLORS (Best matches)
          </Text>
          <HStack gap={2} flexWrap="wrap">
            {colorSuggestions.primary.map((color) =>
              renderColorSwatch(color, true)
            )}
          </HStack>
        </VStack>
      )}

      {/* Accent Colors */}
      {colorSuggestions.accent.length > 0 && (
        <VStack alignItems="stretch" gap={2}>
          <Text fontSize="xs" color="gray.600" fontWeight="medium">
            ACCENT COLORS (Complementary)
          </Text>
          <HStack gap={2} flexWrap="wrap">
            {colorSuggestions.accent.map((color) =>
              renderColorSwatch(color, false)
            )}
          </HStack>
        </VStack>
      )}

      {/* Colors to Avoid */}
      {colorSuggestions.avoid.length > 0 && (
        <VStack alignItems="stretch" gap={2}>
          <Text fontSize="xs" color="red.600" fontWeight="medium">
            ⚠️ AVOID THESE COLORS (Weather inappropriate)
          </Text>
          <HStack gap={2} flexWrap="wrap">
            {colorSuggestions.avoid.map((color) => (
              <Box
                key={color}
                w="40px"
                h="40px"
                bg={COLOR_MAP[color] || "#9ca3af"}
                borderRadius="md"
                position="relative"
                opacity="0.6"
                _hover={{ opacity: "0.8" }}
                transition="opacity 0.2s"
                title={`${color.replace(
                  /_/g,
                  " "
                )} - Not recommended for current weather`}
              >
                {/* X mark overlay */}
                <Box
                  position="absolute"
                  top="50%"
                  left="50%"
                  transform="translate(-50%, -50%)"
                  fontSize="16px"
                  color="red.500"
                  fontWeight="bold"
                >
                  ✕
                </Box>
              </Box>
            ))}
          </HStack>
        </VStack>
      )}

      {/* Color Theory Tips */}
      <Box
        p={3}
        bg="blue.50"
        borderRadius="md"
        border="1px"
        borderColor="blue.200"
      >
        <Text fontSize="xs" color="blue.700" fontWeight="medium" mb={1}>
          💡 Color Styling Tips
        </Text>
        <VStack alignItems="start" gap={1}>
          <Text fontSize="xs" color="blue.600">
            • Primary colors work best for main garments (shirts, pants)
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Use accent colors for accessories and details
          </Text>
          <Text fontSize="xs" color="blue.600">
            • Avoid listed colors as they may show weather stains or retain heat
          </Text>
        </VStack>
      </Box>
    </VStack>
  );
}
