#!/bin/bash
# Stop the snake animation.
PIDFILE="/tmp/medium-hike-snake.pid"
LOGFILE="/tmp/medium-hike-debug.log"

echo "$(date): stop-snake.sh called" >> "$LOGFILE"

if [ -f "$PIDFILE" ]; then
  PID="$(cat "$PIDFILE")"
  echo "$(date): killing PID $PID" >> "$LOGFILE"
  rm -f "$PIDFILE"
  kill "$PID" 2>/dev/null || true
  kill -- -"$PID" 2>/dev/null || true
else
  echo "$(date): no pidfile found" >> "$LOGFILE"
  pkill -f "snake\.py" 2>/dev/null || true
fi

exit 0
