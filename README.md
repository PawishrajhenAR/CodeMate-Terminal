# CodeMate Terminal - AI-Powered Web Terminal

![CodeMate Terminal](https://img.shields.io/badge/CodeMate-Terminal-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🚀 Live Demo

Experience the AI-powered terminal interface with natural language processing capabilities.

## ✨ Features

- **🤖 AI Natural Language Processing** - Execute commands using natural language
- **⚡ Real-time Command Execution** - Instant command processing and output
- **📝 Command History & Auto-completion** - Smart command suggestions
- **📊 System Monitoring** - Real-time system stats and process monitoring
- **📁 File Operations** - Complete file system access and manipulation
- **🔧 CodeMate Integration** - AI-powered code analysis and debugging
- **🌐 Cross-platform Web Access** - Works on any device with a browser
- **🎨 Modern UI** - Sleek terminal interface with Gemini CLI styling

## 🖥️ Terminal Capabilities

### Basic Commands
```bash
ls          # List directory contents
pwd         # Print working directory
cd          # Change directory
mkdir       # Create directories
rm          # Remove files/directories
cat         # Display file contents
cp          # Copy files
mv          # Move/rename files
```

### System Commands
```bash
ps          # Show running processes
free        # Display memory usage
df          # Show disk usage
uptime      # System uptime
whoami      # Current user
system_info # Detailed system information
```

### AI-Powered Features
```bash
ask "how do I create a folder?"
translate "show me my files"
codemate debug filename.py
codemate review code.js
codemate optimize script.py
```

### Natural Language Examples
- "create a folder called test"
- "show me my files"
- "what's my memory usage?"
- "create a new folder called demo and move file1.txt into it"
- "find files called readme"
- "search for function in *.py files"

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python 3.9+ with HTTP server
- **Libraries**: psutil for system monitoring
- **Deployment**: Vercel serverless functions
- **AI Integration**: Natural language processing engine

## 📦 Local Development

### Prerequisites
- Python 3.9 or higher
- Git

### Quick Start
```bash
# Clone the repository
git clone https://github.com/PawishrajhenAR/CodeMate-Terminal.git
cd CodeMate-Terminal

# Install dependencies
pip install -r requirements.txt

# Run local server
python run_local_server.py
```

Open your browser and navigate to `http://localhost:3000`

## 🚀 Deployment

### Deploy to Vercel

1. **Via Vercel CLI:**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

2. **Via GitHub Integration:**
- Connect your GitHub repository to Vercel
- Auto-deployment on every push to main branch

3. **Manual Deployment:**
- Upload project files to Vercel dashboard
- Configure build settings

### Environment Variables
No environment variables required for basic functionality.

## 📁 Project Structure

```
CodeMate-Terminal/
├── api/
│   └── terminal.py          # Backend API handler
├── public/
│   └── index.html          # Frontend interface
├── vercel.json             # Vercel configuration
├── requirements.txt        # Python dependencies
├── run_local_server.py     # Local development server
└── README.md              # This file
```

## 🎯 Key Features Explained

### Permission System
- Clean permission request interface
- Direct access to terminal after approval
- No intermediate screens

### Terminal Interface
- Fixed input bar at bottom (always visible)
- Automatic scrolling when output exceeds view
- Command history navigation (↑/↓ arrows)
- Tab completion for commands
- Click-to-focus functionality

### AI Natural Language Processing
- Converts natural language to terminal commands
- Smart command translation
- Context-aware responses
- Multi-step command support

### File Operations
- All operations work in current working directory
- Relative path support
- Error handling and feedback
- Progress indication for long operations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for CodeMate.ai Hackathon
- Inspired by modern terminal interfaces
- Thanks to the open-source community

## 📞 Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the documentation
- Review the troubleshooting guide

---

**Made with ❤️ for the CodeMate.ai Hackathon**
