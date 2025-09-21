# CodeMate Terminal for macOS

A professional AI-powered terminal designed for the CodeMate.ai hackathon, featuring seamless integration with CodeMate's AI ecosystem and optimized for macOS.

## 🚀 Features

### Core Terminal Functionality
- **File Operations**: `ls`, `cd`, `pwd`, `mkdir`, `rm`, `touch`, `cat`, `cp`, `mv`
- **System Monitoring**: `ps`, `top`, `df`, `du`, `free`, `uptime`, `whoami`, `date`
- **Search & Text**: `find`, `grep`, `which`, `whereis`
- **Utilities**: `echo`, `history`, `clear`, `help`, `exit`
- **Command History**: Persistent command history with arrow key navigation
- **Auto-completion**: Tab completion for commands
- **Error Handling**: Comprehensive error handling for invalid commands

### CodeMate Integration
- **Debug Code**: `codemate debug <file>` - AI-powered code debugging
- **Code Review**: `codemate review <file>` - Professional code review
- **Code Optimization**: `codemate optimize <file>` - Performance optimization
- **Test Generation**: `codemate test <file>` - AI-generated test cases
- **Documentation**: `codemate docs <file>` - Auto-generated documentation
- **AI Chat**: `codemate chat <question>` - Interactive AI assistance
- **Status Check**: `codemate status` - Integration status

### AI Features
- **Natural Language Commands**: Type natural language queries that get converted to terminal commands
- **Complex Multi-Step Commands**: Handle complex operations like "create a new folder called test and move file1.txt into it"
- **Command Chaining**: Automatically convert complex requests to chained commands using &&
- **Question Answering**: Ask questions about commands and CodeMate features
- **Command Translation**: Convert natural language to actual terminal commands
- **Enhanced Auto-Completion**: Tab completion for commands, files, and natural language
- **Advanced History**: Search command history with `history -s <term>`

### Modern UI
- **Professional Banner**: CodeMate-branded ASCII art banner
- **Rich UI**: Tables, panels, and colored output optimized for macOS
- **macOS Integration**: Native Terminal.app integration
- **Professional Design**: Clean, modern interface for hackathon presentation

## 📦 Installation

1. **Clone or download the project files**
2. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements_macos.txt
   ```

## 🚀 Usage

### Basic Usage
Run the CodeMate terminal:
```bash
python3 codemate_terminal.py
```

### Launch in macOS Terminal
To launch the terminal in macOS Terminal.app:

**Python launcher:**
```bash
python3 launch_macos.py
```

## 📋 Command Reference

### File Operations
- `ls [path]` - List directory contents
- `cd [path]` - Change directory
- `pwd` - Print working directory
- `mkdir <dir>` - Create directory
- `rm <file/dir>` - Remove file or directory
- `touch <file>` - Create empty file
- `cat <file>` - Display file contents
- `cp <src> <dest>` - Copy file or directory
- `mv <src> <dest>` - Move/rename file or directory

### System Information
- `ps` - Show running processes
- `top` - Show system processes (interactive)
- `df` - Show disk usage
- `du <path>` - Show directory size
- `free` - Show memory usage
- `uptime` - Show system uptime
- `whoami` - Show current user
- `date` - Show current date/time

### CodeMate Integration
- `codemate debug <file>` - Debug code with CodeMate AI
- `codemate review <file>` - Review code with CodeMate
- `codemate optimize <file>` - Optimize code with CodeMate
- `codemate test <file>` - Generate test cases with CodeMate
- `codemate docs <file>` - Generate documentation with CodeMate
- `codemate chat <question>` - Chat with CodeMate AI
- `codemate status` - Check CodeMate integration status

### AI Features
- `ask <question>` - Ask natural language questions
- `translate <text>` - Convert natural language to commands

### 🤖 AI Natural Language Examples

#### Simple Commands:
```bash
# Create operations
"create a folder called test"           → mkdir test
"make a file named readme.txt"         → touch readme.txt
"show me my files"                     → ls
"what's my memory usage"               → free
"go to the documents folder"           → cd documents
```

#### Complex Multi-Step Commands:
```bash
# Create and move operations
"create a new folder called test and move file1.txt into it"
→ mkdir test && mv file1.txt test/

# Backup operations
"make a backup folder and copy all .py files to it"
→ mkdir backup && cp *.py backup/

# File organization
"organize all .txt files into a documents folder"
→ mkdir documents && mv *.txt documents/
```

#### Enhanced Features:
- **Tab Completion**: Press Tab for intelligent command and file completion
- **Command History**: Use ↑↓ arrows or Ctrl+R to search history
- **History Search**: `history -s <term>` to search command history
- **Command Chaining**: Use && to chain commands together

### Utilities
- `echo <text>` - Print text
- `history` - Show command history
- `clear` - Clear screen
- `help` - Show help
- `exit/quit` - Exit terminal

## 💡 Examples

### Basic File Operations
```bash
$ mkdir codemate_project
$ cd codemate_project
$ touch main.py
$ echo "print('Hello CodeMate!')" > main.py
$ cat main.py
$ ls
```

### CodeMate Integration
```bash
$ codemate debug main.py
$ codemate review main.py
$ codemate optimize main.py
$ codemate test main.py
$ codemate docs main.py
$ codemate chat "How do I optimize this code?"
$ codemate status
```

### AI-Powered Commands
```bash
$ ask how to debug code with CodeMate
$ translate create a project folder and debug the main file
$ ask what CodeMate features are available
```

### System Monitoring
```bash
$ ps
$ top
$ free
$ df
$ uptime
```

## 🏗️ Project Structure

```
CodeMate-Terminal/
├── codemate_terminal.py    # 🎨 Main terminal with CodeMate integration
├── launch_macos.py        # 🪟 macOS launcher for Terminal.app
├── requirements_macos.txt # 📦 macOS-specific dependencies
└── README.md              # 📚 Documentation
```

## 🔧 Requirements

- **macOS**: 10.14+ (Mojave or later)
- **Python**: 3.6+
- **Dependencies**:
  - psutil (for system monitoring)
  - pathlib2 (for enhanced path operations)
  - rich (for beautiful UI)
  - colorama (for cross-platform colors)

## 🎯 CodeMate.ai Integration

This terminal is designed to showcase integration with [CodeMate.ai](https://docs.codemate.ai/) features:

- **Debug Code Agent**: AI-powered debugging assistance
- **Code Review Agent**: Professional code review capabilities
- **Optimize Code Agent**: Performance optimization suggestions
- **Generate Test Cases Agent**: Automated test case generation
- **Swagger Agent**: API documentation integration
- **Knowledge Base**: Access to CodeMate's knowledge repository

## 🏆 Hackathon Features

### Professional Presentation
- **Branded Interface**: CodeMate-themed design
- **Professional Banner**: ASCII art showcasing CodeMate branding
- **Rich UI**: Modern, clean interface suitable for presentations
- **macOS Optimization**: Native macOS Terminal.app integration

### Demo Capabilities
- **Live Code Analysis**: Demonstrate CodeMate's AI capabilities
- **Interactive Commands**: Show real-time AI assistance
- **Professional Output**: Clean, formatted results for judges
- **Cross-Platform**: Works seamlessly on macOS

## 🚀 Getting Started for Hackathon

1. **Quick Setup**:
   ```bash
   git clone <repository>
   cd CodeMate-Terminal
   pip3 install -r requirements_macos.txt
   python3 launch_macos.py
   ```

2. **Demo Commands**:
   ```bash
   codemate status
   ask how does CodeMate help with debugging?
   translate create a Python file and review it with CodeMate
   ```

3. **Showcase Features**:
   - Professional UI with CodeMate branding
   - AI-powered command interpretation
   - Integration with CodeMate.ai ecosystem
   - macOS-native terminal experience

## 📄 License

This project is created for the CodeMate.ai hackathon and is provided as-is for educational and demonstration purposes.

## 🤝 Contributing

This project is part of the CodeMate.ai hackathon. For questions or contributions, please refer to the hackathon guidelines.

---

**Built for CodeMate.ai Hackathon** 🚀
