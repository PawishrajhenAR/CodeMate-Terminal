#!/usr/bin/env python3
"""
CodeMate Terminal - Simple Startup Script
Run this to start the web terminal locally
"""

import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("🚀 CodeMate Terminal Web Edition")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('api/terminal.py'):
        print("❌ Error: Please run this script from the maccodemate directory")
        print("   Current directory:", os.getcwd())
        return 1
    
    if not os.path.exists('public/index.html'):
        print("❌ Error: public/index.html not found")
        return 1
    
    print("✅ Starting CodeMate Terminal Server...")
    print("🌐 Server will be available at: http://localhost:3000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        # Start the server
        subprocess.run([sys.executable, 'run_local_server.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
