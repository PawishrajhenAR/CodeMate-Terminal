#!/bin/bash

echo "🚀 CodeMate Terminal - GitHub Push Helper"
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
    
    echo "🔗 Remote repository:"
    git remote -v
    echo ""
    
    echo "📋 Commits ready to push:"
    git log --oneline -5
    echo ""
    
    echo "🚀 Attempting to push to GitHub..."
    echo ""
    
    # Try to push
    if git push -u origin main; then
        echo "✅ Successfully pushed to GitHub!"
        echo "🔗 Repository: https://github.com/Harishs1212/CodeMate-Terminal"
        echo ""
        echo "🎯 Next step: Deploy to Vercel!"
        echo "1. Go to https://vercel.com"
        echo "2. Sign in with GitHub"
        echo "3. Click 'New Project'"
        echo "4. Import 'Harishs1212/CodeMate-Terminal'"
        echo "5. Deploy automatically!"
    else
        echo "❌ Push failed. This usually means authentication is needed."
        echo ""
        echo "🔧 To fix this, you need to authenticate with GitHub:"
        echo ""
        echo "Option 1 - Personal Access Token (Recommended):"
        echo "1. Go to https://github.com/settings/tokens"
        echo "2. Click 'Generate new token (classic)'"
        echo "3. Select 'repo' scope"
        echo "4. Copy the token"
        echo "5. Run: git push -u origin main"
        echo "6. Username: Harishs1212"
        echo "7. Password: [paste your token]"
        echo ""
        echo "Option 2 - SSH Key:"
        echo "1. Generate SSH key: ssh-keygen -t ed25519 -C 'your_email@example.com'"
        echo "2. Add to GitHub: https://github.com/settings/keys"
        echo "3. Change remote: git remote set-url origin git@github.com:Harishs1212/CodeMate-Terminal.git"
        echo "4. Push: git push -u origin main"
        echo ""
        echo "Option 3 - Manual Upload:"
        echo "1. Go to https://github.com/Harishs1212/CodeMate-Terminal"
        echo "2. Click 'uploading an existing file'"
        echo "3. Drag all files from this directory"
        echo "4. Commit with message: 'Initial commit: AI-Powered CodeMate Terminal'"
    fi
else
    echo "❌ Git repository not found. Please run:"
    echo "   git init"
    echo "   git remote add origin https://github.com/Harishs1212/CodeMate-Terminal.git"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git push -u origin main"
fi

echo ""
echo "📱 After successful push, your terminal will be available at:"
echo "   https://your-project-name.vercel.app"