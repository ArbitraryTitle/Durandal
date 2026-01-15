# UESC Task Monitor // Marathon Edition

A parallel task execution visualizer inspired by the aesthetic of Bungie's Marathon (2026). Monitors and displays concurrent threads with that cyberpunk colony ship terminal vibe.

![Marathon Aesthetic](https://img.shields.io/badge/aesthetic-marathon-00d9ff?style=for-the-badge)
![Status](https://img.shields.io/badge/status-operational-00ff88?style=for-the-badge)

## Features

- **Real-time thread visualization** - watch parallel tasks execute with animated progress bars
- **Timeline event logging** - chronological execution history with status indicators
- **Marathon-inspired UI** - dark cyan/orange/purple color scheme, geometric panels, terminal aesthetics
- **JavaScript API** - integrate with your own applications to visualize actual parallel execution
- **Responsive design** - works on desktop and mobile

## Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/marathon-task-viz.git
cd marathon-task-viz

# Open in browser
open index.html
# or
python3 -m http.server 8000
```

Then navigate to `http://localhost:8000`

## Usage

### Interactive Demo

Click the buttons to simulate tasks:
- **INITIALIZE TASK** - spawn a single thread
- **SPAWN PARALLEL THREADS** - create 5 concurrent tasks (simulates Claude's parallel tool calls)
- **PURGE LOGS** - clear all threads and timeline events

### JavaScript API

Integrate with your own code:

```javascript
// Start a single task
taskMonitor.startTask("Read file: config.json", 3000);

// Start multiple parallel tasks
taskMonitor.startParallelTasks([
    { name: "Bash: git status", duration: 2000 },
    { name: "Read: script.py", duration: 1500 },
    { name: "Grep: search pattern", duration: 2500 }
]);

// Log custom events
taskMonitor.logEvent("Branch created successfully", "completed");
taskMonitor.logEvent("Error: file not found", "failed");

// Get current stats
const stats = taskMonitor.getStats();
console.log(`Active: ${stats.activeThreads}, Completed: ${stats.completedTasks}`);
```

## Aesthetic Details

The visual design draws from Marathon's UI:

- **Color Palette**
  - Background: `#0a0e14` (deep space black)
  - Primary Accent: `#7fff00` (chartreuse/lime green)
  - Secondary Accents: `#ff6b35` (orange/amber), `#00d9ff` (cyan/teal)
  - Highlight: `#b537f2` (purple/magenta)

- **Typography**: Share Tech Mono (monospace terminal font)

- **Visual Effects**
  - Glitch animations on title
  - Neon glow shadows
  - Geometric clip-path panels
  - Grid pattern background
  - Animated progress bars with shimmer

## Use Cases

- **AI/LLM Monitoring** - visualize Claude's parallel tool execution
- **Build Systems** - monitor concurrent compilation tasks
- **CI/CD Pipelines** - track parallel job execution
- **Data Processing** - show multi-threaded operations
- **General Parallelism** - any scenario with concurrent tasks

## Integration Example

For monitoring Claude Code parallel tool calls:

```javascript
// When Claude makes parallel tool calls
const tools = [
    { name: "Read: slide38.xml", duration: 800 },
    { name: "Read: slide39.xml", duration: 750 },
    { name: "Read: slide40.xml", duration: 900 }
];

taskMonitor.startParallelTasks(tools);
```

## Technical Notes

- Pure vanilla JS, no frameworks
- Single-page application
- CSS Grid and Flexbox layouts
- Responsive breakpoints at 768px
- Custom scrollbar styling
- Keyframe animations for all effects

## Future Enhancements

- [ ] WebSocket support for live task streaming
- [ ] Save/export timeline logs
- [ ] Custom color theme editor
- [ ] Task dependency visualization
- [ ] Performance metrics dashboard
- [ ] Sound effects (terminal beeps, completion chimes)

## Inspiration

Built for visualizing parallel AI agent execution, styled after the UESC Marathon terminal interfaces from Bungie's upcoming extraction shooter. That dark retrofuture aesthetic with modern cyberpunk sensibilities.

## License

MIT - do whatever you want with it

---

**SECURITY CLEARANCE: ALPHA-7 // DO NOT DISTRIBUTE**
