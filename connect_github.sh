#!/bin/bash

echo "🔗 Cursor to GitHub Connection Helper"
echo "===================================="

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Please run this script from the maccodemate directory"
    echo "   cd /Users/harish/Downloads/CodeMate/maccodemate"
    exit 1
fi

echo "✅ Found CodeMate Terminal project"
echo "📁 Current directory: $(pwd)"
echo ""

# Check git configuration
echo "🔧 Current Git Configuration:"
echo "Repository: $(git remote get-url origin)"
echo "Branch: $(git branch --show-current)"
echo "User: $(git config user.name)"
echo "Email: $(git config user.email)"
echo ""

# Check git status
echo "📦 Git Status:"
git status --short
echo ""

echo "🚀 EASIEST METHOD - Personal Access Token:"
echo "=========================================="
echo ""
echo "1. 🌐 Go to: https://github.com/settings/tokens"
echo "2. ➕ Click 'Generate new token (classic)'"
echo "3. 📝 Note: 'CodeMate Terminal Access'"
echo "4. ⏰ Expiration: 90 days"
echo "5. ✅ Scopes: Select 'repo'"
echo "6. 🔑 Click 'Generate token'"
echo "7. 📋 COPY THE TOKEN (you won't see it again!)"
echo ""
echo "8. 💻 Then run this command:"
echo "   git push -u origin main"
echo ""
echo "9. 📝 When prompted:"
echo "   Username: Harishs1212"
echo "   Password: [paste your token]"
echo ""

echo "🔄 Alternative - Manual Upload:"
echo "==============================="
echo ""
echo "1. 🌐 Go to: https://github.com/Harishs1212/CodeMate-Terminal"
echo "2. 📁 Click 'uploading an existing file'"
echo "3. 📦 Drag all files from this directory"
echo "4. 💾 Commit message: 'AI-Powered CodeMate Terminal'"
echo "5. ✅ Click 'Commit changes'"
echo ""

echo "🧪 After GitHub Push - Deploy to Vercel:"
echo "========================================"
echo ""
echo "1. 🌐 Go to: https://vercel.com"
echo "2. 🔐 Sign in with GitHub"
echo "3. ➕ Click 'New Project'"
echo "4. 📥 Import 'Harishs1212/CodeMate-Terminal'"
echo "5. 🚀 Deploy automatically!"
echo ""

echo "🎯 Your terminal will be live at:"
echo "   https://your-project-name.vercel.app"
echo ""

echo "📋 Files ready for upload:"
echo "========================="
ls -la | grep -E "\.(py|json|html|md|sh|txt)$" | head -10
if [ $(ls -la | grep -E "\.(py|json|html|md|sh|txt)$" | wc -l) -gt 10 ]; then
    echo "... and $(($(ls -la | grep -E "\.(py|json|html|md|sh|txt)$" | wc -l) - 10)) more files"
fi
