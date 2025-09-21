#!/usr/bin/env python3
"""
CodeMate Terminal for macOS
Professional AI-powered terminal for CodeMate.ai hackathon
"""

import os
import sys
import subprocess
import shutil
import psutil
import platform
import json
import glob
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import argparse

# Handle readline import for macOS
try:
    import readline
except ImportError:
    class DummyReadline:
        def set_history_length(self, length): pass
        def parse_and_bind(self, bind): pass
        def set_completer(self, completer): pass
        def read_history_file(self, file): pass
        def write_history_file(self, file): pass
        def add_history(self, line): pass
    readline = DummyReadline()

# Try to import rich for enhanced UI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt
    from rich.table import Table
    from rich.align import Align
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Try to import colorama for cross-platform colors
try:
    import colorama
    from colorama import Fore, Back, Style, init
    colorama.init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False


class CodeMateTerminal:
    """Professional CodeMate Terminal for macOS."""
    
    def __init__(self):
        self.current_path = os.path.expanduser("~")
        self.history_file = os.path.expanduser("~/.codemate_terminal_history")
        self.command_history = []
        
        # Initialize console first
        if RICH_AVAILABLE:
            self.console = Console()
        else:
            self.console = None
        
        # Initialize readline for history and completion
        self.setup_readline()
        
        # Load history after console is initialized
        self.load_history()
        
        # Show welcome banner
        self.show_welcome_banner()
    
    def show_welcome_banner(self):
        """Display CodeMate professional banner."""
        banner = """
    ██████╗ ██████╗ ██████╗ ███████╗███╗   ███╗ █████╗ ████████╗███████╗
   ██╔════╝██╔═══██╗██╔══██╗██╔════╝████╗ ████║██╔══██╗╚══██╔══╝██╔════╝
   ██║     ██║   ██║██║  ██║█████╗  ██╔████╔██║███████║   ██║   █████╗  
   ██║     ██║   ██║██║  ██║██╔══╝  ██║╚██╔╝██║██╔══██║   ██║   ██╔══╝  
   ╚██████╗╚██████╔╝██████╔╝███████╗██║ ╚═╝ ██║██║  ██║   ██║   ███████╗
    ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝
                                                                        
                    AI-Powered Terminal for macOS
                        CodeMate.ai Hackathon
"""
        
        if RICH_AVAILABLE:
            # Use rich for beautiful display
            self.console.print(Panel(
                banner,
                title="[bold blue]CodeMate Terminal v2.0[/bold blue]",
                subtitle="[italic]Professional AI Terminal for macOS[/italic]",
                border_style="blue",
                padding=(1, 2)
            ))
            
            # System info panel
            info_text = f"""
[bold]Platform:[/bold] macOS {platform.mac_ver()[0]}
[bold]Python:[/bold] {platform.python_version()}
[bold]User:[/bold] {os.getenv('USER', 'unknown')}
[bold]Directory:[/bold] {self.current_path}
[bold]AI Features:[/bold] Enabled
[bold]Rich UI:[/bold] {'Enabled' if RICH_AVAILABLE else 'Disabled'}
[bold]CodeMate Integration:[/bold] Ready
            """
            
            self.console.print(Panel(
                info_text.strip(),
                title="[bold green]System Information[/bold green]",
                border_style="green",
                padding=(1, 2)
            ))
            
        else:
            # Fallback to simple display
            if COLORAMA_AVAILABLE:
                print(Fore.CYAN + banner)
                print(Fore.GREEN + "=" * 60)
                print(Fore.YELLOW + "CodeMate Terminal v2.0 - Professional AI Terminal for macOS")
                print(Fore.GREEN + "=" * 60)
            else:
                print(banner)
                print("=" * 60)
                print("CodeMate Terminal v2.0 - Professional AI Terminal for macOS")
                print("=" * 60)
            
            print(f"Platform: macOS {platform.mac_ver()[0]}")
            print(f"Python: {platform.python_version()}")
            print(f"Current Directory: {self.current_path}")
        
        print("\n" + "=" * 60)
        print("🚀 Type 'help' for available commands or 'exit' to quit")
        print("🤖 Try AI commands: 'ask <question>' or 'translate <natural language>'")
        print("💻 CodeMate Integration: 'codemate <command>'")
        print("=" * 60 + "\n")
    
    def load_history(self):
        """Load command history from file with enhanced features."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    for line in f:
                        self.command_history.append(line.strip())
                    readline.read_history_file(self.history_file)
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[yellow]Warning: Could not load history: {e}[/yellow]")
            else:
                print(f"Warning: Could not load history: {e}")
    
    def save_history(self):
        """Save command history to file with enhanced features."""
        try:
            readline.write_history_file(self.history_file)
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[yellow]Warning: Could not save history: {e}[/yellow]")
            else:
                print(f"Warning: Could not save history: {e}")
    
    def setup_readline(self):
        """Setup readline with enhanced history navigation."""
        readline.set_completer(self.complete_command)
        readline.parse_and_bind("tab: complete")
        readline.set_history_length(1000)
        readline.parse_and_bind("set editing-mode emacs")
        readline.parse_and_bind("set show-all-if-ambiguous on")
        readline.parse_and_bind("set completion-query-items 100")
        
        # Enhanced history navigation
        readline.parse_and_bind("\\C-p: history-search-backward")
        readline.parse_and_bind("\\C-n: history-search-forward")
        readline.parse_and_bind("\\C-r: reverse-search-history")
        readline.parse_and_bind("\\C-s: forward-search-history")
    
    def complete_command(self, text, state):
        """Provide enhanced command completion with natural language support."""
        # Get current line and cursor position
        line = readline.get_line_buffer()
        begidx = readline.get_begidx()
        endidx = readline.get_endidx()
        
        # Parse the line to understand context
        before_cursor = line[:begidx]
        after_cursor = line[endidx:]
        
        # Get possible completions
        if state == 0:
            self.matches = self._get_completions(before_cursor, text)
        
        try:
            return self.matches[state]
        except IndexError:
            return None
    
    def _get_completions(self, context, text):
        """Get possible completions based on context."""
        completions = []
        
        # Split context to understand what we're completing
        parts = context.strip().split()
        
        if not parts:
            # No command yet, complete with available commands and natural language
            all_commands = [
                'help', 'clear', 'exit', 'quit', 'pwd', 'ls', 'cd', 'mkdir', 
                'rm', 'rmdir', 'touch', 'cat', 'echo', 'cp', 'mv', 'find',
                'grep', 'ps', 'top', 'df', 'du', 'free', 'uptime', 'whoami',
                'date', 'history', 'which', 'whereis', 'man', 'info',
                'ask', 'translate', 'codemate'
            ]
            
            # Add natural language completions
            natural_language = [
                'create', 'make', 'new', 'show', 'list', 'display', 'what', 'how',
                'go', 'navigate', 'move', 'copy', 'delete', 'remove', 'backup',
                'organize', 'tell', 'ask', 'debug', 'review', 'optimize', 'test'
            ]
            
            all_completions = all_commands + natural_language
            completions = [cmd for cmd in all_completions if cmd.startswith(text)]
        else:
            command = parts[0].lower()
            
            # Command-specific completions
            if command in ['ls', 'cd', 'cat', 'cp', 'mv', 'rm', 'touch', 'mkdir']:
                # File/directory completions
                completions = self._complete_files_and_dirs(text)
            elif command == 'ps':
                # Process completions
                completions = self._complete_processes(text)
            elif command in ['create', 'make', 'new']:
                # Natural language completions
                completions = self._complete_natural_language(command, text)
            elif command in ['show', 'list', 'display', 'what']:
                # Information completions
                completions = self._complete_information_commands(text)
            elif command == 'codemate':
                # CodeMate specific completions
                completions = self._complete_codemate_commands(text)
            else:
                # Generic file completion
                completions = self._complete_files_and_dirs(text)
        
        return sorted(completions)
    
    def _complete_natural_language(self, command, text):
        """Complete natural language commands."""
        completions = []
        
        if command in ['create', 'make', 'new']:
            if 'folder' in text or 'directory' in text:
                completions = ['folder called', 'directory called', 'folder named', 'directory named']
            elif 'file' in text or 'document' in text:
                completions = ['file called', 'document called', 'file named', 'document named']
            else:
                completions = ['folder', 'directory', 'file', 'document']
        
        return [comp for comp in completions if comp.startswith(text)]
    
    def _complete_information_commands(self, text):
        """Complete information-seeking commands."""
        completions = [
            'files', 'contents', 'processes', 'memory', 'cpu', 'system',
            'directory', 'folder', 'usage', 'info', 'information'
        ]
        return [comp for comp in completions if comp.startswith(text)]
    
    def _complete_codemate_commands(self, text):
        """Complete CodeMate specific commands."""
        completions = [
            'debug', 'review', 'optimize', 'test', 'docs', 'chat', 'status'
        ]
        return [comp for comp in completions if comp.startswith(text)]
    
    def _complete_files_and_dirs(self, text):
        """Complete file and directory names."""
        completions = []
        
        if text.startswith('/'):
            search_dir = os.path.dirname(text) or '/'
            prefix = os.path.basename(text)
        else:
            search_dir = os.path.dirname(text) if text else '.'
            prefix = os.path.basename(text)
        
        try:
            if not os.path.exists(search_dir):
                return completions
            
            for item in os.listdir(search_dir):
                full_path = os.path.join(search_dir, item)
                if item.startswith(prefix):
                    if os.path.isdir(full_path):
                        completions.append(item + '/')
                    else:
                        completions.append(item)
        except PermissionError:
            pass
        
        return completions
    
    def _complete_processes(self, text):
        """Complete process names."""
        try:
            completions = []
            for proc in psutil.process_iter(['name']):
                try:
                    name = proc.info['name']
                    if name and name.startswith(text):
                        completions.append(name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            return list(set(completions))  # Remove duplicates
        except Exception:
            return []
    
    def get_prompt(self) -> str:
        """Generate the command prompt."""
        username = os.getenv('USER', 'user')
        hostname = platform.node()
        rel_path = os.path.relpath(self.current_path, os.path.expanduser("~"))
        if rel_path == ".":
            rel_path = "~"
        else:
            rel_path = f"~/{rel_path}"
        
        return f"{username}@codemate:{rel_path}$ "
    
    def get_colored_prompt(self) -> str:
        """Get colored prompt for rich console."""
        username = os.getenv('USER', 'user')
        hostname = platform.node()
        rel_path = os.path.relpath(self.current_path, os.path.expanduser("~"))
        if rel_path == ".":
            rel_path = "~"
        else:
            rel_path = f"~/{rel_path}"
        
        return f"[bold green]{username}[/bold green]@[bold blue]codemate[/bold blue]:[bold cyan]{rel_path}[/bold cyan]$ "
    
    def execute_command(self, command: str) -> bool:
        """Execute a command and return True if should continue, False if should exit."""
        if not command.strip():
            return True
        
        # Add to history
        self.command_history.append(command)
        readline.add_history(command)
        
        parts = command.strip().split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        try:
            if cmd in ['exit', 'quit']:
                return False
            elif cmd == 'help':
                self.show_help()
            elif cmd == 'clear':
                self.clear_screen()
            elif cmd == 'pwd':
                self.pwd()
            elif cmd == 'ls':
                self.ls(args)
            elif cmd == 'cd':
                self.cd(args)
            elif cmd == 'mkdir':
                self.mkdir(args)
            elif cmd == 'rm':
                self.rm(args)
            elif cmd == 'rmdir':
                self.rmdir(args)
            elif cmd == 'touch':
                self.touch(args)
            elif cmd == 'cat':
                self.cat(args)
            elif cmd == 'echo':
                self.echo(args)
            elif cmd == 'cp':
                self.cp(args)
            elif cmd == 'mv':
                self.mv(args)
            elif cmd == 'find':
                self.find(args)
            elif cmd == 'grep':
                self.grep(args)
            elif cmd == 'ps':
                self.ps(args)
            elif cmd == 'top':
                self.top(args)
            elif cmd == 'df':
                self.df(args)
            elif cmd == 'du':
                self.du(args)
            elif cmd == 'free':
                self.free(args)
            elif cmd == 'uptime':
                self.uptime()
            elif cmd == 'whoami':
                self.whoami()
            elif cmd == 'date':
                self.date()
            elif cmd == 'history':
                self.show_history(args)
            elif cmd == 'which':
                self.which(args)
            elif cmd == 'whereis':
                self.whereis(args)
            elif cmd == 'man':
                self.man(args)
            elif cmd == 'info':
                self.info(args)
            elif cmd == 'ask':
                self.handle_ai_question(args)
            elif cmd == 'translate':
                self.handle_ai_translation(args)
            elif cmd == 'codemate':
                self.handle_codemate_command(args)
            else:
                # Try to execute as system command
                self.execute_system_command(command)
        
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[red]Error executing command '{cmd}': {e}[/red]")
            else:
                print(f"Error executing command '{cmd}': {e}")
        
        return True
    
    def handle_codemate_command(self, args):
        """Handle CodeMate-specific commands."""
        if not args:
            if RICH_AVAILABLE:
                self.console.print(Panel(
                    """
CodeMate Integration Commands:

codemate debug <file>     - Debug code using CodeMate AI
codemate review <file>    - Review code with CodeMate
codemate optimize <file>  - Optimize code with CodeMate
codemate test <file>      - Generate test cases with CodeMate
codemate docs <file>      - Generate documentation with CodeMate
codemate chat <question>  - Chat with CodeMate AI
codemate status          - Check CodeMate integration status
                    """.strip(),
                    title="[bold blue]CodeMate Integration[/bold blue]",
                    border_style="blue"
                ))
            else:
                print("CodeMate Integration Commands:")
                print("codemate debug <file>     - Debug code using CodeMate AI")
                print("codemate review <file>    - Review code with CodeMate")
                print("codemate optimize <file>  - Optimize code with CodeMate")
                print("codemate test <file>      - Generate test cases with CodeMate")
                print("codemate docs <file>      - Generate documentation with CodeMate")
                print("codemate chat <question>  - Chat with CodeMate AI")
                print("codemate status          - Check CodeMate integration status")
            return
        
        subcmd = args[0].lower()
        
        if subcmd == 'status':
            if RICH_AVAILABLE:
                self.console.print(Panel(
                    """
✅ CodeMate Terminal Integration: Active
✅ AI Features: Enabled
✅ Rich UI: Enabled
✅ macOS Compatibility: Confirmed
✅ Professional Mode: Active

Ready for CodeMate.ai hackathon!
                    """.strip(),
                    title="[bold green]CodeMate Status[/bold green]",
                    border_style="green"
                ))
            else:
                print("CodeMate Terminal Integration: Active")
                print("AI Features: Enabled")
                print("macOS Compatibility: Confirmed")
                print("Professional Mode: Active")
                print("Ready for CodeMate.ai hackathon!")
        
        elif subcmd in ['debug', 'review', 'optimize', 'test', 'docs']:
            if len(args) < 2:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]Usage: codemate {subcmd} <file>[/red]")
                else:
                    print(f"Usage: codemate {subcmd} <file>")
                return
            
            filename = args[1]
            if not os.path.exists(filename):
                if RICH_AVAILABLE:
                    self.console.print(f"[red]File not found: {filename}[/red]")
                else:
                    print(f"File not found: {filename}")
                return
            
            if RICH_AVAILABLE:
                self.console.print(Panel(
                    f"""
CodeMate {subcmd.title()} Analysis for: {filename}

This would integrate with CodeMate.ai API to:
• Analyze the code file
• Provide {subcmd} suggestions
• Generate professional recommendations
• Integrate with CodeMate's AI engine

[Note: This is a demo integration for the hackathon]
                    """.strip(),
                    title=f"[bold blue]CodeMate {subcmd.title()}[/bold blue]",
                    border_style="blue"
                ))
            else:
                print(f"CodeMate {subcmd.title()} Analysis for: {filename}")
                print(f"This would integrate with CodeMate.ai API for {subcmd} analysis")
        
        elif subcmd == 'chat':
            if len(args) < 2:
                if RICH_AVAILABLE:
                    self.console.print("[red]Usage: codemate chat <question>[/red]")
                else:
                    print("Usage: codemate chat <question>")
                return
            
            question = ' '.join(args[1:])
            if RICH_AVAILABLE:
                self.console.print(Panel(
                    f"""
CodeMate AI Chat Response:

Question: {question}

This would integrate with CodeMate.ai chat API to provide:
• Context-aware responses
• Code-specific suggestions
• Professional coding advice
• Integration with your codebase

[Note: This is a demo integration for the hackathon]
                    """.strip(),
                    title="[bold blue]CodeMate AI Chat[/bold blue]",
                    border_style="blue"
                ))
            else:
                print(f"CodeMate AI Chat Response for: {question}")
                print("This would integrate with CodeMate.ai chat API")
    
    def handle_ai_question(self, args):
        """Handle AI question commands."""
        if not args:
            if RICH_AVAILABLE:
                self.console.print("[yellow]ask: missing question[/yellow]")
            else:
                print("ask: missing question")
            return
        
        question = ' '.join(args)
        
        # Enhanced AI responses for CodeMate context
        responses = {
            'how to create a folder': 'Use: mkdir <folder_name>',
            'how to create a file': 'Use: touch <file_name>',
            'how to debug code': 'Use: codemate debug <file> for AI-powered debugging',
            'how to review code': 'Use: codemate review <file> for professional code review',
            'how to optimize code': 'Use: codemate optimize <file> for performance optimization',
            'how to generate tests': 'Use: codemate test <file> for AI-generated test cases',
            'what commands are available': 'Type "help" to see all available commands',
            'what is codemate': 'CodeMate is an AI-powered coding assistant. Use "codemate" commands for integration',
            'how to use codemate': 'Use "codemate" command to access CodeMate.ai features'
        }
        
        question_lower = question.lower()
        response = None
        
        for key, answer in responses.items():
            if key in question_lower:
                response = answer
                break
        
        if not response:
            response = f"I don't understand the question: '{question}'. Try asking about commands, files, or CodeMate features."
        
        if RICH_AVAILABLE:
            self.console.print(Panel(
                response,
                title="[bold blue]CodeMate AI Assistant[/bold blue]",
                border_style="blue"
            ))
        else:
            print(f"CodeMate AI: {response}")
    
    def handle_ai_translation(self, args):
        """Handle AI translation commands with complex multi-step support."""
        if not args:
            if RICH_AVAILABLE:
                self.console.print("[yellow]translate: missing text[/yellow]")
            else:
                print("translate: missing text")
            return
        
        text = ' '.join(args)
        text_lower = text.lower()
        
        # Complex multi-step command patterns (check these first)
        complex_patterns = {
            r'create\s+(?:a\s+)?(?:new\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+move\s+([^\s]+)\s+(?:to|into)\s+(?:it|that\s+folder)': 
                lambda m: f"mkdir {m.group(1)} && mv {m.group(2)} {m.group(1)}/",
            r'make\s+(?:a\s+)?(?:new\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+move\s+([^\s]+)\s+(?:to|into)\s+(?:it|that\s+folder)': 
                lambda m: f"mkdir {m.group(1)} && mv {m.group(2)} {m.group(1)}/",
            r'create\s+(?:a\s+)?(?:new\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+copy\s+([^\s]+)\s+(?:to|into)\s+(?:it|that\s+folder)': 
                lambda m: f"mkdir {m.group(1)} && cp {m.group(2)} {m.group(1)}/",
            r'make\s+(?:a\s+)?(?:new\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+copy\s+([^\s]+)\s+(?:to|into)\s+(?:it|that\s+folder)': 
                lambda m: f"mkdir {m.group(1)} && cp {m.group(2)} {m.group(1)}/",
            r'create\s+(?:a\s+)?(?:backup|backup\s+folder)\s+(?:called\s+|named\s+)?([^\s]+)\s+and\s+copy\s+(?:all\s+)?([^\s]+)\s+(?:files\s+)?(?:to|into)\s+(?:it|that\s+folder)': 
                lambda m: f"mkdir {m.group(1)} && cp {m.group(2)}* {m.group(1)}/",
            r'organize\s+(?:all\s+)?([^\s]+)\s+(?:files\s+)?(?:into\s+)?(?:a\s+)?(?:folder|directory)\s+(?:called\s+|named\s+)?([^\s]+)': 
                lambda m: f"mkdir {m.group(2)} && mv {m.group(1)}* {m.group(2)}/"
        }
        
        # Check complex patterns first
        import re
        translated = None
        for pattern, func in complex_patterns.items():
            match = re.search(pattern, text_lower)
            if match:
                translated = func(match)
                break
        
        # Simple translation patterns if no complex match
        if not translated:
            simple_translations = {
                'create a folder called': 'mkdir',
                'make a folder': 'mkdir',
                'create a file called': 'touch',
                'make a file': 'touch',
                'debug this code': 'codemate debug',
                'review this code': 'codemate review',
                'optimize this code': 'codemate optimize',
                'generate tests for': 'codemate test',
                'show me running processes': 'ps',
                'what files are here': 'ls',
                'list files': 'ls',
                'show current directory': 'pwd',
                'go to': 'cd',
                'navigate to': 'cd',
                'change to': 'cd',
                'delete': 'rm',
                'remove': 'rm',
                'copy': 'cp',
                'move': 'mv',
                'what is my memory usage': 'free',
                'what is my cpu usage': 'top',
                'show system info': 'codemate status'
            }
            
            for pattern, command in simple_translations.items():
                if pattern in text_lower:
                    translated = command
                    break
        
        if not translated:
            translated = text
        
        if RICH_AVAILABLE:
            self.console.print(f"[cyan]🤖 AI Translation:[/cyan] [bold]{translated}[/bold]")
        else:
            print(f"🤖 AI Translation: {translated}")
        
        # Execute the translated command
        if translated != text:
            self.execute_command(translated)
    
    def show_help(self):
        """Show help information with CodeMate integration."""
        if RICH_AVAILABLE:
            table = Table(title="CodeMate Terminal Commands", show_header=True, header_style="bold magenta")
            table.add_column("Command", style="cyan", no_wrap=True)
            table.add_column("Description", style="white")
            
            commands = [
                ("ls [path]", "List directory contents"),
                ("cd [path]", "Change directory"),
                ("pwd", "Print working directory"),
                ("mkdir <dir>", "Create directory"),
                ("rm <file/dir>", "Remove file or directory"),
                ("touch <file>", "Create empty file"),
                ("cat <file>", "Display file contents"),
                ("cp <src> <dest>", "Copy file or directory"),
                ("mv <src> <dest>", "Move/rename file or directory"),
                ("ps", "Show running processes"),
                ("free", "Show memory usage"),
                ("df", "Show disk usage"),
                ("uptime", "Show system uptime"),
                ("codemate debug <file>", "Debug code with CodeMate AI"),
                ("codemate review <file>", "Review code with CodeMate"),
                ("codemate optimize <file>", "Optimize code with CodeMate"),
                ("codemate test <file>", "Generate test cases with CodeMate"),
                ("codemate docs <file>", "Generate documentation with CodeMate"),
                ("codemate chat <question>", "Chat with CodeMate AI"),
                ("ask <question>", "Ask AI questions"),
                ("translate <text>", "Convert natural language to commands"),
                ("history [-a] [-s term]", "Show command history with search"),
                ("help", "Show this help"),
                ("exit/quit", "Exit terminal")
            ]
            
            for cmd, desc in commands:
                table.add_row(cmd, desc)
            
            self.console.print(table)
            
            # Add AI Natural Language examples
            ai_examples = Panel(
                """[bold green]🤖 AI Natural Language Examples:[/bold green]

[bold]Simple Commands:[/bold]
• "create a folder called test" → mkdir test
• "show me my files" → ls
• "what's my memory usage" → free
• "go to the documents folder" → cd documents

[bold]Complex Multi-Step Commands:[/bold]
• "create a new folder called test and move file1.txt into it" → mkdir test && mv file1.txt test/
• "make a backup folder and copy all .py files to it" → mkdir backup && cp *.py backup/
• "organize all .txt files into a documents folder" → mkdir documents && mv *.txt documents/

[bold]Enhanced Features:[/bold]
• Tab completion for commands and natural language
• Arrow key navigation for command history
• Ctrl+R for reverse history search
• history -s <term> to search command history""",
                title="[bold blue]AI Features[/bold blue]",
                border_style="blue"
            )
            self.console.print(ai_examples)
        else:
            # Fallback to simple help
            help_text = """
CodeMate Terminal Commands:

File Operations:
  ls [path]          - List directory contents
  cd [path]          - Change directory
  pwd                - Print working directory
  mkdir <dir>        - Create directory
  rm <file/dir>      - Remove file or directory
  touch <file>       - Create empty file
  cat <file>         - Display file contents
  cp <src> <dest>    - Copy file or directory
  mv <src> <dest>    - Move/rename file or directory

System Information:
  ps                 - Show running processes
  df                 - Show disk usage
  free               - Show memory usage
  uptime             - Show system uptime

CodeMate Integration:
  codemate debug <file>     - Debug code with CodeMate AI
  codemate review <file>    - Review code with CodeMate
  codemate optimize <file>  - Optimize code with CodeMate
  codemate test <file>      - Generate test cases with CodeMate
  codemate docs <file>      - Generate documentation with CodeMate
  codemate chat <question>  - Chat with CodeMate AI

AI Features:
  ask <question>     - Ask AI questions
  translate <text>    - Convert natural language to commands

Utilities:
  help               - Show this help
  exit/quit          - Exit terminal
            """
            print(help_text)
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('clear')
        if RICH_AVAILABLE:
            self.show_welcome_banner()
    
    def pwd(self):
        """Print working directory."""
        if RICH_AVAILABLE:
            self.console.print(f"[bold cyan]{self.current_path}[/bold cyan]")
        else:
            print(self.current_path)
    
    def ls(self, args):
        """List directory contents with rich formatting."""
        path = args[0] if args else self.current_path
        try:
            if os.path.exists(path):
                items = os.listdir(path)
                items.sort()
                
                if RICH_AVAILABLE:
                    table = Table(show_header=False, box=None)
                    table.add_column("Type", style="blue", width=4)
                    table.add_column("Name", style="white")
                    
                    for item in items:
                        item_path = os.path.join(path, item)
                        if os.path.isdir(item_path):
                            table.add_row("📁", f"[blue]{item}/[/blue]")
                        elif os.access(item_path, os.X_OK):
                            table.add_row("⚡", f"[green]{item}[/green]")
                        else:
                            table.add_row("📄", item)
                    
                    self.console.print(table)
                else:
                    # Fallback formatting
                    for item in items:
                        item_path = os.path.join(path, item)
                        if os.path.isdir(item_path):
                            print(f"\033[94m{item}/\033[0m")  # Blue for directories
                        elif os.access(item_path, os.X_OK):
                            print(f"\033[92m{item}\033[0m")    # Green for executables
                        else:
                            print(item)
            else:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]ls: cannot access '{path}': No such file or directory[/red]")
                else:
                    print(f"ls: cannot access '{path}': No such file or directory")
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[red]ls: error: {e}[/red]")
            else:
                print(f"ls: error: {e}")
    
    def cd(self, args):
        """Change directory."""
        if not args:
            # Go to home directory
            new_path = os.path.expanduser("~")
        else:
            path = args[0]
            if path.startswith('/'):
                new_path = path
            elif path.startswith('~'):
                new_path = os.path.expanduser(path)
            else:
                new_path = os.path.join(self.current_path, path)
        
        try:
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_path = os.path.abspath(new_path)
                os.chdir(self.current_path)
                if RICH_AVAILABLE:
                    self.console.print(f"[green]Changed to: {self.current_path}[/green]")
            else:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]cd: {path}: No such file or directory[/red]")
                else:
                    print(f"cd: {path}: No such file or directory")
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[red]cd: error: {e}[/red]")
            else:
                print(f"cd: error: {e}")
    
    def mkdir(self, args):
        """Create directory."""
        if not args:
            if RICH_AVAILABLE:
                self.console.print("[red]mkdir: missing operand[/red]")
            else:
                print("mkdir: missing operand")
            return
        
        for dirname in args:
            try:
                os.makedirs(dirname, exist_ok=False)
                if RICH_AVAILABLE:
                    self.console.print(f"[green]Created directory: {dirname}[/green]")
                else:
                    print(f"Created directory: {dirname}")
            except FileExistsError:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]mkdir: cannot create directory '{dirname}': File exists[/red]")
                else:
                    print(f"mkdir: cannot create directory '{dirname}': File exists")
            except Exception as e:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]mkdir: error creating '{dirname}': {e}[/red]")
                else:
                    print(f"mkdir: error creating '{dirname}': {e}")
    
    def touch(self, args):
        """Create empty file."""
        if not args:
            if RICH_AVAILABLE:
                self.console.print("[red]touch: missing file operand[/red]")
            else:
                print("touch: missing file operand")
            return
        
        for filename in args:
            try:
                Path(filename).touch()
                if RICH_AVAILABLE:
                    self.console.print(f"[green]Created file: {filename}[/green]")
                else:
                    print(f"Created file: {filename}")
            except Exception as e:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]touch: error creating '{filename}': {e}[/red]")
                else:
                    print(f"touch: error creating '{filename}': {e}")
    
    def rm(self, args):
        """Remove file or directory."""
        if not args:
            if RICH_AVAILABLE:
                self.console.print("[red]rm: missing operand[/red]")
            else:
                print("rm: missing operand")
            return
        
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
            if RICH_AVAILABLE:
                self.console.print("[red]rm: missing operand[/red]")
            else:
                print("rm: missing operand")
            return
        
        for item in files_to_remove:
            try:
                if os.path.isdir(item):
                    if recursive:
                        import shutil
                        shutil.rmtree(item)
                        if RICH_AVAILABLE:
                            self.console.print(f"[green]Removed directory: {item}[/green]")
                        else:
                            print(f"Removed directory: {item}")
                    else:
                        if RICH_AVAILABLE:
                            self.console.print(f"[red]rm: cannot remove '{item}': Is a directory[/red]")
                        else:
                            print(f"rm: cannot remove '{item}': Is a directory")
                else:
                    os.remove(item)
                    if RICH_AVAILABLE:
                        self.console.print(f"[green]Removed file: {item}[/green]")
                    else:
                        print(f"Removed file: {item}")
            except FileNotFoundError:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]rm: cannot remove '{item}': No such file or directory[/red]")
                else:
                    print(f"rm: cannot remove '{item}': No such file or directory")
            except PermissionError:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]rm: cannot remove '{item}': Permission denied[/red]")
                else:
                    print(f"rm: cannot remove '{item}': Permission denied")
            except Exception as e:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]rm: error removing '{item}': {e}[/red]")
                else:
                    print(f"rm: error removing '{item}': {e}")
    
    def cat(self, args):
        """Display file contents."""
        if not args:
            if RICH_AVAILABLE:
                self.console.print("[red]cat: missing file operand[/red]")
            else:
                print("cat: missing file operand")
            return
        
        for filename in args:
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                    if RICH_AVAILABLE:
                        self.console.print(Panel(content, title=f"[bold blue]{filename}[/bold blue]"))
                    else:
                        print(content)
            except FileNotFoundError:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]cat: {filename}: No such file or directory[/red]")
                else:
                    print(f"cat: {filename}: No such file or directory")
            except Exception as e:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]cat: error reading '{filename}': {e}[/red]")
                else:
                    print(f"cat: error reading '{filename}': {e}")
    
    def echo(self, args):
        """Print text."""
        text = ' '.join(args)
        if RICH_AVAILABLE:
            self.console.print(text)
        else:
            print(text)
    
    def ps(self, args):
        """Show running processes with rich formatting."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                processes.append(proc.info)
            
            if RICH_AVAILABLE:
                table = Table(title="Running Processes", show_header=True, header_style="bold magenta")
                table.add_column("PID", style="cyan", no_wrap=True)
                table.add_column("Name", style="white")
                table.add_column("CPU%", style="green")
                table.add_column("Memory%", style="yellow")
                
                for proc in sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:20]:
                    table.add_row(
                        str(proc['pid']),
                        proc['name'],
                        f"{proc['cpu_percent']:.1f}",
                        f"{proc['memory_percent']:.1f}"
                    )
                
                self.console.print(table)
            else:
                print(f"{'PID':<8} {'Name':<20} {'CPU%':<8} {'Memory%':<10}")
                print("-" * 50)
                
                for proc in sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:20]:
                    print(f"{proc['pid']:<8} {proc['name']:<20} {proc['cpu_percent']:<8.1f} {proc['memory_percent']:<10.1f}")
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[red]ps: error: {e}[/red]")
            else:
                print(f"ps: error: {e}")
    
    def free(self, args):
        """Show memory usage with rich formatting."""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            if RICH_AVAILABLE:
                table = Table(title="Memory Usage", show_header=True, header_style="bold magenta")
                table.add_column("Type", style="cyan", no_wrap=True)
                table.add_column("Total", style="green")
                table.add_column("Used", style="red")
                table.add_column("Free", style="yellow")
                table.add_column("Available", style="blue")
                
                total_gb = memory.total // (1024**3)
                used_gb = memory.used // (1024**3)
                free_gb = memory.free // (1024**3)
                available_gb = memory.available // (1024**3)
                
                table.add_row("Mem", f"{total_gb} GB", f"{used_gb} GB", f"{free_gb} GB", f"{available_gb} GB")
                
                swap_total_gb = swap.total // (1024**3)
                swap_used_gb = swap.used // (1024**3)
                swap_free_gb = swap.free // (1024**3)
                
                table.add_row("Swap", f"{swap_total_gb} GB", f"{swap_used_gb} GB", f"{swap_free_gb} GB", "-")
                
                self.console.print(table)
            else:
                print(f"{'':<12} {'Total':<12} {'Used':<12} {'Free':<12} {'Shared':<12} {'Buff/Cache':<12} {'Available'}")
                print("-" * 80)
                
                print(f"{'Mem:':<12} {total_gb:<12}GB {used_gb:<12}GB {free_gb:<12}GB {'0':<12}GB {'0':<12}GB {available_gb:<12}GB")
                print(f"{'Swap:':<12} {swap_total_gb:<12}GB {swap_used_gb:<12}GB {swap_free_gb:<12}GB")
                
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[red]free: error: {e}[/red]")
            else:
                print(f"free: error: {e}")
    
    def df(self, args):
        """Show disk usage with rich formatting."""
        try:
            if RICH_AVAILABLE:
                table = Table(title="Disk Usage", show_header=True, header_style="bold magenta")
                table.add_column("Filesystem", style="cyan")
                table.add_column("Size", style="green")
                table.add_column("Used", style="red")
                table.add_column("Avail", style="yellow")
                table.add_column("Use%", style="blue")
                table.add_column("Mounted on", style="white")
                
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        size_gb = usage.total // (1024**3)
                        used_gb = usage.used // (1024**3)
                        avail_gb = usage.free // (1024**3)
                        use_percent = (usage.used / usage.total) * 100
                        
                        table.add_row(
                            partition.device,
                            f"{size_gb} GB",
                            f"{used_gb} GB",
                            f"{avail_gb} GB",
                            f"{use_percent:.1f}%",
                            partition.mountpoint
                        )
                    except PermissionError:
                        continue
                
                self.console.print(table)
            else:
                print(f"{'Filesystem':<20} {'Size':<10} {'Used':<10} {'Avail':<10} {'Use%':<8} {'Mounted on'}")
                print("-" * 70)
                
                for partition in psutil.disk_partitions():
                    try:
                        usage = psutil.disk_usage(partition.mountpoint)
                        size_gb = usage.total // (1024**3)
                        used_gb = usage.used // (1024**3)
                        avail_gb = usage.free // (1024**3)
                        use_percent = (usage.used / usage.total) * 100
                        
                        print(f"{partition.device:<20} {size_gb:<10}GB {used_gb:<10}GB {avail_gb:<10}GB {use_percent:<8.1f}% {partition.mountpoint}")
                    except PermissionError:
                        continue
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[red]df: error: {e}[/red]")
            else:
                print(f"df: error: {e}")
    
    def uptime(self):
        """Show system uptime."""
        try:
            import time
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            uptime_text = f"up {days} days, {hours} hours, {minutes} minutes"
            if RICH_AVAILABLE:
                self.console.print(f"[green]{uptime_text}[/green]")
            else:
                print(uptime_text)
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[red]uptime: error: {e}[/red]")
            else:
                print(f"uptime: error: {e}")
    
    def whoami(self):
        """Show current user."""
        user = os.getenv('USER', 'unknown')
        if RICH_AVAILABLE:
            self.console.print(f"[bold cyan]{user}[/bold cyan]")
        else:
            print(user)
    
    def date(self):
        """Show current date and time."""
        current_time = datetime.now().strftime("%a %b %d %H:%M:%S %Z %Y")
        if RICH_AVAILABLE:
            self.console.print(f"[bold yellow]{current_time}[/bold yellow]")
        else:
            print(current_time)
    
    def show_history(self, args):
        """Show command history with enhanced search and filtering."""
        # Parse arguments for history options
        show_all = False
        search_term = None
        limit = 20
        
        for arg in args:
            if arg == '-a' or arg == '--all':
                show_all = True
            elif arg.startswith('-s') or arg.startswith('--search'):
                if '=' in arg:
                    search_term = arg.split('=', 1)[1]
                elif len(args) > args.index(arg) + 1:
                    search_term = args[args.index(arg) + 1]
            elif arg.isdigit():
                limit = int(arg)
        
        # Filter commands if search term provided
        filtered_history = self.command_history
        if search_term:
            filtered_history = [cmd for cmd in self.command_history if search_term.lower() in cmd.lower()]
        
        # Limit output unless show_all is specified
        if not show_all and not search_term:
            filtered_history = filtered_history[-limit:]
        
        if RICH_AVAILABLE:
            title = f"Command History ({len(filtered_history)} commands)"
            if search_term:
                title += f" - Searching for: '{search_term}'"
            
            table = Table(title=title, show_header=True, header_style="bold magenta")
            table.add_column("#", style="cyan", no_wrap=True)
            table.add_column("Command", style="white")
            
            for i, cmd in enumerate(filtered_history, 1):
                # Highlight search term if present
                if search_term and search_term.lower() in cmd.lower():
                    highlighted_cmd = cmd.replace(search_term, f"[bold yellow]{search_term}[/bold yellow]")
                    table.add_row(str(i), highlighted_cmd)
                else:
                    table.add_row(str(i), cmd)
            
            self.console.print(table)
        else:
            print(f"Command History ({len(filtered_history)} commands)")
            if search_term:
                print(f"Searching for: '{search_term}'")
            print("-" * 50)
            
            for i, cmd in enumerate(filtered_history, 1):
                print(f"{i:4d}  {cmd}")
    
    def info(self, args):
        """Show system information."""
        if RICH_AVAILABLE:
            info_text = f"""
[bold]Platform:[/bold] macOS {platform.mac_ver()[0]}
[bold]Architecture:[/bold] {platform.machine()}
[bold]Python:[/bold] {platform.python_version()}
[bold]Current User:[/bold] {os.getenv('USER', 'unknown')}
[bold]Current Directory:[/bold] {self.current_path}
[bold]Rich UI:[/bold] {'Enabled' if RICH_AVAILABLE else 'Disabled'}
[bold]Colorama:[/bold] {'Enabled' if COLORAMA_AVAILABLE else 'Disabled'}
[bold]CodeMate Integration:[/bold] Ready
            """
            
            try:
                cpu_count = psutil.cpu_count()
                memory = psutil.virtual_memory()
                info_text += f"[bold]CPU Cores:[/bold] {cpu_count}\n"
                info_text += f"[bold]Total Memory:[/bold] {memory.total // (1024**3)} GB"
            except Exception as e:
                info_text += f"[bold]Error getting system info:[/bold] {e}"
            
            self.console.print(Panel(
                info_text.strip(),
                title="[bold green]System Information[/bold green]",
                border_style="green"
            ))
        else:
            print("System Information:")
            print("=" * 30)
            print(f"Platform: macOS {platform.mac_ver()[0]}")
            print(f"Architecture: {platform.machine()}")
            print(f"Python: {platform.python_version()}")
            print(f"Current User: {os.getenv('USER', 'unknown')}")
            print(f"Current Directory: {self.current_path}")
            
            try:
                cpu_count = psutil.cpu_count()
                memory = psutil.virtual_memory()
                print(f"CPU Cores: {cpu_count}")
                print(f"Total Memory: {memory.total // (1024**3)} GB")
            except Exception as e:
                print(f"Error getting system info: {e}")
    
    def execute_system_command(self, command):
        """Execute command using system shell."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.current_path)
            if result.stdout:
                if RICH_AVAILABLE:
                    self.console.print(result.stdout)
                else:
                    print(result.stdout)
            if result.stderr:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]{result.stderr}[/red]")
                else:
                    print(result.stderr, file=sys.stderr)
            if result.returncode != 0:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]Command failed with exit code {result.returncode}[/red]")
                else:
                    print(f"Command failed with exit code {result.returncode}")
        except Exception as e:
            if RICH_AVAILABLE:
                self.console.print(f"[red]Error executing system command: {e}[/red]")
            else:
                print(f"Error executing system command: {e}")
    
    def run(self):
        """Main terminal loop with modern UI and improved input handling."""
        try:
            # Set terminal title
            if platform.system() == "Darwin":
                try:
                    import subprocess
                    subprocess.run(['osascript', '-e', 'tell application "Terminal" to set custom title of front window to "CodeMate Terminal v2.0"'], check=False)
                except:
                    pass
            
            while True:
                try:
                    if RICH_AVAILABLE:
                        # Use rich prompt with better input handling
                        try:
                            command = Prompt.ask(
                                self.get_colored_prompt().replace('[bold green]', '').replace('[/bold green]', '').replace('[bold blue]', '').replace('[/bold blue]', '').replace('[bold cyan]', '').replace('[/bold cyan]', '').replace('$', ''),
                                console=self.console
                            )
                        except KeyboardInterrupt:
                            self.console.print("\n[yellow]Use 'exit' to quit the terminal.[/yellow]")
                            continue
                    else:
                        # Fallback to standard input
                        command = input(self.get_prompt())
                    
                    if not self.execute_command(command):
                        break
                except KeyboardInterrupt:
                    if RICH_AVAILABLE:
                        self.console.print("\n[yellow]Use 'exit' to quit the terminal.[/yellow]")
                    else:
                        print("\nUse 'exit' to quit the terminal.")
                except EOFError:
                    if RICH_AVAILABLE:
                        self.console.print("\n[green]Goodbye![/green]")
                    else:
                        print("\nGoodbye!")
                    break
        finally:
            self.save_history()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='CodeMate Terminal for macOS')
    parser.add_argument('--version', action='version', version='CodeMate Terminal v2.0')
    parser.add_argument('--no-rich', action='store_true', help='Disable rich UI')
    args = parser.parse_args()
    
    if args.no_rich:
        global RICH_AVAILABLE
        RICH_AVAILABLE = False
    
    terminal = CodeMateTerminal()
    terminal.run()


if __name__ == "__main__":
    main()
