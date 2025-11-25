# Terminal Troubleshooting Guide

## VS Code Terminal Won't Start

### Quick Fixes

1. **Reset Terminal Configuration**
   - Open VS Code Settings (⌘,)
   - Search for "terminal.integrated.shell"
   - Set to `/bin/zsh`
   - Or use the `.vscode/settings.json` file created in this project

2. **Kill All Terminal Processes**
   ```bash
   # In a working terminal (outside VS Code)
   pkill -f "code.*terminal"
   ```

3. **Reset VS Code Terminal**
   - Press `⌘K` then `⌘S` to save and reload
   - Or: Command Palette (⌘⇧P) → "Terminal: Kill All Terminals"
   - Then create a new terminal

4. **Check for Hanging Startup Scripts**
   ```bash
   # Test if zsh starts normally
   zsh -c "echo 'Shell works'"
   
   # Check startup scripts for issues
   zsh -x ~/.zshrc 2>&1 | head -20
   ```

5. **Use External Terminal**
   - Command Palette (⌘⇧P) → "Terminal: Open in External Terminal"
   - This bypasses VS Code's terminal integration

### Advanced Troubleshooting

#### Check Terminal Profile
```bash
# Verify shell path
which zsh
# Should output: /bin/zsh
```

#### Test Shell Startup
```bash
# Test with minimal config
zsh --no-rcs
# If this works, your .zshrc might have issues
```

#### Check VS Code Terminal Logs
- View → Output → Select "Terminal" from dropdown
- Look for error messages

#### Reset VS Code Terminal Settings
1. Open Settings (⌘,)
2. Search "terminal"
3. Click "Reset Setting" on any terminal-related settings
4. Restart VS Code

### Common Issues

**Issue: Terminal shows "⌘K to generate command"**
- This is VS Code waiting for input
- Try pressing `Esc` to cancel
- Or kill the terminal and create a new one

**Issue: Terminal hangs on startup**
- Check `.zshrc` for blocking commands
- Look for `read`, `wait`, or network calls
- Temporarily rename `.zshrc` to test:
  ```bash
  mv ~/.zshrc ~/.zshrc.backup
  # Test terminal, then restore if needed
  mv ~/.zshrc.backup ~/.zshrc
  ```

**Issue: Terminal profile not found**
- Verify shell exists: `ls -la /bin/zsh`
- Check VS Code settings for correct path
- Try absolute path: `/bin/zsh`

### VS Code Settings Created

A `.vscode/settings.json` file has been created with proper terminal configuration:
- Shell path: `/bin/zsh`
- Default profile: `zsh`
- Inherit environment: `true`

### Still Not Working?

1. **Restart VS Code completely**
   ```bash
   # Kill all VS Code processes
   killall "Visual Studio Code" 2>/dev/null || killall "Code" 2>/dev/null
   # Then reopen VS Code
   ```

2. **Check VS Code Extensions**
   - Disable terminal-related extensions
   - Test if terminal works without them
   - Re-enable one by one to find culprit

3. **Reinstall VS Code Terminal**
   - This is usually not necessary
   - But if all else fails, reinstall VS Code

4. **Use External Terminal**
   - Terminal.app or iTerm2
   - Configure VS Code to open external terminal
   - Settings → Terminal → External → Set to your preferred terminal

### Quick Test

Run this in a working terminal (outside VS Code):
```bash
cd /Users/michaelmataluni/Documents/AbeOne_Master
code .
# Then try opening a terminal in VS Code
```

If this works, the issue was likely a VS Code state problem that's now resolved.

