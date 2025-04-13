# CI/CD Pipeline Project

A complete CI/CD pipeline implementation for microservice deployment using GitHub Actions and Docker.

## Project Overview

This project implements a continuous integration and continuous deployment (CI/CD) pipeline for automating the build, test, and deployment processes of applications. The pipeline is specifically demonstrated with a simple "Point Management Tool" application.

## Features

- Automated code linting and testing
- Docker containerization
- Integration with AWS ECR for image storage
- Automated deployment workflows
- Security best practices implementation

## Structure

- `point-management-app/`: Example application demonstrating the CI/CD pipeline
  - A simple REST API for managing user points
  - Streamlit UI for interacting with the API
- `.github/workflows/`: GitHub Actions workflow definitions
- `deploy.sh`: Deployment script for AWS

## Setup

1. Clone this repository
2. Create a `.env` file based on `.env.example`
3. Install dependencies: `cd point-management-app && npm install`
4. Run tests: `npm test`

## Usage

### Local Development

```bash
# Start the API service
cd point-management-app
npm start

# Run the Streamlit UI (in another terminal)
cd point-management-app
streamlit run app.py
```

### Docker Usage

```bash
# Build the Docker image
docker build -t point-management-api ./point-management-app

# Run the container
docker run -p 3001:3000 -d --name point-management-api point-management-api
```

## CI/CD Pipeline

The GitHub Actions workflow automates:

1. Linting and testing on pull requests
2. Building and pushing Docker images on successful merges
3. Deploying to AWS on main/master branch updates

## License

MIT