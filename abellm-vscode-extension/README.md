#  AbëLLM VS Code Extension

**Replace Cursor.ai with your own AbëLLM system**

This extension uses VS Code as an event bus layer to connect to your AbëLLM backend, providing:
-  Code completions (via LSP Server)
-  Chat interface (via REST API)
-  Code actions (via MCP Server)
-  Zero external API costs

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Build Extension

```bash
npm run compile
```

### 3. Start Your AbëLLM Backend

```bash
# In your AbeOne_Master directory
python -m aiagentsuite.integration.server
```

### 4. Install Extension

```bash
# Package extension
npm run package

# Install locally
code --install-extension abellm-vscode-1.0.0.vsix
```

### 5. Use Extension

1. Open VS Code
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
3. Type "AbëLLM: Open Chat"
4. Start chatting with your own LLM!

## Configuration

Edit VS Code settings:

```json
{
  "abellm.lspServer": "ws://localhost:3000",
  "abellm.mcpServer": "http://localhost:3001",
  "abellm.restApi": "http://localhost:8000",
  "abellm.enableCompletions": true,
  "abellm.enableChat": true
}
```

## Architecture

VS Code Extension (Event Bus) → AbëLLM Backend → Orbital Modules

See `ABELLM_VSCODE_EXTENSION_ARCHITECTURE.md` for complete architecture details.

## Cost Savings

- **Cursor.ai:** $20-40/month per user
- **AbëLLM:** $0 (uses your existing infrastructure)
- **Annual Savings:** $1,200-$4,800 per 10 users

---

**Pattern:** ABELLM × VSCODE × EVENT_BUS × ORBITAL × ONE  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

