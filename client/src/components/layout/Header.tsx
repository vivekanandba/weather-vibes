'use client';

import { Box, Flex, Heading, IconButton } from '@chakra-ui/react';
import { HamburgerIcon } from '@chakra-ui/icons';
import { useUIStore } from '../stores/useUIStore';

export default function Header() {
  const { isSidebarOpen, setSidebarOpen } = useUIStore();

  return (
    <Box
      as="header"
      bg="white"
      borderBottom="1px"
      borderColor="gray.200"
      px={4}
      py={3}
      position="sticky"
      top={0}
      zIndex={100}
      boxShadow="sm"
    >
      <Flex justify="space-between" alignItems="center">
        <Flex alignItems="center" gap={3}>
          <IconButton
            aria-label="Toggle sidebar"
            onClick={() => setSidebarOpen(!isSidebarOpen)}
          >
            <HamburgerIcon />
          </IconButton>
          <Heading size="md" color="blue.600">
            🌤️ Weather Vibes
          </Heading>
        </Flex>
      </Flex>
    </Box>
  );
}
