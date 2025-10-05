'use client';

import { Toaster as ChakraToaster, Toast, createToaster } from '@chakra-ui/react';

// Global toaster instance for Chakra v3
export const toaster = createToaster({
  placement: 'top-end',
});

export function Toaster() {
  return (
    <ChakraToaster toaster={toaster}>
      {(toast) => (
        <Toast.Root
          key={toast.id}
          data-type={toast.type}
          style={{
            zIndex: 9999,
            position: 'fixed',
            top: '20px',
            right: '20px',
            minWidth: '300px',
            maxWidth: '400px',
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '12px 16px',
          }}
        >
          <Toast.Indicator
            style={{
              flexShrink: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          />
          <div
            style={{
              flex: 1,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'flex-start',
              gap: '4px',
            }}
          >
            <Toast.Title
              style={{
                fontWeight: '600',
                fontSize: '14px',
                lineHeight: '1.2',
                margin: 0,
              }}
            >
              {toast.title}
            </Toast.Title>
            {toast.description ? (
              <Toast.Description
                style={{
                  fontSize: '13px',
                  lineHeight: '1.3',
                  opacity: '0.9',
                  margin: 0,
                }}
              >
                {toast.description}
              </Toast.Description>
            ) : null}
          </div>
          <Toast.CloseTrigger
            style={{
              flexShrink: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '4px',
              borderRadius: '4px',
              cursor: 'pointer',
            }}
          />
        </Toast.Root>
      )}
    </ChakraToaster>
  );
}
