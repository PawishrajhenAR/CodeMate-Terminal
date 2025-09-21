# 🚀 CodeMate Terminal Web Edition - Complete Setup Guide

## 🎨 **UI Design - Gemini/Cursor CLI Style**
The terminal now looks exactly like **Gemini CLI** or **Cursor CLI**:
- **Dark theme**: GitHub dark colors (`#0d1117` background, `#e6edf3` text)
- **Modern fonts**: SF Mono, Monaco, Inconsolata, Roboto Mono
- **Blue accents**: `#58a6ff` for prompts and highlights
- **Clean borders**: Subtle gray borders (`#30363d`)
- **Rounded corners**: Modern 6px border radius
- **Arrow prompt**: `➜` instead of traditional `$`

## 🖥️ **How to Run the Python Backend**

### **Method 1: Simple Start (Recommended)**
```bash
cd maccodemate
python start.py
```

### **Method 2: Direct Server Start**
```bash
cd maccodemate
python run_local_server.py
```

### **Method 3: Windows Batch File**
```bash
cd maccodemate
start_server.bat
```

### **Method 4: Unix Shell Script**
```bash
cd maccodemate
./start_server.sh
```

## 🌐 **Access the Terminal**
Once the server starts, open your browser and go to:
**http://localhost:3000**

## 🔧 **What Happens When You Start:**

1. **Server starts** on port 3000
2. **Browser opens automatically** (if possible)
3. **Permission screen** appears first
4. **User grants access** → Welcome screen with system info
5. **User clicks "START TERMINAL"** → Full terminal interface

## 📁 **File Structure (Always work in maccodemate folder):**
```
maccodemate/
├── api/
│   └── terminal.py          # Backend API
├── public/
│   └── index.html           # Frontend (Gemini/Cursor style)
├── start.py                 # Simple startup script
├── run_local_server.py      # Main server
├── start_server.bat         # Windows startup
├── start_server.sh          # Unix startup
├── test_connection.py       # Test script
├── test_web_terminal.py     # Full test suite
├── requirements.txt         # Python dependencies
├── vercel.json             # Vercel config
└── deploy_web.sh           # Deploy script
```

## 🚀 **Deploy to Vercel**
```bash
cd maccodemate
bash deploy_web.sh
```

## 🧪 **Test the Terminal**
```bash
cd maccodemate
python test_connection.py
```

## ✨ **Features Available:**
- **AI Natural Language Processing**
- **Real-time Command Execution**
- **Command History & Auto-completion**
- **System Monitoring**
- **File Operations**
- **CodeMate Integration**
- **Cross-platform Web Access**

## 🎯 **Terminal Commands:**
- `ls`, `cd`, `pwd`, `mkdir`, `rm`, `cp`, `mv`
- `ps`, `top`, `free`, `df`, `du`
- `find`, `grep`, `which`, `whereis`
- `help`, `clear`, `history`
- `codemate status`, `codemate debug`
- `ask "question"`, `translate "text"`

## 🤖 **AI Examples:**
- "create a folder called test"
- "show me my files"
- "what's my memory usage"
- "create a new folder called demo and move file1.txt into it"

---

**Always work inside the `maccodemate` folder for all operations!**
