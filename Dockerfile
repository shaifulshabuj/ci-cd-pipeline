FROM node:18-alpine AS build

# Create app directory
WORKDIR /usr/src/app

# Copy package files and install dependencies
COPY package*.json ./
# Remove deprecated --only=production flag
RUN npm ci || npm install

# Copy application code
COPY . .

# Build application if needed
RUN npm run build || echo "No build script found"

# Production stage
FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

# Set NODE_ENV
ENV NODE_ENV=production

# Create a non-root user to run the application
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Copy from build stage - be more selective with what we copy
COPY --from=build /usr/src/app/node_modules/ ./node_modules/
COPY --from=build /usr/src/app/package*.json ./
COPY --from=build /usr/src/app/dist/ ./dist/
COPY --from=build /usr/src/app/public/ ./public/
COPY --from=build /usr/src/app/server.js ./server.js
COPY --from=build /usr/src/app/app.js ./app.js

# Set proper permissions
RUN chown -R appuser:appgroup /usr/src/app

# Use the non-root user
USER appuser

# Expose the port your app will run on
EXPOSE 3000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

# Start the application
CMD ["node", "server.js"]