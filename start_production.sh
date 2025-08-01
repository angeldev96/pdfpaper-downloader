#!/bin/bash

echo "Starting production server for PDF Downloader..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Check if virtual environment exists, if not, create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create downloads directory if it doesn't exist
if [ ! -d "downloads" ]; then
    echo "Creating downloads directory..."
    mkdir -p downloads
    chmod 755 downloads
fi

# Create temporary directory if it doesn't exist
if [ ! -d "temp" ]; then
    echo "Creating temporary directory..."
    mkdir -p temp
    chmod 755 temp
fi

# Start the production server
echo "Starting production server at http://127.0.0.1:5000"
python run_production.py

# The virtual environment will be automatically deactivated when the script closes
deactivate