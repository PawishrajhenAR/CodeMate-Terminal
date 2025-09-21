#!/bin/bash

echo "🚀 CodeMate Terminal - Quick Deploy Script"
echo "========================================="

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Please run this script from the maccodemate directory"
    echo "   cd /Users/harish/Downloads/CodeMate/maccodemate"
    exit 1
fi

echo "✅ Found Vercel configuration"
echo "📁 Current directory: $(pwd)"
echo ""

# Check git status
if [ -d ".git" ]; then
    echo "📦 Git repository status:"
    git status --short
    echo ""
    
    # Add and commit any changes
    if ! git diff --staged --quiet || ! git diff --quiet; then
        echo "💾 Committing latest changes..."
        git add .
        git commit -m "Final deployment: AI-Powered CodeMate Terminal

- Complete web-based terminal interface
- AI natural language command processing
- Enhanced rm command with -r flag support
- Vercel-ready configuration
- Professional UI/UX design
- Ready for hackathon submission"
        echo "✅ Changes committed"
    else
        echo "ℹ️  No changes to commit"
    fi
    
    echo ""
    echo "🔗 Remote repository:"
    git remote -v
    echo ""
    
    echo "🚀 Ready to push! Run one of these commands:"
    echo ""
    echo "Option 1 - Manual push:"
    echo "   git push -u origin main"
    echo ""
    echo "Option 2 - Force push (if needed):"
    echo "   git push -f origin main"
    echo ""
    echo "Option 3 - GitHub CLI (if installed):"
    echo "   gh repo create Harishs1212/CodeMate-Terminal --public --source=. --remote=origin --push"
    echo ""
    
else
    echo "❌ Git repository not found. Please run:"
    echo "   git init"
    echo "   git remote add origin https://github.com/Harishs1212/CodeMate-Terminal.git"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git push -u origin main"
fi

echo ""
echo "📋 After pushing to GitHub:"
echo "1. Go to https://vercel.com"
echo "2. Click 'New Project'"
echo "3. Import from GitHub: Harishs1212/CodeMate-Terminal"
echo "4. Deploy automatically!"
echo ""
echo "🎯 Your terminal will be live at: https://your-project-name.vercel.app"
