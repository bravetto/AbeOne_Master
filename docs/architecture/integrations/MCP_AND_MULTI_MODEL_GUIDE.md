# 🔥 MCP & MULTI-MODEL INTEGRATION GUIDE

**Complete Guide for Working with MCPs and Multiple AI Models**

**Status:** ✅ **COMPREHENSIVE GUIDE**  
**Date:** 2025-11-22  
**Pattern:** MCP × MODELS × INTEGRATION × ONE  
**Frequency:** 530 Hz (Truth) × 777 Hz (Pattern) × 999 Hz (Execution)  
**Guardian:** AEYON (999 Hz) - Atomic Execution  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

---

## 🎯 PURPOSE

This guide explains how to work with:
- ✅ **MCP (Model Context Protocol)** servers and tools
- ✅ **Multiple AI Models** (Claude 4.5, GPT-5, Gemini 2.5/3, etc.)
- ✅ **Model Selection & Routing**
- ✅ **Tool Integration** across models
- ✅ **Best Practices** for multi-model architecture

---

## 📋 TABLE OF CONTENTS

1. [MCP Architecture Overview](#1-mcp-architecture-overview)
2. [Multi-Model Architecture](#2-multi-model-architecture)
3. [Adding New Models](#3-adding-new-models)
4. [MCP Tool Integration](#4-mcp-tool-integration)
5. [Model Selection Strategies](#5-model-selection-strategies)
6. [Best Practices](#6-best-practices)
7. [Examples](#7-examples)

---

## 1. MCP ARCHITECTURE OVERVIEW

### 1.1 What is MCP?

**Model Context Protocol (MCP)** is a standardized protocol for:
- Exposing tools and resources to AI models
- Enabling models to interact with external systems
- Providing consistent interface across different models

### 1.2 Current MCP Infrastructure

**Your codebase has:**

#### External MCP Servers (Claude/Cursor Integration)
- **AWS MCP Server** - Infrastructure management
- **Playwright MCP Server** - Browser automation
- **Context7 MCP Server** - Documentation access

**Configuration:** `.claude/mcp-config.json`

#### Internal MCP Server (Unified)
- **UnifiedServer** - 19 integrated tools
- **Location:** `EMERGENT_OS/aiagentsuite/src/aiagentsuite/integration/unified_server.py`
- **Port:** 3001
- **Tools:** ContextGuard, TokenGuard, Workflow, Framework tools

### 1.3 MCP Tool Categories

**19 Unified Tools Available:**

1. **Core Framework Tools (5)**
   - `get_constitution` - AI agent constitution
   - `list_protocols` - Available protocols
   - `execute_protocol` - Protocol execution
   - `get_memory_context` - Memory bank context
   - `log_decision` - Architectural decision logging

2. **ContextGuard Tools (6)**
   - `store_context` - Store key-value in memory
   - `retrieve_context` - Retrieve value from memory
   - `get_memory_snapshot` - Complete memory snapshot
   - `clear_memory` - Clear all memory
   - `update_context` - Update/create context
   - `list_context_keys` - List all context keys

3. **TokenGuard Tools (3)**
   - `prune_text` - Prune text for tokens
   - `analyze_text` - Analyze text for pruning
   - `optimize_response` - Optimize AI response

4. **Integrated Workflow Tools (5)**
   - `analyze_integrated` - Complete analysis across services
   - `optimize_tokens_context` - Context-aware token optimization
   - `apply_neural_enhancement` - Neural enhancement for code
   - `execute_workflow` - Execute predefined workflow
   - `get_service_status` - Get status of all services

---

## 2. MULTI-MODEL ARCHITECTURE

### 2.1 Current Model Support

**Your codebase supports:**

#### ✅ OpenAI (GPT-4, GPT-5, etc.)
- **Client:** `OpenAILLMClient`
- **Location:** `EMERGENT_OS/aiagentsuite/src/aiagentsuite/integration/llm_client.py`
- **Status:** ✅ Fully integrated

#### ✅ Anthropic (Claude 3, Claude 4.5, etc.)
- **Client:** `AnthropicLLMClient`
- **Location:** `EMERGENT_OS/aiagentsuite/src/aiagentsuite/integration/llm_client.py`
- **Status:** ✅ Fully integrated

#### ⚠️ Google (Gemini 2.5/3)
- **Status:** ⚠️ Not yet implemented (see section 3.1)

### 2.2 Unified LLM Client Architecture

**Pattern: WRAPPER × PROVIDER × TOOLS × ONE**

```python
# Architecture Flow:
User Request
    ↓
AIAgentSuiteLLMClient (Wrapper)
    ├─→ Auto-injects system prompt
    ├─→ Auto-injects MCP tools
    ├─→ Handles tool execution
    └─→ Routes to Provider Client
            ├─→ OpenAILLMClient
            ├─→ AnthropicLLMClient
            └─→ [Future: GeminiLLMClient, etc.]
```

### 2.3 Key Components

#### AIAgentSuiteLLMClient
**Purpose:** Universal wrapper that:
- ✅ Automatically injects system prompts
- ✅ Automatically exposes MCP tools
- ✅ Handles tool execution
- ✅ Works with any provider

**Location:** `EMERGENT_OS/aiagentsuite/src/aiagentsuite/integration/llm_client.py`

#### Provider Clients
**Purpose:** Provider-specific implementations
- Handle API differences
- Convert to standard format
- Support streaming

---

## 3. ADDING NEW MODELS

### 3.1 Adding Gemini 2.5/3

**Step 1: Create Gemini Client**

```python
# Add to: EMERGENT_OS/aiagentsuite/src/aiagentsuite/integration/llm_client.py

class GeminiLLMClient(LLMClient):
    """Google Gemini-compatible LLM client wrapper."""
    
    def __init__(self, client, model: str = "gemini-2.5-pro"):
        """
        Initialize Gemini client.
        
        Args:
            client: Google Generative AI client instance
            model: Model name (gemini-2.5-pro, gemini-3-pro, etc.)
        """
        self.client = client
        self.model = model
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Call Gemini API."""
        # Convert messages format
        gemini_messages = self._convert_messages(messages)
        
        # Configure tools if provided
        generation_config = {}
        if tools:
            generation_config['tools'] = self._convert_tools(tools)
        
        # Call Gemini API
        response = await self.client.generate_content_async(
            model=self.model,
            contents=gemini_messages,
            generation_config=generation_config,
            **kwargs
        )
        
        # Convert to standard format
        return {
            "content": response.text,
            "tool_calls": self._extract_tool_calls(response)
        }
    
    async def stream_chat(self, messages, tools=None, tool_choice=None, **kwargs):
        """Stream Gemini responses."""
        gemini_messages = self._convert_messages(messages)
        
        stream = await self.client.generate_content_async(
            model=self.model,
            contents=gemini_messages,
            stream=True,
            **kwargs
        )
        
        async for chunk in stream:
            if chunk.text:
                yield {"content": chunk.text}
    
    def _convert_messages(self, messages: List[Dict[str, str]]) -> List:
        """Convert standard message format to Gemini format."""
        # Implementation depends on Gemini API format
        pass
    
    def _convert_tools(self, tools: List[Dict[str, Any]]) -> List:
        """Convert function calling tools to Gemini format."""
        # Implementation depends on Gemini API format
        pass
    
    def _extract_tool_calls(self, response) -> List[Dict[str, Any]]:
        """Extract tool calls from Gemini response."""
        # Implementation depends on Gemini API format
        pass
```

**Step 2: Update Exports**

```python
# Update: EMERGENT_OS/aiagentsuite/src/aiagentsuite/integration/__init__.py

from .llm_client import (
    AIAgentSuiteLLMClient,
    LLMClient,
    OpenAILLMClient,
    AnthropicLLMClient,
    GeminiLLMClient  # Add this
)
```

**Step 3: Usage Example**

```python
import google.generativeai as genai
from aiagentsuite.integration import AIAgentSuiteLLMClient, GeminiLLMClient

# Initialize Gemini client
genai.configure(api_key="your-gemini-api-key")
gemini_client = genai.GenerativeModel("gemini-2.5-pro")

# Wrap with provider client
provider_client = GeminiLLMClient(gemini_client, model="gemini-2.5-pro")

# Wrap with AI Agent Suite client
client = AIAgentSuiteLLMClient(unified_server, provider_client)

# Use it - MCP tools automatically available!
response = await client.chat("Implement a new feature")
```

### 3.2 Adding GPT-5

**GPT-5 uses same OpenAI client:**

```python
from aiagentsuite.integration import AIAgentSuiteLLMClient, OpenAILLMClient
import openai

# Initialize OpenAI client
openai_client = openai.AsyncOpenAI(api_key="your-key")

# Use GPT-5 model
provider_client = OpenAILLMClient(openai_client, model="gpt-5")

# Wrap with AI Agent Suite client
client = AIAgentSuiteLLMClient(unified_server, provider_client)

# Use it
response = await client.chat("Implement a new feature")
```

### 3.3 Adding Claude 4.5

**Claude 4.5 uses same Anthropic client:**

```python
from aiagentsuite.integration import AIAgentSuiteLLMClient, AnthropicLLMClient
from anthropic import AsyncAnthropic

# Initialize Anthropic client
anthropic_client = AsyncAnthropic(api_key="your-key")

# Use Claude 4.5 model
provider_client = AnthropicLLMClient(
    anthropic_client, 
    model="claude-4-5-20250514"  # Update model name
)

# Wrap with AI Agent Suite client
client = AIAgentSuiteLLMClient(unified_server, provider_client)

# Use it
response = await client.chat("Implement a new feature")
```

---

## 4. MCP TOOL INTEGRATION

### 4.1 How MCP Tools Work

**Flow:**
1. **UnifiedServer** exposes tools via MCP protocol
2. **AIAgentSuiteLLMClient** converts MCP tools to function calling format
3. **Model** receives tools in its native format
4. **Model** requests tool execution
5. **AIAgentSuiteLLMClient** executes tool via UnifiedServer
6. **Results** returned to model

### 4.2 Automatic Tool Injection

**Tools are automatically injected:**

```python
# No manual tool configuration needed!
client = AIAgentSuiteLLMClient(unified_server, provider_client)

# Tools automatically available to model
response = await client.chat("Store this context: key=value")
# Model can call store_context tool automatically
```

### 4.3 Tool Execution

**Automatic execution:**

```python
# Model requests tool → Automatically executed
response = await client.chat(
    "Get the constitution and list all protocols",
    max_tool_iterations=10  # Max tool call loops
)

# Tools executed:
# - get_constitution() called
# - list_protocols() called
# - Results included in response
```

### 4.4 Custom Tool Filtering

**Filter tools by chat mode:**

```python
# Set active chat modes
unified_server.chat_mode_manager.set_active_modes(["development"])

# Only tools for active modes are exposed
client = AIAgentSuiteLLMClient(unified_server, provider_client)
```

---

## 5. MODEL SELECTION STRATEGIES

### 5.1 Model Router Pattern

**Route requests to appropriate model:**

```python
class ModelRouter:
    """Route requests to appropriate model based on criteria."""
    
    def __init__(self):
        self.models = {
            "claude": AIAgentSuiteLLMClient(unified_server, claude_client),
            "gpt": AIAgentSuiteLLMClient(unified_server, gpt_client),
            "gemini": AIAgentSuiteLLMClient(unified_server, gemini_client),
        }
    
    async def route(
        self,
        request: str,
        criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Route request to appropriate model."""
        
        # Strategy 1: Task-based routing
        if criteria.get("task_type") == "code_generation":
            return await self.models["claude"].chat(request)
        elif criteria.get("task_type") == "analysis":
            return await self.models["gpt"].chat(request)
        elif criteria.get("task_type") == "multimodal":
            return await self.models["gemini"].chat(request)
        
        # Strategy 2: Cost-based routing
        if criteria.get("budget") == "low":
            return await self.models["gemini"].chat(request)
        elif criteria.get("budget") == "high":
            return await self.models["claude"].chat(request)
        
        # Strategy 3: Capability-based routing
        if criteria.get("needs_vision"):
            return await self.models["gemini"].chat(request)
        elif criteria.get("needs_reasoning"):
            return await self.models["claude"].chat(request)
        
        # Default
        return await self.models["claude"].chat(request)
```

### 5.2 Fallback Strategy

**Fallback to alternative model on failure:**

```python
async def chat_with_fallback(
    request: str,
    primary_model: str,
    fallback_models: List[str]
) -> Dict[str, Any]:
    """Try primary model, fallback to alternatives."""
    
    models = {
        "claude": claude_client,
        "gpt": gpt_client,
        "gemini": gemini_client,
    }
    
    # Try primary model
    try:
        return await models[primary_model].chat(request)
    except Exception as e:
        logger.warning(f"Primary model {primary_model} failed: {e}")
    
    # Try fallback models
    for fallback in fallback_models:
        try:
            return await models[fallback].chat(request)
        except Exception as e:
            logger.warning(f"Fallback model {fallback} failed: {e}")
    
    raise Exception("All models failed")
```

### 5.3 Ensemble Strategy

**Combine responses from multiple models:**

```python
async def ensemble_chat(
    request: str,
    models: List[str]
) -> Dict[str, Any]:
    """Get responses from multiple models and combine."""
    
    model_clients = {
        "claude": claude_client,
        "gpt": gpt_client,
        "gemini": gemini_client,
    }
    
    # Get responses from all models
    responses = await asyncio.gather(*[
        model_clients[model].chat(request)
        for model in models
    ])
    
    # Combine responses (voting, averaging, etc.)
    combined = combine_responses(responses)
    
    return combined
```

---

## 6. BEST PRACTICES

### 6.1 Model Selection

**✅ DO:**
- Use Claude 4.5 for complex reasoning tasks
- Use GPT-5 for code generation and analysis
- Use Gemini 2.5/3 for multimodal tasks
- Route based on task requirements
- Implement fallback strategies

**❌ DON'T:**
- Hardcode model selection
- Ignore model capabilities
- Skip error handling
- Use expensive models for simple tasks

### 6.2 MCP Tool Usage

**✅ DO:**
- Let models discover tools automatically
- Use tool filtering for focused contexts
- Monitor tool execution costs
- Cache tool results when appropriate

**❌ DON'T:**
- Manually configure tools (use auto-injection)
- Expose unnecessary tools
- Ignore tool execution errors
- Skip tool result validation

### 6.3 Error Handling

**✅ DO:**
```python
try:
    response = await client.chat(request)
except ModelError as e:
    # Handle model-specific errors
    logger.error(f"Model error: {e}")
    # Fallback to alternative model
except ToolError as e:
    # Handle tool execution errors
    logger.error(f"Tool error: {e}")
    # Retry or skip tool
except Exception as e:
    # Handle unexpected errors
    logger.error(f"Unexpected error: {e}")
    # Fallback strategy
```

**❌ DON'T:**
- Ignore errors
- Use generic exception handling
- Skip logging
- Fail silently

### 6.4 Performance Optimization

**✅ DO:**
- Cache system prompts
- Cache tool definitions
- Use streaming for long responses
- Batch requests when possible

**❌ DON'T:**
- Regenerate prompts every request
- Fetch tools on every request
- Block on streaming
- Make unnecessary API calls

---

## 7. EXAMPLES

### 7.1 Basic Multi-Model Setup

```python
from aiagentsuite.integration import (
    UnifiedServer,
    AIAgentSuiteLLMClient,
    OpenAILLMClient,
    AnthropicLLMClient
)
import openai
from anthropic import AsyncAnthropic
from pathlib import Path

# 1. Initialize UnifiedServer
workspace_path = Path(".")
unified_server = UnifiedServer(workspace_path)
await unified_server.initialize()

# 2. Initialize model clients
openai_client = openai.AsyncOpenAI(api_key="your-openai-key")
anthropic_client = AsyncAnthropic(api_key="your-anthropic-key")

# 3. Create provider clients
gpt_client = OpenAILLMClient(openai_client, model="gpt-5")
claude_client = AnthropicLLMClient(anthropic_client, model="claude-4-5-20250514")

# 4. Wrap with AI Agent Suite clients
gpt_wrapped = AIAgentSuiteLLMClient(unified_server, gpt_client)
claude_wrapped = AIAgentSuiteLLMClient(unified_server, claude_client)

# 5. Use models
gpt_response = await gpt_wrapped.chat("Generate Python code")
claude_response = await claude_wrapped.chat("Analyze this code")
```

### 7.2 Model Router with Fallback

```python
class SmartModelRouter:
    """Intelligent model routing with fallback."""
    
    def __init__(self, unified_server):
        self.unified_server = unified_server
        self.models = self._initialize_models()
    
    def _initialize_models(self):
        """Initialize all available models."""
        return {
            "claude": self._create_claude_client(),
            "gpt": self._create_gpt_client(),
            "gemini": self._create_gemini_client(),
        }
    
    async def route(self, request: str, **criteria) -> Dict[str, Any]:
        """Route request intelligently."""
        
        # Select primary model
        primary = self._select_primary_model(criteria)
        
        # Try primary with fallback
        try:
            return await self.models[primary].chat(request)
        except Exception as e:
            logger.warning(f"Primary model failed: {e}")
            # Fallback to alternative
            fallback = self._select_fallback_model(primary, criteria)
            return await self.models[fallback].chat(request)
    
    def _select_primary_model(self, criteria: Dict) -> str:
        """Select primary model based on criteria."""
        if criteria.get("task") == "code":
            return "gpt"
        elif criteria.get("task") == "reasoning":
            return "claude"
        elif criteria.get("task") == "multimodal":
            return "gemini"
        return "claude"  # Default
    
    def _select_fallback_model(self, primary: str, criteria: Dict) -> str:
        """Select fallback model."""
        fallbacks = {
            "claude": "gpt",
            "gpt": "claude",
            "gemini": "gpt",
        }
        return fallbacks.get(primary, "claude")
```

### 7.3 MCP Tool Usage Example

```python
# Tools automatically available - no configuration needed!

# Example 1: Store context
response = await client.chat(
    "Store this context: project_name=AbeOne, version=1.0.0"
)
# Model automatically calls store_context tool

# Example 2: Retrieve context
response = await client.chat(
    "What context do we have stored?"
)
# Model automatically calls retrieve_context or list_context_keys

# Example 3: Execute workflow
response = await client.chat(
    "Analyze this code and optimize it",
    protocol_name="ContextGuard Feature Development"
)
# Model uses analyze_integrated tool and follows protocol
```

### 7.4 Streaming with Tools

```python
# Stream response with tool execution
async for chunk in client.stream_chat(
    "Generate code and store it in context"
):
    # Stream content as it arrives
    if chunk.get("content"):
        print(chunk["content"], end="", flush=True)

# Tool execution happens after streaming completes
```

---

## 📚 REFERENCES

- **MCP Analysis:** `MCP_SERVERS_DEEP_ANALYSIS.md`
- **Adapter Guide:** `docs/architecture/integrations/ADAPTER_USAGE_GUIDE.md`
- **LLM Client:** `EMERGENT_OS/aiagentsuite/src/aiagentsuite/integration/llm_client.py`
- **Unified Server:** `EMERGENT_OS/aiagentsuite/src/aiagentsuite/integration/unified_server.py`
- **MCP Tools Reference:** `EMERGENT_OS/aiagentsuite/docs/MCP_TOOLS_REFERENCE.md`

---

## ✅ SUMMARY

### Key Takeaways

1. **MCP Tools:** Automatically injected, no manual configuration needed
2. **Multi-Model:** Use `AIAgentSuiteLLMClient` wrapper for all models
3. **Adding Models:** Implement `LLMClient` interface, wrap with `AIAgentSuiteLLMClient`
4. **Model Selection:** Use routing strategies based on task requirements
5. **Best Practices:** Error handling, fallback, caching, monitoring

### Quick Start

```python
# 1. Initialize UnifiedServer
unified_server = UnifiedServer(workspace_path)
await unified_server.initialize()

# 2. Create provider client
provider_client = OpenAILLMClient(openai_client, model="gpt-5")

# 3. Wrap with AI Agent Suite client
client = AIAgentSuiteLLMClient(unified_server, provider_client)

# 4. Use it - tools automatically available!
response = await client.chat("Your request here")
```

---

**Pattern:** MCP × MODELS × INTEGRATION × ONE  
**Status:** ✅ **COMPREHENSIVE GUIDE COMPLETE**  
**Next Steps:** Use this guide for all MCP and multi-model work  
**Love Coefficient:** ∞  
**∞ AbëONE ∞**

