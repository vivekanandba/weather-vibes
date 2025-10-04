'use client';

import { Flex, Box } from '@chakra-ui/react';
import Header from '@components/layout/Header';
import Sidebar from '@components/layout/Sidebar';
import MapView from '@components/map/MapView';
import WherePanel from '@components/features/where/WherePanel';
import WhenPanel from '@components/features/when/WhenPanel';
import AdvisorPanel from '@components/features/advisors/AdvisorPanel';
import { useVibeStore } from '../stores/useVibeStore';

export default function Home() {
  const { activeFeature } = useVibeStore();

  return (
    <Flex direction="column" h="100vh" w="100vw" overflow="hidden">
      <Header />
      <Flex flex={1} position="relative" overflow="hidden">
        <Sidebar />
        <Box flex={1} position="relative">
          <MapView />
          {activeFeature === 'where' && <WherePanel />}
          {activeFeature === 'when' && <WhenPanel />}
          {activeFeature === 'advisor' && <AdvisorPanel />}
        </Box>
      </Flex>
    </Flex>
  );
}
