#!/bin/bash

echo "🔄 Restarting Backend with Cache Clear"
echo "========================================"

# Kill any existing Python processes running main.py
echo "1. Stopping existing backend..."
pkill -f "python.*main.py" 2>/dev/null || echo "   No existing backend found"

# Clear Python cache
echo "2. Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "   ✅ Cache cleared"

# Wait a moment
sleep 1

# Start backend
echo "3. Starting backend..."
python main.py

