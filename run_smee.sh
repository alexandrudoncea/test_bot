#!/bin/bash
# Run Smee client in the background
smee -u https://smee.io/ybYJFTBTTflxvP --target http://localhost:5000/webhook &
echo "Smee client started"

# Start Flask app
python3 backend/app.py
