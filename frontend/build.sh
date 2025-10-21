#!/bin/sh
# Build script for Render deployment
# This ensures VITE_API_URL is available during build

# Set default API URL if not provided
: ${VITE_API_URL:=https://ml-backend-api.onrender.com}

echo "Building with VITE_API_URL=${VITE_API_URL}"

# Build the application with environment variable
npm run build
