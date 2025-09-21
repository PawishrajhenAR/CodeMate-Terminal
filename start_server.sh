#!/bin/bash

echo "🚀 CodeMate Terminal Web Edition - Local Server"
echo "================================================"
echo "Starting local server..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.6+ and try again"
    exit 1
fi

# Check if required files exist
if [ ! -f "api/terminal.py" ]; then
    echo "❌ Error: api/terminal.py not found"
    echo "Make sure you're running this from the maccodemate directory"
    exit 1
fi

if [ ! -f "public/index.html" ]; then
    echo "❌ Error: public/index.html not found"
    echo "Make sure you're running this from the maccodemate directory"
    exit 1
fi

# Start the server
echo "✅ Starting CodeMate Terminal Web Server..."
echo "🌐 The terminal will open in your browser automatically"
echo "🛑 Press Ctrl+C to stop the server"
echo

python3 run_local_server.py
