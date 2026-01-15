#!/usr/bin/env python3
"""
Durandal Logger - Automatic task logging for Claude tool execution
Import this module to automatically log tasks to the Durandal visualizer
"""

import json
import urllib.request
import urllib.error
from contextlib contextmanager
import time
from typing import Optional

class DurandalLogger:
    def __init__(self, server_url="http://localhost:8000"):
        self.server_url = server_url
        self.enabled = True

    def _send_event(self, endpoint, data):
        """Send event to Durandal server"""
        if not self.enabled:
            return False

        try:
            req = urllib.request.Request(
                f"{self.server_url}{endpoint}",
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=1) as response:
                return response.status == 200
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError):
            # Silently fail if server not available
            return False

    def task_start(self, name: str, duration: Optional[int] = None):
        """Log task start"""
        return self._send_event('/task/start', {
            'name': name,
            'duration': duration
        })

    def log(self, message: str, status: str = 'running'):
        """Log an event (status: running|completed|failed)"""
        return self._send_event('/task/log', {
            'message': message,
            'status': status
        })

    @contextmanager
    def task(self, name: str):
        """Context manager for automatic task logging"""
        self.task_start(name)
        start_time = time.time()
        try:
            yield self
            duration = int((time.time() - start_time) * 1000)
            self.log(f"{name} completed [{duration}ms]", 'completed')
        except Exception as e:
            self.log(f"{name} failed: {str(e)}", 'failed')
            raise

# Global instance
logger = DurandalLogger()

# Convenience functions
def task_start(name: str, duration: Optional[int] = None):
    """Start a task"""
    logger.task_start(name, duration)

def log(message: str, status: str = 'running'):
    """Log an event"""
    logger.log(message, status)

@contextmanager
def task(name: str):
    """Context manager for tasks"""
    with logger.task(name):
        yield

# Example usage:
"""
from durandal_logger import task_start, log, task

# Simple logging
task_start("Read config.json", 1000)
log("Found 3 configuration files", "running")
log("Configuration loaded", "completed")

# Or use context manager
with task("Process data"):
    # Your code here
    pass
"""
