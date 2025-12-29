#!/bin/bash

set -e

echo "=== Colima Switch & Docker Desktop Cleanup ==="

echo "Checking for Colima..."
if ! command -v colima &> /dev/null; then
  echo "Colima not found. Installing via Homebrew..."
  brew install colima
else
  echo "Colima already installed."
fi

echo "Starting Colima..."
colima start

echo "Switching Docker context to Colima..."
docker context use colima

echo "Stopping Docker Desktop if running..."
osascript -e 'quit app "Docker"'

echo
read -p "Do you want to remove Docker Desktop and all its user data? (y/N): " confirm
if [[ "$confirm" =~ ^[Yy]$ ]]; then
  echo "Removing Docker Desktop application..."
  rm -rf /Applications/Docker.app

  echo "Removing Docker Desktop support files..."
  rm -rf ~/Library/Containers/com.docker.docker
  rm -rf ~/.docker
  rm -rf ~/Library/Group\ Containers/group.com.docker
  rm -rf ~/Library/Application\ Support/Docker\ Desktop
  rm -rf ~/Library/Preferences/com.docker.docker.plist
  rm -rf ~/Library/Saved\ Application\ State/com.electron.docker-frontend.savedState

  echo "Docker Desktop and its user data have been removed."
else
  echo "Cleanup skipped. Docker Desktop files remain."
fi

echo "Colima is now your Docker backend."
