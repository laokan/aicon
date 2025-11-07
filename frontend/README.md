# AICG Frontend

Vue.js frontend for AICG Content Distribution Platform.

## Architecture Principles

### Clean Directory Structure
```
frontend/
├── index.html              # Entry HTML file (only)
├── package.json           # Dependencies and scripts
├── vite.config.js         # Build configuration
├── .eslintrc.cjs          # ESLint configuration
├── .prettierrc            # Prettier configuration
├── src/                   # All source code
│   ├── main.js           # Application entry point
│   ├── App.vue           # Root component
│   ├── assets/           # Static assets
│   │   └── styles/       # Global styles
│   ├── components/       # Reusable components
│   │   └── common/       # Common UI components
│   ├── views/            # Page components
│   ├── router/           # Route configuration
│   ├── stores/           # Pinia state management
│   ├── services/         # API services
│   ├── composables/      # Vue composables
│   └── utils/            # Utility functions
└── tests/                # Test files
```

### Key Principles
1. **Single Responsibility**: Each file has one clear purpose
2. **Separation of Concerns**: UI, logic, and data are separated
3. **Consistent Naming**: Use kebab-case for files, PascalCase for components
4. **Minimal Root Files**: Only essential configuration files in root directory

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test:e2e
```