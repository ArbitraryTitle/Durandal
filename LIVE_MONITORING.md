# Durandal Live Monitoring

Real-time visualization of parallel task execution using Server-Sent Events (SSE).

## Quick Start

### 1. Start the Server

```bash
cd /home/user/marathon-task-viz
python3 server.py
```

You'll see:
```
╔═══════════════════════════════════════════════════════════════╗
║                     DURANDAL TASK MONITOR                     ║
║                   UESC Marathon - Live Feed                   ║
╚═══════════════════════════════════════════════════════════════╝

Server running at: http://localhost:8000
```

### 2. Open the Visualizer

Open your browser to: **http://localhost:8000/live.html**

You'll see the Marathon-themed interface with:
- **CONNECTION** status (shows LIVE when connected)
- **ACTIVE THREADS** panel on the left
- **EVENT STREAM** timeline on the right

### 3. Send Task Events

Now whenever Claude executes tools, log them to see real-time visualization.

## Logging Methods

### Method 1: Quick Shell Commands

```bash
# Start a task
python3 log_task.py "Read: config.json" 1500

# Log an event
python3 log_task.py --log "File processed successfully" completed
python3 log_task.py --log "Error: file not found" failed
```

### Method 2: Python Integration

```python
from durandal_logger import task_start, log, task

# Simple logging
task_start("Bash: git status", 800)
log("Repository status checked", "completed")

# Context manager (auto-completion)
with task("Grep: search patterns"):
    # Your code here
    pass  # Automatically logs completion with duration
```

### Method 3: Manual HTTP Requests

```bash
# Start a task
curl -X POST http://localhost:8000/task/start \
  -H "Content-Type: application/json" \
  -d '{"name": "Read: slide38.xml", "duration": 1200}'

# Log an event
curl -X POST http://localhost:8000/task/log \
  -H "Content-Type: application/json" \
  -d '{"message": "Found 10 cocktail entries", "status": "completed"}'
```

## Event Types

### Task Start
```json
{
  "name": "Read: config.json",
  "duration": 1500  // optional, in milliseconds
}
```

Creates a thread visualization with progress bar.

### Log Event
```json
{
  "message": "Task completed successfully",
  "status": "running|completed|failed"
}
```

Adds an entry to the timeline:
- **running** = cyan dot
- **completed** = chartreuse dot
- **failed** = red dot

## Claude Integration Example

When Claude makes parallel tool calls, log them:

```bash
# Terminal 1: Server running
python3 server.py

# Terminal 2: Log Claude's actions
python3 log_task.py "Read: slide38.xml" 800 &
python3 log_task.py "Read: slide39.xml" 750 &
python3 log_task.py "Read: slide40.xml" 900 &
python3 log_task.py --log "Loaded 3 slides in parallel" completed
```

The visualizer will show all three tasks running simultaneously with animated progress bars.

## Real-World Usage

### Scenario: Claude sorting cocktail tables

```python
from durandal_logger import task_start, log

# Initial exploration
task_start("Bash: find *.xml files", 500)
log("Found 7 slide files", "completed")

# Parallel reads
for i in range(38, 45):
    task_start(f"Read: slide{i}.xml", 800)

log("Extracted 62 cocktail entries", "completed")

# Processing
with task("Sort by year and date"):
    # sorting logic
    pass

# Writing back
for i in range(38, 45):
    task_start(f"Write: slide{i}.xml", 600)

log("All slides updated", "completed")
```

This creates a visual representation of:
1. Single task for file discovery
2. 7 parallel read operations
3. Processing step
4. 7 parallel write operations
5. Timeline events showing progress

## Architecture

```
┌─────────────────┐
│   Browser       │
│   (live.html)   │
└────────┬────────┘
         │ SSE Stream
         │ (GET /events)
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Python Server  │◄─────│  Task Loggers    │
│  (server.py)    │      │  (log_task.py)   │
└─────────────────┘      └──────────────────┘
         │                         ▲
         │                         │
         │                   POST /task/start
         │                   POST /task/log
         │                         │
         └─────────────────────────┘
```

1. **Server** (`server.py`) - HTTP server + SSE broadcaster
2. **Visualizer** (`live.html`) - Marathon-themed UI with SSE client
3. **Loggers** - Tools to send task events

## Features

- **Real-time updates** via Server-Sent Events
- **Automatic reconnection** with exponential backoff
- **Parallel thread visualization** with progress bars
- **Timeline events** with status indicators
- **Zero configuration** - just run and open browser

## Troubleshooting

### "Connection: DISCONNECTED"

Server not running. Start it:
```bash
python3 server.py
```

### Tasks not appearing

Check server terminal for errors. Try manual test:
```bash
curl -X POST http://localhost:8000/task/start \
  -H "Content-Type: application/json" \
  -d '{"name": "Test task"}'
```

### Port already in use

Run on different port:
```bash
python3 server.py 8080
```

Then open: http://localhost:8080/live.html

## Advanced: Browser Console Debugging

Open browser console (F12) to see:
```
[DURANDAL] Connecting to event stream...
[DURANDAL] Connected to live feed
[EVENT] {type: 'task_start', name: 'Read: config.json', ...}
```

## Future: Automatic Claude Integration

To truly automate this, we'd need:

1. **Claude Code hooks** - if Claude Code exposes pre/post tool execution hooks
2. **Network proxy** - intercept HTTP requests to Claude API
3. **Custom client** - modified Claude Code that logs tool calls

For now, manual logging gives you full visibility into parallel execution as it happens.

---

**UESC CLEARANCE: ALPHA-7 // LIVE FEED ACTIVE**
