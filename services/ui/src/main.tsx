import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { QueryClientProvider } from '@tanstack/react-query'
import './index.css'
import App from './App.tsx'
import { queryClient } from './lib/api'

// Display a friendly error if the backend is not running
window.addEventListener('unhandledrejection', (event: PromiseRejectionEvent) => {
  const error = event.reason;
  if (error?.isAxiosError && !error?.response) {
    console.error('Backend connection error - make sure your server is running.')
  }
});

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
)