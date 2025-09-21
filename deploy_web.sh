#!/bin/bash

# CodeMate Terminal Web Deployment Script
echo "🚀 CodeMate Terminal Web Deployment"
echo "=================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json not found. Make sure you're in the maccodemate directory."
    exit 1
fi

# Check if API file exists
if [ ! -f "api/terminal.py" ]; then
    echo "❌ api/terminal.py not found."
    exit 1
fi

# Check if frontend exists
if [ ! -f "public/index.html" ]; then
    echo "❌ public/index.html not found."
    exit 1
fi

echo "✅ All files found. Starting deployment..."

# Deploy to Vercel
echo "📦 Deploying to Vercel..."
vercel --prod

echo ""
echo "🎉 Deployment complete!"
echo "🌐 Your CodeMate Terminal is now live!"
echo ""
echo "📋 Features available:"
echo "  ✅ AI-powered natural language commands"
echo "  ✅ Full terminal emulation in browser"
echo "  ✅ Command history and auto-completion"
echo "  ✅ System monitoring (ps, free, df, cpu)"
echo "  ✅ File operations (ls, cd, mkdir, rm, etc.)"
echo "  ✅ CodeMate integration commands"
echo "  ✅ Modern responsive web interface"
echo ""
echo "🤖 Try these AI commands:"
echo "  • 'create a folder called test'"
echo "  • 'show me my files'"
echo "  • 'what's my memory usage'"
echo "  • 'create a new folder called demo and move file1.txt into it'"
echo ""
echo "🎯 Perfect for hackathon demos!"
