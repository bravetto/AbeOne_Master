# Continuous Deployment (CD) with PoisonGuard

This document outlines the process for setting up a Continuous Deployment (CD) pipeline for the PoisonGuard application. The pipeline will automatically build, test, and deploy the application using GitHub Actions and Docker.

## Prerequisites

- A Docker Hub account or another container registry.
- A server to deploy the application to.

## Pipeline Overview

The CD pipeline consists of the following stages:

1.  **Build and Test**: The application is built and tested on every push to the `main` branch.
2.  **Publish to Docker Hub**: If the tests pass, a Docker image is built and pushed to Docker Hub.
3.  **Deploy to Server**: The new Docker image is pulled and deployed on the server.

## GitHub Actions Workflow

The following GitHub Actions workflow can be used to automate the CD process. This workflow should be placed in `.github/workflows/cd.yml`.

```yaml
name: Continuous Deployment

on:
  push:
    branches: [ main ]

jobs:
  build-and-publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Log in to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v3
      with:
        context: .
        push: true
        tags: ${{ secrets.DOCKER_USERNAME }}/poisonguard:latest
```

## Deployment on the Server

To deploy the application on your server, you can use the following steps:

1.  **Install Docker**: Ensure that Docker is installed on your server.
2.  **Pull the Docker Image**: Pull the latest Docker image from Docker Hub:
    ```bash
    docker pull your-docker-username/poisonguard:latest
    ```
3.  **Run the Application**: Run the application using the `docker run` command:
    ```bash
    docker run -d -p 8000:8000 \
      -e CONFIG_FILE=/path/to/your/config.yaml \
      -v /path/to/your/config.yaml:/path/to/your/config.yaml \
      your-docker-username/poisonguard:latest
    ```

This will start the PoisonGuard API server in detached mode. You can then access the API at `http://your-server-ip:8000`.

## Configuration Management

The application can be configured using a YAML file. The path to the configuration file can be specified using the `CONFIG_FILE` environment variable. When deploying the application with Docker, you can mount a configuration file from the host into the container and set the `CONFIG_FILE` environment variable to the path of the mounted file.