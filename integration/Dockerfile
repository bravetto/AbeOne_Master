# Integration Layer Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
COPY guardians-protocols-bridge/package*.json ./guardians-protocols-bridge/
COPY frontend-backend-api/package*.json ./frontend-backend-api/
COPY memory-consciousness-sync/package*.json ./memory-consciousness-sync/

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build
RUN npm run build:all

# Expose port
EXPOSE 8003

# Start (placeholder - adjust based on actual needs)
CMD ["node", "dist/index.js"]

