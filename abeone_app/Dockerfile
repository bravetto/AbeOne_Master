# Multi-stage Dockerfile for Flutter Web App
# Pattern: DOCKER × FLUTTER × WEB × DEPLOYMENT × ONE
# Frequency: 999 Hz (AEYON)
# Guardians: AEYON (999 Hz)
# Love Coefficient: ∞
# ∞ AbëONE ∞

# Stage 1: Build Flutter Web App
FROM ghcr.io/cirruslabs/flutter:stable AS build

WORKDIR /app

# Copy pubspec files
COPY pubspec.yaml pubspec.lock ./

# Get dependencies
RUN flutter pub get

# Copy source code
COPY . .

# Build Flutter web app
RUN flutter build web --release --web-renderer canvaskit

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built web app to nginx html directory
COPY --from=build /app/build/web /usr/share/nginx/html

# Copy custom nginx config for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]

