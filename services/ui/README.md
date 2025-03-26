# Postgres Project UI

A simple dashboard UI built with best practices.

## Features

- React + TypeScript
- Tailwind CSS for styling
- shadcn/ui components
- Feature-based architecture
- React Router for navigation
- React Query for data fetching
- Zustand for state management

## Project Structure

```
/ui
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable UI components
│   │   ├── Layout/      # Layout components
│   │   └── ui/          # shadcn UI components
│   ├── features/        # Feature modules
│   │   └── dashboard/   # Dashboard feature components
│   ├── lib/             # Utilities and services
│   ├── pages/           # Route components
│   ├── App.tsx          # Root component
│   └── main.tsx         # Entry point
└── ...config files
```

## Architecture

This application follows a feature-based architecture:

- **Pages**: Container components that correspond to routes
- **Features**: Business logic and feature-specific components
- **Components**: Reusable UI components used across features
- **Lib**: Utilities, API services, and stores

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Environment Variables

- `VITE_API_URL`: API URL (defaults to "http://localhost:8000")
