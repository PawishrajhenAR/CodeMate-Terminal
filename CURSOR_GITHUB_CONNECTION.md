# 🔗 Connect Cursor to GitHub - Complete Guide

## 📋 Current Git Configuration
✅ **Repository**: `https://github.com/Harishs1212/CodeMate-Terminal.git`
✅ **Remote**: `origin` (configured)
✅ **Branch**: `main`
✅ **Credential Helper**: `store` (configured)

## 🚀 Method 1: Personal Access Token (Recommended)

### Step 1: Create GitHub Personal Access Token
1. **Go to GitHub Settings**:
   - Visit: https://github.com/settings/tokens
   - Click "Generate new token (classic)"

2. **Configure Token**:
   - **Note**: "CodeMate Terminal Access"
   - **Expiration**: 90 days (or your preference)
   - **Scopes**: Select `repo` (Full control of private repositories)

3. **Generate and Copy Token**:
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately (you won't see it again)

### Step 2: Configure Git Credentials
```bash
cd /Users/harish/Downloads/CodeMate/maccodemate

# Set up credentials
git config --global credential.helper store

# Try to push (will prompt for credentials)
git push -u origin main
# Username: Harishs1212
# Password: [paste your token here]
```

## 🚀 Method 2: SSH Key Setup

### Step 1: Generate SSH Key
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "harish@example.com"

# When prompted:
# - Press Enter for default file location
# - Enter passphrase (optional but recommended)
```

### Step 2: Add SSH Key to GitHub
1. **Copy Public Key**:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. **Add to GitHub**:
   - Go to: https://github.com/settings/keys
   - Click "New SSH key"
   - **Title**: "MacBook Pro - CodeMate Terminal"
   - **Key**: Paste the public key
   - Click "Add SSH key"

### Step 3: Update Git Remote
```bash
cd /Users/harish/Downloads/CodeMate/maccodemate

# Change to SSH URL
git remote set-url origin git@github.com:Harishs1212/CodeMate-Terminal.git

# Test connection
ssh -T git@github.com

# Push code
git push -u origin main
```

## 🚀 Method 3: GitHub CLI (If Available)

### Install GitHub CLI
```bash
# Install via Homebrew
brew install gh

# Login to GitHub
gh auth login
# Choose: GitHub.com
# Choose: HTTPS
# Choose: Yes (authenticate Git with GitHub credentials)
# Choose: Login with a web browser
```

### Push Code
```bash
cd /Users/harish/Downloads/CodeMate/maccodemate
gh repo create Harishs1212/CodeMate-Terminal --public --source=. --remote=origin --push
```

## 🚀 Method 4: Manual Upload (Easiest)

### Upload via GitHub Web Interface
1. **Go to Repository**:
   - Visit: https://github.com/Harishs1212/CodeMate-Terminal

2. **Upload Files**:
   - Click "uploading an existing file"
   - Drag all files from `/Users/harish/Downloads/CodeMate/maccodemate/`
   - Commit message: "AI-Powered CodeMate Terminal - Web Interface"
   - Click "Commit changes"

## 🧪 Test Connection

### Verify Git Configuration
```bash
cd /Users/harish/Downloads/CodeMate/maccodemate

# Check remote
git remote -v

# Check status
git status

# Check configuration
git config --list | grep user
```

### Test Push
```bash
# Add any new files
git add .

# Commit changes
git commit -m "Update: Connect to GitHub"

# Push to GitHub
git push -u origin main
```

## 🔧 Troubleshooting

### If Authentication Fails:
1. **Check Token Permissions**: Ensure `repo` scope is selected
2. **Verify Username**: Use `Harishs1212` (exact case)
3. **Clear Credentials**: `git config --global --unset credential.helper`
4. **Try SSH**: Switch to SSH method if HTTPS fails

### If Repository Not Found:
1. **Check Repository URL**: Ensure it's exactly `https://github.com/Harishs1212/CodeMate-Terminal.git`
2. **Verify Repository Exists**: Visit the URL in browser
3. **Check Permissions**: Ensure you have write access

### If Push Fails:
1. **Pull First**: `git pull origin main`
2. **Resolve Conflicts**: If any merge conflicts
3. **Force Push**: `git push -f origin main` (use carefully)

## 🎯 After Successful Push

### Deploy to Vercel:
1. Go to https://vercel.com
2. Sign in with GitHub
3. Import `Harishs1212/CodeMate-Terminal`
4. Deploy automatically!

### Your Terminal Will Be Live At:
`https://your-project-name.vercel.app`

## 📱 Quick Commands Summary

```bash
# Navigate to project
cd /Users/harish/Downloads/CodeMate/maccodemate

# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push -u origin main
```

## 🎉 Ready to Deploy!

Once connected to GitHub, your AI-powered CodeMate Terminal will be ready for Vercel deployment and hackathon submission!
