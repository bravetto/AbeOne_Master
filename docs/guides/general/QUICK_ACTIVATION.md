# QUICK ACTIVATION

## One Command

```bash
./scripts/activate-event-driven.sh
```

## Three Steps

### 1. Install Git Hooks
```bash
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
```

### 2. Start Boundary Watcher (Optional)
```bash
node scripts/boundary-watcher-native.js
```

### 3. Use Pulse Anytime
```bash
node scripts/pulse.js
```

## That's It!

- Git commits/pushes auto-update source of truth  
- File changes auto-update (if watcher running)  
- Manual sync with `pulse` anytime

