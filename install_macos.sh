#!/bin/bash

# CodeMate Terminal Installation Script for macOS
# Professional AI-powered terminal for CodeMate.ai hackathon

echo "🚀 CodeMate Terminal Installation for macOS"
echo "=============================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    echo "   Visit: https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip3 is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✅ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements_macos.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Error installing dependencies"
    exit 1
fi

# Make launcher executable
chmod +x launch_macos.py

echo ""
echo "🎉 Installation complete!"
echo ""
echo "🚀 To run CodeMate Terminal:"
echo "   python3 codemate_terminal.py"
echo ""
echo "🚀 To launch in macOS Terminal:"
echo "   python3 launch_macos.py"
echo ""
echo "📚 For more information, see README_macos.md"
echo ""
echo "Ready for CodeMate.ai hackathon! 🏆"
