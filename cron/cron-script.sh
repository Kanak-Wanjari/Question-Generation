#!/bin/bash

# Navigate to the project directory
cd /home/ubuntu/Question-Generation

# Pull the latest changes from the repository
git pull origin main

# Check if the JSON file exists, if not, exit with error
if [ ! -f "Generated_Prompts.json" ]; then
    echo "Generated_Prompts.json not found, exiting..." >> /home/ubuntu/Question-Generation/logs/cronjob.log
    exit 1
fi

# Create the logs directory if it doesn't exist
mkdir -p /home/ubuntu/Question-Generation/logs

# Activate the virtual environment
source venv/bin/activate

# Run the Python script
python3 Interview_Question_Generator.py >> /home/ubuntu/Question-Generation/logs/cronjob.log 2>&1
