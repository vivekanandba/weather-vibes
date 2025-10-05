#!/bin/bash

# Weather Vibes Backend Server Startup Script

# Navigate to server directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Set Python path and run the server
PYTHONPATH=/Users/kirankumar.g/Projects/weather-vibes/server python app/main.py
