# Use Node.js for building the React app
FROM node:20 AS build

WORKDIR /frontend

# Copy package.json and package-lock.json
COPY blogpostui/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the React app (including public folder)
COPY blogpostui/ ./

# Build the React app
RUN npm run build

# Use a lightweight server to serve the build
FROM node:20

WORKDIR /frontend

# Install serve globally
RUN npm install -g serve

# Copy the build output from the previous stage
COPY --from=build /frontend/build ./build

# Expose port
EXPOSE 3000

# Run the app
CMD ["serve", "-s", "build", "-l", "3000"]
