#!/usr/bin/env bash
# Build script for Render
set -o errexit

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Setting up directories..."
mkdir -p data/chroma_db

echo "Build completed successfully!"