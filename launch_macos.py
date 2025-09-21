#!/usr/bin/env python3
"""
CodeMate Terminal Launcher for macOS
Professional AI-powered terminal for CodeMate.ai hackathon
"""

import subprocess
import sys
import os
import platform
import tempfile


def create_macos_launcher():
    """Create macOS-specific launcher script."""
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'codemate_terminal.py'))
    
    # Create AppleScript for macOS Terminal
    applescript = f'''
tell application "Terminal"
    activate
    set newTab to do script "cd '{os.path.dirname(script_path)}' && python3 '{script_path}'"
    set custom title of newTab to "CodeMate Terminal v2.0"
    set background color of newTab to {{0, 0, 0}}
    set cursor color of newTab to {{0, 255, 0}}
end tell
'''
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.scpt', delete=False) as f:
        f.write(applescript)
        temp_script = f.name
    
    return temp_script


def launch_macos_terminal():
    """Launch terminal in macOS Terminal app."""
    if platform.system() == "Darwin":  # macOS
        try:
            # Method 1: Use AppleScript
            temp_script = create_macos_launcher()
            subprocess.run(['osascript', temp_script])
            print("🚀 CodeMate Terminal launched in macOS Terminal!")
            
            # Clean up
            import threading
            import time
            
            def cleanup():
                time.sleep(2)
                try:
                    os.unlink(temp_script)
                except:
                    pass
            
            threading.Thread(target=cleanup, daemon=True).start()
            
        except Exception as e:
            print(f"Error with AppleScript: {e}")
            try:
                # Method 2: Use osascript directly
                script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'codemate_terminal.py'))
                subprocess.run([
                    'osascript', '-e',
                    f'tell app "Terminal" to do script "cd {os.path.dirname(script_path)} && python3 {script_path}"'
                ])
                print("🚀 CodeMate Terminal launched in macOS Terminal!")
            except Exception as e2:
                print(f"Error launching terminal: {e2}")
                print("Falling back to current window...")
                subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'codemate_terminal.py')])
    else:
        print("This launcher is designed for macOS.")
        subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), 'codemate_terminal.py')])


def main():
    """Main launcher function."""
    print("🚀 CodeMate Terminal Launcher for macOS")
    print("=" * 50)
    print("Professional AI-powered terminal for CodeMate.ai hackathon")
    print("")
    
    # Check dependencies
    try:
        import rich
        print("✅ Rich UI library found")
    except ImportError:
        print("⚠️  Installing required dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "colorama", "psutil"])
            print("✅ Dependencies installed successfully!")
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
    
    print("\nLaunching CodeMate Terminal...")
    launch_macos_terminal()


if __name__ == "__main__":
    main()
