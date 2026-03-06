# medium-hike

A Claude Code plugin that shows **MEDIUM HIKE** snaking across the top of your
terminal while Claude is thinking.

## Install

### Option A: Direct from GitHub

```
/plugin marketplace add YOUR_GITHUB_USERNAME/medium-hike-plugin
/plugin install medium-hike@medium-hike-plugin
```

### Option B: Local testing

```bash
claude --plugin-dir /path/to/medium-hike-plugin
```

## How it works

- **`UserPromptSubmit`** hook launches an animation in the background
- **`Stop`** hook kills it when Claude finishes responding
- The animation writes directly to `/dev/tty` using ANSI escape codes,
  bouncing bold magenta text horizontally across row 1

## Caveats

Writing to `/dev/tty` during Claude Code's rendering is inherently hacky and
may cause visual glitches. Adjust `row` or `sleep` in `hooks/snake.sh` to taste.
