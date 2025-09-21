#!/usr/bin/env python3
"""
Simple local server for CodeMate Terminal Web Edition
Runs the web terminal locally without requiring Vercel CLI
"""

import http.server
import socketserver
import os
import sys
import webbrowser
import json
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the terminal API
from api.terminal import TerminalAPI

# Create a global API instance
api_instance = TerminalAPI()

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that serves static files and API endpoints."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.join(os.path.dirname(__file__), 'public'), **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path.startswith('/api/'):
            # Handle API requests
            try:
                if self.path == '/api/terminal':
                    response = {"status": "running", "version": "2.0", "type": "web"}
                elif self.path == '/api/welcome':
                    response = api_instance.get_welcome_info()
                elif self.path == '/api/help':
                    response = {"help": "Use /api/execute with POST to run commands"}
                else:
                    response = {"error": "Unknown endpoint"}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_error(500, f"API Error: {e}")
        else:
            # Serve static files
            if self.path == '/':
                self.path = '/index.html'
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path.startswith('/api/'):
            try:
                # Read the request body
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                if self.path == '/api/execute':
                    data = json.loads(post_data.decode())
                    response = api_instance.execute_command(data.get('command', ''))
                else:
                    response = {"error": "Unknown endpoint"}
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_error(500, f"API Error: {e}")
        else:
            self.send_error(404, "Not Found")
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def main():
    """Start the local server."""
    PORT = 3000
    
    print("🚀 CodeMate Terminal Web Edition - Local Server")
    print("=" * 60)
    print(f"Starting server on port {PORT}...")
    
    # Check if required files exist
    if not os.path.exists('api/terminal.py'):
        print("❌ Error: api/terminal.py not found")
        return 1
    
    if not os.path.exists('public/index.html'):
        print("❌ Error: public/index.html not found")
        return 1
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print(f"✅ Server running at http://localhost:{PORT}")
            print("🌐 Opening browser...")
            
            # Open browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}')
            except:
                print("⚠️  Could not open browser automatically")
                print(f"   Please open http://localhost:{PORT} manually")
            
            print("\n📋 Features available:")
            print("  ✅ Permission request screen")
            print("  ✅ CodeMate ASCII banner")
            print("  ✅ System information display")
            print("  ✅ AI natural language processing")
            print("  ✅ Full terminal emulation")
            print("  ✅ Command shortcuts and status bar")
            
            print("\n🛑 Press Ctrl+C to stop the server")
            print("=" * 60)
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return 0
    except OSError as e:
        if e.errno == 10048:  # Port already in use
            print(f"❌ Error: Port {PORT} is already in use")
            print("   Please close other applications using this port")
            print("   Or run: netstat -ano | findstr :3000")
        else:
            print(f"❌ Error starting server: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())