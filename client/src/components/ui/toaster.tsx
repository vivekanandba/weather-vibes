'use client';

import { Toaster as ChakraToaster, Toast, createToaster } from '@chakra-ui/react';

// Global toaster instance for Chakra v3
export const toaster = createToaster({ placement: 'top-end' });

export function Toaster() {
  return (
    <ChakraToaster toaster={toaster}>
      {(toast) => (
        <Toast.Root key={toast.id}>
          <Toast.Indicator />
          <Toast.Title>{toast.title}</Toast.Title>
          {toast.description ? <Toast.Description>{toast.description}</Toast.Description> : null}
          <Toast.CloseTrigger />
        </Toast.Root>
      )}
    </ChakraToaster>
  );
}
