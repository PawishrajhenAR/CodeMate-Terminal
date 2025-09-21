from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import subprocess
import re
import shutil
import glob
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path

# Try to import psutil, fallback if not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    import platform
    PLATFORM_AVAILABLE = True
except ImportError:
    PLATFORM_AVAILABLE = False

class TerminalAPI:
    """Enhanced API wrapper for CodeMate Terminal functionality."""
    
    def __init__(self):
        # Start in C: drive by default (Windows) or root directory (Unix)
        if os.name == 'nt':  # Windows
            self.current_path = 'C:\\'
        else:  # Unix/Linux/Mac
            self.current_path = '/'
        self.command_history = []
        self.session_id = f"session_{int(time.time())}"
        
        # Initialize system info
        self.system_info = self._get_system_info()
        
        # Enhanced AI patterns for natural language processing
        self.ai_patterns = {
            # Complex multi-step commands (check these first)
            'create_and_move': [
                r'create\s+(?:a\s+)?(?:new\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+move\s+([^\s]+)\s+(?:to|into)\s+(?:it|that\s+folder)',
                r'make\s+(?:a\s+)?(?:new\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+move\s+([^\s]+)\s+(?:to|into)\s+(?:it|that\s+folder)',
                r'new\s+(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+move\s+([^\s]+)\s+(?:to|into)\s+(?:it|that\s+folder)',
                r'create\s+(?:a\s+)?(?:new\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+move\s+([^\s]+)\s+(?:to|into)\s+it',
                r'make\s+(?:a\s+)?(?:new\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+move\s+([^\s]+)\s+(?:to|into)\s+it'
            ],
            'create_and_copy': [
                r'create\s+(?:a\s+)?(?:new\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+copy\s+([^\s]+)\s+(?:to|into)\s+(?:it|that\s+folder)',
                r'make\s+(?:a\s+)?(?:new\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+copy\s+([^\s]+)\s+(?:to|into)\s+(?:it|that\s+folder)',
                r'new\s+(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+copy\s+([^\s]+)\s+(?:to|into)\s+(?:it|that\s+folder)'
            ],
            'backup_files': [
                r'create\s+(?:a\s+)?(?:backup|backup\s+folder)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+copy\s+(?:all\s+)?([^\s]+)\s+(?:files\s+)?(?:to|into)\s+(?:it|that\s+folder)',
                r'make\s+(?:a\s+)?(?:backup|backup\s+folder)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+copy\s+(?:all\s+)?([^\s]+)\s+(?:files\s+)?(?:to|into)\s+(?:it|that\s+folder)'
            ],
            'organize_files': [
                r'create\s+(?:a\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+move\s+(?:all\s+)?([^\s]+)\s+(?:files\s+)?(?:to|into)\s+(?:it|that\s+folder)',
                r'organize\s+(?:all\s+)?([^\s]+)\s+(?:files\s+)?(?:into\s+)?(?:a\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)'
            ],
            
            # Simple single commands
            'create_folder': [
                r'create\s+(?:a\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)',
                r'make\s+(?:a\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)',
                r'new\s+(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)',
                r'add\s+(?:a\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)'
            ],
            'create_file': [
                r'create\s+(?:a\s+)?(?:file|document)\s+(?:called\s+|named\s+)?([^\s]+)',
                r'make\s+(?:a\s+)?(?:file|document)\s+(?:called\s+|named\s+)?([^\s]+)',
                r'new\s+(?:file|document)\s+(?:called\s+|named\s+)?([^\s]+)',
                r'add\s+(?:a\s+)?(?:file|document)\s+(?:called\s+|named\s+)?([^\s]+)'
            ],
            'move_file': [
                r'move\s+([^\s]+)\s+(?:to|into)\s+([^\s]+)',
                r'put\s+([^\s]+)\s+(?:in|into)\s+([^\s]+)',
                r'transfer\s+([^\s]+)\s+(?:to|into)\s+([^\s]+)',
                r'relocate\s+([^\s]+)\s+(?:to|into)\s+([^\s]+)'
            ],
            'copy_file': [
                r'copy\s+([^\s]+)\s+(?:to|into)\s+([^\s]+)',
                r'duplicate\s+([^\s]+)\s+(?:to|into)\s+([^\s]+)',
                r'backup\s+([^\s]+)\s+(?:to|into)\s+([^\s]+)'
            ],
            'delete_file': [
                r'delete\s+([^\s]+)',
                r'remove\s+([^\s]+)',
                r'erase\s+([^\s]+)',
                r'get\s+rid\s+of\s+([^\s]+)'
            ],
            'list_files': [
                r'list\s+(?:files|contents)',
                r'show\s+(?:files|contents)',
                r'show\s+me\s+(?:my\s+)?(?:files|contents)',
                r'what\s+(?:files|is)\s+in\s+(?:this\s+)?directory',
                r'display\s+(?:files|contents)',
                r'see\s+(?:files|contents)'
            ],
            'change_directory': [
                r'go\s+(?:to\s+|into\s+)?(?:the\s+)?([^\s]+(?:\s+[^\s]+)*)',
                r'navigate\s+(?:to\s+)?(?:the\s+)?([^\s]+(?:\s+[^\s]+)*)',
                r'enter\s+(?:the\s+)?([^\s]+(?:\s+[^\s]+)*)',
                r'change\s+(?:to\s+)?(?:the\s+)?([^\s]+(?:\s+[^\s]+)*)',
                r'switch\s+(?:to\s+)?(?:the\s+)?([^\s]+(?:\s+[^\s]+)*)'
            ],
            'show_help': [
                r'help\s+(?:me\s+)?(?:with\s+)?(?:commands|terminal)',
                r'what\s+(?:commands|can)\s+i\s+(?:use|do)',
                r'how\s+do\s+i\s+(?:use|work\s+with)\s+this',
                r'show\s+me\s+(?:the\s+)?(?:commands|help)'
            ],
            'system_info': [
                r'what\s+(?:is\s+)?(?:my\s+)?(?:system|computer)\s+(?:info|information)',
                r'show\s+(?:me\s+)?(?:system|computer)\s+(?:info|information)',
                r'tell\s+me\s+(?:about\s+)?(?:my\s+)?(?:system|computer)',
                r'display\s+(?:system|computer)\s+(?:info|information)'
            ],
            'process_info': [
                r'what\s+(?:are\s+)?(?:the\s+)?(?:running\s+)?processes',
                r'show\s+(?:me\s+)?(?:the\s+)?(?:running\s+)?processes',
                r'list\s+(?:the\s+)?(?:running\s+)?processes',
                r'display\s+(?:the\s+)?(?:running\s+)?processes'
            ],
            'memory_info': [
                r'what\s+(?:is\s+)?(?:my\s+)?(?:memory|ram)\s+(?:usage|info)',
                r'show\s+(?:me\s+)?(?:memory|ram)\s+(?:usage|info)',
                r'tell\s+me\s+(?:about\s+)?(?:my\s+)?(?:memory|ram)',
                r'display\s+(?:memory|ram)\s+(?:usage|info)'
            ],
            'cpu_info': [
                r'what\s+(?:is\s+)?(?:my\s+)?(?:cpu|processor)\s+(?:usage|info)',
                r'show\s+(?:me\s+)?(?:cpu|processor)\s+(?:usage|info)',
                r'tell\s+me\s+(?:about\s+)?(?:my\s+)?(?:cpu|processor)',
                r'display\s+(?:cpu|processor)\s+(?:usage|info)'
            ],
            'codemate_commands': [
                r'debug\s+(?:this\s+)?(?:code\s+)?(?:file\s+)?([^\s]+)',
                r'review\s+(?:this\s+)?(?:code\s+)?(?:file\s+)?([^\s]+)',
                r'optimize\s+(?:this\s+)?(?:code\s+)?(?:file\s+)?([^\s]+)',
                r'test\s+(?:this\s+)?(?:code\s+)?(?:file\s+)?([^\s]+)',
                r'document\s+(?:this\s+)?(?:code\s+)?(?:file\s+)?([^\s]+)'
            ],
            'find_files': [
                r'find\s+(?:files\s+)?(?:called\s+|named\s+)?([^\s]+)',
                r'search\s+(?:for\s+)?(?:files\s+)?(?:called\s+|named\s+)?([^\s]+)',
                r'locate\s+(?:files\s+)?(?:called\s+|named\s+)?([^\s]+)'
            ],
            'grep_search': [
                r'search\s+(?:for\s+)?(?:text\s+)?([^\s]+)\s+(?:in\s+)?(?:files\s+)?([^\s]+)',
                r'find\s+(?:text\s+)?([^\s]+)\s+(?:in\s+)?(?:files\s+)?([^\s]+)',
                r'grep\s+([^\s]+)\s+(?:in\s+)?([^\s]+)'
            ]
        }
    
    def _get_system_info(self) -> Dict[str, str]:
        """Get system information."""
        info = {
            "platform": "Unknown",
            "python_version": sys.version.split()[0],
            "user": os.getenv('USER', 'unknown'),
            "current_directory": self.current_path,
            "psutil_available": str(PSUTIL_AVAILABLE),
            "platform_available": str(PLATFORM_AVAILABLE)
        }
        
        if PLATFORM_AVAILABLE:
            try:
                info["platform"] = f"{platform.system()} {platform.release()}"
                info["architecture"] = platform.machine()
            except:
                pass
        
        if PSUTIL_AVAILABLE:
            try:
                info["cpu_count"] = str(psutil.cpu_count())
                info["memory_total"] = f"{psutil.virtual_memory().total // (1024**3)} GB"
            except:
                pass
        
        return info
    
    def get_system_banner(self) -> str:
        """Get CodeMate ASCII banner."""
        banner = """
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                       ║
║      ██████╗ ██████╗ ██████╗ ███████╗███╗   ███╗ █████╗ ████████╗███████╗          ║
║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗ ████║██╔══██╗╚══██╔══╝██╔════╝          ║
║     ██║     ██║   ██║██║  ██║█████╗  ██╔████╔██║███████║   ██║   █████╗            ║
║     ██║     ██║   ██║██║  ██║██╔══╝  ██║╚██╔╝██║██╔══██║   ██║   ██╔══╝            ║
║     ╚██████╗╚██████╔╝██████╔╝███████╗██║ ╚═╝ ██║██║  ██║   ██║   ███████╗          ║
║      ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝          ║
║                                                                                       ║
║                           AI-Powered Terminal                                        ║
║                         CodeMate.ai Hackathon                                        ║
║                                                                                       ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
"""
        return banner.strip()
    
    def get_welcome_info(self) -> Dict[str, any]:
        """Get comprehensive welcome information."""
        info = {
            "banner": self.get_system_banner(),
            "system_info": self.system_info,
            "features": [
                "AI Natural Language Processing",
                "Real-time Command Execution", 
                "Command History & Auto-completion",
                "System Monitoring",
                "File Operations",
                "CodeMate Integration",
                "Cross-platform Web Access"
            ],
            "ai_examples": [
                "create a folder called test",
                "show me my files", 
                "what's my memory usage",
                "create a new folder called demo and move file1.txt into it",
                "find files called readme",
                "search for function in *.py files",
                "tell me about my system",
                "debug this code file"
            ],
            "permission_granted": True,
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat()
        }
        return info
    
    def process_natural_language(self, command: str) -> Optional[str]:
        """Process natural language commands and convert them to terminal commands."""
        command_lower = command.lower().strip()
        
        # Check each pattern category
        for category, patterns in self.ai_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, command_lower)
                if match:
                    if category == 'create_folder':
                        folder_name = match.group(1)
                        return f"mkdir {folder_name}"
                    elif category == 'create_file':
                        file_name = match.group(1)
                        return f"touch {file_name}"
                    elif category == 'move_file':
                        source, dest = match.groups()
                        return f"mv {source} {dest}"
                    elif category == 'copy_file':
                        source, dest = match.groups()
                        return f"cp {source} {dest}"
                    elif category == 'delete_file':
                        file_name = match.group(1)
                        return f"rm {file_name}"
                    elif category == 'list_files':
                        return "ls"
                    elif category == 'change_directory':
                        dir_name = match.group(1)
                        return f"cd {dir_name}"
                    elif category == 'show_help':
                        return "help"
                    elif category == 'system_info':
                        return "system_info"
                    elif category == 'process_info':
                        return "ps"
                    elif category == 'memory_info':
                        return "free"
                    elif category == 'cpu_info':
                        return "cpu"
                    elif category == 'codemate_commands':
                        file_name = match.group(1)
                        if 'debug' in command_lower:
                            return f"codemate debug {file_name}"
                        elif 'review' in command_lower:
                            return f"codemate review {file_name}"
                        elif 'optimize' in command_lower:
                            return f"codemate optimize {file_name}"
                        elif 'test' in command_lower:
                            return f"codemate test {file_name}"
                        elif 'document' in command_lower:
                            return f"codemate docs {file_name}"
                    elif category == 'find_files':
                        file_pattern = match.group(1)
                        return f"find . -name '*{file_pattern}*'"
                    elif category == 'grep_search':
                        if len(match.groups()) == 2:
                            search_text, file_pattern = match.groups()
                            return f"grep '{search_text}' {file_pattern}"
                        else:
                            search_text = match.group(1)
                            return f"grep '{search_text}' *"
                    
                    # Complex multi-step commands
                    elif category == 'create_and_move':
                        folder_name, file_name = match.groups()
                        return f"mkdir {folder_name} && mv {file_name} {folder_name}/"
                    elif category == 'create_and_copy':
                        folder_name, file_name = match.groups()
                        return f"mkdir {folder_name} && cp {file_name} {folder_name}/"
                    elif category == 'backup_files':
                        backup_name, file_pattern = match.groups()
                        return f"mkdir {backup_name} && cp {file_pattern}* {backup_name}/"
                    elif category == 'organize_files':
                        if len(match.groups()) == 2:
                            file_pattern, folder_name = match.groups()
                            return f"mkdir {folder_name} && mv {file_pattern}* {folder_name}/"
                        else:
                            folder_name, file_pattern = match.groups()
                            return f"mkdir {folder_name} && mv {file_pattern}* {folder_name}/"
        
        return None
    
    def execute_command(self, command: str, natural_language: bool = False) -> Dict[str, any]:
        """Execute a command and return structured output."""
        if not command.strip():
            return {"output": "", "exit_code": 0, "error": None}
        
        # Add to history
        self.command_history.append(command.strip())
        
        # Process natural language if requested
        ai_translation = None
        if natural_language:
            ai_command = self.process_natural_language(command)
            if ai_command:
                ai_translation = ai_command
                command = ai_command
            else:
                return {
                    "output": f"Could not understand natural language command: '{command}'",
                    "exit_code": 1,
                    "error": "Natural language processing failed",
                    "ai_translation": None
                }
        
        # Check for command chaining (&&)
        if ' && ' in command:
            result = self._execute_command_chain(command)
            result["ai_translation"] = ai_translation
            return result
        
        # Parse command
        parts = command.strip().split()
        if not parts:
            return {"output": "", "exit_code": 0, "error": None, "ai_translation": ai_translation}
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        # Handle built-in commands
        if cmd in self._get_builtin_commands():
            output, exit_code = self._execute_builtin(cmd, args)
            return {"output": output, "exit_code": exit_code, "error": None, "ai_translation": ai_translation}
        
        # Execute external command
        output, exit_code = self._execute_external(command)
        return {"output": output, "exit_code": exit_code, "error": None, "ai_translation": ai_translation}
    
    def _execute_command_chain(self, command: str) -> Dict[str, any]:
        """Execute a chain of commands separated by &&."""
        commands = [cmd.strip() for cmd in command.split(' && ')]
        output_lines = []
        exit_code = 0
        
        for i, cmd in enumerate(commands):
            cmd_output, cmd_exit_code = self._execute_single_command(cmd)
            
            if cmd_output:
                output_lines.append(f"Step {i+1}: {cmd_output}")
            
            if cmd_exit_code != 0:
                exit_code = cmd_exit_code
                output_lines.append(f"Command failed with exit code {cmd_exit_code}")
                break  # Stop execution on first failure
        
        return {
            "output": "\n".join(output_lines),
            "exit_code": exit_code,
            "error": None if exit_code == 0 else f"Command chain failed at step {i+1}"
        }
    
    def _execute_single_command(self, command: str) -> Tuple[str, int]:
        """Execute a single command."""
        parts = command.strip().split()
        if not parts:
            return "", 0
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        # Handle built-in commands
        if cmd in self._get_builtin_commands():
            return self._execute_builtin(cmd, args)
        
        # Execute external command
        return self._execute_external(command)
    
    def _get_builtin_commands(self) -> List[str]:
        """Get list of built-in commands."""
        return [
            'ls', 'pwd', 'cd', 'mkdir', 'rm', 'rmdir', 'touch', 'cat', 'cp', 'mv',
            'ps', 'free', 'df', 'du', 'uptime', 'whoami', 'date', 'find', 'grep',
            'which', 'whereis', 'echo', 'help', 'exit', 'quit', 'clear', 'history', 
            'system_info', 'cpu', 'codemate', 'ask', 'translate'
        ]
    
    def _execute_builtin(self, cmd: str, args: List[str]) -> Tuple[str, int]:
        """Execute built-in commands."""
        try:
            if cmd == 'ls':
                return self._cmd_ls(args)
            elif cmd == 'pwd':
                return self._cmd_pwd(args)
            elif cmd == 'cd':
                return self._cmd_cd(args)
            elif cmd == 'mkdir':
                return self._cmd_mkdir(args)
            elif cmd == 'rm':
                return self._cmd_rm(args)
            elif cmd == 'touch':
                return self._cmd_touch(args)
            elif cmd == 'cat':
                return self._cmd_cat(args)
            elif cmd == 'cp':
                return self._cmd_cp(args)
            elif cmd == 'mv':
                return self._cmd_mv(args)
            elif cmd == 'ps':
                return self._cmd_ps(args)
            elif cmd == 'free':
                return self._cmd_free(args)
            elif cmd == 'df':
                return self._cmd_df(args)
            elif cmd == 'uptime':
                return self._cmd_uptime(args)
            elif cmd == 'whoami':
                return self._cmd_whoami(args)
            elif cmd == 'date':
                return self._cmd_date(args)
            elif cmd == 'system_info':
                return self._cmd_system_info(args)
            elif cmd == 'cpu':
                return self._cmd_cpu(args)
            elif cmd == 'du':
                return self._cmd_du(args)
            elif cmd == 'rmdir':
                return self._cmd_rmdir(args)
            elif cmd == 'find':
                return self._cmd_find(args)
            elif cmd == 'grep':
                return self._cmd_grep(args)
            elif cmd == 'which':
                return self._cmd_which(args)
            elif cmd == 'whereis':
                return self._cmd_whereis(args)
            elif cmd == 'echo':
                return self._cmd_echo(args)
            elif cmd == 'codemate':
                return self._cmd_codemate(args)
            elif cmd == 'ask':
                return self._cmd_ask(args)
            elif cmd == 'translate':
                return self._cmd_translate(args)
            elif cmd == 'help':
                return self._cmd_help(args)
            elif cmd == 'history':
                return self._cmd_history(args)
            elif cmd == 'clear':
                return self._cmd_clear(args)
            else:
                return f"Unknown command: {cmd}", 1
        except Exception as e:
            return f"Error executing {cmd}: {e}", 1
    
    def _execute_external(self, command: str) -> Tuple[str, int]:
        """Execute external commands."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.current_path
            )
            return result.stdout + result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "Command timed out", 1
        except Exception as e:
            return f"Error executing command: {e}", 1
    
    # Built-in command implementations
    def _cmd_ls(self, args: List[str]) -> Tuple[str, int]:
        """List directory contents."""
        try:
            path = args[0] if args else self.current_path
            items = os.listdir(path)
            output = []
            for item in sorted(items):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    output.append(f"📁 {item}/")
                else:
                    output.append(f"📄 {item}")
            return "\n".join(output), 0
        except Exception as e:
            return f"ls: {e}", 1
    
    def _cmd_pwd(self, args: List[str]) -> Tuple[str, int]:
        """Print working directory."""
        return self.current_path, 0
    
    def _cmd_cd(self, args: List[str]) -> Tuple[str, int]:
        """Change directory."""
        if not args:
            self.current_path = os.path.expanduser("~")
            return "", 0
        
        try:
            new_path = os.path.abspath(os.path.join(self.current_path, args[0]))
            if os.path.isdir(new_path):
                self.current_path = new_path
                return "", 0
            else:
                return f"cd: {args[0]}: No such directory", 1
        except Exception as e:
            return f"cd: {e}", 1
    
    def _cmd_mkdir(self, args: List[str]) -> Tuple[str, int]:
        """Create directory."""
        if not args:
            return "mkdir: missing operand", 1
        
        try:
            # Create directory in current working directory
            dir_name = args[0]
            full_path = os.path.join(self.current_path, dir_name)
            os.makedirs(full_path, exist_ok=True)
            return f"Created directory: {dir_name} at {full_path}", 0
        except Exception as e:
            return f"mkdir: {e}", 1
    
    def _cmd_rm(self, args: List[str]) -> Tuple[str, int]:
        """Remove file or directory."""
        if not args:
            return "rm: missing operand", 1
        
        # Handle flags
        recursive = False
        files_to_remove = []
        
        for arg in args:
            if arg.startswith('-'):
                if 'r' in arg or 'R' in arg:
                    recursive = True
                # Skip other flags for now
            else:
                files_to_remove.append(arg)
        
        if not files_to_remove:
            return "rm: missing operand", 1
        
        results = []
        for item in files_to_remove:
            try:
                # Handle relative paths from current directory
                full_path = item
                if not os.path.isabs(item):
                    full_path = os.path.join(self.current_path, item)
                
                if os.path.isdir(full_path):
                    if recursive:
                        import shutil
                        shutil.rmtree(full_path)
                        results.append(f"Removed directory: {item}")
                    else:
                        results.append(f"rm: cannot remove '{item}': Is a directory")
                else:
                    os.remove(full_path)
                    results.append(f"Removed file: {item}")
            except FileNotFoundError:
                results.append(f"rm: cannot remove '{item}': No such file or directory")
            except PermissionError:
                results.append(f"rm: cannot remove '{item}': Permission denied")
            except Exception as e:
                results.append(f"rm: error removing '{item}': {e}")
        
        return "\n".join(results), 0
    
    def _cmd_touch(self, args: List[str]) -> Tuple[str, int]:
        """Create empty file."""
        if not args:
            return "touch: missing operand", 1
        
        try:
            # Create file in current working directory
            file_name = args[0]
            full_path = os.path.join(self.current_path, file_name)
            with open(full_path, 'a'):
                pass
            return f"Created file: {file_name} at {full_path}", 0
        except Exception as e:
            return f"touch: {e}", 1
    
    def _cmd_cat(self, args: List[str]) -> Tuple[str, int]:
        """Display file contents."""
        if not args:
            return "cat: missing operand", 1
        
        try:
            # Handle relative paths from current directory
            file_path = args[0]
            if not os.path.isabs(file_path):
                file_path = os.path.join(self.current_path, file_path)
            
            with open(file_path, 'r') as f:
                return f.read(), 0
        except Exception as e:
            return f"cat: {e}", 1
    
    def _cmd_cp(self, args: List[str]) -> Tuple[str, int]:
        """Copy file or directory."""
        if len(args) < 2:
            return "cp: missing operand", 1
        
        try:
            import shutil
            # Handle relative paths from current directory
            source = args[0]
            dest = args[1]
            
            if not os.path.isabs(source):
                source = os.path.join(self.current_path, source)
            if not os.path.isabs(dest):
                dest = os.path.join(self.current_path, dest)
            
            shutil.copy2(source, dest)
            return f"Copied {args[0]} to {args[1]}", 0
        except Exception as e:
            return f"cp: {e}", 1
    
    def _cmd_mv(self, args: List[str]) -> Tuple[str, int]:
        """Move/rename file or directory."""
        if len(args) < 2:
            return "mv: missing operand", 1
        
        try:
            import shutil
            # Handle relative paths from current directory
            source = args[0]
            dest = args[1]
            
            if not os.path.isabs(source):
                source = os.path.join(self.current_path, source)
            if not os.path.isabs(dest):
                dest = os.path.join(self.current_path, dest)
            
            shutil.move(source, dest)
            return f"Moved {args[0]} to {args[1]}", 0
        except Exception as e:
            return f"mv: {e}", 1
    
    def _cmd_ps(self, args: List[str]) -> Tuple[str, int]:
        """Show running processes."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    info = proc.info
                    processes.append(f"{info['pid']:6d} {info['name']:20s} {info['cpu_percent']:6.1f}%")
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return "\n".join(processes[:20]), 0  # Limit to 20 processes
        except Exception as e:
            return f"ps: {e}", 1
    
    def _cmd_free(self, args: List[str]) -> Tuple[str, int]:
        """Show memory usage."""
        try:
            memory = psutil.virtual_memory()
            return f"""Memory Usage:
Total: {memory.total // (1024**3)} GB
Available: {memory.available // (1024**3)} GB
Used: {memory.used // (1024**3)} GB ({memory.percent:.1f}%)
Free: {memory.free // (1024**3)} GB""", 0
        except Exception as e:
            return f"free: {e}", 1
    
    def _cmd_df(self, args: List[str]) -> Tuple[str, int]:
        """Show disk usage."""
        try:
            disk = psutil.disk_usage('/')
            return f"""Disk Usage:
Total: {disk.total // (1024**3)} GB
Used: {disk.used // (1024**3)} GB
Free: {disk.free // (1024**3)} GB
Usage: {(disk.used / disk.total) * 100:.1f}%""", 0
        except Exception as e:
            return f"df: {e}", 1
    
    def _cmd_uptime(self, args: List[str]) -> Tuple[str, int]:
        """Show system uptime."""
        try:
            uptime = psutil.boot_time()
            current_time = datetime.now().timestamp()
            uptime_seconds = current_time - uptime
            hours = int(uptime_seconds // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            return f"System uptime: {hours}h {minutes}m", 0
        except Exception as e:
            return f"uptime: {e}", 1
    
    def _cmd_whoami(self, args: List[str]) -> Tuple[str, int]:
        """Show current user."""
        return os.getenv('USER', 'unknown'), 0
    
    def _cmd_date(self, args: List[str]) -> Tuple[str, int]:
        """Show current date/time."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0
    
    def _cmd_system_info(self, args: List[str]) -> Tuple[str, int]:
        """Show system information."""
        try:
            info = f"""System Information:
Platform: {platform.system()} {platform.release()}
Architecture: {platform.machine()}
Python: {platform.python_version()}
User: {os.getenv('USER', 'unknown')}
Current Directory: {self.current_path}
CPU Cores: {psutil.cpu_count()}
Memory: {psutil.virtual_memory().total // (1024**3)} GB"""
            return info, 0
        except Exception as e:
            return f"system_info: {e}", 1
    
    def _cmd_cpu(self, args: List[str]) -> Tuple[str, int]:
        """Show CPU usage."""
        if not PSUTIL_AVAILABLE:
            return "CPU info not available (psutil not installed)", 1
        
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            info = f"""CPU Information:
Usage: {cpu_percent:.1f}%
Cores: {cpu_count}
Current Frequency: {cpu_freq.current:.0f} MHz
Min Frequency: {cpu_freq.min:.0f} MHz
Max Frequency: {cpu_freq.max:.0f} MHz"""
            return info, 0
        except Exception as e:
            return f"cpu: {e}", 1
    
    def _cmd_du(self, args: List[str]) -> Tuple[str, int]:
        """Show directory size."""
        path = args[0] if args else self.current_path
        
        try:
            if not PSUTIL_AVAILABLE:
                return "Directory size info not available (psutil not installed)", 1
            
            # Get directory size
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(filepath)
                    except (OSError, IOError):
                        pass
            
            size_mb = total_size / (1024 * 1024)
            return f"Directory size: {size_mb:.2f} MB", 0
        except Exception as e:
            return f"du: {e}", 1
    
    def _cmd_rmdir(self, args: List[str]) -> Tuple[str, int]:
        """Remove empty directory."""
        if not args:
            return "rmdir: missing operand", 1
        
        try:
            os.rmdir(args[0])
            return f"Removed directory: {args[0]}", 0
        except OSError as e:
            return f"rmdir: {e}", 1
        except Exception as e:
            return f"rmdir: {e}", 1
    
    def _cmd_find(self, args: List[str]) -> Tuple[str, int]:
        """Find files."""
        if not args:
            return "find: missing search pattern", 1
        
        try:
            pattern = args[0]
            results = []
            
            for root, dirs, files in os.walk(self.current_path):
                for file in files:
                    if pattern in file:
                        results.append(os.path.join(root, file))
            
            if results:
                return "\n".join(results[:20]), 0  # Limit to 20 results
            else:
                return f"No files found matching '{pattern}'", 0
        except Exception as e:
            return f"find: {e}", 1
    
    def _cmd_grep(self, args: List[str]) -> Tuple[str, int]:
        """Search for text in files."""
        if len(args) < 1:
            return "grep: missing search pattern", 1
        
        try:
            pattern = args[0]
            file_pattern = args[1] if len(args) > 1 else "*"
            
            results = []
            for root, dirs, files in os.walk(self.current_path):
                for file in files:
                    if file_pattern == "*" or file.endswith(file_pattern.replace("*", "")):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                                for line_num, line in enumerate(f, 1):
                                    if pattern in line:
                                        results.append(f"{filepath}:{line_num}: {line.strip()}")
                        except (OSError, IOError, UnicodeDecodeError):
                            continue
            
            if results:
                return "\n".join(results[:20]), 0  # Limit to 20 results
            else:
                return f"No matches found for '{pattern}'", 0
        except Exception as e:
            return f"grep: {e}", 1
    
    def _cmd_which(self, args: List[str]) -> Tuple[str, int]:
        """Find command location."""
        if not args:
            return "which: missing command name", 1
        
        try:
            command = args[0]
            # Simple which implementation
            path_dirs = os.environ.get('PATH', '').split(os.pathsep)
            
            for path_dir in path_dirs:
                command_path = os.path.join(path_dir, command)
                if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
                    return command_path, 0
            
            return f"which: {command}: not found", 1
        except Exception as e:
            return f"which: {e}", 1
    
    def _cmd_whereis(self, args: List[str]) -> Tuple[str, int]:
        """Find command location and documentation."""
        if not args:
            return "whereis: missing command name", 1
        
        try:
            command = args[0]
            results = []
            
            # Find binary
            path_dirs = os.environ.get('PATH', '').split(os.pathsep)
            for path_dir in path_dirs:
                command_path = os.path.join(path_dir, command)
                if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
                    results.append(f"bin: {command_path}")
                    break
            
            # Find man pages
            man_dirs = ['/usr/share/man', '/usr/local/man', '/opt/homebrew/share/man']
            for man_dir in man_dirs:
                if os.path.exists(man_dir):
                    for root, dirs, files in os.walk(man_dir):
                        for file in files:
                            if file.startswith(command + '.'):
                                results.append(f"man: {os.path.join(root, file)}")
                                break
            
            if results:
                return "\n".join(results), 0
            else:
                return f"whereis: {command}: not found", 1
        except Exception as e:
            return f"whereis: {e}", 1
    
    def _cmd_echo(self, args: List[str]) -> Tuple[str, int]:
        """Print text."""
        text = ' '.join(args)
        return text, 0
    
    def _cmd_codemate(self, args: List[str]) -> Tuple[str, int]:
        """CodeMate integration commands."""
        if not args:
            help_text = """CodeMate Integration Commands:

codemate debug <file>     - Debug code using CodeMate AI
codemate review <file>    - Review code with CodeMate
codemate optimize <file>  - Optimize code with CodeMate
codemate test <file>      - Generate test cases with CodeMate
codemate docs <file>      - Generate documentation with CodeMate
codemate chat <question>  - Chat with CodeMate AI
codemate status          - Check CodeMate integration status"""
            return help_text, 0
        
        subcmd = args[0].lower()
        
        if subcmd == 'status':
            status_text = """✅ CodeMate Terminal Integration: Active
✅ AI Features: Enabled
✅ Web Interface: Ready
✅ Natural Language Processing: Working
✅ Command History: Enabled
✅ System Monitoring: Available

Ready for CodeMate.ai hackathon!"""
            return status_text, 0
        
        elif subcmd in ['debug', 'review', 'optimize', 'test', 'docs']:
            if len(args) < 2:
                return f"Usage: codemate {subcmd} <file>", 1
            
            filename = args[1]
            if not os.path.exists(filename):
                return f"File not found: {filename}", 1
            
            result_text = f"""CodeMate {subcmd.title()} Analysis for: {filename}

This would integrate with CodeMate.ai API to:
• Analyze the code file
• Provide {subcmd} suggestions
• Generate professional recommendations
• Integrate with CodeMate's AI engine

[Note: This is a demo integration for the hackathon]"""
            return result_text, 0
        
        elif subcmd == 'chat':
            if len(args) < 2:
                return "Usage: codemate chat <question>", 1
            
            question = ' '.join(args[1:])
            result_text = f"""CodeMate AI Chat Response:

Question: {question}

This would integrate with CodeMate.ai chat API to provide:
• Context-aware responses
• Code-specific suggestions
• Professional coding advice
• Integration with your codebase

[Note: This is a demo integration for the hackathon]"""
            return result_text, 0
        
        else:
            return f"Unknown CodeMate command: {subcmd}", 1
    
    def _cmd_ask(self, args: List[str]) -> Tuple[str, int]:
        """Ask AI questions."""
        if not args:
            return "ask: missing question", 1
        
        question = ' '.join(args)
        question_lower = question.lower()
        
        # Enhanced AI responses
        responses = {
            'how to create a folder': 'Use: mkdir <folder_name>',
            'how to create a file': 'Use: touch <file_name>',
            'how to debug code': 'Use: codemate debug <file> for AI-powered debugging',
            'how to review code': 'Use: codemate review <file> for professional code review',
            'how to optimize code': 'Use: codemate optimize <file> for performance optimization',
            'how to generate tests': 'Use: codemate test <file> for AI-generated test cases',
            'what commands are available': 'Type "help" to see all available commands',
            'what is codemate': 'CodeMate is an AI-powered coding assistant. Use "codemate" commands for integration',
            'how to use codemate': 'Use "codemate" command to access CodeMate.ai features',
            'how to find files': 'Use: find <pattern> or "find files called <name>"',
            'how to search text': 'Use: grep <pattern> <file> or "search for <text> in <files>"',
            'how to check system': 'Use: system_info, ps, free, df, or cpu commands',
            'how to navigate': 'Use: cd <directory> or "go to <directory>"',
            'how to copy files': 'Use: cp <source> <destination> or "copy <file> to <location>"',
            'how to move files': 'Use: mv <source> <destination> or "move <file> to <location>"'
        }
        
        response = None
        for key, answer in responses.items():
            if key in question_lower:
                response = answer
                break
        
        if not response:
            response = f"I don't understand the question: '{question}'. Try asking about commands, files, or CodeMate features."
        
        return f"CodeMate AI: {response}", 0
    
    def _cmd_translate(self, args: List[str]) -> Tuple[str, int]:
        """Convert natural language to commands."""
        if not args:
            return "translate: missing text", 1
        
        text = ' '.join(args)
        translated = self.process_natural_language(text)
        
        if translated:
            return f"AI Translation: {translated}", 0
        else:
            return f"Could not translate: '{text}'", 1
    
    def _cmd_help(self, args: List[str]) -> Tuple[str, int]:
        """Show help information."""
        help_text = """CodeMate Terminal Commands:

File Operations:
  ls [path]              List directory contents
  pwd                    Print working directory
  cd [path]              Change directory
  mkdir <dir>            Create directory
  rm <file/dir>          Remove file or directory
  rmdir <dir>            Remove empty directory
  touch <file>           Create empty file
  cat <file>             Display file contents
  cp <src> <dest>        Copy file or directory
  mv <src> <dest>        Move/rename file or directory

Search & Navigation:
  find <pattern>         Find files by name
  grep <pattern> [file]  Search for text in files
  which <command>        Find command location
  whereis <command>      Find command and documentation

System Information:
  ps                     Show running processes
  free                   Show memory usage
  df                     Show disk usage
  du [path]              Show directory size
  uptime                 Show system uptime
  whoami                 Show current user
  date                   Show current date/time
  system_info            Show detailed system information
  cpu                    Show CPU usage

CodeMate Integration:
  codemate debug <file>     Debug code with CodeMate AI
  codemate review <file>    Review code with CodeMate
  codemate optimize <file>  Optimize code with CodeMate
  codemate test <file>      Generate test cases with CodeMate
  codemate docs <file>      Generate documentation with CodeMate
  codemate chat <question>  Chat with CodeMate AI
  codemate status          Check CodeMate integration status

AI Features:
  ask <question>         Ask AI questions about commands
  translate <text>        Convert natural language to commands
  Use natural language commands like:
  • "create a folder called test"
  • "show me my files"
  • "what's my memory usage"
  • "create a new folder called test and move file1.txt into it"
  • "find files called readme"
  • "search for function in *.py files"

Utilities:
  echo <text>            Print text
  help                   Show this help message
  history                Show command history
  clear                  Clear screen
  exit/quit              Exit terminal"""
        return help_text, 0
    
    def _cmd_history(self, args: List[str]) -> Tuple[str, int]:
        """Show command history."""
        if not self.command_history:
            return "No commands in history", 0
        
        output = []
        for i, cmd in enumerate(self.command_history[-20:], 1):
            output.append(f"{i:4d}  {cmd}")
        
        return "\n".join(output), 0
    
    def _cmd_clear(self, args: List[str]) -> Tuple[str, int]:
        """Clear screen."""
        return "CLEAR_SCREEN", 0


# Global terminal instance
terminal_api = TerminalAPI()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/api/terminal':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                "status": "success",
                "message": "CodeMate Terminal API",
                "current_path": terminal_api.current_path,
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/api/help':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            help_output, exit_code = terminal_api._cmd_help([])
            response = {
                "status": "success",
                "help": help_output,
                "exit_code": exit_code
            }
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/api/welcome':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            welcome_info = terminal_api.get_welcome_info()
            response = {
                "status": "success",
                "welcome": welcome_info
            }
            self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "error", "message": "Not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/api/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                command = data.get('command', '')
                
                # Store original command for AI translation display
                original_command = command
                
                # Execute command (AI processing happens inside execute_command)
                result = terminal_api.execute_command(command, data.get('natural_language', False))
                
                # Get AI translation from result
                ai_translation = result.get('ai_translation')
                
                response = {
                    "status": "success",
                    "command": original_command,
                    "ai_translation": ai_translation,
                    "output": result["output"],
                    "exit_code": result["exit_code"],
                    "error": result["error"],
                    "current_path": terminal_api.current_path,
                    "timestamp": datetime.now().isoformat()
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {
                    "status": "error",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/api/translate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                text = data.get('text', '')
                
                translated = terminal_api.process_natural_language(text)
                
                response = {
                    "status": "success",
                    "original": text,
                    "translated": translated,
                    "timestamp": datetime.now().isoformat()
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {
                    "status": "error",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"status": "error", "message": "Not found"}
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# Global terminal API instance
terminal_api = TerminalAPI()

if __name__ == '__main__':
    from http.server import HTTPServer
    
    # Create HTTP server
    server = HTTPServer(('localhost', 8000), handler)
    print("🚀 CodeMate Terminal API Server running on http://localhost:8000")
    print("📱 Web interface: Open public/index.html in your browser")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        server.shutdown()
