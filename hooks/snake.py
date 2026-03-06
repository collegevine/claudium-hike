#!/usr/bin/env python3
"""
Animate "MEDIUM HIKE" as a meandering snake across the terminal.
Writes directly to /dev/tty. Self-terminates when inference ends.
"""

import os
import random
import signal
import sys
import time

TEXT = "MEDIUM HIKE"
SPEED = 0.08
MAX_LIFETIME = 300
STALE_TIMEOUT = 3  # die if pidfile untouched for this long
PIDFILE = "/tmp/medium-hike-snake.pid"
LOGFILE = "/tmp/medium-hike-debug.log"

COLORS = [
    "\033[1;35m",
    "\033[1;36m",
    "\033[1;33m",
    "\033[1;32m",
    "\033[1;31m",
    "\033[1;34m",
]
RESET = "\033[0m"


def log(msg):
    with open(LOGFILE, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} snake: {msg}\n")


def get_terminal_size():
    try:
        cols, rows = os.get_terminal_size(
            os.open("/dev/tty", os.O_RDWR)
        )
    except Exception:
        cols, rows = 80, 24
    return cols, rows


def write_tty(s):
    try:
        tty.write(s)
        tty.flush()
    except Exception:
        sys.exit(0)


def cleanup(reason="unknown", *_):
    log(f"cleanup: {reason}")
    write_tty("\033[?25h")
    for r, c in prev_positions:
        write_tty(f"\033[{r};{c}H ")
    write_tty("\033[u")
    sys.exit(0)


def should_stop():
    """PID file gone, changed, or stale = time to die."""
    # File deleted?
    if not os.path.exists(PIDFILE):
        log("pidfile gone")
        return "pidfile_gone"

    # PID changed (new snake replaced us)?
    try:
        with open(PIDFILE) as f:
            pid = int(f.read().strip())
            if pid != os.getpid():
                log(f"pid mismatch: file={pid} self={os.getpid()}")
                return "pid_mismatch"
    except Exception as e:
        log(f"pidfile read error: {e}")
        return "pidfile_error"

    # Stale? File not touched since we started.
    try:
        age = time.time() - os.path.getmtime(PIDFILE)
        if age > STALE_TIMEOUT:
            log(f"pidfile stale: age={age:.1f}s")
            return "stale"
    except Exception as e:
        log(f"mtime error: {e}")
        return "mtime_error"

    return None


tty = open("/dev/tty", "w")
prev_positions = []

signal.signal(signal.SIGTERM, lambda *_: cleanup("SIGTERM"))
signal.signal(signal.SIGINT, lambda *_: cleanup("SIGINT"))

log(f"started pid={os.getpid()}")

cols, rows = get_terminal_size()

head_row = random.randint(1, rows)
head_col = random.randint(1, cols)
dx = random.choice([-1, 0, 1])
dy = random.choice([-1, 1])

body = []
for i in range(len(TEXT)):
    body.append((head_row, max(1, head_col - i)))

write_tty("\033[?25l")
write_tty("\033[s")

start_time = time.monotonic()
frame = 0

while True:
    if time.monotonic() - start_time > MAX_LIFETIME:
        cleanup("max_lifetime")

    frame += 1
    # Check every ~0.5s (6 frames at 80ms)
    if frame % 6 == 0:
        reason = should_stop()
        if reason:
            cleanup(reason)

    if random.random() < 0.05:
        cols, rows = get_terminal_size()

    if random.random() < 0.3:
        dx = random.choice([-1, 0, 0, 1])
    if random.random() < 0.2:
        dy = random.choice([-1, -1, 0, 1, 1])

    new_row = body[0][0] + dx
    new_col = body[0][1] + dy

    if new_row < 1 or new_row > rows:
        dx = -dx
        new_row = body[0][0] + dx
    if new_col < 1 or new_col > cols:
        dy = -dy
        new_col = body[0][1] + dy

    new_row = max(1, min(rows, new_row))
    new_col = max(1, min(cols, new_col))

    if prev_positions:
        old_r, old_c = prev_positions[-1]
        write_tty(f"\033[{old_r};{old_c}H ")

    body = [(new_row, new_col)] + body[:-1]

    for i, (r, c) in enumerate(body):
        color = COLORS[i % len(COLORS)]
        write_tty(f"\033[{r};{c}H{color}{TEXT[i]}{RESET}")

    write_tty("\033[u")

    prev_positions = list(body)
    time.sleep(SPEED)
