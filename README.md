# Coolify Docker Test Python API

A test project built with Python, FastAPI, and Uvicorn, specifically designed to verify Docker image deployment compatibility with Coolify. This repository serves as a proof-of-concept for running containerized Python applications on Coolify's infrastructure.

## Purpose

The main objectives of this repository are:
- Test Docker image deployment on Coolify platform
- Verify container orchestration and proxy handling
- Demonstrate proper configuration for Python applications in Coolify
- Provide a minimal, but production-ready container setup

## Features

- Root endpoint (`/`) returning a welcome message and timestamp
- Version endpoint (`/version`) showing application details
- Detailed JSON logging for debugging
- Docker support for easy deployment
- Coolify-ready configuration
- FastAPI Swagger documentation at `/docs`

## Prerequisites

- Python 3.11 or higher
- pip
- Docker

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the development server:
   ```bash
   python src/main.py
   ```

The API will be available at `http://localhost:3000`

## Docker Instructions

### Building Docker Images

To build for a specific architecture:

```bash
# For ARM64 (e.g., Apple Silicon M1/M2)
docker build -t coolify-docker-test-python-api:0.1.6-arm64 .

# For AMD64 (Intel/AMD processors)
docker build --platform linux/amd64 -t coolify-docker-test-python-api:0.1.6-amd64 .
```

### Publishing to Docker Hub

1. Tag your architecture-specific image:
```bash
# For ARM64
docker tag coolify-docker-test-python-api:0.1.6-arm64 YOUR_DOCKERHUB_USERNAME/coolify-docker-test-python-api:0.1.6-arm64

# For AMD64
docker tag coolify-docker-test-python-api:0.1.6-amd64 YOUR_DOCKERHUB_USERNAME/coolify-docker-test-python-api:0.1.6-amd64
```

2. Push to Docker Hub:
```bash
# Push ARM64 version
docker push YOUR_DOCKERHUB_USERNAME/coolify-docker-test-python-api:0.1.6-arm64

# Push AMD64 version
docker push YOUR_DOCKERHUB_USERNAME/coolify-docker-test-python-api:0.1.6-amd64
```

### Platform Compatibility Notes

- Due to Python package compilation requirements, platform-specific builds are necessary
- For Coolify deployment, use the AMD64 version (version-amd64 tag)
- For local development on ARM machines (M1/M2 Macs), use the ARM64 version (version-arm64 tag)
- The image tag follows Docker's official naming convention: `name:version-platform`

## Deploying to Coolify

This repository is specifically designed to test Docker image deployment on Coolify. It serves as a validation tool for:
- Docker image compatibility with Coolify
- Container networking and proxy configuration
- Environment variable handling
- Health check functionality

### Option 1: Using Dockerfile in Coolify

1. In Coolify, create a new service
2. Choose "Dockerfile" as the deployment method
3. Copy the contents of the Dockerfile from this repository
4. Set the following environment variables:
   - `PORT=3000`
   - `PYTHONUNBUFFERED=1`
5. Deploy the service and monitor the logs for any issues

### Option 2: Using Pre-built Docker Image

1. In Coolify, create a new service
2. Choose "Docker Image" as the deployment method
3. Enter your Docker image URL: `YOUR_DOCKERHUB_USERNAME/coolify-docker-test-python-api:0.1.6-amd64`
4. Set the following environment variables:
   - `PORT=3000`
   - `PYTHONUNBUFFERED=1`
5. Deploy the service and verify the deployment

### Verifying the Deployment

After deployment, you can verify the setup by:
1. Checking if the service is healthy in Coolify dashboard
2. Accessing the root endpoint (`/`) through the provided URL
3. Checking the `/version` endpoint for correct version information
4. Accessing the Swagger documentation at `/docs`
5. Monitoring the logs for detailed request information

## Testing the API

You can test the API using curl:

```bash
# Test root endpoint
curl http://localhost:3000/

# Test version endpoint
curl http://localhost:3000/version
```

Or visit the Swagger documentation at `http://localhost:3000/docs`

## Debugging

The application includes detailed JSON logging:
- All HTTP requests are logged automatically
- Request headers and client information are captured
- Response times and status codes are tracked
- Each request has a unique request ID for tracing

## Version History

- 0.1.0: Initial release
  - Basic API endpoints (/, /version)
  - JSON logging
  - Docker support
  - Coolify compatibility

## License

ISC
