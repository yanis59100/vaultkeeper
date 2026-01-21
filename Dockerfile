FROM node:20-slim

WORKDIR /app

# Copy backend only
COPY backend/package*.json ./
COPY backend/ ./

# Install production dependencies
RUN npm ci --omit=dev

# Expose port
EXPOSE 3000

# Start app
CMD ["npm", "start"]
