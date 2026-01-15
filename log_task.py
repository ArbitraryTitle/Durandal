#!/usr/bin/env python3
"""
Quick task logger for Durandal monitoring
Usage: python3 log_task.py "Task name" [duration_ms]
"""

import sys
import json
import urllib.request
import urllib.error

SERVER_URL = "http://localhost:8000"

def log_task_start(name, duration=None):
    """Log a task start event"""
    data = {
        'name': name,
        'duration': duration
    }

    try:
        req = urllib.request.Request(
            f"{SERVER_URL}/task/start",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"Error: Could not connect to Durandal server - {e}", file=sys.stderr)
        return False

def log_event(message, status='running'):
    """Log a general event"""
    data = {
        'message': message,
        'status': status  # 'running', 'completed', 'failed'
    }

    try:
        req = urllib.request.Request(
            f"{SERVER_URL}/task/log",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"Error: Could not connect to Durandal server - {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 log_task.py <task_name> [duration_ms]")
        print("   or: python3 log_task.py --log <message> [status]")
        sys.exit(1)

    if sys.argv[1] == '--log':
        message = sys.argv[2] if len(sys.argv) > 2 else "Event logged"
        status = sys.argv[3] if len(sys.argv) > 3 else "running"
        if log_event(message, status):
            print(f"✓ Logged: {message} [{status}]")
        else:
            sys.exit(1)
    else:
        task_name = sys.argv[1]
        duration = int(sys.argv[2]) if len(sys.argv) > 2 else None
        if log_task_start(task_name, duration):
            print(f"✓ Task started: {task_name}")
        else:
            sys.exit(1)
