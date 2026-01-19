#!/bin/bash
# Deploy Git container to cloud (AWS/Azure/GCP)

set -e

CLOUD_PROVIDER=${1:-aws}

echo "☁️  Deploying Queztl-Core Git to $CLOUD_PROVIDER..."

case $CLOUD_PROVIDER in
    aws)
        echo "🔸 Deploying to AWS ECS..."
        
        # Build and push to ECR
        AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
        AWS_REGION=${AWS_REGION:-us-east-1}
        ECR_REPO="queztl-git"
        
        # Create ECR repo if not exists
        aws ecr describe-repositories --repository-names $ECR_REPO --region $AWS_REGION 2>/dev/null || \
            aws ecr create-repository --repository-name $ECR_REPO --region $AWS_REGION
        
        # Login to ECR
        aws ecr get-login-password --region $AWS_REGION | \
            docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
        
        # Build and push
        docker build -t $ECR_REPO .
        docker tag $ECR_REPO:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest
        docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest
        
        echo "✅ Pushed to ECR: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest"
        echo "📝 Use the ECS task definition in ../cloud_configs/aws_ecs.json"
        ;;
    
    azure)
        echo "🔷 Deploying to Azure..."
        
        # Azure Container Registry
        ACR_NAME=${ACR_NAME:-queztlregistry}
        
        # Login to ACR
        az acr login --name $ACR_NAME
        
        # Build and push
        docker build -t queztl-git .
        docker tag queztl-git:latest $ACR_NAME.azurecr.io/queztl-git:latest
        docker push $ACR_NAME.azurecr.io/queztl-git:latest
        
        echo "✅ Pushed to ACR: $ACR_NAME.azurecr.io/queztl-git:latest"
        ;;
    
    gcp)
        echo "🔶 Deploying to Google Cloud..."
        
        # GCP Project
        GCP_PROJECT=${GCP_PROJECT:-queztl-core}
        
        # Build and push to GCR
        gcloud builds submit --tag gcr.io/$GCP_PROJECT/queztl-git
        
        echo "✅ Pushed to GCR: gcr.io/$GCP_PROJECT/queztl-git:latest"
        echo "📝 Deploy to Cloud Run: gcloud run deploy queztl-git --image gcr.io/$GCP_PROJECT/queztl-git --platform managed"
        ;;
    
    docker-hub)
        echo "🐋 Deploying to Docker Hub..."
        
        DOCKER_USERNAME=${DOCKER_USERNAME:-queztl}
        
        docker build -t queztl-git .
        docker tag queztl-git:latest $DOCKER_USERNAME/queztl-git:latest
        docker push $DOCKER_USERNAME/queztl-git:latest
        
        echo "✅ Pushed to Docker Hub: $DOCKER_USERNAME/queztl-git:latest"
        ;;
    
    *)
        echo "❌ Unknown provider: $CLOUD_PROVIDER"
        echo "Usage: $0 [aws|azure|gcp|docker-hub]"
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment complete!"
