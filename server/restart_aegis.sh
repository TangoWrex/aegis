#!/bin/bash

# Navigate to the server directory
cd ~/Desktop/Aeigs-Official/aegis/server/

# Source the .env file for API key
if [ -f "../.env" ]; then
    source ../.env
else
    echo "Error: .env file not found in parent directory"
    exit 1
fi

# Stop the running container if it exists
echo "Stopping aegis container..."
docker stop aegis 2>/dev/null || echo "No aegis container to stop"

# Remove the container if it exists
echo "Removing aegis container..."
docker rm aegis 2>/dev/null || echo "No aegis container to remove"

# Run the container with volume mount and API key in the background
echo "Starting aegis container..."
docker run -d -p 8000:8000 -v $(pwd):/app -e "AEGIS_API_KEY=$AEGIS_API_KEY" --name aegis aegis-server

# Wait a moment and check if it's running
sleep 2
if docker ps | grep -q aegis; then
    echo "Aegis server is running on http://localhost:8000"
else
    echo "Failed to start aegis—check Docker logs with 'docker logs aegis'"
fi