#!/bin/bash
# Build and run the Lubuntu dev container with VNC and SSH support

IMAGE_NAME=lubuntu-dev
CONTAINER_NAME=lubuntu-dev
WORKSPACE_DIR=$(pwd)
VNC_PORT=6080
SSH_PORT=2222

# Build the image

echo "[+] Building $IMAGE_NAME..."
docker build -f infra/Dockerfile.lubuntu-dev -t $IMAGE_NAME . || exit 1

echo "[+] Stopping/removing any existing $CONTAINER_NAME..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

# Run the container with VNC and SSH ports exposed, mounting the workspace

echo "[+] Starting $CONTAINER_NAME with VNC on :$VNC_PORT and SSH on :$SSH_PORT..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $VNC_PORT:6080 \
  -p $SSH_PORT:22 \
  -v $WORKSPACE_DIR:/workspace \
  $IMAGE_NAME

echo "[+] Container started."
echo "- VNC: http://localhost:$VNC_PORT"
echo "- VS Code server: http://localhost:$CODE_PORT (login: admin / Welcome2026#!)"
echo "- Workspace mounted at /workspace"
CODE_PORT=8080
echo "[+] Starting $CONTAINER_NAME with VNC on :$VNC_PORT and VS Code server on :$CODE_PORT..."
docker run -d \
  --name $CONTAINER_NAME \
  -p $VNC_PORT:6080 \
  -p $CODE_PORT:8080 \
  -v $WORKSPACE_DIR:/workspace \
  $IMAGE_NAME
