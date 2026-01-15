#!/usr/bin/env python3
"""
Durandal - Live Task Monitor Server
Real-time visualization of parallel task execution
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import threading
import queue
from datetime import datetime
from urllib.parse import parse_qs
import sys
import os

# Global event queue for SSE
event_queue = queue.Queue()

class DurandalHandler(SimpleHTTPRequestHandler):
    """Custom handler for task monitoring"""

    def do_GET(self):
        if self.path == '/events':
            # Server-Sent Events endpoint
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            print("[SSE] Client connected for event stream")

            # Send initial connection event
            self.send_event({
                'type': 'connected',
                'timestamp': datetime.now().isoformat()
            })

            # Keep connection open and send events
            try:
                while True:
                    event = event_queue.get(timeout=30)  # 30s keepalive
                    if event is None:
                        break
                    self.send_event(event)
            except queue.Empty:
                # Keepalive ping
                self.send_event({'type': 'ping'})
            except (BrokenPipeError, ConnectionResetError):
                print("[SSE] Client disconnected")
        else:
            # Serve static files
            super().do_GET()

    def do_POST(self):
        if self.path == '/task/start':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                event = {
                    'type': 'task_start',
                    'name': data.get('name', 'Unnamed Task'),
                    'duration': data.get('duration'),
                    'timestamp': datetime.now().isoformat()
                }
                event_queue.put(event)

                print(f"[TASK START] {event['name']}")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode())
            except Exception as e:
                print(f"[ERROR] Failed to process task start: {e}")
                self.send_response(400)
                self.end_headers()

        elif self.path == '/task/log':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))
                event = {
                    'type': 'log',
                    'message': data.get('message', ''),
                    'status': data.get('status', 'running'),
                    'timestamp': datetime.now().isoformat()
                }
                event_queue.put(event)

                print(f"[LOG] {event['message']} [{event['status']}]")

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'ok'}).encode())
            except Exception as e:
                print(f"[ERROR] Failed to process log: {e}")
                self.send_response(400)
                self.end_headers()

        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def send_event(self, event):
        """Send a Server-Sent Event"""
        event_str = f"data: {json.dumps(event)}\n\n"
        self.wfile.write(event_str.encode('utf-8'))
        self.wfile.flush()

    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def run_server(port=8000):
    """Start the Durandal monitoring server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DurandalHandler)

    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║                     DURANDAL TASK MONITOR                     ║
║                   UESC Marathon - Live Feed                   ║
╚═══════════════════════════════════════════════════════════════╝

Server running at: http://localhost:{port}
Event stream:      http://localhost:{port}/events

Open live.html in your browser to see real-time task visualization.

API Endpoints:
  POST /task/start  - Start a new task
  POST /task/log    - Log an event
  GET  /events      - SSE event stream

Press Ctrl+C to stop.
""")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Durandal server stopped.")
        sys.exit(0)

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
