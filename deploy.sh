#!/bin/bash

# Configuration variables
DOCKER_USERNAME="seannicho"
WEB_IMAGE_NAME="sit-distributed-website"
DB_IMAGE_NAME="sit-distributed-db"
IMAGE_TAG="latest"
NAMESPACE="default" # Change this if you're using a specific namespace in Kubernetes

# Log into Docker
echo "Logging into Docker..."
docker login

# Step 1: Build and Push the Docker DB image
echo "Redirecting to MySQL directory..."
cd "/Users/seannicholas/Developer/SIT/Y2_T1/Cloud and Distributed Computing/project/cloud-resource-pooling/MySQL"

echo "Building Docker DB image..."
sudo docker build -t $DOCKER_USERNAME/$DB_IMAGE_NAME:$IMAGE_TAG .

echo "Pushing Docker DB image to Docker Hub..."
docker push $DOCKER_USERNAME/$DB_IMAGE_NAME:$IMAGE_TAG

# Step 2: Build and Push the Docker Web image
echo "Redirecting to Website directory..."
cd "/Users/seannicholas/Developer/SIT/Y2_T1/Cloud and Distributed Computing/project/cloud-resource-pooling/Website"

echo "Building Docker Web image..."
sudo docker build -t $DOCKER_USERNAME/$WEB_IMAGE_NAME:$IMAGE_TAG .

echo "Pushing Docker Web image to Docker Hub..."
docker push $DOCKER_USERNAME/$WEB_IMAGE_NAME:$IMAGE_TAG

# Step 3: Update Kubernetes Deployments
# Update the database deployment (if exists)
echo "Updating Kubernetes DB deployment..."
kubectl set image deployment/mysql mysql=$DOCKER_USERNAME/$DB_IMAGE_NAME:$IMAGE_TAG --namespace=$NAMESPACE

# Update the web application deployment
echo "Updating Kubernetes Web deployment..."
kubectl set image deployment/web-app app-container=$DOCKER_USERNAME/$WEB_IMAGE_NAME:$IMAGE_TAG --namespace=$NAMESPACE

# Step 4: Force rollout restart for the web application deployment
echo "Restarting Kubernetes Web deployment to apply changes..."
kubectl rollout restart deployment/web-app --namespace=$NAMESPACE

# Step 5: Check the status of the deployment
echo "Checking deployment status..."
kubectl rollout status deployment/web-app --namespace=$NAMESPACE

echo "Deployment complete! Access the application at 127.0.0.1:80"
