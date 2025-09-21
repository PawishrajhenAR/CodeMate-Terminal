#!/bin/bash

echo "🚀 CodeMate Terminal - Manual GitHub Upload Helper"
echo "==============================================="

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Please run this script from the maccodemate directory"
    echo "   cd /Users/harish/Downloads/CodeMate/maccodemate"
    exit 1
fi

echo "✅ Found Vercel configuration"
echo "📁 Current directory: $(pwd)"
echo ""

echo "📋 Files ready for GitHub upload:"
echo "================================="
ls -la | grep -E "\.(py|json|html|md|sh|txt)$"
echo ""

echo "🎯 Manual GitHub Upload Instructions:"
echo "==================================="
echo ""
echo "1. 🌐 Open GitHub Repository:"
echo "   https://github.com/Harishs1212/CodeMate-Terminal"
echo ""
echo "2. 📁 Click 'uploading an existing file'"
echo ""
echo "3. 📦 Upload these files (drag and drop):"
echo "   - api/terminal.py"
echo "   - public/index.html"
echo "   - vercel.json"
echo "   - package.json"
echo "   - requirements.txt"
echo "   - All .md files"
echo "   - All .sh files"
echo ""
echo "4. 💾 Commit message:"
echo "   'AI-Powered CodeMate Terminal - Web Interface'"
echo ""
echo "5. ✅ Click 'Commit changes'"
echo ""

echo "🚀 After GitHub Upload - Deploy to Vercel:"
echo "=========================================="
echo ""
echo "1. 🌐 Go to https://vercel.com"
echo "2. 🔐 Sign in with GitHub"
echo "3. ➕ Click 'New Project'"
echo "4. 📥 Import 'Harishs1212/CodeMate-Terminal'"
echo "5. 🚀 Deploy automatically!"
echo ""

echo "🎯 Your terminal will be live at:"
echo "   https://your-project-name.vercel.app"
echo ""

echo "🧪 Features ready for demo:"
echo "=========================="
echo "✅ AI Natural Language Commands"
echo "✅ Command History & Auto-completion"
echo "✅ File Operations (ls, mkdir, rm, touch, cat, cp, mv)"
echo "✅ System Monitoring (ps, free, df, uptime, whoami, date)"
echo "✅ Modern Web UI"
echo "✅ Real-time Command Execution"
echo ""

echo "🏆 Perfect for hackathon submission!"
