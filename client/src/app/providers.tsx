'use client';

import { ChakraProvider, defaultSystem } from '@chakra-ui/react';
import { Toaster } from '../components/ui/toaster';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60 * 1000, // 1 minute
            refetchOnWindowFocus: false,
          },
        },
      })
  );

  return (
    <QueryClientProvider client={queryClient}>
      <ChakraProvider value={defaultSystem}>
        {children}
        <Toaster />
      </ChakraProvider>
    </QueryClientProvider>
  );
}
