#!/bin/bash
# Quick test of Durandal live monitoring

echo "Testing Durandal live monitoring..."
echo ""

# Simulate parallel tool execution
echo "→ Starting parallel tasks..."
python3 log_task.py "Read: config.json" 1200 &
python3 log_task.py "Bash: git status" 800 &
python3 log_task.py "Grep: TODO in *.py" 1500 &
sleep 0.2

python3 log_task.py --log "Parallel tasks initiated" running
sleep 1.5

echo "→ Logging completion..."
python3 log_task.py --log "All reads completed" completed
sleep 0.5

echo "→ Starting sequential tasks..."
python3 log_task.py "Write: output.json" 600
sleep 0.8

python3 log_task.py --log "Processing finished successfully" completed

echo ""
echo "✓ Test completed. Check the visualizer!"
