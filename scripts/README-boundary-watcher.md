# Boundary Watcher

Two versions available:

## Option 1: boundary-watcher.js (Requires chokidar)

Uses `chokidar` for robust file watching. More reliable but requires installation.

**Install chokidar:**
```bash
npm install chokidar
```

**Run:**
```bash
node scripts/boundary-watcher.js
```

## Option 2: boundary-watcher-native.js (No Dependencies)

Uses Node's built-in `fs.watch`. Works out of the box, but may have limitations on some systems.

**Run:**
```bash
node scripts/boundary-watcher-native.js
```

## What It Does

- Watches for file changes in the workspace
- Automatically updates `.ai-context-source-of-truth.json` on changes
- Automatically generates all dashboards after updates
- Ignores common directories (node_modules, .git, etc.)
- Debounced updates (waits 1 second after last change)

## Usage

Run in background:
```bash
nohup node scripts/boundary-watcher-native.js > /dev/null 2>&1 &
```

Or use a process manager like PM2:
```bash
pm2 start scripts/boundary-watcher-native.js --name boundary-watcher
```

