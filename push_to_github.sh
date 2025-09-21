#!/bin/bash

echo "🚀 CodeMate Terminal - GitHub Push Script"
echo "========================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Please run:"
    echo "   git init"
    echo "   git remote add origin https://github.com/Harishs1212/CodeMate-Terminal.git"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ Remote origin not set. Please run:"
    echo "   git remote add origin https://github.com/Harishs1212/CodeMate-Terminal.git"
    exit 1
fi

echo "✅ Git repository is ready"
echo "📁 Current directory: $(pwd)"
echo "🔗 Remote URL: $(git remote get-url origin)"
echo ""

# Add all files
echo "📦 Adding files to git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️  No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "Update: AI-Powered CodeMate Terminal

- Enhanced web-based terminal interface
- AI natural language command processing  
- Command history and auto-completion
- Fixed rm command with -r flag support
- Vercel-ready deployment configuration
- Python backend API with proper error handling
- Modern responsive frontend design
- Cross-platform compatibility"
fi

echo ""
echo "🚀 Ready to push to GitHub!"
echo ""
echo "To push manually, run:"
echo "   git push -u origin main"
echo ""
echo "Or if you have GitHub CLI installed:"
echo "   gh repo create Harishs1212/CodeMate-Terminal --public --source=. --remote=origin --push"
echo ""
echo "📋 Files ready for push:"
git status --porcelain | head -10
if [ $(git status --porcelain | wc -l) -gt 10 ]; then
    echo "... and $(($(git status --porcelain | wc -l) - 10)) more files"
fi
