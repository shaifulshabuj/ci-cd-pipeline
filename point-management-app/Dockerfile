FROM node:18-alpine AS build

# Create app directory
WORKDIR /usr/src/app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci

# Copy application code
COPY . .

# Run tests
RUN npm test

# Production stage
FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

# Set NODE_ENV
ENV NODE_ENV=production

# Create a non-root user to run the application
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy only necessary files from build stage
COPY --from=build /usr/src/app/package*.json ./
COPY --from=build /usr/src/app/node_modules/ ./node_modules/
COPY --from=build /usr/src/app/server.js ./

# Set proper permissions
RUN chown -R appuser:appgroup /usr/src/app

# Use the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 3000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

# Start the application
CMD ["node", "server.js"]