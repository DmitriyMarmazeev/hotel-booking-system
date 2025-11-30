#!/bin/bash

# Load environment variables
set -a
source .env
set +a

# Build and push images
docker-compose -f docker-compose.prod.yml build
docker push $DOCKER_USERNAME/hotel-booking-backend:latest
docker push $DOCKER_USERNAME/hotel-booking-frontend:latest

# Deploy to server
ssh $SERVER_USERNAME@$SERVER_HOST << 'EOF'
    docker pull $DOCKER_USERNAME/hotel-booking-backend:latest
    docker pull $DOCKER_USERNAME/hotel-booking-frontend:latest
    
    docker stop backend frontend database || true
    docker rm backend frontend database || true
    
    docker-compose -f docker-compose.prod.yml up -d
EOF

echo "Deployment completed successfully!"