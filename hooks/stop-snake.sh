#!/bin/bash
# Stop the snake animation.
PIDFILE="/tmp/medium-hike-snake.pid"
LOGFILE="/tmp/medium-hike-debug.log"

echo "$(date): stop-snake.sh called" >> "$LOGFILE"

if [ -f "$PIDFILE" ]; then
  PID="$(cat "$PIDFILE")"
  echo "$(date): killing PID $PID" >> "$LOGFILE"
  rm -f "$PIDFILE"
  kill "$PID" 2>/dev/null
  # Also kill the entire process group to catch children
  kill -- -"$PID" 2>/dev/null
else
  echo "$(date): no pidfile found" >> "$LOGFILE"
  # Fallback: kill any lingering snake processes
  pkill -f "snake\.py" 2>/dev/null
fi
