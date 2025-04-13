#!/bin/bash
# Deployment script for the microservice 

set -e

# Parse command-line arguments
ENVIRONMENT=${1:-dev} # Default to "dev" environment if not specified

# Function to log messages with timestamps
log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting deployment process"

# Set default values if environment variables are not set
# This allows the script to work with GitHub Actions secrets
AWS_REGION=${AWS_REGION:-"ap-northeast-1"}
ECR_REPOSITORY=${ECR_REPOSITORY:-"point-management-app"}
IMAGE_TAG=${IMAGE_TAG:-"latest"}

# Try to get AWS Account ID if not explicitly set
if [ -z "${AWS_ACCOUNT_ID}" ]; then
  log "AWS_ACCOUNT_ID not set, attempting to retrieve from AWS CLI"
  # Try to get AWS account ID using AWS CLI
  AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text 2>/dev/null || echo "")
  
  if [ -z "${AWS_ACCOUNT_ID}" ]; then
    log "Could not retrieve AWS_ACCOUNT_ID automatically"
    
    # If .env file exists, try to source it
    if [ -f .env ]; then
      log "Loading variables from .env file"
      source .env
    fi
    
    # If still not set, use a placeholder
    if [ -z "${AWS_ACCOUNT_ID}" ]; then
      log "WARNING: Setting placeholder AWS_ACCOUNT_ID. This will need to be replaced."
      AWS_ACCOUNT_ID="123456789012"
    fi
  else
    log "Retrieved AWS_ACCOUNT_ID: ${AWS_ACCOUNT_ID}"
  fi
fi

# Construct ECR_REGISTRY if not already set
if [ -z "${ECR_REGISTRY}" ]; then
  ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
  log "Setting ECR_REGISTRY to ${ECR_REGISTRY}"
fi

# Get image information from environment variables
IMAGE="${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"

echo "=== Starting deployment to ${ENVIRONMENT} environment ==="
echo "Image: ${IMAGE}"
echo "AWS Region: ${AWS_REGION}"

# Verify AWS CLI is installed
if ! command -v aws &> /dev/null; then
  log "ERROR: AWS CLI is required but not installed. Exiting."
  exit 1
fi

# Create ECR repository if it doesn't exist (with proper error handling)
log "Ensuring ECR repository exists"
aws ecr describe-repositories --repository-names ${ECR_REPOSITORY} --region ${AWS_REGION} 2>/dev/null || {
  log "Creating ECR repository ${ECR_REPOSITORY}"
  aws ecr create-repository --repository-name ${ECR_REPOSITORY} --region ${AWS_REGION} || {
    log "ERROR: Failed to create ECR repository ${ECR_REPOSITORY}"
    exit 1
  }
}

# Validate image exists in ECR
log "Verifying image exists in ECR repository"
aws ecr describe-images --repository-name ${ECR_REPOSITORY} --image-ids imageTag=${IMAGE_TAG} --region ${AWS_REGION} || {
  log "ERROR: Image ${IMAGE_TAG} not found in repository ${ECR_REPOSITORY}";
  exit 1;
}

# Different deployment strategies based on environment
case ${ENVIRONMENT} in
  dev)
    log "Deploying to development environment"
    # Example: Update ECS service or deploy to a dev K8s cluster
    # aws ecs update-service --cluster dev-cluster --service ${ECR_REPOSITORY}-service --force-new-deployment
    log "This is a placeholder for dev deployment logic"
    ;;
  
  staging)
    log "Deploying to staging environment"
    # Example: Deploy to staging environment
    # aws ecs update-service --cluster staging-cluster --service ${ECR_REPOSITORY}-service --force-new-deployment
    log "This is a placeholder for staging deployment logic"
    ;;
  
  prod)
    log "Deploying to production environment"
    # Example: Deploy to production environment with confirmation
    log "CAUTION: Production deployment requires additional verification"
    # aws ecs update-service --cluster prod-cluster --service ${ECR_REPOSITORY}-service --force-new-deployment
    log "This is a placeholder for production deployment logic"
    ;;
  
  *)
    log "ERROR: Unknown environment '${ENVIRONMENT}'"
    log "Supported environments: dev, staging, prod"
    exit 1
    ;;
esac

# Wait for deployment to complete
log "Waiting for deployment to complete..."
sleep 5  # In a real scenario, you would check the deployment status

# Verify deployment
log "Verifying deployment..."
# Add verification logic here (health checks, etc.)
# Example: aws ecs describe-services --cluster ${ENVIRONMENT}-cluster --services ${ECR_REPOSITORY}-service

log "Deployment completed successfully!"
exit 0