#!/bin/bash

# CodeMate Terminal - Quick Deploy Script
# This script helps you deploy to Vercel quickly

echo "🚀 CodeMate Terminal - Vercel Deployment Script"
echo "=============================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Vercel CLI. Please install manually:"
        echo "   npm install -g vercel"
        exit 1
    fi
    echo "✅ Vercel CLI installed successfully"
else
    echo "✅ Vercel CLI found"
fi

# Check if user is logged in
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel:"
    vercel login
    if [ $? -ne 0 ]; then
        echo "❌ Login failed. Please try again."
        exit 1
    fi
else
    echo "✅ Already logged in to Vercel"
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
echo "✅ Dependencies installed"

# Test the API locally first
echo "🧪 Testing API locally..."
python test_api.py &
TEST_PID=$!

# Start Vercel dev server
echo "🚀 Starting Vercel dev server..."
vercel dev &
VERCEL_PID=$!

# Wait a bit for servers to start
sleep 5

# Test the API
echo "🔍 Testing API endpoints..."
python test_api.py

# Stop test processes
kill $TEST_PID 2>/dev/null
kill $VERCEL_PID 2>/dev/null

echo ""
echo "🎯 Ready to deploy!"
echo "Run: vercel --prod"
echo ""
echo "📋 Or follow the full deployment guide in DEPLOYMENT.md"
echo ""
echo "🎉 Happy coding with CodeMate Terminal!"
