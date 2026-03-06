#!/bin/bash
# Kill any existing snake, then start a new one in the background.
PIDFILE="/tmp/medium-hike-snake.pid"
LOGFILE="/tmp/medium-hike-debug.log"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "$(date): start-snake.sh called" >> "$LOGFILE"

if [ -f "$PIDFILE" ]; then
  OLD_PID="$(cat "$PIDFILE")"
  echo "$(date): killing old PID $OLD_PID" >> "$LOGFILE"
  kill "$OLD_PID" 2>/dev/null
  rm -f "$PIDFILE"
fi

python3 "$SCRIPT_DIR/snake.py" &
echo $! > "$PIDFILE"
echo "$(date): started new snake PID $!" >> "$LOGFILE"
