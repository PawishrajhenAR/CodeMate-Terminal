from http.server import BaseHTTPRequestHandler
import json
import os
import sys
import subprocess
import re
from typing import Dict, List, Optional, Tuple
import psutil
import platform
from datetime import datetime

# Add the parent directory to the path to import codemate_terminal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TerminalAPI:
    """API wrapper for CodeMate Terminal functionality."""
    
    def __init__(self):
        self.current_path = os.path.expanduser("~")
        self.command_history = []
        
        # AI patterns for natural language processing
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
            ]
        }
    
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
            'ls', 'pwd', 'cd', 'mkdir', 'rm', 'touch', 'cat', 'cp', 'mv',
            'ps', 'free', 'df', 'uptime', 'whoami', 'date', 'find', 'grep',
            'help', 'exit', 'quit', 'clear', 'history', 'system_info', 'cpu'
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
            os.makedirs(args[0], exist_ok=True)
            return f"Created directory: {args[0]}", 0
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
                if os.path.isdir(item):
                    if recursive:
                        import shutil
                        shutil.rmtree(item)
                        results.append(f"Removed directory: {item}")
                    else:
                        results.append(f"rm: cannot remove '{item}': Is a directory")
                else:
                    os.remove(item)
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
            with open(args[0], 'a'):
                pass
            return f"Created file: {args[0]}", 0
        except Exception as e:
            return f"touch: {e}", 1
    
    def _cmd_cat(self, args: List[str]) -> Tuple[str, int]:
        """Display file contents."""
        if not args:
            return "cat: missing operand", 1
        
        try:
            with open(args[0], 'r') as f:
                return f.read(), 0
        except Exception as e:
            return f"cat: {e}", 1
    
    def _cmd_cp(self, args: List[str]) -> Tuple[str, int]:
        """Copy file or directory."""
        if len(args) < 2:
            return "cp: missing operand", 1
        
        try:
            import shutil
            shutil.copy2(args[0], args[1])
            return f"Copied {args[0]} to {args[1]}", 0
        except Exception as e:
            return f"cp: {e}", 1
    
    def _cmd_mv(self, args: List[str]) -> Tuple[str, int]:
        """Move/rename file or directory."""
        if len(args) < 2:
            return "mv: missing operand", 1
        
        try:
            import shutil
            shutil.move(args[0], args[1])
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
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            return f"CPU Usage: {cpu_percent:.1f}%", 0
        except Exception as e:
            return f"cpu: {e}", 1
    
    def _cmd_help(self, args: List[str]) -> Tuple[str, int]:
        """Show help information."""
        help_text = """CodeMate Terminal Commands:

File Operations:
  ls [path]              List directory contents
  pwd                    Print working directory
  cd [path]              Change directory
  mkdir <dir>            Create directory
  rm <file/dir>          Remove file or directory
  touch <file>           Create empty file
  cat <file>             Display file contents
  cp <src> <dest>        Copy file or directory
  mv <src> <dest>        Move/rename file or directory

System Information:
  ps                     Show running processes
  free                   Show memory usage
  df                     Show disk usage
  uptime                 Show system uptime
  whoami                 Show current user
  date                   Show current date/time
  system_info            Show detailed system information
  cpu                    Show CPU usage

AI Features:
  Use natural language commands like:
  • "create a folder called test"
  • "show me my files"
  • "what's my memory usage"
  • "create a new folder called test and move file1.txt into it"

Utilities:
  help                   Show this help message
  history                Show command history
  clear                  Clear screen"""
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
        return "", 0


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
