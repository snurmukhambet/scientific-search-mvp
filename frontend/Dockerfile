# Multi-stage build for production optimization
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Build argument for API URL (passed from Render envVars)
ARG VITE_API_URL=https://ml-backend-api.onrender.com
ENV VITE_API_URL=$VITE_API_URL

# Debug: Print API URL
RUN echo "Building with VITE_API_URL=${VITE_API_URL}"

# Build the application
RUN npm run build

# Production stage with nginx
FROM nginx:alpine

# Install gettext for envsubst (environment variable substitution)
RUN apk add --no-cache gettext

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx configuration as template
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Expose ports (80 for docker-compose, 3000 for Render)
EXPOSE 80 3000

# Start nginx with environment variable substitution for PORT
# If PORT is not set, defaults to 80 for backward compatibility with docker-compose
CMD ["/bin/sh", "-c", "export PORT=${PORT:-80} && envsubst '$$PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]