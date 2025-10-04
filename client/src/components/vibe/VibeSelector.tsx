'use client';

import {
  Box,
  Text,
  HStack,
} from '@chakra-ui/react';
import {
  MenuRoot,
  MenuTrigger,
  MenuContent,
  MenuItem,
  MenuSeparator,
} from '@chakra-ui/react';
import { Button } from '@chakra-ui/react';
import { ChevronDownIcon } from '@chakra-ui/icons';
import { useVibeStore } from '../stores/useVibeStore';
import { getStandardVibes, getAdvisorVibes } from '../config/vibes';

export default function VibeSelector() {
  const { selectedVibe, setSelectedVibe } = useVibeStore();

  const standardVibes = getStandardVibes();
  const advisorVibes = getAdvisorVibes();

  return (
    <MenuRoot>
      <MenuTrigger asChild>
        <Button width="full" textAlign="left">
          {selectedVibe ? (
            <HStack gap={2}>
              <Text>{selectedVibe.icon}</Text>
              <Text>{selectedVibe.name}</Text>
            </HStack>
          ) : (
            'Select a vibe...'
          )}
          <ChevronDownIcon />
        </Button>
      </MenuTrigger>
      <MenuContent maxH="400px" overflowY="auto">
        <Box px={3} py={2}>
          <Text fontSize="xs" fontWeight="bold" color="gray.500">
            STANDARD VIBES
          </Text>
        </Box>
        {standardVibes.map((vibe) => (
          <MenuItem
            key={vibe.id}
            value={vibe.id}
            onClick={() => setSelectedVibe(vibe)}
          >
            <HStack gap={2}>
              <Text fontSize="lg">{vibe.icon}</Text>
              <Box>
                <Text fontWeight="medium">{vibe.name}</Text>
                {vibe.description && (
                  <Text fontSize="xs" color="gray.600">
                    {vibe.description}
                  </Text>
                )}
              </Box>
            </HStack>
          </MenuItem>
        ))}

        <MenuSeparator />

        <Box px={3} py={2}>
          <Text fontSize="xs" fontWeight="bold" color="gray.500">
            AI ADVISORS
          </Text>
        </Box>
        {advisorVibes.map((vibe) => (
          <MenuItem
            key={vibe.id}
            value={vibe.id}
            onClick={() => setSelectedVibe(vibe)}
          >
            <HStack gap={2}>
              <Text fontSize="lg">{vibe.icon}</Text>
              <Box>
                <Text fontWeight="medium">{vibe.name}</Text>
                {vibe.description && (
                  <Text fontSize="xs" color="gray.600">
                    {vibe.description}
                  </Text>
                )}
              </Box>
            </HStack>
          </MenuItem>
        ))}
      </MenuContent>
    </MenuRoot>
  );
}
