# GitHub Setup Instructions

The repository has been initialized locally at `/home/user/marathon-task-viz`

## Push to GitHub

### Option 1: Using GitHub CLI (if installed)

```bash
cd /home/user/marathon-task-viz
gh repo create marathon-task-viz --public --source=. --remote=origin --push
```

### Option 2: Manual Setup

1. Go to https://github.com/new
2. Create a new repository named `marathon-task-viz`
3. Don't initialize with README (we already have one)
4. Run these commands:

```bash
cd /home/user/marathon-task-viz
git remote add origin https://github.com/YOUR_USERNAME/marathon-task-viz.git
git branch -M main
git push -u origin main
```

### Option 3: Using SSH

```bash
cd /home/user/marathon-task-viz
git remote add origin git@github.com:YOUR_USERNAME/marathon-task-viz.git
git branch -M main
git push -u origin main
```

## Files Included

- `index.html` - Main application interface
- `style.css` - Marathon-inspired styling (cyan/orange/purple aesthetic)
- `script.js` - Task visualization logic and API
- `README.md` - Project documentation
- `SETUP.md` - This file

## Quick Test

To test locally before pushing:

```bash
cd /home/user/marathon-task-viz
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

You should see:
- Dark Marathon-themed interface
- "UESC TASK MONITOR" header with glitch effect
- Status bar showing system stats
- Thread visualization panel
- Timeline panel
- Control buttons

Click "SPAWN PARALLEL THREADS" to see the visualization in action!
