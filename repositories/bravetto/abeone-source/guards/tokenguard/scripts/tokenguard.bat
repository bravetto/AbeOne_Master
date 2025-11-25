@echo off
REM TokenGuard Tool Launcher
REM Usage: tokenguard [command] [args...]
REM Example: tokenguard demo
REM Example: tokenguard optimize "Your text" --confidence 0.5

python "%~dp0tokenguard_tool.py" %*