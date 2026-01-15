# Deploy Durandal on GitHub Codespaces

Run the live monitoring visualizer in the cloud with zero local setup.

## Setup (5 minutes)

### 1. Create a Codespace

1. Go to https://github.com/ArbitraryTitle/Durandal
2. Click the green **"Code"** button
3. Click **"Codespaces"** tab
4. Click **"Create codespace on main"**

A browser-based VS Code will open with a terminal at the bottom.

### 2. Start the Server

In the terminal at the bottom, run:

```bash
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

### 3. Open the Visualizer

A popup will appear saying **"Your application running on port 8000 is available"**

Click **"Open in Browser"**

OR manually:
1. Look for **"PORTS"** tab at bottom (next to TERMINAL)
2. Find port 8000
3. Click the globe icon to open in browser
4. Add `/live.html` to the URL

### 4. Test It

In a **new terminal** (click + next to terminal tab), run:

```bash
./test_live.sh
```

Watch the visualizer - you'll see tasks appear in real-time with chartreuse progress bars!

## For Live Monitoring During Our Chat

Keep the codespace open with:
- **Terminal 1**: Running `python3 server.py`
- **Browser tab**: Open to the visualizer (`/live.html`)

When Claude works on tasks, he can log them and you'll see real-time visualization.

## Codespace Tips

- **Free tier**: 60 hours/month, 2-core, 4GB RAM
- **Auto-sleep**: Codespace sleeps after 30 min idle
- **Wake up**: Just reopen it, run `python3 server.py` again
- **Delete when done**: Settings → "..." → Delete to free resources

## Alternative: Deploy to Vercel/Railway

If you want it always-on without managing codespaces, I can help deploy to:
- **Railway** - free tier, one-click Python deployment
- **Render** - free tier, stays awake during use
- **Fly.io** - free tier with persistent URLs

Let me know if you want those instructions instead!

---

**Easiest path: Codespaces is probably fastest for now since the repo is already there.**
